# 飲食控管專題 - 快速設置指南

## 📋 前置準備

### 1. 安裝 Python
確保已安裝 Python 3.9 或以上版本:
```bash
python --version
```

### 2. 取得 Gemini API Key

1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登入 Google 帳號
3. 點擊 "Create API Key"
4. 複製產生的 API Key

## 🚀 快速開始

### 步驟 1: 安裝依賴套件

```bash
# 在專案根目錄執行
pip install -r requirements.txt
```

### 步驟 2: 設置環境變數

#### 方法 A: 建立 .env 檔案 (推薦)

複製範例檔案:
```bash
cp .env.example .env
```

編輯 `.env` 檔案,填入你的 API Key:
```
GEMINI_API_KEY=你的_GEMINI_API_KEY
DATABASE_URL=你的_DATABASE_URL
```

#### 方法 B: 設置系統環境變數

**Windows (命令提示字元)**:
```cmd
set GEMINI_API_KEY=你的_API_KEY
```

**Windows (PowerShell)**:
```powershell
$env:GEMINI_API_KEY="你的_API_KEY"
```

**Linux/Mac**:
```bash
export GEMINI_API_KEY=你的_API_KEY
```

### 步驟 3: 測試 AI 模組

```bash
cd AI
python test_gemini.py
```

如果看到 "🎉 所有測試通過!" 表示設置成功!

### 步驟 4: 啟動後端服務

```bash
# 回到專案根目錄
cd ..

# 啟動 FastAPI 服務
python -m api.main
# 或使用 uvicorn
uvicorn api.main:app --reload
```

服務啟動後,訪問:
- API 文件: http://localhost:8000/docs
- 健康檢查: http://localhost:8000/api/ai/health

## 📁 專案結構

```
code/
├── AI/                          # AI 模組
│   ├── __init__.py
│   ├── gemini_service.py        # Gemini API 核心服務
│   ├── config.py                # 配置檔案
│   ├── test_gemini.py           # 測試腳本
│   └── README.md
├── api/                         # FastAPI 後端
│   ├── main.py                  # 主程式
│   ├── routers/                 # API 路由
│   │   ├── ai.py               # AI 相關 API
│   │   ├── user.py             # 使用者 API
│   │   ├── diary.py            # 飲食紀錄 API
│   │   └── social.py           # 社群 API
│   └── services/
├── models/                      # 資料模型
│   └── __init__.py
├── .env                         # 環境變數 (請勿提交到 Git)
├── .env.example                 # 環境變數範例
├── requirements.txt             # Python 依賴
└── SETUP.md                     # 本文件
```

## 🧪 測試 API

### 使用 curl

**1. 檢查 AI 服務狀態**:
```bash
curl http://localhost:8000/api/ai/health
```

**2. 營養分析**:
```bash
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "meals": [
      {
        "food_name": "雞胸肉",
        "calories": 165,
        "protein": 31,
        "carbs": 0,
        "fat": 3.6
      }
    ]
  }'
```

**3. 餐點推薦**:
```bash
curl -X POST http://localhost:8000/api/ai/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "age": 25,
      "gender": "male",
      "height": 175,
      "weight": 70,
      "activity_level": "moderate",
      "goal": "maintain"
    },
    "preferences": "高蛋白"
  }'
```

### 使用 FastAPI 互動式文件

訪問 http://localhost:8000/docs 可以直接在瀏覽器測試所有 API。

## 🔧 常見問題

### Q1: 顯示 "GEMINI_API_KEY 未設置"

**解決方法**:
1. 確認已建立 `.env` 檔案
2. 確認 `.env` 檔案中有 `GEMINI_API_KEY=你的KEY`
3. 重新啟動服務

### Q2: Import Error - 找不到 AI 模組

**解決方法**:
```bash
# 在專案根目錄執行,而不是 AI 資料夾內
python -m api.main
```

### Q3: Gemini API 呼叫失敗

**可能原因**:
1. API Key 錯誤或已過期
2. 網路連線問題
3. 超過免費額度限制

**解決方法**:
1. 重新產生 API Key
2. 檢查網路連線
3. 查看 [API 使用量](https://aistudio.google.com/)

### Q4: 模組版本衝突

**解決方法**:
```bash
# 建議使用虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 重新安裝依賴
pip install -r requirements.txt
```

## 📊 API 端點總覽

| 端點 | 方法 | 功能 | 狀態 |
|------|------|------|------|
| `/api/ai/health` | GET | 檢查服務狀態 | ✅ |
| `/api/ai/analyze` | POST | 營養分析 | ✅ |
| `/api/ai/recommend` | POST | 餐點推薦 | ✅ |
| `/api/ai/question` | POST | 營養問答 | ✅ |
| `/api/users/*` | - | 使用者管理 | 🚧 |
| `/api/diary/*` | - | 飲食紀錄 | 🚧 |
| `/api/social/*` | - | 社群功能 | 🚧 |

圖例: ✅ 已完成 | 🚧 開發中 | ❌ 未開始

## 🎯 下一步

1. **前端開發**: 使用 Stitch 建立 UI,透過 `fetch` 呼叫 API
2. **資料庫整合**: 連接 Vercel Postgres 儲存使用者資料
3. **部署**: 將專案部署到 Vercel

## 📚 參考資源

- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [Google Gemini API 文件](https://ai.google.dev/docs)
- [Vercel 部署指南](https://vercel.com/docs)
- [Pydantic 文件](https://docs.pydantic.dev/)

## 🤝 團隊協作

### 後端團隊
- 使用 Git 進行版本控制
- 定義清楚的 API 介面(Pydantic 模型)
- 撰寫單元測試

### 前端團隊
- 參考 API 文件 (http://localhost:8000/docs)
- 使用 `fetch` API 呼叫後端
- 處理 JSON 回應更新 UI

---

如有問題,請參考 [AI/README.md](AI/README.md) 或洽詢團隊成員。
