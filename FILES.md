# 專題檔案說明 - 最終精簡版

## 📁 專案結構

```
code/
├── AI/                    # AI 模組
│   ├── __init__.py       # 模組初始化
│   ├── gemini_service.py # ⭐ AI 核心服務
│   ├── config.py         # 配置檔案
│   ├── README.md         # AI 模組說明
│   └── test_gemini.py    # 測試腳本
│
├── api/                   # FastAPI 後端
│   ├── main.py           # 主程式
│   └── routers/          # API 路由
│       ├── ai.py         # AI API
│       ├── user.py       # 使用者 API
│       ├── diary.py      # 飲食紀錄 API
│       └── social.py     # 社群 API
│
├── models/                # 資料模型
│   └── __init__.py
│
├── chat_simple.py         # ⭐ AI 聊天程式
├── example_usage.py       # 使用範例
├── requirements.txt       # Python 依賴
├── .env.example          # 環境變數範例
├── .gitignore            # Git 忽略清單
│
├── README.md              # 專題總覽
├── SETUP.md               # 設置指南
├── QUICK_REFERENCE.md     # 快速參考
└── FILES.md               # 本文件
```

---

## ⭐ 核心檔案

### 1. AI 聊天程式

**檔案**: `chat_simple.py`

**用途**: 與 AI 營養師對話,支援對話記憶

**使用**:
```bash
python chat_simple.py
```

**特色**:
- ✅ 記住最近 3 輪對話
- ✅ 穩定不被過濾
- ✅ 完整指令系統

**指令**:
- 輸入問題 → AI 回答
- `clear` → 清除歷史
- `history` → 查看記錄
- `q` → 離開

---

### 2. AI 核心模組

**檔案**: `AI/gemini_service.py`

**用途**: Gemini API 核心服務

**功能**:
- `GeminiServiceV2` - AI 基礎服務
- `AIRecommenderV2` - 智慧推薦系統
- 對話記憶管理
- 營養分析
- 餐點推薦

**在程式中使用**:
```python
from AI import GeminiService, AIRecommender

gemini = GeminiService(api_key="你的KEY")
recommender = AIRecommender(gemini)

# 對話會自動記住
answer = recommender.answer_question("午餐推薦什麼?")
```

---

### 3. 使用範例

**檔案**: `example_usage.py`

**用途**: 完整的程式使用範例

**執行**:
```bash
python example_usage.py
```

---

## 📖 文件

### 主要文件

| 檔案 | 說明 | 適合對象 |
|------|------|---------|
| `README.md` | 專題總覽 | 所有人 |
| `SETUP.md` | 詳細設置指南 | 新手 |
| `QUICK_REFERENCE.md` | 快速參考卡片 | 開發者 |
| `AI/README.md` | AI 模組詳細說明 | 後端工程師 |
| `FILES.md` | 本文件 | 所有人 |

### 閱讀順序

1. **第一次使用**: README.md → SETUP.md
2. **開發時查閱**: QUICK_REFERENCE.md → AI/README.md
3. **了解架構**: FILES.md (本文件)

---

## 🚀 快速開始

### 步驟 1: 安裝依賴
```bash
pip install google-generativeai pydantic
```

### 步驟 2: 設置 API Key

方法 A - 建立 .env 檔案:
```bash
cp .env.example .env
# 編輯 .env,填入 GEMINI_API_KEY
```

方法 B - 直接在程式中設置:
```python
gemini = GeminiService(api_key="你的KEY")
```

### 步驟 3: 開始使用
```bash
python chat_simple.py
```

---

## 🎯 功能總覽

### ✅ 已完成功能

1. **對話記憶** - 記住最近 3 輪對話
2. **營養分析** - 分析飲食營養
3. **餐點推薦** - 個人化推薦
4. **營養問答** - AI 營養師問答
5. **健康餐廳推薦** - 推薦健康餐廳

### 🚧 開發中功能

- 使用者認證系統
- 資料庫整合
- 飲食紀錄 CRUD
- 社群功能
- 圖像識別

---

## 💡 常見使用場景

### 場景 1: 對話式諮詢

```bash
python chat_simple.py
```

```
你: 午餐推薦什麼菜?
AI: [推薦番茄炒蛋、糙米飯...]

你: 剛才那個怎麼做?
AI: [記得! 詳細說明番茄炒蛋做法...]
```

### 場景 2: 程式中使用

```python
from AI import GeminiService, AIRecommender

gemini = GeminiService(api_key="KEY")
ai = AIRecommender(gemini)

# 營養分析
analysis = ai.analyze_nutrition(meals)

# 餐點推薦
recommendation = ai.get_meal_recommendations(user_profile)

# 問答
answer = ai.answer_question("減重怎麼吃?")
```

### 場景 3: API 整合

```python
# 在 FastAPI 中使用
from AI import GeminiService, AIRecommender

@app.post("/api/ai/chat")
async def chat(question: str):
    answer = recommender.answer_question(question)
    return {"answer": answer}
```

---

## 📊 檔案統計

### 根目錄 (6 個)
- Python 檔案: 2 個 (chat_simple.py, example_usage.py)
- 文件: 4 個 (README.md, SETUP.md, QUICK_REFERENCE.md, FILES.md)

### AI 模組 (5 個)
- Python 檔案: 4 個 (核心 + 測試)
- 文件: 1 個 (README.md)

### API 後端 (6 個)
- main.py + 5 個路由檔案

**總計**: 約 17 個核心檔案

---

## 🗑️ 已刪除的檔案

### 根目錄 (6 個)
- simple_chat_test.py
- test_memory_quick.py
- chat_with_ai_final.py
- chat_v2.py
- FILES_OVERVIEW.md
- GETTING_STARTED.md

### AI 模組 (4 個)
- gemini_service_v1_backup.py
- CHANGELOG.md
- IMPROVEMENTS.md
- QUICKSTART.md

**共刪除**: 10 個重複/測試檔案

---

## 🔧 設定檔案

| 檔案 | 說明 | 提交 Git |
|------|------|---------|
| `requirements.txt` | Python 依賴 | ✅ 是 |
| `.env.example` | 環境變數範例 | ✅ 是 |
| `.env` | 實際環境變數(含KEY) | ❌ 否 |
| `.gitignore` | Git 忽略清單 | ✅ 是 |

---

## 📞 取得幫助

### 問題排查

1. **無法導入 AI 模組**
   - 檢查是否在專題根目錄執行
   - 確認 AI/__init__.py 存在

2. **API Key 錯誤**
   - 檢查 .env 檔案
   - 確認 KEY 正確無誤

3. **對話記憶不工作**
   - 使用 `chat_simple.py` (最穩定)
   - 確認已安裝 google-generativeai

### 查看文件

- 設置問題 → [SETUP.md](SETUP.md)
- 快速查閱 → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- AI 功能 → [AI/README.md](AI/README.md)

---

## 🎓 學習資源

- FastAPI: https://fastapi.tiangolo.com/
- Gemini API: https://ai.google.dev/docs
- Pydantic: https://docs.pydantic.dev/

---

**整理完成日期**: 2024-11-24
**版本**: 精簡版 V1.0
**檔案數量**: 17 個核心檔案
**狀態**: ✅ 可用於開發
