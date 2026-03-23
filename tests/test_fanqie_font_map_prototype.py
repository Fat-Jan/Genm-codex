from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "prototype_fanqie_font_map.py"


def load_module():
    spec = importlib.util.spec_from_file_location("prototype_fanqie_font_map", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FanqieFontMapPrototypeTests(unittest.TestCase):
    def test_extract_private_use_chars_returns_unique_chars_in_order(self) -> None:
        module = load_module()
        text = "渊系统"

        chars = module.extract_private_use_chars(text)

        self.assertEqual(chars, ["", ""])

    def test_resolve_exact_matches_keeps_only_unique_reference_hits(self) -> None:
        module = load_module()
        subset_signatures = {"": "sig-a", "": "sig-b", "": "sig-c"}
        reference_signatures = {
            "sig-a": ["天"],
            "sig-b": ["无", "舞"],
        }

        mapping = module.resolve_exact_matches(subset_signatures, reference_signatures)

        self.assertEqual(mapping, {"": "天"})

    def test_apply_mapping_replaces_only_known_chars(self) -> None:
        module = load_module()
        text = "渊，系统，正常文本。"

        output = module.apply_mapping(text, {"": "天", "": "无"})

        self.assertEqual(output, "天渊，无系统，正常文本。")

    def test_overlap_score_returns_one_for_identical_features(self) -> None:
        module = load_module()
        left = {("L", ((0, 0), (1, 1))): 2, ("C", ((1, 1), (2, 2), (3, 3), (4, 4))): 1}
        right = {("L", ((0, 0), (1, 1))): 2, ("C", ((1, 1), (2, 2), (3, 3), (4, 4))): 1}

        score = module.overlap_score(left, right)

        self.assertEqual(score, 1.0)

    def test_rank_candidate_features_sorts_by_score_desc(self) -> None:
        module = load_module()
        target = {("L", ((0, 0), (1, 1))): 2}
        candidates = {
            "甲": {("L", ((0, 0), (1, 1))): 2},
            "乙": {("L", ((0, 0), (1, 1))): 1},
            "丙": {("L", ((5, 5), (6, 6))): 1},
        }

        ranked = module.rank_candidate_features(target, candidates, limit=3)

        self.assertEqual([char for char, _ in ranked], ["甲", "乙", "丙"])

    def test_resolve_approximate_matches_requires_score_and_gap(self) -> None:
        module = load_module()
        candidates = {
            "": [("天", 0.24), ("兲", 0.11)],
            "": [("三", 0.38), ("丄", 0.23)],
            "": [("无", 0.19), ("旡", 0.02)],
            "": [("生", 0.77), ("主", 0.74)],
        }

        mapping = module.resolve_approximate_matches(candidates, min_score=0.2, min_gap=0.08)

        self.assertEqual(mapping, {"": "天", "": "三"})

    def test_font_number_defaults_to_zero_for_ttc(self) -> None:
        module = load_module()

        number = module.resolve_font_number(Path("/System/Library/Fonts/PingFang.ttc"), None)

        self.assertEqual(number, 0)

    def test_font_number_stays_none_for_regular_otf(self) -> None:
        module = load_module()

        number = module.resolve_font_number(Path("/tmp/SourceHanSansSC-Regular.otf"), None)

        self.assertIsNone(number)


if __name__ == "__main__":
    unittest.main()
