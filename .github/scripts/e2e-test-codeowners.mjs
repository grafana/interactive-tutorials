// This policy is the union of owners, not path-specific CODEOWNERS matching.
const LOGIN = /^[a-z0-9][a-z0-9-]{0,38}$/i;

export function ownersFromCodeowners(text) {
  if (typeof text !== 'string' || Buffer.byteLength(text) > 131072) {
    throw new Error('The trusted CODEOWNERS file is invalid.');
  }
  const users = new Set();
  let hasOwner = false;
  for (const line of text.split(/\r?\n/)) {
    const fields = line.split('#', 1)[0].trim().split(/\s+/);
    for (const owner of fields.slice(1)) {
      const name = owner.slice(1).toLowerCase();
      if (!owner.startsWith('@')) throw new Error('The trusted CODEOWNERS owner format is unsupported.');
      if (LOGIN.test(name)) users.add(name);
      else if (!/^grafana\/[a-z0-9][a-z0-9_-]{0,99}$/.test(name)) {
        throw new Error('The trusted CODEOWNERS owner format is unsupported.');
      }
      // Team entries are valid policy data but do not grant workflow access.
      hasOwner = true;
    }
  }
  if (!hasOwner) throw new Error('The trusted CODEOWNERS owner list is invalid.');
  return { users };
}

export function allowedActors(raw = '') {
  if (raw === '') return null;
  if (typeof raw !== 'string' || raw.length > 16384) throw new Error('The actor restriction must be a JSON array of logins.');
  let actors;
  try { actors = JSON.parse(raw); } catch { throw new Error('The actor restriction must be a JSON array of logins.'); }
  if (!Array.isArray(actors) ||
      !actors.every((actor) => typeof actor === 'string' && LOGIN.test(actor))) {
    throw new Error('The actor restriction must be a JSON array of logins.');
  }
  return new Set(actors.map((actor) => actor.toLowerCase()));
}

export function isCodeowner(owners, login) {
  return typeof login === 'string' && LOGIN.test(login) && owners.users.has(login.toLowerCase());
}
