# 🍽️ AI 飲食控管專題

基於 Google Gemini API 的智慧飲食管理系統,提供個人化營養分析與餐點推薦。

## 📋 專題概述

本專題使用 FastAPI 後端 + Gemini AI 打造智慧飲食控管系統,核心功能包括:

- ✅ **AI 營養分析**: 自動分析飲食營養並提供改善建議
- ✅ **個人化推薦**: 根據個人資料推薦合適餐點
- ✅ **智慧問答**: AI 營養師即時回答健康問題
- 🚧 **圖像識別**: 拍照辨識食物(規劃中)
- 🚧 **社群分享**: 飲食紀錄社群功能(規劃中)

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 設置 API Key
```bash
# 複製範例檔案
cp .env.example .env

# 編輯 .env,填入你的 Gemini API Key
# 取得 API Key: https://aistudio.google.com/app/apikey
```

### 3. 測試 AI 模組
```bash
cd AI
python test_gemini.py
```

### 4. 啟動服務
```bash
python -m api.main
# 訪問 http://localhost:8000/docs 查看 API 文件
```

詳細設置請參考 [SETUP.md](SETUP.md)

## 📁 專案結構

```
code/
├── AI/                          # 🤖 AI 模組
│   ├── gemini_service.py        # Gemini API 核心服務
│   ├── config.py                # 配置與常數
│   ├── test_gemini.py           # 測試腳本
│   ├── README.md                # AI 模組詳細文件
│   └── QUICKSTART.md            # 快速開始指南
│
├── api/                         # 🌐 FastAPI 後端
│   ├── main.py                  # 主程式入口
│   ├── routers/                 # API 路由
│   │   ├── ai.py               # ✅ AI 相關 API
│   │   ├── user.py             # 🚧 使用者管理
│   │   ├── diary.py            # 🚧 飲食紀錄
│   │   └── social.py           # 🚧 社群功能
│   └── services/                # 業務邏輯
│
├── models/                      # 📊 資料模型
│   └── __init__.py              # Pydantic 模型定義
│
├── example_usage.py             # 📝 完整使用範例
├── requirements.txt             # 📦 Python 依賴
├── .env.example                 # 🔧 環境變數範例
├── SETUP.md                     # 📖 詳細設置指南
└── README.md                    # 📄 本文件
```

## 🎯 核心功能展示

### 1. 營養分析

```python
from AI.gemini_service import GeminiService, AIRecommender, MealData

gemini = GeminiService()
ai = AIRecommender(gemini)

meals = [
    MealData(food_name="雞胸肉", calories=165, protein=31, carbs=0, fat=3.6),
    MealData(food_name="糙米飯", calories=216, protein=5, carbs=45, fat=1.8)
]

analysis = ai.analyze_nutrition(meals)
print(f"總熱量: {analysis.total_calories} 大卡")
print(f"AI 評估: {analysis.analysis}")
print(f"改善建議: {analysis.suggestions}")
```

### 2. 餐點推薦

```python
from AI.gemini_service import UserProfile

user = UserProfile(
    age=25, gender="male", height=175, weight=70,
    activity_level="moderate", goal="lose_weight"
)

recommendation = ai.get_meal_recommendations(user, "高蛋白")
print(f"每日目標: {recommendation.daily_calorie_target} 大卡")
for meal in recommendation.recommended_meals:
    print(f"{meal['type']}: {meal['meal']}")
```

### 3. API 呼叫

```bash
# 檢查服務狀態
curl http://localhost:8000/api/ai/health

# 營養分析
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"meals": [{"food_name": "雞胸肉", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6}]}'
```

更多範例請執行: `python example_usage.py`

## 📊 API 端點

| 端點 | 方法 | 功能 | 狀態 |
|------|------|------|------|
| `/api/ai/health` | GET | 檢查 AI 服務狀態 | ✅ |
| `/api/ai/analyze` | POST | 分析飲食營養 | ✅ |
| `/api/ai/recommend` | POST | 獲取餐點推薦 | ✅ |
| `/api/ai/question` | POST | 營養問答 | ✅ |
| `/api/users/*` | - | 使用者管理 | 🚧 |
| `/api/diary/*` | - | 飲食紀錄 CRUD | 🚧 |
| `/api/social/*` | - | 社群貼文 | 🚧 |

**圖例**: ✅ 已完成 | 🚧 開發中 | ❌ 未開始

詳細 API 文件: http://localhost:8000/docs (啟動服務後訪問)

## 🛠️ 技術棧

### 後端
- **Framework**: FastAPI 0.109
- **AI Model**: Google Gemini 1.5 Flash
- **Validation**: Pydantic 2.5
- **Server**: Uvicorn

### 前端 (規劃)
- **UI Builder**: Stitch (快速產出 HTML/JS)
- **Deployment**: Vercel (PWA 方式)
- **API Client**: JavaScript Fetch API

### 資料庫 (規劃)
- **DB**: PostgreSQL (Vercel Postgres)
- **ORM**: SQLAlchemy

### 部署
- **Platform**: Vercel Serverless Functions
- **CI/CD**: GitHub + Vercel 自動部署

## 📚 文件導覽

- [SETUP.md](SETUP.md) - 詳細設置與安裝指南
- [AI/README.md](AI/README.md) - AI 模組完整文件
- [AI/QUICKSTART.md](AI/QUICKSTART.md) - AI 模組快速開始
- [example_usage.py](example_usage.py) - 完整使用範例

## 🤝 團隊協作指南

### 後端團隊 (2 人)

**工程師 A - 數據與核心**:
- ✅ 建立 FastAPI 基礎架構
- ✅ 整合 Gemini API
- 🚧 Vercel Postgres 連線
- 🚧 使用者認證系統
- 🚧 飲食紀錄 CRUD

**工程師 B - AI 與社群**:
- ✅ 開發 AI 分析邏輯
- ✅ Gemini Prompt Engineering
- 🚧 社群功能 API
- 🚧 Google Maps 整合

### 前端團隊 (1 人)
- 🚧 使用 Stitch 建立 UI
- 🚧 整合後端 API
- 🚧 PWA 配置

### 協作流程
1. **定義數據合約**: 使用 Pydantic 模型
2. **API 優先開發**: 後端先定義好所有 API 介面
3. **版本控制**: 使用 Git/GitHub
4. **測試驅動**: 撰寫單元測試確保品質

## 🧪 測試

### 單元測試
```bash
# 測試 AI 模組
cd AI
python test_gemini.py

# 測試完整功能
python example_usage.py
```

### API 測試
```bash
# 啟動服務
python -m api.main

# 訪問互動式文件
# http://localhost:8000/docs
```

## 🔧 常見問題

### Q: 顯示 "GEMINI_API_KEY 未設置"
**A**: 請參考 [SETUP.md](SETUP.md) 設置環境變數

### Q: Import Error
**A**: 確保在專案根目錄執行,而非子資料夾內

### Q: API 呼叫失敗
**A**: 檢查 API Key 是否正確、網路連線、免費額度

詳細故障排除請見 [SETUP.md](SETUP.md#常見問題)

## 📈 開發進度

- [x] FastAPI 基礎架構
- [x] Gemini API 整合
- [x] AI 營養分析功能
- [x] AI 餐點推薦功能
- [x] AI 問答功能
- [ ] 使用者認證系統
- [ ] 資料庫整合
- [ ] 飲食紀錄 CRUD
- [ ] 社群功能
- [ ] 圖像識別
- [ ] 前端 UI
- [ ] Vercel 部署

## 🎓 學習資源

- [FastAPI 官方教學](https://fastapi.tiangolo.com/tutorial/)
- [Google Gemini API 文件](https://ai.google.dev/docs)
- [Pydantic 使用指南](https://docs.pydantic.dev/)
- [Vercel 部署教學](https://vercel.com/docs)

## 📄 授權

本專題為教育用途,請遵守:
- Google Gemini API 使用條款
- 各開源套件的授權協議

## 👥 貢獻者

- 後端工程師 A
- 後端工程師 B
- 前端工程師

---

**開始使用**: 閱讀 [SETUP.md](SETUP.md) 開始你的開發之旅!

**需要幫助?** 查看文件或執行 `python example_usage.py` 了解完整使用流程。
