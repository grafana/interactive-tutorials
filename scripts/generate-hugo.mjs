#!/usr/bin/env node

/**
 * Generates Hugo-compatible index.md files from enriched content.json files.
 *
 * Usage:
 *   node scripts/generate-hugo.mjs <learning-path-slug> [--website-dir <path>] [--dry-run]
 *
 * Example:
 *   node scripts/generate-hugo.mjs linux-server-integration-lj
 *   node scripts/generate-hugo.mjs linux-server-integration-lj --dry-run
 *   node scripts/generate-hugo.mjs linux-server-integration-lj --website-dir ../website
 */

import { readFileSync, writeFileSync, readdirSync, statSync, mkdirSync, existsSync } from 'node:fs';
import { join, basename, dirname, resolve } from 'node:path';

const REPO_ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const DEFAULT_WEBSITE_DIR = resolve(REPO_ROOT, '../website');

function toYamlValue(value, indent = 0) {
  if (value === null || value === undefined) return 'null';
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  if (typeof value === 'number') return String(value);

  if (typeof value === 'string') {
    if (value.includes('\n') || value.includes(': ') || value.includes('#') ||
        value.startsWith('{') || value.startsWith('[') || value.startsWith("'") ||
        value.startsWith('"') || value === '' || value === 'true' || value === 'false' ||
        value === 'null' || value === 'yes' || value === 'no') {
      return `'${value.replace(/'/g, "''")}'`;
    }
    return value;
  }

  if (Array.isArray(value)) {
    if (value.length === 0) return '[]';
    const pad = '  '.repeat(indent);
    return '\n' + value.map(item => {
      if (typeof item === 'object' && item !== null && !Array.isArray(item)) {
        const entries = Object.entries(item);
        const first = entries[0];
        const rest = entries.slice(1);
        const firstRendered = toYamlValue(first[1], indent + 2);
        let line = `${pad}  - ${first[0]}:${firstRendered.startsWith('\n') ? '' : ' '}${firstRendered}`;
        for (const [k, v] of rest) {
          const rendered = toYamlValue(v, indent + 2);
          line += `\n${pad}    ${k}:${rendered.startsWith('\n') ? '' : ' '}${rendered}`;
        }
        return line;
      }
      return `${pad}  - ${toYamlValue(item, indent + 1)}`;
    }).join('\n');
  }

  if (typeof value === 'object') {
    const pad = '  '.repeat(indent);
    return '\n' + Object.entries(value).map(([k, v]) => {
      const rendered = toYamlValue(v, indent + 1);
      if (rendered.startsWith('\n')) {
        return `${pad}  ${k}:${rendered}`;
      }
      return `${pad}  ${k}: ${rendered}`;
    }).join('\n');
  }

  return String(value);
}

function buildFrontMatter(json, pathfinderDataPath) {
  const { website, title } = json;
  const lines = ['---'];

  if (website.menuTitle) lines.push(`menuTitle: ${toYamlValue(website.menuTitle)}`);
  lines.push(`title: ${toYamlValue(title)}`);
  if (website.description) lines.push(`description: ${toYamlValue(website.description)}`);

  if (website.keywords) {
    lines.push(`keywords:${toYamlValue(website.keywords, 0)}`);
  }

  if (website.grafana) {
    lines.push(`grafana:${toYamlValue(website.grafana, 0)}`);
  }

  lines.push(`weight: ${website.weight}`);
  if (website.step != null) lines.push(`step: ${website.step}`);
  lines.push('layout: single-journey');

  if (website.cta) {
    const rendered = toYamlValue(website.cta, 0);
    lines.push(`cta:${rendered}`);
  }

  if (website.related_journeys) {
    const rendered = toYamlValue(website.related_journeys, 0);
    lines.push(`related_journeys:${rendered}`);
  }

  if (website.side_journeys) {
    const rendered = toYamlValue(website.side_journeys, 0);
    lines.push(`side_journeys:${rendered}`);
  }

  if (website.troubleshooting) {
    const rendered = toYamlValue(website.troubleshooting, 0);
    lines.push(`troubleshooting:${rendered}`);
  }

  lines.push(`pathfinder_data: ${pathfinderDataPath}`);
  lines.push('---');

  return lines.join('\n');
}

function generateMilestoneMarkdown(json, pathfinderDataPath) {
  const frontMatter = buildFrontMatter(json, pathfinderDataPath);
  return `${frontMatter}\n\n{{< pathfinder/json >}}\n`;
}

function discoverMilestones(lpDir) {
  return readdirSync(lpDir)
    .filter(entry => {
      const full = join(lpDir, entry);
      return statSync(full).isDirectory() && existsSync(join(full, 'content.json'));
    })
    .sort();
}

function websiteSlug(lpSlug) {
  return lpSlug.replace(/-lj$/, '');
}

function run() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const webIdx = args.indexOf('--website-dir');
  const websiteDir = webIdx !== -1 ? resolve(args[webIdx + 1]) : DEFAULT_WEBSITE_DIR;
  const slug = args.find(a => !a.startsWith('--') && (webIdx === -1 || a !== args[webIdx + 1]));

  if (!slug) {
    console.error('Usage: node scripts/generate-hugo.mjs <learning-path-slug> [--website-dir <path>] [--dry-run]');
    process.exit(1);
  }

  const lpDir = join(REPO_ROOT, slug);
  if (!existsSync(lpDir)) {
    console.error(`Learning path directory not found: ${lpDir}`);
    process.exit(1);
  }

  const milestones = discoverMilestones(lpDir);
  const webSlug = websiteSlug(slug);
  const outputBase = join(websiteDir, 'content/docs/learning-paths', webSlug);

  console.log(`\nGenerating Hugo markdown for: ${slug}`);
  console.log(`  Source: ${lpDir}`);
  console.log(`  Output: ${outputBase}`);
  console.log(`  Milestones found: ${milestones.length}`);
  console.log(`  Dry run: ${dryRun}\n`);

  let generated = 0;
  let skipped = 0;

  for (const milestone of milestones) {
    const jsonPath = join(lpDir, milestone, 'content.json');
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));

    if (!json.website) {
      console.log(`  SKIP  ${milestone}/content.json (no website key)`);
      skipped++;
      continue;
    }

    const pathfinderData = `${slug}/${milestone}`;
    const md = generateMilestoneMarkdown(json, pathfinderData);
    const outPath = join(outputBase, milestone, 'index.md');

    if (dryRun) {
      console.log(`  WOULD WRITE  ${milestone}/index.md`);
      console.log('  ' + '-'.repeat(60));
      console.log(md.split('\n').map(l => '  ' + l).join('\n'));
      console.log('  ' + '-'.repeat(60));
    } else {
      mkdirSync(dirname(outPath), { recursive: true });
      writeFileSync(outPath, md);
      console.log(`  WROTE  ${milestone}/index.md`);
    }
    generated++;
  }

  console.log(`\nDone: ${generated} generated, ${skipped} skipped`);
}

run();
