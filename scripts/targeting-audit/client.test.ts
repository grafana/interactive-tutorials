import fs from 'fs';
import { rankRecommendations, legacyRelevance, localRelevance } from './recommendation-ranking';
import type { Recommendation } from '../types/context.types';

// Run in a disposable pinned Pathfinder checkout. Server responses are the real
// handler's output; this verifies client completion/fallback behavior on this catalog.
const results = JSON.parse(fs.readFileSync(process.env.AUDIT_RESULTS!, 'utf8'));
const scenarios = JSON.parse(fs.readFileSync(process.env.AUDIT_SCENARIOS!, 'utf8'));
const inventory = JSON.parse(fs.readFileSync(process.env.AUDIT_INVENTORY!, 'utf8'));
const manifests = new Map(inventory.map((x: any) => [x.id, x]));
const rec = (r: any): Recommendation => ({
  title: r.id, url: `bundled:${r.id}`, type: 'package', repository: 'interactive-tutorials',
  relevance: r.relevance, matchAccuracy: r.accuracy,
  manifest: { id: r.id, type: (manifests.get(r.id) as any)?.type ?? 'guide', ...((manifests.get(r.id) as any)?.prerequisites ?? {}) },
});
it('ranks every catalog scenario with and without completion, retaining stronger tiers', () => {
  for (const scenario of scenarios) {
    const candidates = results.after[scenario.name]['10'].map(rec);
    const ranked = rankRecommendations(candidates, scenario.context.path);
    for (let i = 1; i < ranked.length; i++) expect(ranked[i-1]!.relevance!.tier).toBeGreaterThanOrEqual(ranked[i]!.relevance!.tier);
    if (ranked.length > 1) {
      const marked = ranked.map((r, i) => ({...r, completionPercentage:i===0 ? 100 : 0}));
      const done = rankRecommendations(marked, scenario.context.path);
      for (let i = 1; i < done.length; i++) {
        expect(done[i-1]!.relevance!.tier).toBeGreaterThanOrEqual(done[i]!.relevance!.tier);
        if (done[i-1]!.relevance!.tier===done[i]!.relevance!.tier) expect(done[i-1]!.completionPercentage).toBeLessThanOrEqual(done[i]!.completionPercentage!);
      }
    }
  }
});
it('keeps richer rules out of offline fallback for the entire catalog', () => {
  for (const item of inventory) {
    const match=item.after?.match;
    if (!match) continue;
    const richer=Object.keys(match).length && /"(?:tag|allTags|tagIn|userRole|userRoleIn|source|sourceIn|urlRegex)"/.test(JSON.stringify(match));
    for(const scenario of scenarios.filter((s:any)=>s.include.includes(item.id))) {
      const relevance=localRelevance(match,scenario.context.path,scenario.context.platform);
      if(richer) expect(relevance).toBeUndefined(); else expect(relevance).toBeDefined();
    }
  }
});
it('old responses remain rankable without fabricated task evidence', () => {
  const legacy=results.after['matrix:explore-selected-loki']['10'].map(rec).map((r:Recommendation)=>{
    const {relevance,...without}=r;
    return {...without,relevance:legacyRelevance(without,'/explore')};
  });
  expect(rankRecommendations(legacy)).toHaveLength(legacy.length);
  legacy.forEach((r:Recommendation)=>expect(r.relevance!.tier).toBe(0));
});
