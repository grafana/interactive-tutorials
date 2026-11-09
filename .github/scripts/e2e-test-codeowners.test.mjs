import assert from 'node:assert/strict';
import test from 'node:test';
import { allowedActors, isCodeowner, ownersFromCodeowners } from './e2e-test-codeowners.mjs';
import { authorize } from './e2e-test.mjs';

const text = '* @maintainer\n/.github/ @infrastructure\n/guide/ @author @grafana/guide-team\n/other/ @AUTHOR # comment\n';
const event = (login = 'author') => ({ comment: { user: { login, id: 123 } } });
const env = { GITHUB_TOKEN: 'synthetic-read-token' };
const response = (data, status = 200) => new Response(JSON.stringify(data), { status });
const permission = { permission: 'write', user: { id: 123 } };

test('all individual owners qualify, not just infrastructure owners', () => {
  const owners = ownersFromCodeowners(text);
  assert.deepEqual([...owners.users], ['maintainer', 'infrastructure', 'author']);
  for (const login of ['maintainer', 'infrastructure', 'author', 'AUTHOR']) {
    assert.equal(isCodeowner(owners, login), true);
  }
});
test('empty-owner rules do not remove owners from the union', () => {
  assert.deepEqual([...ownersFromCodeowners('/guide/ @author\n/guide/\n').users], ['author']);
});
test('team entries do not grant individual access', () => {
  const owners = ownersFromCodeowners('/guide/ @grafana/guide-team\n');
  for (const login of ['member', 'guide-team', 'grafana', 'outsider']) {
    assert.equal(isCodeowner(owners, login), false);
  }
});
for (const value of ['', '# comment', '/guide/ user@example.com', '/guide/ @other-org/team', '/guide/ @bad/path/name', 'x'.repeat(131073)]) {
  test(`reject unsupported CODEOWNERS ${value.slice(0, 40)}`, () => assert.throws(() => ownersFromCodeowners(value)));
}
for (const raw of ['"operator-login"', 'null', '{}', 'true', '[123]', '[null]', '[{}]', '["bad/login"]', 'not-json', ' '.repeat(16385)]) {
  test(`reject actor restriction ${raw.slice(0, 30)}`, () => assert.throws(() => allowedActors(raw)));
}
test('actor restriction is exact, case-insensitive, and cannot broaden ownership', async () => {
  assert.equal(allowedActors(), null);
  assert.equal(allowedActors('[]').size, 0);
  assert.equal(allowedActors('["Operator-login"]').has('operator'), false);
  assert.equal(allowedActors('["AUTHOR"]').has('author'), true);
  await assert.rejects(authorize(event('outsider'), { ...env, PR_E2E_ALLOWED_ACTORS: '["outsider"]' }, () => assert.fail('network'), text), /not an individually listed CODEOWNER/);
});
test('restricted owner is denied without network calls', async () => {
  await assert.rejects(authorize(event(), { ...env, PR_E2E_ALLOWED_ACTORS: '[]' }, () => assert.fail('network'), text), /actor restriction/);
});
test('authorized owner still needs current write permission and exact user identity', async () => {
  for (const data of [permission, { ...permission, permission: 'read' }, { ...permission, user: { id: 456 } }]) {
    const operation = authorize(event(), env, async (url, options) => {
      assert.equal(url, 'https://api.github.com/repos/grafana/interactive-tutorials/collaborators/author/permission');
      assert.equal(options.headers.Authorization, 'Bearer synthetic-read-token');
      return response(data);
    }, text);
    if (data === permission) await operation;
    else await assert.rejects(operation, /current repository write permission/);
  }
});
test('team-only caller is denied without membership or submission requests', async () => {
  await assert.rejects(authorize(event('member'), env, () => assert.fail('network'), text), /not an individually listed CODEOWNER/);
});
test('individually listed team member qualifies without a membership lookup', async () => {
  await authorize(event('member'), env, async () => response(permission), text + '/guide/ @member\n');
});
test('non-JSON HTTP failure retains status without exposing provider text', async () => {
  await assert.rejects(authorize(event(), env, async () => new Response('private-provider-detail', { status: 401 }), text), (error) => {
    assert.match(error.message, /HTTP 401/);
    assert.equal(error.message.includes('private-provider-detail'), false);
    return true;
  });
});
