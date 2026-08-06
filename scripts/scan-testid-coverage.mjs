#!/usr/bin/env node
// Scan provisioned plugins for interactive JSX elements lacking a data-testid.
// AST-based via the TypeScript compiler API (no type checking — parse only).
import { createRequire } from "node:module";
import { readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const ts = createRequire(import.meta.url)("/Users/jackwestbrook/dev/sandbox/react-detect-plugins/node_modules/typescript");

const CLONES = "/Users/jackwestbrook/dev/sandbox/react-detect-plugins/plugins";
const DEV = "/Users/jackwestbrook/dev/grafana";

// slug -> scan root(s). Default: <clones>/<slug>/src
const ROOT_OVERRIDES = {
  "grafana-app-observability-app": [`${DEV}/app-observability-plugin/plugin/src`],
  "grafana-irm-app": [`${DEV}/irm/packages/@plugins`, `${DEV}/irm/packages/@grafana-irm`],
  "grafana-ml-app": [`${DEV}/machine-learning/ui-plugins/grafana-ml-app/src`],
  "grafana-llm-app": [`${DEV}/grafana-llm-app/packages/grafana-llm-app/src`],
  "grafana-k8s-app": [`${DEV}/grafana-k8s-plugin/src`],
  "grafana-sigil-app": [`${CLONES}/grafana-sigil-app/apps/plugin/src`],
  "grafana-assistant-app": [`${CLONES}/grafana-assistant-app/apps/plugin/src`],
};
const NO_SOURCE = ["elasticsearch", "grafana-labels-app", "grafana-labelmanagement-app"];

const SLUGS = ["clexporter-app","elasticsearch","grafana-adaptive-metrics-app","grafana-adaptivelogs-app",
"grafana-adaptivetraces-app","grafana-advisor-app","grafana-agentictesting-app","grafana-app-observability-app",
"grafana-asserts-app","grafana-assistant-app","grafana-auth-app","grafana-cmab-app","grafana-collector-app",
"grafana-csp-app","grafana-dbo11y-app","grafana-demodashboards-app","grafana-easystart-app","grafana-exploretraces-app",
"grafana-irm-app","grafana-k8s-app","grafana-kowalski-app","grafana-labelmanagement-app","grafana-labels-app",
"grafana-llm-app","grafana-logvolumeexplorer-app","grafana-lokiexplore-app","grafana-metricsdrilldown-app",
"grafana-ml-app","grafana-pathfinder-app","grafana-pdc-app","grafana-pyroscope-app","grafana-servicecenter-app",
"grafana-setupguide-app","grafana-sigil-app","grafana-slo-app","grafana-synthetic-monitoring-app",
"grafanacloud-cardinality-management-app","k6-app","mssql","opentsdb","stackdriver","tempo","zipkin"];

const NATIVE_INTERACTIVE = new Set(["button", "a", "input", "select", "textarea"]);
const COMPONENT_INTERACTIVE = new Set([
  "Button","LinkButton","IconButton","ToolbarButton","ClipboardButton","ConfirmButton","DeleteButton",
  "Input","AutoSizeInput","SecretInput","NumberInput","TextArea","Select","MultiSelect","AsyncSelect",
  "AsyncMultiSelect","Combobox","MultiCombobox","Checkbox","Switch","InlineSwitch","RadioButtonGroup",
  "RadioButtonList","MenuItem","Tab","FilterPill","FileUpload","Slider","TagsInput","DatePickerWithInput",
  "TimeRangeInput","TimeRangePicker","TimeOfDayPicker","DateTimePicker","CallToActionCard","TextLink",
  "SegmentInput","Segment","SegmentAsync","UnitPicker","ColorPicker","DataSourcePicker","FolderPicker",
]);
const COVERED_ATTRS = new Set(["data-testid", "data-cy", "data-pathfinder", "dataTestId", "testId", "data-test-id"]);
const PARTIAL_ATTRS = new Set(["aria-label", "ariaLabel", "id", "inputId", "name", "htmlFor"]);
const SKIP_FILE = /(\.test\.|\.spec\.|\.stor(y|ies)\.|__mocks__|__tests__|\/tests?\/|\/e2e(-tests)?\/|\/cypress\/|\/fixtures\/|\/mocks\/|jest)/;

function* walkFiles(dir) {
  let entries;
  try { entries = readdirSync(dir); } catch { return; }
  for (const e of entries) {
    if (e === "node_modules" || e === "dist" || e === ".git") { continue; }
    const p = join(dir, e);
    let st;
    try { st = statSync(p); } catch { continue; }
    if (st.isDirectory()) { yield* walkFiles(p); }
    else if (p.endsWith(".tsx") && !SKIP_FILE.test(p)) { yield p; }
  }
}

function tagName(node) {
  const t = node.tagName;
  return t ? t.getText() : "";
}

function analyzeOpeningElement(node, sf, filePath, items) {
  const name = tagName(node);
  const base = name.includes(".") ? name.split(".").pop() : name;
  const attrs = node.attributes.properties;
  let hasOnClick = false, covered = false, partialVia = null, hasSpread = false;
  for (const a of attrs) {
    if (ts.isJsxSpreadAttribute(a)) { hasSpread = true; continue; }
    const an = a.name ? a.name.getText() : "";
    if (an === "onClick" || an === "onSubmit") { hasOnClick = true; }
    if (COVERED_ATTRS.has(an)) { covered = true; }
    if (PARTIAL_ATTRS.has(an) && !partialVia) { partialVia = an; }
  }
  const isInteractive = NATIVE_INTERACTIVE.has(name) || COMPONENT_INTERACTIVE.has(base) ||
    (name === "Menu.Item") || hasOnClick;
  if (!isInteractive || covered) { return; }
  const { line } = sf.getLineAndCharacterOfPosition(node.getStart());
  items.push({
    file: filePath, line: line + 1, component: name,
    coverage: partialVia ? "partial" : (hasSpread ? "spread" : "none"),
    partialVia,
  });
}

function scanFile(filePath, items) {
  const text = readFileSync(filePath, "utf8");
  const sf = ts.createSourceFile(filePath, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const visit = (node) => {
    if (ts.isJsxOpeningElement(node) || ts.isJsxSelfClosingElement(node)) {
      analyzeOpeningElement(node, sf, filePath, items);
    }
    ts.forEachChild(node, visit);
  };
  visit(sf);
}

const report = {};
for (const slug of SLUGS) {
  if (NO_SOURCE.includes(slug)) {
    report[slug] = { status: "no-source" };
    continue;
  }
  const roots = ROOT_OVERRIDES[slug] || [`${CLONES}/${slug}/src`];
  const items = [];
  let files = 0;
  for (const root of roots) {
    for (const f of walkFiles(root)) {
      files++;
      try { scanFile(f, items); } catch (e) { console.error(`parse error ${f}: ${e.message}`); }
    }
  }
  // relativize paths against the longest matching root
  for (const it of items) {
    for (const root of roots) {
      if (it.file.startsWith(root)) { it.file = it.file.slice(root.length + 1); break; }
    }
  }
  const byComponent = {};
  for (const it of items) { byComponent[it.component] = (byComponent[it.component] || 0) + 1; }
  const byCoverage = { none: 0, partial: 0, spread: 0 };
  for (const it of items) { byCoverage[it.coverage]++; }
  report[slug] = { status: "scanned", roots, filesScanned: files, uncovered: items.length, byCoverage, byComponent, items };
  console.error(`${slug}: ${files} files, ${items.length} uncovered (none=${byCoverage.none} partial=${byCoverage.partial} spread=${byCoverage.spread})`);
}

const OUT = "/private/tmp/claude-501/-Users-jackwestbrook-dev-sandbox-react-detect-plugins/e0c10898-47cc-43ca-b061-34d774150e38/scratchpad";
writeFileSync(join(OUT, "testid-coverage.json"), JSON.stringify({ generated: "2026-08-06", report }, null, 1));
console.error("written testid-coverage.json");
