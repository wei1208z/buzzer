# 🚀 即時多人作答與搶答系統 (Real-time Multiplayer Buzzer System)

🎉 **線上體驗版 (Live Demo)：** [https://buzzer-wt11.onrender.com](https://buzzer-wt11.onrender.com)
🎙️ **主持人專屬控制台：** [https://buzzer-wt11.onrender.com/host](https://buzzer-wt11.onrender.com/host)

這是一個基於 **Python (FastAPI) + WebSocket** 與 **Docker** 架構開發的輕量級即時多人作答系統。系統採前後端分離設計，具備專屬的「主持人中控台」與「參賽者介面」，非常適合用於課堂互動、團康遊戲或線上搶答活動。

---

## ✨ 核心特色功能

- **🚀 超低延遲 WebSocket 雙向連線**：後端統一作為唯一的裁判基準，確保作答與鎖定的時間絕對公平。
- **📝 支援自訂答案與無人數上限**：參賽者除了輸入姓名，還可以提交文字答案，且系統無作答人數上限。
- **🤖 智慧裝置識別 (支援同名玩家)**：前端自動配發唯一隱藏 UUID，就算全班都輸入一樣的名字，系統也能精準辨識每個人的裝置，不會互相干擾鎖定狀態。
- **🔐 主持人動態密碼與排他機制**：
  - 登入密碼自動與「當天日期 (YYYYMMDD)」掛鉤（例如 2026年5月17日 的密碼即為 `20260517`）。
  - 系統嚴格限制**最多只能有一位主持人登入**，防止多重身分造成活動混亂；且未登入者無法透過 API 惡意觸發重置。
- **🛡️ 畫面安全防護**：前端具備防止超長字串惡意洗頻、破版溢出的 CSS 防護機制。
- **🐳 完美 Docker 容器化**：前後端完全整合，一鍵即可完成本地或雲端部署。

---

## 💻 技術堆疊 (Tech Stack)

- **後端 (Backend)**：Python 3.10, FastAPI, Uvicorn, WebSockets
- **前端 (Frontend)**：HTML5, CSS3, Vanilla JavaScript
- **部署 (Deployment)**：Docker, Docker Compose, Render (PaaS)

---

## 🎮 如何使用 (線上版教學)

### 🎙️ 給主持人 (活動主辦方)
1. 進入 [主持人控制台](https://buzzer-wt11.onrender.com/host)。
2. 於登入畫面輸入**當天日期的 8 碼數字**（如 `20260517`）。
3. 進入儀表板後，點擊 **「🟢 開放作答」**，所有參賽者的畫面將瞬間解鎖。
4. 參賽者送出答案後，畫面會即時更新「已答人數」與「詳細答案名單」。
5. 點擊 **「🛑 鎖定作答」** 即可隨時結算該回合。

### 📱 給參賽者 (玩家)
1. 使用手機或電腦進入主網址：[https://buzzer-wt11.onrender.com](https://buzzer-wt11.onrender.com)。
2. 輸入您的「姓名」與「答案」（可選）。
3. 緊盯畫面！一旦主持人開放，畫面會變成綠色，請立刻點擊 **「搶答」** 按鈕送出答案。

---

## 🛠️ 本地端快速啟動 (Local Deployment)

如果您想在自己的電腦或區域網路內運行此系統，請確保已安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。

### 1. 啟動伺服器
在包含 `docker-compose.yml` 的專案根目錄下，開啟終端機並執行：
```bash
docker-compose up -d --build