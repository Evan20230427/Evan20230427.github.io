import re
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class HtmlIntegrityTests(unittest.TestCase):
    def test_root_index_html_exists_and_valid(self):
        root_index = BASE_DIR / "index.html"
        self.assertTrue(root_index.exists(), "Root index.html must exist")
        content = root_index.read_text(encoding="utf-8")

        # 確保不含有跳出專案目錄的絕對轉址路徑
        self.assertNotIn('url=/nagoya-2026/', content)
        self.assertNotIn('href="/nagoya-2026/"', content)

        # 確保包含必要的單頁應用元素
        self.assertIn('id="day-cards"', content)
        self.assertIn('id="map"', content)
        self.assertIn('id="hotel-cards"', content)
        self.assertIn('id="matrix-rows"', content)
        self.assertIn('id="toast"', content)

    def test_legacy_subfolder_index_exists(self):
        legacy_index = BASE_DIR / "nagoya-2026" / "index.html"
        self.assertTrue(legacy_index.exists(), "nagoya-2026/index.html must exist")
        content = legacy_index.read_text(encoding="utf-8")
        self.assertNotIn('url=/nagoya-2026/', content)

    def test_404_html_exists(self):
        page_404 = BASE_DIR / "404.html"
        self.assertTrue(page_404.exists(), "404.html must exist")
        content = page_404.read_text(encoding="utf-8")
        self.assertIn("404", content)
        self.assertIn("Nagoya-Travel-Planning-Website", content)


if __name__ == "__main__":
    unittest.main()
