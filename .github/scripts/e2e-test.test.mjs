import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync, writeFileSync, rmSync, existsSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { POLICY, parseCommand, commandFromEvent, buildSubmission, prepare, submit, publicResponse, validateSubmission, workflowTokenURL } from './e2e-test.mjs';

const env = {
  GITHUB_EVENT_NAME: 'issue_comment', GITHUB_REPOSITORY: POLICY.repository,
  GITHUB_REF: 'refs/heads/main', GITHUB_RUN_ID: '321', GITHUB_TOKEN: 'synthetic-github-read-token',
  GOOGLE_ID_TOKEN: 'google.payload.signature',
  ACTIONS_ID_TOKEN_REQUEST_URL: 'https://pipelines.actions.githubusercontent.com/example/idtoken?api-version=2.0',
  ACTIONS_ID_TOKEN_REQUEST_TOKEN: 'synthetic-oidc-request-token',
};
const event = () => ({
  action: 'created',
  repository: { id: POLICY.repositoryId, full_name: POLICY.repository, default_branch: 'main' },
  issue: { number: 42, pull_request: { url: 'unused' } },
  comment: { id: 1234, body: '/e2e-test first-dashboard', user: { type: 'User' } },
});
const pr = () => ({ number: 42, state: 'open', merged: false,
  base: { repo: { id: POLICY.repositoryId } },
  head: { sha: 'a'.repeat(40), repo: { id: POLICY.repositoryId, fork: false } },
});
const submission = () => buildSubmission(event(), env, pr(), 'first-dashboard');
const response = (data, status = 200) => new Response(JSON.stringify(data), { status });
const accepted = (sub = submission(), state = 'running') => ({
  code: 'ACCEPTED', status: {
    requestId: `pr-${sub.repositoryId}-${sub.prNumber}-${sub.commentId}`,
    headSha: sub.headSha, packageId: sub.packageId, state,
  },
});

for (const body of ['/e2e-test first-dashboard', ' \t/e2e-test\nfirst-dashboard\r\n', '\u0085/e2e-test\u2003a_b-2\u0085']) {
  test(`accept whole command ${JSON.stringify(body)}`, () => assert.equal(parseCommand(body).kind, 'run'));
}
for (const body of ['', 'text /e2e-test first-dashboard', '> /e2e-test first-dashboard', '```\n/e2e-test first-dashboard\n```', '/e2e-test-status', '\ufeff/e2e-test first-dashboard']) {
  test(`ignore non-command ${JSON.stringify(body)}`, () => assert.equal(parseCommand(body).kind, 'ignore'));
}
for (const body of ['/e2e-test', '/e2e-test guide extra', '/e2e-test ../guide', '/e2e-test guide/path', '/e2e-test Guide', '/e2e-test guide.id', '/e2e-test $(id)', '/e2e-test -guide', `/e2e-test ${'a'.repeat(65)}`]) {
  test(`usage for invalid command ${JSON.stringify(body)}`, () => assert.equal(parseCommand(body).kind, 'usage'));
}
test('package ID boundary matches coordinator', () => {
  assert.equal(parseCommand(`/e2e-test ${'a'.repeat(64)}`).kind, 'run');
  assert.equal(parseCommand('a'.repeat(65537)).kind, 'ignore');
});

for (const [name, mutate] of [
  ['edited comment', (e) => { e.action = 'edited'; }],
  ['ordinary issue', (e) => { delete e.issue.pull_request; }],
  ['bot', (e) => { e.comment.user.type = 'Bot'; }],
]) {
  test(`ignore ${name} without API calls`, async () => {
    const e = event(); mutate(e);
    const result = await prepare(e, env, () => { assert.fail('unexpected API call'); });
    assert.equal(result.kind, 'ignore');
  });
}
for (const [name, environment, mutate] of [
  ['wrong event name', { ...env, GITHUB_EVENT_NAME: 'pull_request' }, () => {}],
]) {
  test(name, () => { const e = event(); mutate(e); assert.equal(commandFromEvent(e, environment).kind, 'ignore'); });
}
for (const [name, environment, mutate] of [
  ['wrong ref', { ...env, GITHUB_REF: 'refs/pull/42/head' }, () => {}],
  ['wrong repository environment', { ...env, GITHUB_REPOSITORY: 'attacker/tutorials' }, () => {}],
  ['wrong repository ID', env, (e) => { e.repository.id++; }],
  ['wrong repository name', env, (e) => { e.repository.full_name = 'attacker/tutorials'; }],
  ['wrong default branch', env, (e) => { e.repository.default_branch = 'attacker'; }],
]) {
  test(`reject ${name}`, () => { const e = event(); mutate(e); assert.throws(() => commandFromEvent(e, environment)); });
}
test('bare command gets usage without API calls', async () => {
  const e = event(); e.comment.body = '/e2e-test';
  const result = await prepare(e, env, () => assert.fail('unexpected API call'));
  assert.equal(result.kind, 'usage'); assert.match(result.message, /Usage:/);
});
test('preparation captures current SHA without downloading source', async () => {
  const calls = [];
  const result = await prepare(event(), env, async (url, options) => {
    calls.push(url);
    assert.equal(url, `https://api.github.com/repos/${POLICY.repository}/pulls/42`);
    assert.equal(options.headers.Authorization, `Bearer ${env.GITHUB_TOKEN}`);
    assert.equal(options.redirect, 'error');
    return response(pr());
  });
  assert.equal(calls.length, 1); assert.deepEqual(result.submission, submission());
});
for (const [name, mutate] of [
  ['fork', (p) => { p.head.repo.id = 999; p.head.repo.fork = true; }],
  ['deleted head repo', (p) => { p.head.repo = null; }],
  ['closed PR', (p) => { p.state = 'closed'; }],
  ['merged PR', (p) => { p.merged = true; }],
  ['wrong PR', (p) => { p.number++; }],
  ['wrong base repository', (p) => { p.base.repo.id++; }],
  ['malformed SHA', (p) => { p.head.sha = '$(id)'; }],
]) {
  test(`reject ${name} before obtaining cloud tokens`, async () => {
    const p = pr(); mutate(p);
    await assert.rejects(prepare(event(), env, async () => response(p)));
  });
}
for (const runId of ['0', '-1', 'NaN', '1e5', '9007199254740992']) {
  test(`reject invalid run ID ${runId}`, () => assert.throws(() => buildSubmission(event(), { ...env, GITHUB_RUN_ID: runId }, pr(), 'guide')));
}
test('reject GitHub denial without exposing provider text', async () => {
  await assert.rejects(prepare(event(), env, async () => response({ message: env.GITHUB_TOKEN }, 403)), /HTTP 403/);
});
test('reject oversized PR response', async () => {
  await assert.rejects(prepare(event(), env, async () => new Response('x'.repeat(512 * 1024 + 1))), /oversized/);
});

for (const url of ['http://pipelines.actions.githubusercontent.com/idtoken', 'https://evil.example/idtoken', 'https://pipelines.actions.githubusercontent.com.evil.example/', 'https://user@pipelines.actions.githubusercontent.com/idtoken', 'https://pipelines.actions.githubusercontent.com:444/idtoken', 'https://pipelines.actions.githubusercontent.com/#fragment', 'invalid']) {
  test(`reject untrusted OIDC endpoint ${url}`, () => assert.throws(() => workflowTokenURL(url)));
}
test('OIDC URL preserves existing parameters and sets reviewed audience', () => {
  const url = workflowTokenURL(`${env.ACTIONS_ID_TOKEN_REQUEST_URL}&audience=wrong`);
  assert.equal(url.searchParams.get('audience'), POLICY.audience);
  assert.equal(url.searchParams.get('api-version'), '2.0');
});
test('reject malformed prepared data', () => {
  assert.throws(() => validateSubmission({ ...submission(), unexpected: true }));
  assert.throws(() => validateSubmission({ ...submission(), commentId: 1.5 }));
  assert.throws(() => validateSubmission({ ...submission(), repositoryId: 99 }));
  assert.throws(() => validateSubmission({ ...submission(), packageId: '../guide' }));
});
test('submit uses distinct Google and GitHub tokens and never polls', async () => {
  const calls = [], masks = [];
  const sub = submission();
  const result = await submit(sub, env, { mask: (token) => masks.push(token), fetchImpl: async (url, options) => {
    calls.push({ url: String(url), options });
    assert.equal(options.redirect, 'error'); assert.ok(options.signal instanceof AbortSignal);
    if (calls.length === 1) {
      assert.equal(new URL(url).searchParams.get('audience'), POLICY.audience);
      assert.equal(options.headers.Authorization, `Bearer ${env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}`);
      return response({ value: 'workflow.payload.signature' });
    }
    assert.equal(url, `${POLICY.coordinator}/v1/pr-test-requests`);
    assert.equal(options.method, 'POST');
    assert.equal(options.headers.Authorization, `Bearer ${env.GOOGLE_ID_TOKEN}`);
    assert.equal(options.headers['X-GitHub-Workflow-Token'], 'workflow.payload.signature');
    assert.deepEqual(JSON.parse(options.body), sub);
    return response(accepted(sub), 202);
  } });
  assert.equal(calls.length, 2); assert.equal(result.code, 'ACCEPTED');
  assert.deepEqual(masks, [env.GOOGLE_ID_TOKEN, 'workflow.payload.signature']);
  assert.equal(JSON.stringify(sub).includes('token'), false);
});
test('transport failure is sanitized and not retried', async () => {
  let calls = 0;
  await assert.rejects(submit(submission(), env, { fetchImpl: async () => {
    calls++; throw new Error(`private provider error ${env.GOOGLE_ID_TOKEN}`);
  } }), (error) => !error.message.includes(env.GOOGLE_ID_TOKEN));
  assert.equal(calls, 1);
});
test('submission transport failure never retries the POST', async () => {
  let calls = 0;
  await assert.rejects(submit(submission(), env, { fetchImpl: async () => {
    calls++;
    if (calls === 1) return response({ value: 'workflow.payload.signature' });
    throw new Error('private provider details');
  } }), /No automatic retry/);
  assert.equal(calls, 2);
});
test('reject missing Google token before any request', async () => {
  await assert.rejects(submit(submission(), { ...env, GOOGLE_ID_TOKEN: '' }, { fetchImpl: () => assert.fail('unexpected request') }));
});
test('reject malformed or newline-injected OIDC token before POST', async () => {
  let calls = 0;
  await assert.rejects(submit(submission(), env, { fetchImpl: async () => {
    calls++; return response({ value: 'workflow.payload.signature\n::error::injection' });
  } }));
  assert.equal(calls, 1);
});
for (const [code, status] of [['BUSY', 409], ['HEAD_CHANGED', 409], ['ACCESS_DENIED', 403], ['WORKFLOW_DENIED', 403], ['ADMISSION_DISABLED', 503], ['INSPECTION_REQUIRED', 503], ['PR_CLOSED', 409], ['FORK_UNSUPPORTED', 409]]) {
  test(`bounded coordinator rejection ${code}`, () => {
    assert.deepEqual(publicResponse(status, { code, providerError: 'never exposed' }, submission()), { code, accepted: false });
  });
}
test('duplicate response does not imply a test pass', () => {
  const body = accepted(); body.code = 'DUPLICATE'; body.status.state = 'completed';
  assert.equal(publicResponse(200, body, submission()).code, 'DUPLICATE');
});
for (const [name, mutate] of [
  ['unknown code', (r) => { r.code = 'secret response'; }],
  ['wrong request ID', (r) => { r.status.requestId = 'wrong'; }],
  ['wrong SHA', (r) => { r.status.headSha = 'b'.repeat(40); }],
  ['wrong package', (r) => { r.status.packageId = 'wrong'; }],
  ['untrusted state', (r) => { r.status.state = '<script>raw-provider-text</script>'; }],
]) {
  test(`reject coordinator ${name}`, () => { const r = accepted(); mutate(r); assert.throws(() => publicResponse(202, r, submission())); });
}
test('reject mismatched HTTP status', () => assert.throws(() => publicResponse(200, accepted(), submission())));
test('CLI usage writes safe summary and never prepares a request', () => {
  const dir = mkdtempSync(join(tmpdir(), 'pr-e2e-helper-test-'));
  try {
    const e = event(); e.comment.body = '/e2e-test';
    const eventFile = join(dir, 'event.json'), summary = join(dir, 'summary'), output = join(dir, 'output');
    writeFileSync(eventFile, JSON.stringify(e));
    const result = spawnSync(process.execPath, [new URL('./e2e-test.mjs', import.meta.url).pathname, 'prepare'], {
      env: { ...process.env, ...env, RUNNER_TEMP: dir, GITHUB_EVENT_PATH: eventFile, GITHUB_STEP_SUMMARY: summary, GITHUB_OUTPUT: output }, encoding: 'utf8',
    });
    assert.equal(result.status, 0); assert.match(readFileSync(summary, 'utf8'), /Usage:/);
    assert.equal(readFileSync(output, 'utf8'), 'submit=false\n');
    assert.equal(existsSync(join(dir, 'pathfinder-pr-e2e-submission.json')), false);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
test('CLI preparation and submission keep tokens out of files and summaries', () => {
  const dir = mkdtempSync(join(tmpdir(), 'pr-e2e-helper-test-'));
  try {
    const eventFile = join(dir, 'event.json'), summary = join(dir, 'summary'), output = join(dir, 'output');
    const mock = join(dir, 'mock.mjs'), file = join(dir, 'pathfinder-pr-e2e-submission.json');
    writeFileSync(eventFile, JSON.stringify(event()));
    writeFileSync(mock, `globalThis.fetch = async (url) => {
      const text = String(url);
      if (text.startsWith('https://api.github.com/')) return new Response(${JSON.stringify(JSON.stringify(pr()))});
      if (text.startsWith('https://pipelines.actions.githubusercontent.com/')) return new Response('{"value":"workflow.payload.signature"}');
      if (text === ${JSON.stringify(POLICY.coordinator + '/v1/pr-test-requests')}) return new Response(${JSON.stringify(JSON.stringify(accepted()))}, {status:202});
      throw new Error('Unexpected network request');
    };`);
    const environment = { ...process.env, ...env, RUNNER_TEMP: dir, GITHUB_EVENT_PATH: eventFile, GITHUB_STEP_SUMMARY: summary, GITHUB_OUTPUT: output };
    const helper = new URL('./e2e-test.mjs', import.meta.url).pathname;
    const prepared = spawnSync(process.execPath, ['--import', mock, helper, 'prepare'], { env: environment, encoding: 'utf8' });
    assert.equal(prepared.status, 0);
    assert.deepEqual(JSON.parse(readFileSync(file, 'utf8')), submission());
    assert.equal(statSync(file).mode & 0o777, 0o600);
    const sent = spawnSync(process.execPath, ['--import', mock, helper, 'submit'], { env: environment, encoding: 'utf8' });
    assert.equal(sent.status, 0);
    const text = readFileSync(summary, 'utf8');
    assert.match(text, /ACCEPTED/); assert.match(text, /Submission is not a test result/);
    for (const token of [env.GOOGLE_ID_TOKEN, env.GITHUB_TOKEN, env.ACTIONS_ID_TOKEN_REQUEST_TOKEN, 'workflow.payload.signature']) {
      assert.equal(text.includes(token), false);
      assert.equal(readFileSync(file, 'utf8').includes(token), false);
    }
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
test('CLI failure never exposes input or provider details', () => {
  const dir = mkdtempSync(join(tmpdir(), 'pr-e2e-helper-test-'));
  try {
    const file = join(dir, 'pathfinder-pr-e2e-submission.json'), summary = join(dir, 'summary');
    const secret = 'synthetic-private-provider-token';
    writeFileSync(file, `{"secret":"${secret}"`);
    const result = spawnSync(process.execPath, [new URL('./e2e-test.mjs', import.meta.url).pathname, 'submit'], {
      env: { ...process.env, ...env, RUNNER_TEMP: dir, GITHUB_STEP_SUMMARY: summary }, encoding: 'utf8',
    });
    assert.equal(result.status, 1);
    assert.equal((result.stdout + result.stderr + readFileSync(summary, 'utf8')).includes(secret), false);
    assert.match(readFileSync(summary, 'utf8'), /No automatic retry/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
