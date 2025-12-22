# AI 模組 - Gemini API 整合

這個模組整合了 Google Gemini 語言模型,為飲食控管專題提供 AI 智慧分析與推薦功能。

## 功能特色

### 1. 營養分析 (Nutrition Analysis)
- 分析每日飲食紀錄的總營養素
- 提供專業的營養評估
- 給出 3-5 個具體改善建議

### 2. 個人化餐點推薦 (Meal Recommendation)
- 根據使用者的年齡、性別、身高、體重計算每日熱量需求
- 考慮活動量和健康目標(減重/維持/增肌)
- 推薦早、午、晚三餐
- 支援飲食偏好設定(如素食、低碳等)

### 3. 營養問答 (Q&A)
- 回答使用者的營養健康相關問題
- 提供專業且易懂的建議

## 檔案結構

```
AI/
├── __init__.py           # 模組初始化
├── gemini_service.py     # Gemini API 核心服務
├── config.py             # 配置與常數定義
└── README.md             # 本文件
```

## 快速開始

### 1. 安裝依賴套件

```bash
pip install openai pydantic python-dotenv
```

### 2. 設置 API Key

前往 [Google AI Studio](https://aistudio.google.com/app/apikey) 取得 Gemini API Key。

建立 `.env` 檔案:

```bash
GEMINI_API_KEY=你的_API_KEY
```

或直接設置環境變數:

```bash
# Windows
set GEMINI_API_KEY=你的_API_KEY

# Linux/Mac
export GEMINI_API_KEY=你的_API_KEY
```

### 3. 使用範例

#### Python 直接使用

```python
from AI.gemini_service import GeminiService, AIRecommender, MealData, UserProfile

# 初始化服務
gemini_service = GeminiService()
recommender = AIRecommender(gemini_service)

# 營養分析
meals = [
    MealData(food_name="雞胸肉", calories=165, protein=31, carbs=0, fat=3.6),
    MealData(food_name="糙米飯", calories=216, protein=5, carbs=45, fat=1.8),
]
analysis = recommender.analyze_nutrition(meals)
print(f"總熱量: {analysis.total_calories} 大卡")
print(f"建議: {analysis.suggestions}")

# 餐點推薦
user = UserProfile(
    age=25,
    gender="male",
    height=175,
    weight=70,
    activity_level="moderate",
    goal="maintain"
)
recommendation = recommender.get_meal_recommendations(user)
print(f"每日目標: {recommendation.daily_calorie_target} 大卡")
```

#### 透過 FastAPI 使用

啟動後端服務:

```bash
python -m api.main
# 或
uvicorn api.main:app --reload
```

API 端點:

1. **營養分析**: `POST /api/ai/analyze`
   ```json
   {
     "meals": [
       {
         "food_name": "雞胸肉",
         "calories": 165,
         "protein": 31,
         "carbs": 0,
         "fat": 3.6
       }
     ]
   }
   ```

2. **餐點推薦**: `POST /api/ai/recommend`
   ```json
   {
     "user_profile": {
       "age": 25,
       "gender": "male",
       "height": 175,
       "weight": 70,
       "activity_level": "moderate",
       "goal": "maintain"
     },
     "preferences": "高蛋白"
   }
   ```

3. **營養問答**: `POST /api/ai/question`
   ```json
   {
     "question": "減重期間應該怎麼吃?"
   }
   ```

4. **服務健康檢查**: `GET /api/ai/health`

## 技術架構

### 使用的 AI 模型

- **gemini-1.5-flash**: 快速、經濟,適合大部分任務(預設)
- **gemini-1.5-pro**: 更強大,適合複雜分析

### 營養計算公式

#### 基礎代謝率 (BMR) - Harris-Benedict 公式

**男性**:
```
BMR = 66 + (13.7 × 體重kg) + (5 × 身高cm) - (6.8 × 年齡)
```

**女性**:
```
BMR = 655 + (9.6 × 體重kg) + (1.8 × 身高cm) - (4.7 × 年齡)
```

#### 每日總熱量需求 (TDEE)

```
TDEE = BMR × 活動係數
```

活動係數:
- 久坐 (sedentary): 1.2
- 輕度活動 (light): 1.375
- 中度活動 (moderate): 1.55
- 高度活動 (active): 1.725
- 非常活躍 (very_active): 1.9

#### 目標調整

- 減重 (lose_weight): TDEE - 500 大卡
- 維持 (maintain): TDEE
- 增肌 (gain_muscle): TDEE + 300 大卡

## 資料模型

### MealData
```python
{
    "food_name": str,        # 食物名稱
    "calories": int,         # 熱量(大卡)
    "protein": float,        # 蛋白質(克) - 可選
    "carbs": float,          # 碳水化合物(克) - 可選
    "fat": float,            # 脂肪(克) - 可選
    "timestamp": str         # 時間戳記 - 可選
}
```

### UserProfile
```python
{
    "age": int,              # 年齡
    "gender": str,           # 性別 (male/female)
    "height": float,         # 身高(cm)
    "weight": float,         # 體重(kg)
    "activity_level": str,   # 活動量 (sedentary/light/moderate/active/very_active)
    "goal": str              # 目標 (lose_weight/maintain/gain_muscle)
}
```

## 錯誤處理

所有 API 端點都包含完整的錯誤處理:

- `503 Service Unavailable`: Gemini API 未配置
- `500 Internal Server Error`: AI 服務呼叫失敗

## 開發注意事項

1. **API Key 安全**: 絕對不要將 API Key 提交到 Git
2. **速率限制**: Gemini API 有免費額度限制,注意使用量
3. **回應解析**: AI 回應需要解析,已實作基本的文字解析邏輯
4. **錯誤重試**: 建議在生產環境加入重試機制

## 未來擴充方向

- [ ] 加入圖像辨識功能(Google Vision API)
- [ ] 整合食物營養資料庫
- [ ] 支援多語言
- [ ] 快取常見問題的回答
- [ ] 加入使用者回饋學習機制

## 授權

本專題為教育用途,請遵守 Google Gemini API 使用條款。
