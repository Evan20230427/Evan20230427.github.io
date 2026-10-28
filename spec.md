# 2026 名古屋 5 日親子自由行規劃網站 規格說明書 (spec.md)

## 1. 專案概述與問題診斷 (System Overview & Root Cause Analysis)

### 1.1 專案背景
本專案為「2026 名古屋 5 日親子自由行（2026/11/8 - 11/12）」之互動式行程指南與飯店地圖網站，託管於 GitHub Pages 靜態網站託管服務。

### 1.2 GitHub Pages 失效根本原因剖析 (Root Cause)
1. **儲存庫命名與 GitHub Pages 網址結構差異**：
   - 當儲存庫命名為 `<username>.github.io`（使用者網站）或綁定自訂頂級網域（如 `ai-sideproject.me`）時，網站根目錄為網域根路徑 `https://<domain>/`。
   - 當儲存庫為一般專案儲存庫（`Nagoya-Travel-Planning-Website`）且移除自訂網域改用免費用戶子網域時，GitHub Pages 的正式 URL 變更為**子路徑結構**：
     `https://evan20230427.github.io/Nagoya-Travel-Planning-Website/`
2. **絕對路徑轉址導致 404**：
   - 根目錄原本的 `index.html` 內包含：
     ```html
     <meta http-equiv="refresh" content="0;url=/nagoya-2026/">
     <a href="/nagoya-2026/">點此前往行程網站</a>
     ```
   - 由於 `/nagoya-2026/` 開頭為斜線（絕對路徑），瀏覽器會直接跳轉至根網域：
     `https://evan20230427.github.io/nagoya-2026/`
   - 該路徑跳脫了本儲存庫子目錄 `/Nagoya-Travel-Planning-Website/`，導致 GitHub Pages 回應 **HTTP 404 Not Found**。
3. **解決策略**：
   - **根目錄即應用（Zero-Redirect Single Page Application）**：將完整的名古屋行程指南與互動地圖直接部署於根目錄 [`index.html`](file:///C:/Users/TW-Evan.Chen/Nagoya-Travel-Planning-Website/index.html)，造訪 `https://evan20230427.github.io/Nagoya-Travel-Planning-Website/` 時立即可用，免除額外轉址與白屏延遲。
   - **舊路徑相容性保證**：保留 `nagoya-2026/index.html` 並同步內容，確保透過舊連結造訪的使用者依然能完整瀏覽。
   - **全域 404 智慧防禦**：建立 `404.html`，當使用者輸入任意錯誤路徑時自動導回本專案首頁。

---

## 2. 系統脈絡圖 (System Context Diagram)

```mermaid
flowchart TD
    User["👨‍👩‍👦 使用者 / 家庭旅人"]
    GitHubPages["🌐 GitHub Pages CDN (專案站點)"]
    LeafletCDN["🗺️ OpenStreetMap / Leaflet CDN"]
    TailwindCDN["🎨 Tailwind CSS CDN"]
    LucideCDN["🔣 Lucide Icons CDN"]

    User -->|造訪 https://evan20230427.github.io/Nagoya-Travel-Planning-Website/| GitHubPages
    GitHubPages -->|提供 index.html / 404.html| User
    User -->|載入地圖圖資| LeafletCDN
    User -->|載入前端樣式| TailwindCDN
    User -->|載入向量圖示| LucideCDN
```

---

## 3. 部屬與容器概觀 (Deployment Overview)

```mermaid
flowchart LR
    subgraph GitHubRepo["GitHub 儲存庫: Evan20230427/Nagoya-Travel-Planning-Website"]
        MainBranch["分支: main"]
        RootIndex["/index.html (主應用入口)"]
        SubIndex["/nagoya-2026/index.html (相容入口)"]
        Fallback404["/404.html (智慧防禦頁)"]
    end

    subgraph PagesEnv["GitHub Pages 環境"]
        PagesBuilder["Legacy / Static Pages Engine"]
        PagesDomain["https://evan20230427.github.io/Nagoya-Travel-Planning-Website/"]
    end

    MainBranch -->|自動發布監聽| PagesBuilder
    PagesBuilder --> PagesDomain
```

---

## 4. 模組架構與技術選型 (Architecture & Technology Stack)

| 模組領域 | 選用技術 / 函式庫 | 說明與理由 |
| :--- | :--- | :--- |
| **前端框架** | 原生 HTML5 + Vanilla JS (ES6+) | 輕量極速，零編譯步驟，GitHub Pages 原生免建置直接發布 |
| **樣式排版** | Tailwind CSS (CDN 執行期引擎) | 響應式排版（Mobile-First），適配手機單手操作與桌面大螢幕 |
| **地圖互動** | Leaflet.js v1.9.4 + OpenStreetMap | 免費開源地圖核心，無 Google Maps API Key 額度與外洩風險 |
| **圖示系統** | Lucide Icons v0.468.0 (UMD) | 高辨識度 SVG 圖示，清晰標記交通、飯店、景點與天氣 |
| **資料儲存** | 記憶體內建結構化 JSON 陣列 | 內嵌於腳本中，零伺服器依賴，支援離線與無網路快取 |

---

## 5. 前端模組關係圖 (Frontend Module Architecture)

```mermaid
graph TD
    App["名古屋行程應用 (Nagoya Itinerary App)"]
    
    subgraph DataModule["資料層 (Data Model)"]
        HotelsData["飯店清單資料 (hotels)"]
        SpotsData["景點清單資料 (spots)"]
        DaysData["每日行程資料 (itineraryDays)"]
    end

    subgraph UIComponents["展示層 (UI Components)"]
        NavBar["頁籤導航欄 (Tab Navigation)"]
        ItineraryView["每日行程清單 (Itinerary View)"]
        HotelTableView["飯店綜合比較表 (Hotel Table View)"]
        MapView["Leaflet 互動地圖 (Interactive Map View)"]
        InfoView["自由行實用須知 (Info & Tips View)"]
        ToastNotifier["複製成功提示 (Toast Notification)"]
    end

    subgraph MapController["地圖控制器 (Map Controller)"]
        LeafletInstance["Leaflet Map 實例"]
        HotelMarkers["飯店圖標標記 (Hotel Markers)"]
        SpotMarkers["景點圖標標記 (Spot Markers)"]
    end

    DataModule --> UIComponents
    UIComponents --> MapController
```

---

## 6. 資料模型與 ER 圖 (Data Model & ER Diagram)

```mermaid
erDiagram
    DAY_ITINERARY ||--|{ ACTIVITY_ITEM : contains
    HOTEL_OPTION ||--o{ SPOT_DISTANCE : measures
    SPOT_ITEM ||--o{ SPOT_DISTANCE : referenced

    DAY_ITINERARY {
        int day "第幾天 (1-5)"
        string date "日期 (如 11/8)"
        string weekday "星期"
        string title "每日主題標題"
        string focus "核心景點"
    }

    ACTIVITY_ITEM {
        string time "預估時間"
        string title "活動名稱"
        string desc "活動說明與交通指引"
        string spotCode "關聯景點代碼"
    }

    HOTEL_OPTION {
        string code "飯店代碼 (H1-H6)"
        string name "飯店中文名稱"
        float lat "緯度"
        float lng "經度"
        string station "最近地鐵/車站"
        string walkMin "步行時間"
        string pros "優點特色"
        string cons "缺點與考量"
        string maps "Google Maps 查詢關鍵字"
    }

    SPOT_ITEM {
        string code "景點代碼 (S1-S6)"
        string name "景點名稱"
        float lat "緯度"
        float lng "經度"
        string category "分類 (景點/機場/車站)"
        string businessHours "營業時間"
        string tips "親子遊玩提醒"
    }
```

---

## 7. 關鍵業務流程圖 (Key Workflows)

### 7.1 頁籤切換與地圖重新計算流程

```mermaid
flowchart TD
    Start([使用者點擊頁籤或地圖聯動按鈕]) --> CheckTab{點擊類型}
    CheckTab -->|純頁籤切換| SwitchActive[切換 tab-content active 狀態]
    CheckTab -->|由行程/飯店點擊定位| SetTargetCoords[取得目標點之經緯度與代碼]
    SetTargetCoords --> SwitchToMap[切換至 Map 頁籤]
    SwitchActive --> IsMapActive{當前是否為地圖頁籤?}
    SwitchToMap --> IsMapActive
    IsMapActive -->|是| InitMapCheck{地圖實例是否已建立?}
    IsMapActive -->|否| End([結束])
    InitMapCheck -->|否| CreateLeaflet[建立 L.map 並綁定圖磚與標記]
    InitMapCheck -->|是| InvalidateSize[呼叫 map.invalidateSize 修正容器尺寸]
    CreateLeaflet --> InvalidateSize
    InvalidateSize --> PanToTarget{是否有指定焦點?}
    PanToTarget -->|是| FlyTo[map.setView 聚焦並開啟 Popup 彈窗]
    PanToTarget -->|否| FitAll[維持既有視野或 fitBounds]
    FlyTo --> End
    FitAll --> End
```

### 7.2 行程摘要複製至剪貼簿流程 (LINE 分享)

```mermaid
flowchart TD
    ClickCopy([使用者點擊「複製行程摘要」按鈕]) --> BuildText[組合 5 日行程精華、航班與飯店清單字串]
    BuildText --> CheckClipboardAPI{瀏覽器支援 navigator.clipboard?}
    CheckClipboardAPI -->|支援| AsyncWrite[執行 await navigator.clipboard.writeText]
    CheckClipboardAPI -->|不支援 / 被阻擋| FallbackTextarea[建立隱藏 textarea 並執行 execCommand copy]
    AsyncWrite --> CopySuccess{複製是否成功?}
    FallbackTextarea --> CopySuccess
    CopySuccess -->|成功| ShowToast[顯示浮動提示 Toast: ✅ 已複製行程摘要]
    CopySuccess -->|失敗| PromptFallback[跳出 window.prompt 讓使用者手動全選複製]
    ShowToast --> AutoHide[3.8 秒後自動隱藏 Toast]
    PromptFallback --> EndCopy([結束])
    AutoHide --> EndCopy
```

---

## 8. 序列圖 (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor User as 使用者瀏覽器
    participant GH as GitHub Pages 伺服器
    participant App as 前端入口 (index.html)
    participant Leaflet as Leaflet 地圖引擎

    User->>GH: GET /Nagoya-Travel-Planning-Website/
    GH-->>User: 200 OK (傳回完整 Single Page Application)
    User->>App: DOMContentLoaded 載入與初始化
    App->>App: 渲染行程、飯店比較表與實用資訊
    User->>App: 點選「地圖檢視」頁籤
    App->>Leaflet: 初始化 L.map('map') 並載入圖資標記
    Leaflet-->>User: 顯示包含 H1-H6 與 S1-S6 的互動地圖
    User->>App: 點選「複製行程摘要」
    App->>User: 寫入剪貼簿並彈出 Toast 通知
```

---

## 9. 狀態圖 (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> ItineraryState : 初始載入 (預設行程檢視)

    state ItineraryState {
        [*] --> BrowsingDays
        BrowsingDays --> DayDetail
    }

    state HotelTableState {
        [*] --> ViewingAllHotels
        ViewingAllHotels --> HighlightRow
    }

    state MapState {
        [*] --> MapLoading
        MapLoading --> ViewAllPins : 檢視全覽
        ViewAllPins --> FocusHotel : 聚焦單一飯店 (H1-H6)
        ViewAllPins --> FocusSpot : 聚焦單一景點 (S1-S6)
    }

    state InfoState {
        [*] --> ReadingTips
    }

    ItineraryState --> HotelTableState : 點擊「飯店比較」
    ItineraryState --> MapState : 點擊「地圖模式」或「地圖查看」
    ItineraryState --> InfoState : 點擊「實用資訊」

    HotelTableState --> ItineraryState : 點擊「每日行程」
    HotelTableState --> MapState : 點擊地圖按鈕
    HotelTableState --> InfoState : 點擊「實用資訊」

    MapState --> ItineraryState : 點擊「每日行程」
    MapState --> HotelTableState : 點擊「飯店比較」
    MapState --> InfoState : 點擊「實用資訊」

    InfoState --> ItineraryState : 點擊「每日行程」
```

---

## 10. 虛擬碼 (Pseudocode)

```javascript
// 核心頁籤與地圖切換控制器
function switchTab(targetTabName):
    FOR EACH content IN document.querySelectorAll('.tab-content'):
        IF content.id == targetTabName:
            content.classList.add('active')
        ELSE:
            content.classList.remove('active')

    FOR EACH button IN document.querySelectorAll('[data-tab]'):
        IF button.dataset.tab == targetTabName:
            highlightActiveButton(button)
        ELSE:
            unhighlightInactiveButton(button)

    IF targetTabName == 'map':
        requestAnimationFrame(() => {
            initMapIfNeeded()
            map.invalidateSize() // 避免寬高計算錯誤導致灰屏
        })

// 地圖聚焦指定座標與開啟彈窗
function showOnMap(category, itemCode):
    target = findItemByCode(category, itemCode)
    IF target is NULL: RETURN

    switchTab('map')
    requestAnimationFrame(() => {
        map.invalidateSize()
        map.setView([target.lat, target.lng], 14, { animate: false })
        marker = getMarkerByCode(itemCode)
        IF marker is NOT NULL:
            marker.openPopup()
    })
```
