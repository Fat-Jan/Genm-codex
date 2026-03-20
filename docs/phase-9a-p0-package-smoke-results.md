# Phase 9A / P0 Smoke Results

## Target

- `novel-package`

## Smoke 1: Full packaging proposal

### Prompt shape

- hard-bound project root
- `mode=full`
- read-only

### Result

- pass

### Observed behavior

- correctly stayed inside `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
- read:
  - `.mighty/state.json`
  - `大纲/总纲.md`
  - `.mighty/market-data.json`
- returned:
  - 3 title candidates
  - 2 synopsis variants
  - 3 opening-hook packaging suggestions
  - 1 recommended direction
- did not modify files

### Key conclusion

The skill behaved like a packaging layer instead of falling back to a generic project summary.

---

## Smoke 2: Naming proposal

### Prompt shape

- hard-bound project root
- `mode=naming`
- target character: `林晚照`
- read-only

### Result

- pass

### Observed behavior

- used:
  - `.mighty/state.json`
  - `大纲/总纲.md`
  - `设定集/角色/林晚照.md`
  - `设定集/角色/主角.md`
  - `chapters/番外-林晚照-番外1.md`
  - `shared/references/writing/character-naming-guide.md`
- produced 3 naming directions plus a recommendation to keep `林晚照`
- kept the answer character- and platform-aware
- did not modify files

### Key conclusion

The naming path is not a generic random-name generator. It can anchor proposals to existing canon and packaging tone.

---

## Smoke 3: Synopsis save path

### Prompt shape

- hard-bound project root
- `mode=synopsis`
- `save`

### Result

- pass

### Observed behavior

- created `包装/`
- wrote:
  - `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel/包装/简介方案.md`
- generated 3 synopsis variants
- `.mighty/state.json` hash did not change
- no other project truth files were modified

### Key conclusion

The save path works and stays outside the main truth-bearing state model.

---

## Overall conclusion

- `novel-package`: pass

First-version packaging coverage is now validated across:

- proposal-only mode
- naming mode
- save-to-file mode

This is sufficient to treat `Phase 9A / P0` as started on a working footing.
