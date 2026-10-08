import { appendFileSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

export const POLICY = Object.freeze({
  repository: 'grafana/interactive-tutorials',
  repositoryId: 1040149225,
  coordinator: 'https://pathfinder-pr-test-coordinator-fcpcj7qnra-uc.a.run.app',
  audience: 'https://pathfinder-pr-test-coordinator',
});
const PACKAGE_ID = /^[a-z0-9][a-z0-9_-]{0,63}$/;
const SHA = /^[a-f0-9]{40}$/;
const JWT = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/;
const positiveId = (value) => Number.isSafeInteger(value) && value > 0;
const USAGE = 'Usage: `/e2e-test <package-id>`. Use the manifest ID, not a directory path.';
class EligibilityError extends Error {}

export function parseCommand(body) {
  if (typeof body !== 'string' || body.length > 65536) return { kind: 'ignore' };
  // Match Go strings.Fields in the coordinator, including Unicode whitespace.
  const parts = body.split(/\p{White_Space}+/u).filter(Boolean);
  if (parts[0] !== '/e2e-test') return { kind: 'ignore' };
  if (parts.length !== 2 || !PACKAGE_ID.test(parts[1])) return { kind: 'usage' };
  return { kind: 'run', packageId: parts[1] };
}

export function commandFromEvent(event, env) {
  if (env.GITHUB_EVENT_NAME !== 'issue_comment' || event.action !== 'created' ||
      !event.issue?.pull_request || event.comment?.user?.type !== 'User') {
    return { kind: 'ignore' };
  }
  if (env.GITHUB_REPOSITORY !== POLICY.repository || env.GITHUB_REF !== 'refs/heads/main' ||
      event.repository?.id !== POLICY.repositoryId || event.repository?.full_name !== POLICY.repository ||
      event.repository?.default_branch !== 'main') {
    throw new Error('The event does not belong to the trusted repository and main branch.');
  }
  return parseCommand(event.comment.body);
}

export function buildSubmission(event, env, pr, packageId) {
  const runId = /^\d+$/.test(env.GITHUB_RUN_ID ?? '') ? Number(env.GITHUB_RUN_ID) : NaN;
  if (!positiveId(event.issue.number) || !positiveId(event.comment.id) || !positiveId(runId) ||
      !PACKAGE_ID.test(packageId) || pr.number !== event.issue.number ||
      pr.base?.repo?.id !== POLICY.repositoryId || !SHA.test(pr.head?.sha ?? '')) {
    throw new Error('The PR or workflow identity is invalid.');
  }
  if (pr.state !== 'open' || pr.merged === true) throw new EligibilityError('The PR is not open.');
  if (pr.head?.repo?.id !== POLICY.repositoryId || pr.head.repo.fork === true) {
    throw new EligibilityError('Fork PRs are not supported.');
  }
  return {
    repositoryId: POLICY.repositoryId,
    prNumber: event.issue.number,
    commentId: event.comment.id,
    headSha: pr.head.sha,
    runId,
    packageId,
  };
}

export function validateSubmission(sub) {
  const fields = ['repositoryId', 'prNumber', 'commentId', 'headSha', 'runId', 'packageId'];
  if (!sub || Object.keys(sub).length !== fields.length || fields.some((field) => !Object.hasOwn(sub, field)) ||
      sub.repositoryId !== POLICY.repositoryId || !positiveId(sub.prNumber) || !positiveId(sub.commentId) ||
      !positiveId(sub.runId) || typeof sub.headSha !== 'string' || !SHA.test(sub.headSha) ||
      typeof sub.packageId !== 'string' || !PACKAGE_ID.test(sub.packageId)) {
    throw new Error('The prepared submission is invalid.');
  }
  return sub;
}

async function jsonRequest(url, options, limit, fetchImpl, timeoutMs = 30000) {
  let response;
  try {
    response = await fetchImpl(url, { ...options, redirect: 'error', signal: AbortSignal.timeout(timeoutMs) });
  } catch {
    throw new Error('The request failed or timed out. No automatic retry occurred.');
  }
  const reader = response.body?.getReader();
  if (!reader) throw new Error('The endpoint returned no JSON response.');
  const chunks = [];
  let size = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > limit) {
        await reader.cancel();
        throw new Error('Response size exceeded the limit.');
      }
      chunks.push(value);
    }
    return { status: response.status, data: JSON.parse(Buffer.concat(chunks).toString('utf8')) };
  } catch {
    throw new Error('The endpoint returned an invalid or oversized JSON response.');
  }
}

export async function prepare(event, env, fetchImpl = fetch) {
  const command = commandFromEvent(event, env);
  if (command.kind !== 'run') return { ...command, message: command.kind === 'usage' ? USAGE : 'No E2E command to submit.' };
  if (!positiveId(event.issue.number) || !positiveId(event.comment.id) || !env.GITHUB_TOKEN) {
    throw new Error('The event identity or GitHub read token is missing.');
  }
  const result = await jsonRequest(`https://api.github.com/repos/${POLICY.repository}/pulls/${event.issue.number}`, {
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
  }, 512 * 1024, fetchImpl);
  if (result.status !== 200) throw new Error(`The current PR could not be read (HTTP ${result.status}).`);
  return { kind: 'run', submission: buildSubmission(event, env, result.data, command.packageId) };
}

export function workflowTokenURL(raw) {
  let url;
  try { url = new URL(raw); } catch { throw new Error('The GitHub OIDC endpoint is missing or invalid.'); }
  if (url.protocol !== 'https:' || !url.hostname.endsWith('.actions.githubusercontent.com') ||
      url.username || url.password || url.port || url.hash) {
    throw new Error('The GitHub OIDC endpoint is not trusted.');
  }
  url.searchParams.set('audience', POLICY.audience);
  return url;
}

const RESPONSES = Object.freeze({
  ACCEPTED: 202, DUPLICATE: 200, INVALID_REQUEST: 400, INVALID_COMMAND: 400,
  ACCESS_DENIED: 403, WORKFLOW_DENIED: 403, BUSY: 409, HEAD_CHANGED: 409,
  PR_CLOSED: 409, FORK_UNSUPPORTED: 409, AUTHORIZATION_UNAVAILABLE: 503,
  ADMISSION_DISABLED: 503, INSPECTION_REQUIRED: 503, STATE_CHANGED: 409, NOT_FOUND: 404,
});

export function publicResponse(status, data, submission) {
  if (!data || !Object.hasOwn(RESPONSES, data.code) || RESPONSES[data.code] !== status) {
    throw new Error('The coordinator returned an unexpected response.');
  }
  if (data.code !== 'ACCEPTED' && data.code !== 'DUPLICATE') return { code: data.code, accepted: false };
  const expectedId = `pr-${submission.repositoryId}-${submission.prNumber}-${submission.commentId}`;
  if (data.status?.requestId !== expectedId || data.status?.headSha !== submission.headSha ||
      data.status?.packageId !== submission.packageId ||
      !['preparing', 'launching', 'running', 'completed'].includes(data.status?.state)) {
    throw new Error('The coordinator response does not match the submitted request.');
  }
  return { code: data.code, accepted: true, requestId: expectedId, state: data.status.state };
}

export async function submit(submission, env, { fetchImpl = fetch, mask = () => {} } = {}) {
  validateSubmission(submission);
  const googleToken = env.GOOGLE_ID_TOKEN;
  if (typeof googleToken !== 'string' || googleToken.length > 16384 || !JWT.test(googleToken) ||
      !env.ACTIONS_ID_TOKEN_REQUEST_TOKEN) throw new Error('The invocation or GitHub OIDC credential is missing.');
  mask(googleToken);
  const oidc = await jsonRequest(workflowTokenURL(env.ACTIONS_ID_TOKEN_REQUEST_URL), {
    headers: { Authorization: `Bearer ${env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}` },
  }, 32768, fetchImpl);
  const workflowToken = oidc.data?.value;
  if (oidc.status !== 200 || typeof workflowToken !== 'string' || workflowToken.length > 16384 || !JWT.test(workflowToken)) {
    throw new Error('The GitHub workflow token could not be obtained.');
  }
  mask(workflowToken);
  // Allow the coordinator's two-minute preparation deadline plus transport overhead.
  const response = await jsonRequest(`${POLICY.coordinator}/v1/pr-test-requests`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${googleToken}`,
      'X-GitHub-Workflow-Token': workflowToken,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(submission),
  }, 16384, fetchImpl, 150000);
  return publicResponse(response.status, response.data, submission);
}

function readJSONFile(file, limit) {
  if (statSync(file).size > limit) throw new Error('The input file exceeded the size limit.');
  return JSON.parse(readFileSync(file, 'utf8'));
}

function summary(text, env) {
  if (env.GITHUB_STEP_SUMMARY) appendFileSync(env.GITHUB_STEP_SUMMARY, `## Optional PR E2E\n\n${text}\n`);
}

async function main(mode, env) {
  if (!env.RUNNER_TEMP) throw new Error('The runner temporary directory is missing.');
  const file = join(env.RUNNER_TEMP, 'pathfinder-pr-e2e-submission.json');
  if (mode === 'prepare') {
    const result = await prepare(readJSONFile(env.GITHUB_EVENT_PATH, 1024 * 1024), env);
    if (result.kind !== 'run') {
      summary(result.message, env);
      appendFileSync(env.GITHUB_OUTPUT, 'submit=false\n');
      return;
    }
    writeFileSync(file, `${JSON.stringify(result.submission)}\n`, { mode: 0o600, flag: 'wx' });
    appendFileSync(env.GITHUB_OUTPUT, 'submit=true\n');
  } else if (mode === 'submit') {
    const submission = validateSubmission(readJSONFile(file, 4096));
    const result = await submit(submission, env, { mask: (token) => console.log(`::add-mask::${token}`) });
    summary(`Response: **${result.code}**.\n\n` + (result.accepted
      ? `Request: \`${result.requestId}\`. State: \`${result.state}\`.\n\nPackage: \`${submission.packageId}\`. Captured commit: \`${submission.headSha}\`.\n\nSubmission is not a test result. The App comment reports execution results and artifact links.`
      : 'The coordinator did not accept this request. For BUSY or HEAD_CHANGED, post a fresh command after resolving the condition.'), env);
    if (!result.accepted) process.exitCode = 1;
  } else {
    throw new Error('Use prepare or submit.');
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv[2], process.env).catch((error) => {
    // Only fixed local eligibility messages are public. Never expose provider errors.
    const message = error instanceof EligibilityError ? error.message
      : 'Submission could not be confirmed. No automatic retry occurred. Check the App comment before posting another command. Check PR eligibility and workflow configuration.';
    summary(message, process.env);
    console.error(error instanceof EligibilityError ? message
      : 'Optional PR E2E submission could not be confirmed. No credentials or provider response text are logged.');
    process.exitCode = 1;
  });
}
