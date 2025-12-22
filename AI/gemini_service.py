"""
Gemini API 服務模組 V2 - 改進版
1. 支援對話上下文記憶
2. 針對飲食管理的專業提示詞
3. 更彈性的回答長度和風格
"""

import os
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel

# 使用 Google 官方 SDK (更穩定)
try:
    import google.generativeai as genai
    USE_GOOGLE_SDK = True
except ImportError:
    from openai import OpenAI
    USE_GOOGLE_SDK = False


class MealData(BaseModel):
    """飲食數據模型"""
    food_name: str
    calories: int
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    timestamp: Optional[str] = None


class UserProfile(BaseModel):
    """使用者健康檔案"""
    age: int
    gender: str
    height: float
    weight: float
    activity_level: str
    goal: str
    dietary_preferences: Optional[str] = None  # 新增:飲食偏好


class NutritionAnalysis(BaseModel):
    """營養分析結果"""
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    analysis: str
    suggestions: List[str]


class MealRecommendation(BaseModel):
    """餐點推薦結果"""
    recommended_meals: List[Dict[str, str]]
    reasoning: str
    daily_calorie_target: int


class RestaurantRecommendation(BaseModel):
    """餐廳推薦結果 (新增)"""
    restaurants: List[Dict[str, str]]
    reasoning: str
    health_tips: List[str]


class ConversationMessage(BaseModel):
    """對話訊息"""
    role: str  # 'user' or 'assistant'
    content: str


class GeminiServiceV2:
    """
    Gemini API 服務類別 V2 - 改進版
    支援對話上下文、更智慧的提示詞、更彈性的回答
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Gemini 服務

        Args:
            api_key: Google Gemini API Key (若不提供則從環境變數讀取)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("請設置 GEMINI_API_KEY 環境變數或提供 API Key")

        # 對話歷史記錄
        self.conversation_history: List[ConversationMessage] = []

        # 使用 Google 官方 SDK
        if USE_GOOGLE_SDK:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.use_google_sdk = True
        else:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            self.model_name = "gemini-1.5-flash"
            self.use_google_sdk = False

    def clear_conversation(self):
        """清除對話歷史"""
        self.conversation_history = []

    def get_conversation_context(self, max_messages: int = 10) -> str:
        """
        取得對話上下文

        Args:
            max_messages: 最多保留的對話輪數

        Returns:
            格式化的對話歷史
        """
        if not self.conversation_history:
            return ""

        # 只保留最近的對話
        recent_history = self.conversation_history[-max_messages:]

        context_lines = []
        for msg in recent_history:
            role = "使用者" if msg.role == "user" else "AI營養師"
            context_lines.append(f"{role}: {msg.content}")

        return "\n".join(context_lines)

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        use_context: bool = True,
        max_tokens: int = 800,  # 增加字數限制
        temperature: float = 0.8  # 增加創意性
    ) -> str:
        """
        生成 AI 回應 (支援上下文)

        Args:
            prompt: 使用者提示詞
            system_prompt: 系統提示詞
            use_context: 是否使用對話上下文
            max_tokens: 最大回應長度
            temperature: 創意程度 (0-1)

        Returns:
            AI 生成的回應文字
        """
        # 構建完整提示詞
        full_prompt = prompt

        # 簡化上下文格式
        if use_context and self.conversation_history:
            # 只取最近3輪對話避免太長
            recent = self.conversation_history[-6:]  # 3輪=6則訊息
            context_parts = []
            for msg in recent:
                role = "Q" if msg.role == "user" else "A"
                # 限制每則訊息長度
                content = msg.content[:200] if len(msg.content) > 200 else msg.content
                context_parts.append(f"{role}: {content}")

            if context_parts:
                context = "\n".join(context_parts)
                full_prompt = f"先前對話:\n{context}\n\n現在問題: {prompt}"

        # 使用 Google SDK
        if self.use_google_sdk:
            try:
                # 簡化系統提示詞
                if system_prompt:
                    # 合併但保持簡潔
                    full_prompt = f"{system_prompt[:300]}\n\n{full_prompt}"

                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature
                    )
                )

                # 處理被擋住的情況
                if not response.candidates:
                    raise Exception("回應被安全過濾器擋住")

                if not response.candidates[0].content.parts:
                    raise Exception(f"無法取得回應 (finish_reason: {response.candidates[0].finish_reason})")

                answer = response.text

                # 記錄對話
                self.conversation_history.append(
                    ConversationMessage(role="user", content=prompt)
                )
                self.conversation_history.append(
                    ConversationMessage(role="assistant", content=answer)
                )

                return answer

            except Exception as e:
                raise Exception(f"Gemini API 呼叫失敗: {str(e)}")

        # 使用 OpenAI 兼容介面 (備用)
        else:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": full_prompt})

            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                answer = response.choices[0].message.content

                # 記錄對話
                self.conversation_history.append(
                    ConversationMessage(role="user", content=prompt)
                )
                self.conversation_history.append(
                    ConversationMessage(role="assistant", content=answer)
                )

                return answer

            except Exception as e:
                raise Exception(f"Gemini API 呼叫失敗: {str(e)}")


class AIRecommenderV2:
    """
    AI 推薦系統 V2 - 改進版
    針對飲食管理優化
    """

    def __init__(self, gemini_service: GeminiServiceV2):
        """
        初始化 AI 推薦系統

        Args:
            gemini_service: Gemini 服務實例
        """
        self.gemini = gemini_service

        # 簡化提示詞避免被過濾
        self.nutrition_expert_prompt = "你是營養師,用繁體中文。"

    def analyze_nutrition(self, meals: List[MealData]) -> NutritionAnalysis:
        """
        self.nutrition_expert_prompt = "你是專業營養師,用繁體中文回答。"
        self.nutrition_expert_prompt = "你是專業營養師,用繁體中文回答。"
        self.nutrition_expert_prompt = "你是專業營養師,用繁體中文回答。"
            meals: 飲食紀錄列表

        Returns:
            營養分析結果
        """
        # 計算總營養素
        total_calories = sum(meal.calories for meal in meals)
        total_protein = sum(meal.protein or 0 for meal in meals)
        total_carbs = sum(meal.carbs or 0 for meal in meals)
        total_fat = sum(meal.fat or 0 for meal in meals)

        # 構建提示詞
        meal_list = "\n".join([
            f"- {meal.food_name}: {meal.calories} 大卡 "
            f"(蛋白質: {meal.protein}g, 碳水: {meal.carbs}g, 脂肪: {meal.fat}g)"
            for meal in meals
        ])

        prompt = f"""請分析以下飲食紀錄:

{meal_list}

總計:
- 熱量: {total_calories} 大卡
- 蛋白質: {total_protein}g
- 碳水化合物: {total_carbs}g
- 脂肪: {total_fat}g

請提供:
1. 整體營養評估 (3-4 句話,要具體)
2. 4-6 個實用的改善建議

回應格式:
評估: [你的評估]
建議:
- [建議1]
- [建議2]
- [建議3]
..."""

        response = self.gemini.generate_response(
            prompt,
            self.nutrition_expert_prompt,
            use_context=False,  # 營養分析不需要上下文
            max_tokens=1000
        )

        # 解析回應
        lines = response.strip().split("\n")
        analysis_text = ""
        suggestions = []

        in_suggestions = False
        for line in lines:
            line = line.strip()
            if line.startswith("評估:"):
                analysis_text = line.replace("評估:", "").strip()
            elif line.startswith("建議:"):
                in_suggestions = True
            elif in_suggestions and (line.startswith("-") or line.startswith("•")):
                suggestion = line.lstrip("-•").strip()
                if suggestion:
                    suggestions.append(suggestion)

        return NutritionAnalysis(
            total_calories=total_calories,
            total_protein=total_protein,
            total_carbs=total_carbs,
            total_fat=total_fat,
            analysis=analysis_text or response[:200],
            suggestions=suggestions or ["請保持均衡飲食", "多喝水", "適量運動"]
        )

    def recommend_restaurants(
        self,
        user_profile: UserProfile,
        meal_type: str = "午餐",
        cuisine_preference: Optional[str] = None
    ) -> RestaurantRecommendation:
        """
        推薦健康餐廳 (新功能)

        Args:
            user_profile: 使用者檔案
            meal_type: 餐點類型 (早餐/午餐/晚餐)
            cuisine_preference: 菜系偏好

        Returns:
            餐廳推薦結果
        """
        prompt = f"""請為以下使用者推薦適合的健康餐廳:

使用者資訊:
- 目標: {user_profile.goal}
- 飲食偏好: {user_profile.dietary_preferences or '無特殊限制'}
- 餐點類型: {meal_type}
{f"- 菜系偏好: {cuisine_preference}" if cuisine_preference else ""}

請推薦 3-5 家餐廳類型,並說明理由。

重要:
1. 優先推薦營養均衡、食材新鮮的餐廳
2. 考慮使用者的健康目標
3. 提供具體的餐廳類型或特色
4. 給出健康點餐建議

回應格式:
1. [餐廳類型] - [推薦理由和點餐建議]
2. [餐廳類型] - [推薦理由和點餐建議]
...

健康提醒:
- [提醒1]
- [提醒2]"""

        response = self.gemini.generate_response(
            prompt,
            self.nutrition_expert_prompt,
            use_context=True,  # 使用對話上下文
            max_tokens=1000
        )

        # 解析回應
        restaurants = []
        health_tips = []
        reasoning = ""

        lines = response.strip().split("\n")
        in_tips = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "健康提醒" in line or "注意事項" in line:
                in_tips = True
                continue

            if in_tips:
                if line.startswith("-") or line.startswith("•"):
                    tip = line.lstrip("-•").strip()
                    if tip:
                        health_tips.append(tip)
            else:
                # 解析餐廳推薦
                if line[0].isdigit() and "." in line[:3]:
                    parts = line.split("-", 1)
                    if len(parts) == 2:
                        restaurant_type = parts[0].strip()
                        description = parts[1].strip()
                        restaurants.append({
                            "type": restaurant_type,
                            "description": description
                        })

        reasoning = "根據您的健康目標和飲食偏好推薦"

        return RestaurantRecommendation(
            restaurants=restaurants,
            reasoning=reasoning,
            health_tips=health_tips or ["選擇少油少鹽的烹調方式", "注意食材新鮮度"]
        )

    def get_recipe(self, dish_name: str) -> str:
        """
        取得料理食譜 (新功能,會記住對話)

        Args:
            dish_name: 料理名稱

        Returns:
            詳細食譜
        """
        prompt = f"請提供 {dish_name} 的詳細料理步驟和食譜"

        response = self.gemini.generate_response(
            prompt,
            self.nutrition_expert_prompt,
            use_context=True,  # 重要:使用上下文,會記得之前推薦過什麼
            max_tokens=1200,  # 食譜需要更多字數
            temperature=0.7
        )

        return response

    def answer_question(self, question: str) -> str:
        """
        回答營養問題 (支援對話上下文)

        Args:
            question: 使用者問題

        Returns:
            AI 回答
        """
        response = self.gemini.generate_response(
            question,
            system_prompt=None,  # 不使用,避免被過濾
            use_context=True,
            max_tokens=800,
            temperature=0.8
        )

        return response


# 使用範例
if __name__ == "__main__":
    # 設置 API Key
    API_KEY = "AIzaSyAQ6mbQm6fttYW2se__-jTsOBBDrLLAPdU"

    try:
        # 初始化服務
        gemini = GeminiServiceV2(api_key=API_KEY)
        recommender = AIRecommenderV2(gemini)

        print("=" * 60)
        print("測試 1: 對話上下文記憶")
        print("=" * 60)

        # 第一個問題
        answer1 = recommender.answer_question("午餐推薦什麼菜單?")
        print(f"\n問題 1: 午餐推薦什麼菜單?")
        print(f"AI: {answer1}")

        # 第二個問題(不需要重複說明)
        answer2 = recommender.get_recipe("料理方式和食譜")
        print(f"\n問題 2: 料理方式和食譜")
        print(f"AI: {answer2}")

        print("\n" + "=" * 60)
        print("測試 2: 健康餐廳推薦")
        print("=" * 60)

        user = UserProfile(
            age=25,
            gender="female",
            height=165,
            weight=55,
            activity_level="moderate",
            goal="lose_weight",
            dietary_preferences="偏好清淡、少油"
        )

        restaurants = recommender.recommend_restaurants(user, "午餐", "中式")
        print(f"\n推薦餐廳:")
        for i, r in enumerate(restaurants.restaurants, 1):
            print(f"{i}. {r['type']}")
            print(f"   {r['description']}")

        print(f"\n健康提醒:")
        for tip in restaurants.health_tips:
            print(f"  - {tip}")

    except Exception as e:
        print(f"錯誤: {e}")
