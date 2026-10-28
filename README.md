# 2026 名古屋 5 日親子自由行｜行程指南與飯店互動地圖

![GitHub Pages Deployment](https://img.shields.io/badge/GitHub%20Pages-Active-success)
![HTML5 / TailwindCSS / Leaflet](https://img.shields.io/badge/Stack-HTML5%20%7C%20TailwindCSS%20%7C%20Leaflet.js-blue)
![License](https://img.shields.io/badge/License-MIT-green)

專為 **2026 年 11 月 8 日（日）至 11 月 12 日（四）** 名古屋 5 日親子自由行打造的高效行程規劃與決策輔助網站。整合每日步調、六大候選飯店優劣勢比較、OpenStreetMap 互動地圖以及一鍵 LINE 行程分享功能。

---

## 🌐 線上展示網址 (Live Demo)

- **正式首頁（官方推薦入口）**：
  👉 [https://evan20230427.github.io/Nagoya-Travel-Planning-Website/](https://evan20230427.github.io/Nagoya-Travel-Planning-Website/)
- **相容路徑（舊版書籤亦可直接造訪）**：
  👉 [https://evan20230427.github.io/Nagoya-Travel-Planning-Website/nagoya-2026/](https://evan20230427.github.io/Nagoya-Travel-Planning-Website/nagoya-2026/)

> **💡 GitHub Pages 路徑說明**：
> 本儲存庫為專案型站點（Project Pages），所有網頁資源均託管於 `/Nagoya-Travel-Planning-Website/` 子路徑下。本專案已全面優化為零轉址單頁應用（SPA），並具備相對路徑防禦與 `404.html` 智慧防護，徹底排除絕對路徑導致的 404 問題。

---

## ✨ 核心特色與功能

1. **五日行程節奏規劃**：
   - **Day 1（11/8 日）**：抵達名古屋中部國際機場（NGO）、名鐵特急進市區、飯店 Check-in、名古屋站周邊晚餐（鰻魚飯/手羽先）。
   - **Day 2（11/9 一）**：日本樂高樂園（LEGOLAND Japan）整日暢玩（建議 10:00–17:00）。
   - **Day 3（11/10 二）**：名古屋港水族館（南館海豚秀、北館白鯨、企鵝館）、港區散策。
   - **Day 4（11/11 三）**：動植物園或科學文創（方案 A：東山動植物園；方案 B：名古屋市科學館+榮商圈購物）。
   - **Day 5（11/12 四）**：晨間悠閒早餐、名鐵常滑/新特麗亞機場伴手禮採購、返台（11:40 班機）。
2. **六間候選飯店距離與優劣勢評比 (H1 ～ H6)**：
   - `H1` 名古屋 JR 門樓酒店（JR 名古屋站直結，親子推車首選）
   - `H2` 大和 ROYNET 太閣通口（JR 太閣通口約 4 分鐘，高 CP 值首選）
   - `H3` 名古屋王子大飯店天空塔（青波線笹島演奏廳站直結，高空夜景無敵）
   - `H4` SONO Moon Nagoya（名古屋站步行約 8 分鐘，全新簡約設計風格）
   - `H5` Just Inn Premium（名古屋站步行約 10 分鐘，平價高質感商務）
   - `H6` MYSTAYS 名古屋榮（榮站步行約 7 分鐘，緊鄰熱鬧商圈）
3. **Leaflet 互動式景點與飯店地圖**：
   - 整合 OpenStreetMap 圖資，標記所有候選飯店（綠色圖標 H1~H6）與核心交通/景點（藍/紅色圖標 S1~S6）。
   - 支援「由行程一鍵直達地圖定位」，自動平移視野並開啟詳細介紹彈窗。
4. **一鍵複製 LINE 行程摘要**：
   - 內建一鍵複製按鈕，自動組合易於閱讀的排版文字，方便在 LINE 群組中與家人朋友即時溝通確認。

---

## 🛠️ 本地開發與預覽 (Local Development)

本專案採用純靜態架構，無須複雜建置流程，只需啟動任意本地 HTTP 伺服器即可預覽：

### 方法一：使用 Python 內建伺服器（推薦）
```powershell
# 切換至專案根目錄
cd Nagoya-Travel-Planning-Website

# 啟動本機伺服器 (通訊埠 8000)
python -m http.server 8000
```
瀏覽器開啟：`http://localhost:8000/`

### 方法二：使用 Node.js / npx serve
```powershell
npx serve .
```

---

## 📂 檔案目錄結構

```text
Nagoya-Travel-Planning-Website/
├── index.html            # 網站主入口（零轉址 SPA，直接提供完整功能）
├── nagoya-2026/
│   └── index.html        # 相容入口（提供舊連結直接存取）
├── 404.html              # GitHub Pages 智慧 404 防禦頁面
├── spec.md               # 系統架構規格說明書（含 12 種 Mermaid 架構圖）
├── README.md             # 本說明文件
└── tests/                # 自動化端到端 (E2E) 測試套件
    └── test_e2e.py       # Playwright 網頁功能與路由完整性測試
```

---

## 🔒 資安與隱私宣告 (Security & Privacy)

本專案遵循最高資安與隱私保護原則：
1. **零機密殘留**：無硬編碼之任何個人身分證字號、護照號碼、私密信用卡資訊或付費 API Key。
2. **依賴安全無虞**：所有外部 CDN 腳本（TailwindCSS, Leaflet, Lucide）均使用公開成熟之穩定發行版本。
