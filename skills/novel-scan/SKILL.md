---
name: novel-scan
description: Run a report-only or project-annotate market scan for a Codex-managed novel project by organizing external source candidates, recording confidence, writing `.mighty/market-data.json`, and optionally annotating project-local market state without default profile rewrites.
---

# Novel Scan

Use this skill when the user wants a market/trend scan that informs writing direction or future profile adjustments.

## Positioning

This is an experimental implementation that currently supports:

- `report-only`
- `project-annotate`

It should:

- organize scan targets
- record candidate sources
- summarize findings conservatively
- recommend likely content buckets when evidence supports that
- expose bucket recommendations in a shape downstream skills can consume
- write a local `.mighty/market-data.json`
- optionally annotate project-local market state

It should not by default:

- rewrite `shared/profiles/`
- rewrite project profile state
- pretend that weak or missing sources are strong evidence

## Inputs

- optional `platform`
- optional `genre`
- optional `depth`
  - `quick`
  - `standard`
  - `deep`
- optional explicit mode:
  - `report-only`
  - `project-annotate`

## Preconditions

- `.mighty/` exists or can be created inside the current project

## Data source policy

Follow the Phase 7A contract:

- Level A: official / platform pages
- Level B: stable extraction layer
- Level C: search / aggregation layer
- Level D: user-provided material

If no trustworthy source material is actually fetched or provided in the current run:

- do not fabricate findings
- write a low-confidence skeleton instead

## Output file

- `.mighty/market-data.json`

## Project annotation target

When mode is `project-annotate`, the only project state area this skill may update is:

- `.mighty/state.json` → `market_adjustments`

## Workflow

1. Parse the requested platform / genre / depth.
2. Determine scan mode:
   - default to `report-only`
3. Build a source plan:
   - target platforms
   - candidate source categories
   - trust levels
4. Check what evidence is actually available in the current run:
   - user-provided text
   - local source files
   - explicitly fetched external content if the environment and prompt make that appropriate
5. If evidence is insufficient:
   - write a conservative market-data skeleton
   - set low confidence
   - list the missing evidence
6. If evidence exists:
   - summarize only defensible findings
   - separate findings from suggestions
   - when the platform is 番茄 and the evidence supports it, infer a small set of likely content buckets
   - if first-batch MVP bucket configs exist, read `../../docs/fanqie-mvp-buckets.yaml`
   - when a recommended bucket matches an existing config entry, include:
     - `config_key`
     - `priority_rank`
     - `track`
   - keep bucket reasoning and confidence visible
   - keep trust attribution visible
7. Save the result to `.mighty/market-data.json`.
8. If mode is `project-annotate`:
   - update `.mighty/state.json` conservatively under `market_adjustments`
   - set:
     - `last_applied`
     - `source_scan`
     - `adjustments`
   - only use low-risk, project-local suggestion summaries
   - do not rewrite `shared/profiles/`
9. Return:
   - mode used
   - sources considered
   - confidence
   - recommended buckets when available
   - whether the result is only a scaffold or a real report

## Recommended result shape

```json
{
  "version": "1.0",
  "scan_time": "<timestamp>",
  "mode": "report-only",
  "targets": {
    "platforms": [],
    "genre": ""
  },
  "sources": [],
  "findings": {
    "hot_genres": [],
    "recommended_content_buckets": [
      {
        "bucket_name": "",
        "config_key": "",
        "priority_rank": 0,
        "track": "",
        "confidence": "",
        "reason": ""
      }
    ],
    "hot_tags": [],
    "opening_patterns": [],
    "cool_point_patterns": [],
    "platform_notes": []
  },
  "confidence": {
    "overall": "low",
    "reason": "insufficient trusted source material in current run"
  },
  "gaps": [],
  "apply_recommendations": []
}
```

## Notes

- This version is useful even when it only records a source plan plus confidence and gaps.
- Treat “report-only” as the safe default.
- `project-annotate` may update project-local `market_adjustments`, but must not alter shared assets.
- If the user explicitly asks for real external collection and the environment supports it, keep source attribution visible and do not overstate confidence.
- When bucket recommendations are produced, keep them small and ranked; prefer 1-3 defensible candidates over a long speculative list.
- When `config_key` is available, prefer the exact key from `fanqie-mvp-buckets.yaml` so downstream skills can consume the recommendation without fuzzy matching.
