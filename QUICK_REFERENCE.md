# 🚀 快速參考卡片

## 📦 立即開始 (30 秒)

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 設置 API Key
set GEMINI_API_KEY=你的KEY  # Windows
export GEMINI_API_KEY=你的KEY  # Linux/Mac

# 3. 測試
python AI/test_gemini.py

# 4. 啟動服務
python -m api.main
```

**取得 API Key**: https://aistudio.google.com/app/apikey

---

## 📁 檔案導覽

| 檔案 | 用途 |
|------|------|
| [README.md](README.md) | 專題總覽 |
| [SETUP.md](SETUP.md) | 詳細設置指南 |
| [AI/README.md](AI/README.md) | AI 模組完整文件 |
| [AI/QUICKSTART.md](AI/QUICKSTART.md) | AI 快速開始 |
| [example_usage.py](example_usage.py) | 使用範例 |

---

## 🎯 核心 API

### Python 使用

```python
from AI.gemini_service import GeminiService, AIRecommender, MealData, UserProfile

# 初始化
gemini = GeminiService()
ai = AIRecommender(gemini)

# 營養分析
meals = [MealData(food_name="雞胸肉", calories=165, protein=31, carbs=0, fat=3.6)]
result = ai.analyze_nutrition(meals)

# 餐點推薦
user = UserProfile(age=25, gender="male", height=175, weight=70,
                   activity_level="moderate", goal="maintain")
rec = ai.get_meal_recommendations(user)

# 問答
answer = ai.answer_nutrition_question("減重應該怎麼吃?")
```

### HTTP API

```bash
# 健康檢查
GET http://localhost:8000/api/ai/health

# 營養分析
POST http://localhost:8000/api/ai/analyze
Content-Type: application/json
{"meals": [{"food_name": "雞胸肉", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6}]}

# 餐點推薦
POST http://localhost:8000/api/ai/recommend
Content-Type: application/json
{"user_profile": {"age": 25, "gender": "male", "height": 175, "weight": 70,
                   "activity_level": "moderate", "goal": "maintain"}}

# 問答
POST http://localhost:8000/api/ai/question
Content-Type: application/json
{"question": "減重應該怎麼吃?"}
```

---

## 📊 資料模型

### MealData (飲食數據)
```python
{
    "food_name": str,     # 食物名稱
    "calories": int,      # 熱量 (大卡)
    "protein": float,     # 蛋白質 (g) - 可選
    "carbs": float,       # 碳水 (g) - 可選
    "fat": float          # 脂肪 (g) - 可選
}
```

### UserProfile (使用者檔案)
```python
{
    "age": int,                # 年齡
    "gender": str,             # "male" / "female"
    "height": float,           # 身高 (cm)
    "weight": float,           # 體重 (kg)
    "activity_level": str,     # 活動量等級
    "goal": str                # 目標
}
```

**活動量等級**:
- `"sedentary"` - 久坐
- `"light"` - 輕度活動
- `"moderate"` - 中度活動
- `"active"` - 高度活動
- `"very_active"` - 非常活躍

**目標**:
- `"lose_weight"` - 減重
- `"maintain"` - 維持
- `"gain_muscle"` - 增肌

---

## 🔧 常用指令

### 開發
```bash
# 啟動開發伺服器 (自動重載)
uvicorn api.main:app --reload

# 執行測試
python AI/test_gemini.py

# 執行範例
python example_usage.py
```

### 測試 API
```bash
# 使用 curl
curl http://localhost:8000/api/ai/health

# 使用瀏覽器
http://localhost:8000/docs  # 互動式 API 文件
```

### 環境管理
```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安裝依賴
pip install -r requirements.txt
```

---

## ❓ 常見問題速查

| 問題 | 解決方法 |
|------|---------|
| `GEMINI_API_KEY 未設置` | 設置環境變數或建立 `.env` |
| `ModuleNotFoundError` | 執行 `pip install -r requirements.txt` |
| `Import Error` | 確保在專案根目錄執行 |
| API 呼叫失敗 | 檢查 API Key、網路、免費額度 |

詳細故障排除: [SETUP.md](SETUP.md#常見問題)

---

## 📞 取得幫助

1. 查看 [SETUP.md](SETUP.md) 詳細設置指南
2. 查看 [AI/README.md](AI/README.md) AI 模組文件
3. 執行 `python example_usage.py` 查看完整範例
4. 訪問 http://localhost:8000/docs 查看 API 文件

---

## 🎯 快速測試清單

- [ ] 安裝依賴 (`pip install -r requirements.txt`)
- [ ] 設置 API Key
- [ ] 執行測試 (`python AI/test_gemini.py`)
- [ ] 啟動服務 (`python -m api.main`)
- [ ] 訪問 API 文件 (http://localhost:8000/docs)
- [ ] 執行範例 (`python example_usage.py`)

全部通過? 🎉 開始開發吧!

---

**提示**: 將此檔案保存為書籤,方便隨時查閱!
