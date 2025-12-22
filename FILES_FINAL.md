# 專題檔案說明 (整理後)

## 📁 核心檔案

### AI 模組 (AI/)

| 檔案 | 說明 | 狀態 |
|------|------|------|
| `__init__.py` | 模組初始化,導出 V2 類別 | ✅ 主要 |
| `gemini_service.py` | **Gemini API 核心服務 V2** | ⭐ 主要 |
| `config.py` | 配置與常數 | ✅ 輔助 |
| `README.md` | AI 模組文件 | 📖 文件 |
| `IMPROVEMENTS.md` | V2 改進說明 | 📖 文件 |
| `CHANGELOG.md` | 更新日誌 | 📖 文件 |
| `QUICKSTART.md` | 快速開始 | 📖 文件 |
| `test_gemini.py` | 測試腳本 | 🧪 測試 |
| `gemini_service_v1_backup.py` | V1 備份 | 💾 備份 |

### API 後端 (api/)

| 檔案 | 說明 | 狀態 |
|------|------|------|
| `main.py` | FastAPI 主程式 | ✅ 主要 |
| `routers/ai.py` | AI API 路由 | ✅ 主要 |
| `routers/user.py` | 使用者 API | 🚧 開發中 |
| `routers/diary.py` | 飲食紀錄 API | 🚧 開發中 |
| `routers/social.py` | 社群 API | 🚧 開發中 |

### 根目錄檔案

| 檔案 | 說明 | 用途 |
|------|------|------|
| `chat_v2.py` | **AI 聊天程式 V2** | ⭐ 推薦使用 |
| `chat_with_ai_final.py` | 簡單聊天程式 | ✅ 備用 |
| `test_memory_quick.py` | 快速測試對話記憶 | 🧪 測試 |
| `example_usage.py` | 完整使用範例 | 📖 範例 |
| `requirements.txt` | Python 依賴 | ⚙️ 配置 |
| `.env.example` | 環境變數範例 | ⚙️ 配置 |
| `.gitignore` | Git 忽略清單 | ⚙️ 配置 |

### 文件

| 檔案 | 說明 |
|------|------|
| `README.md` | 專題總覽 |
| `SETUP.md` | 詳細設置指南 |
| `GETTING_STARTED.md` | 快速上手 |
| `QUICK_REFERENCE.md` | 快速參考 |
| `FILES_OVERVIEW.md` | 完整檔案說明 |
| `FILES_FINAL.md` | 本文件(整理後) |

---

## 🗑️ 已刪除的重複檔案

以下檔案已刪除(功能重複或測試用):

- `ai_demo_simulation.py` - 模擬示範(已整合到 chat_v2.py)
- `chat_demo.py` - 舊版聊天(已被 chat_v2.py 取代)
- `check_models.py` - 檢查模型(測試用,已不需要)
- `compare_v1_v2.py` - 比較文件(已整合到 IMPROVEMENTS.md)
- `demo_without_api.py` - 無 API 示範(已不需要)
- `quick_chat_test.py` - 快速測試(已被 chat_v2.py 取代)
- `test.py` - 空檔案
- `test_improved_ai.py` - 改進測試(已被 test_memory_quick.py 取代)
- `test_real_ai.py` - 真實測試(已被 chat_v2.py 取代)
- `test_with_google_sdk.py` - SDK 測試(已不需要)

---

## ✅ 核心功能文件

### 1. AI 聊天 (推薦)

**使用**: `chat_v2.py`

```bash
python chat_v2.py
```

**特色**:
- ✅ 支援對話記憶
- ✅ 智慧推薦健康餐廳
- ✅ 彈性回答長度
- ✅ 完整的指令系統

**指令**:
- 輸入問題 → AI 回答(會記住上下文)
- `clear` → 清除對話歷史
- `history` → 查看對話記錄
- `examples` → 範例問題
- `q` 或 `exit` → 離開

### 2. 快速測試

**使用**: `test_memory_quick.py`

```bash
python test_memory_quick.py
```

**用途**: 驗證對話記憶功能是否正常

### 3. 程式中使用

```python
from AI import GeminiService, AIRecommender

# 初始化
gemini = GeminiService(api_key="你的KEY")
recommender = AIRecommender(gemini)

# 對話會自動記住上下文
answer1 = recommender.answer_question("午餐推薦什麼?")
answer2 = recommender.answer_question("剛才那道菜怎麼做?")  # ✓ 會記得

# 清除對話歷史
gemini.clear_conversation()
```

---

## 📊 V2 改進總結

### 問題 1: 無法記住對話上下文 ✅ 已解決
- 新增 `conversation_history` 記錄對話
- 自動保留最近 3 輪對話
- 構建上下文提示詞

### 問題 2: 餐廳推薦不夠健康 ✅ 已解決
- 新增 `recommend_restaurants()` 方法
- 系統提示詞強調健康優先
- 考慮使用者健康目標

### 問題 3: 回答長度不夠彈性 ✅ 已解決
- `max_tokens` 增加到 800
- `temperature` 增加到 0.8
- 簡單問題 2-3 句,複雜問題 4-6 句

---

## 🎯 快速開始

### 步驟 1: 安裝依賴
```bash
pip install google-generativeai pydantic
```

### 步驟 2: 設置 API Key
```bash
# 編輯 .env 檔案
GEMINI_API_KEY=你的KEY
```

或在程式中直接設置:
```python
gemini = GeminiService(api_key="你的KEY")
```

### 步驟 3: 開始使用
```bash
python chat_v2.py
```

---

## 📖 相關文件

- [AI/README.md](AI/README.md) - AI 模組詳細說明
- [AI/IMPROVEMENTS.md](AI/IMPROVEMENTS.md) - V2 改進詳情
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速參考卡片

---

## 🔄 版本說明

- **V1** (gemini_service_v1_backup.py): 原始版本,已備份
- **V2** (gemini_service.py): ⭐ 當前版本,支援對話記憶

**建議**: 全部使用 V2 版本

---

## 📞 取得幫助

遇到問題?
1. 查看 [SETUP.md](SETUP.md#常見問題)
2. 執行 `python test_memory_quick.py` 測試
3. 查看 [AI/IMPROVEMENTS.md](AI/IMPROVEMENTS.md)

---

**整理日期**: 2024-11-24
**版本**: V2.0 (對話記憶版)
**狀態**: ✅ 可用於生產環境
