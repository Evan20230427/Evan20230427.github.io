import threading
import time
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

PORT = 8765
BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = Path(r"C:\Users\TW-Evan.Chen\.gemini\antigravity-cli\brain\5bd86a94-eeb2-4a25-8077-4c3424678f23")


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        # 靜音本地伺服器請求日誌
        pass


class NagoyaWebsiteE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 啟動本機測試 HTTP 伺服器
        cls.server = HTTPServer(("127.0.0.1", PORT), CustomHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5)

        # 啟動 Playwright 瀏覽器
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_root_homepage_loads_and_switches_tabs(self):
        page = self.browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(f"http://127.0.0.1:{PORT}/index.html")

        # 1. 驗證標題與首頁關鍵文字
        self.assertIn("2026 名古屋 5 日親子自由行", page.title())
        header_text = page.locator("header h1").text_content()
        self.assertIn("名古屋 5 日行程＆飯店距離地圖", header_text)

        # 2. 驗證預設行程頁籤顯示 5 天卡片
        day_cards = page.locator("#day-cards article")
        self.assertEqual(day_cards.count(), 5)

        # 3. 測試切換至「路線與飯店地圖」頁籤
        page.click("button[data-tab='map']")
        page.wait_for_selector("#tab-map.active")
        page.wait_for_timeout(1000)  # 等待 Leaflet 動畫與渲染
        map_div = page.locator("#map")
        self.assertTrue(map_div.is_visible())
        pins = page.locator(".custom-pin")
        self.assertGreaterEqual(pins.count(), 7)  # 包含名驛 + 6 飯店 + 景點

        # 4. 測試切換至「6 間飯店特色」頁籤
        page.click("button[data-tab='hotels']")
        page.wait_for_selector("#tab-hotels.active")
        hotel_cards = page.locator("#hotel-cards article")
        self.assertEqual(hotel_cards.count(), 6)

        # 5. 測試切換至「決策比較表」頁籤
        page.click("button[data-tab='matrix']")
        page.wait_for_selector("#tab-matrix.active")
        matrix_rows = page.locator("#matrix-rows tr")
        self.assertEqual(matrix_rows.count(), 6)

        # 6. 測試複製行程按鈕與浮動提示 (Toast)
        page.click("#copy-summary")
        toast = page.locator("#toast")
        page.wait_for_selector("#toast:not(.hidden)", timeout=3000)
        self.assertIn("已複製行程摘要", toast.text_content())

        # 7. 拍攝首頁完整 E2E 截圖作為客觀存證
        screenshot_path = ARTIFACT_DIR / "e2e_nagoya_homepage.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        self.assertTrue(screenshot_path.exists())
        page.close()

    def test_02_legacy_subfolder_loads_consistently(self):
        page = self.browser.new_page(viewport={"width": 1280, "height": 800})
        response = page.goto(f"http://127.0.0.1:{PORT}/nagoya-2026/index.html")
        self.assertEqual(response.status, 200)
        self.assertIn("2026 名古屋 5 日親子自由行", page.title())
        day_cards = page.locator("#day-cards article")
        self.assertEqual(day_cards.count(), 5)
        page.close()

    def test_03_404_fallback_page_structure(self):
        page = self.browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(f"http://127.0.0.1:{PORT}/404.html")
        self.assertIn("找不到頁面", page.title())
        h1_text = page.locator("h1").text_content()
        self.assertIn("找不到您要造訪的頁面", h1_text)
        home_link = page.locator("#home-link")
        self.assertTrue(home_link.is_visible())

        # 拍攝 404 頁面截圖
        screenshot_path = ARTIFACT_DIR / "e2e_nagoya_404.png"
        page.screenshot(path=str(screenshot_path))
        self.assertTrue(screenshot_path.exists())
        page.close()


if __name__ == "__main__":
    unittest.main()
