import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "shared" / "templates" / "profile-bucket-registry-v1.json"


class ProfileBucketRegistryTests(unittest.TestCase):
    def test_registry_exists_and_contains_key_fanqie_mappings(self) -> None:
        self.assertTrue(REGISTRY_PATH.exists(), "profile bucket registry is missing")
        payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], "1.0")
        mappings = payload["fanqie_bucket_keys"]
        self.assertEqual(mappings["gongdou_zhai"]["bucket_name"], "宫斗宅斗")
        self.assertEqual(mappings["gongdou_zhai"]["profile_slug"], "palace-intrigue")
        self.assertEqual(mappings["dushi_naodong"]["bucket_name"], "都市脑洞")


if __name__ == "__main__":
    unittest.main()
