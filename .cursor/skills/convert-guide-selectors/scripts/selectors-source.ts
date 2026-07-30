/**
 * Loads @grafana/e2e-selectors from a grafana/grafana checkout.
 *
 * These scripts live in this repo but the selectors package lives in grafana/grafana, so the
 * location cannot be a relative import — it must be supplied:
 *
 *   GRAFANA_REPO=/path/to/grafana tsx <script>.ts ...
 *
 * Defaults to a sibling ../grafana checkout when the variable is unset.
 */
import path from 'node:path';
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

export async function loadSelectors(): Promise<{
  versionedComponents: any;
  versionedPages: any;
  resolveSelectors: (tree: any, version: string) => any;
}> {
  const repo =
    process.env.GRAFANA_REPO ?? path.resolve(process.cwd(), '..', 'grafana');
  const base = path.join(repo, 'packages', 'grafana-e2e-selectors', 'src');

  if (!fs.existsSync(path.join(base, 'selectors', 'components.ts'))) {
    throw new Error(
      `Could not find @grafana/e2e-selectors sources under ${base}.\n` +
        `Set GRAFANA_REPO to your grafana/grafana checkout, e.g.\n` +
        `  GRAFANA_REPO=~/Repos/grafana tsx ${path.basename(process.argv[1] ?? 'script.ts')} ...`
    );
  }

  const [components, pages, resolver] = await Promise.all([
    import(pathToFileURL(path.join(base, 'selectors', 'components.ts')).href),
    import(pathToFileURL(path.join(base, 'selectors', 'pages.ts')).href),
    import(pathToFileURL(path.join(base, 'resolver.ts')).href),
  ]);

  return {
    versionedComponents: components.versionedComponents,
    versionedPages: pages.versionedPages,
    resolveSelectors: resolver.resolveSelectors,
  };
}
