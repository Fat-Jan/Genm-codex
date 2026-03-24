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

## Fanqie rule position

When this skill is used in a Fanqie-first project, treat it as an upstream signal producer.

It may:

- recommend likely content buckets
- summarize title / opening / pattern observations

It must not:

- override canon
- override the active project bucket without explicit human or workflow choice
- override bucket rules or writing-technique rules already selected downstream
- bypass `setting gate` and write external facts straight into `设定集/`

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
- optional `.mighty/research-candidates.json`

## Executable helper

当前仓库提供了一个最小可执行脚本：

- `python3 scripts/novel_scan.py <project_root> --platform <平台> --genre <题材> --depth quick --mode report-only`

它的定位是：

- 先把 source plan、外部来源抓取结果和 confidence 落成真实文件
- `project-annotate` 时，只在当前证据达到中高可信后，再把项目级建议收成 sidecar + 轻量 state 摘要
- 优先复用 `scripts/acquire_source_text.py`，避免单个抓取工具失效就把整条扫描链卡死

当前内置默认来源仍然有限：

- 已内置：`番茄 + 玄幻 + quick`
- 其他组合建议显式传 `--source-url`

## Optional setting-gate handoff

When the scan produces a conservative truth-gap signal, it may also emit:

- `.mighty/research-candidates.json`

This file is optional and should only be used as:

- candidate input for `setting gate`
- review-queue material

It must not be treated as:

- confirmed canon
- direct `设定集/` write authority

Current minimal CLI shape:

- `python3 scripts/novel_scan.py <project_root> --platform 番茄 --genre 宫斗宅斗 --depth quick --mode project-annotate --emit-research-candidates`
- `python3 scripts/setting_gate.py <project_root> --stage outline --candidates-file .mighty/research-candidates.json`

## Project annotation target

When mode is `project-annotate`, the preferred project update target is:

- `.mighty/market-adjustments.json`

but only when the current run has medium/high confidence evidence.

Otherwise:

- keep only `.mighty/market-data.json`
- do not leave stale `market-adjustments` sidecars behind

and the runtime state should only keep a lightweight summary/pointer.

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
   - if Fanqie-first packaging / writing guidance is relevant, also read:
     - `../../docs/fanqie-writing-techniques.md`
     - `../../docs/fanqie-rule-priority-matrix.md`
   - use writing-technique rules only to classify:
     - title patterns
     - opening patterns
     - payoff patterns
     not to rewrite downstream rules
   - when a recommended bucket matches an existing config entry, include:
     - `config_key`
     - `priority_rank`
     - `track`
   - keep bucket reasoning and confidence visible
   - keep trust attribution visible
7. Save the result to `.mighty/market-data.json`.
8. If mode is `project-annotate`:
   - only update `.mighty/market-adjustments.json` when confidence is medium/high
   - keep `.mighty/state.json` only as a summary / pointer when guidance has been externalized
   - set:
     - `last_applied`
     - `source_scan`
     - `adjustments`
   - only use low-risk, project-local suggestion summaries
   - if confidence stays low or the result degrades to skeleton, keep only `market-data.json`
   - do not rewrite `shared/profiles/`
   - when the project is blocked by `setting gate`, treat scan results as candidate input for the gate and review queue, not as confirmed canon
9. If explicit candidate emission is requested:
   - write `.mighty/research-candidates.json` only for conservative truth-gap candidates
   - keep the file small and review-oriented
   - do not emit broad speculative fact dumps
   - do not bypass `setting gate`
10. Return:
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
- `project-annotate` may update project-local market-adjustment sidecar data, but must not alter shared assets.
- `novel-scan` is upstream of `setting gate` when external research is truly needed; it should feed candidate material, not direct canon writes.
- optional research candidate output is a handoff seam, not a second truth system.
- If the user explicitly asks for real external collection and the environment supports it, keep source attribution visible and do not overstate confidence.
- When bucket recommendations are produced, keep them small and ranked; prefer 1-3 defensible candidates over a long speculative list.
- When `config_key` is available, prefer the exact key from `fanqie-mvp-buckets.yaml` so downstream skills can consume the recommendation without fuzzy matching.
