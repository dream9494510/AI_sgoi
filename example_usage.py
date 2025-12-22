"""
完整使用範例
展示如何在飲食控管專題中使用 AI 模組
"""

import os
from AI.gemini_service import (
    GeminiService,
    AIRecommender,
    MealData,
    UserProfile
)


def example_1_daily_analysis():
    """範例 1: 分析一天的飲食"""
    print("=" * 60)
    print("範例 1: 分析今日飲食紀錄")
    print("=" * 60)

    # 初始化 AI 服務
    gemini = GeminiService()
    recommender = AIRecommender(gemini)

    # 模擬使用者的一天飲食紀錄
    daily_meals = [
        # 早餐
        MealData(
            food_name="蛋餅",
            calories=280,
            protein=12.0,
            carbs=35.0,
            fat=10.0,
            timestamp="2024-11-24 08:00"
        ),
        MealData(
            food_name="豆漿",
            calories=120,
            protein=7.0,
            carbs=12.0,
            fat=4.0,
            timestamp="2024-11-24 08:00"
        ),
        # 午餐
        MealData(
            food_name="雞腿便當",
            calories=750,
            protein=35.0,
            carbs=90.0,
            fat=25.0,
            timestamp="2024-11-24 12:30"
        ),
        # 晚餐
        MealData(
            food_name="鮭魚沙拉",
            calories=350,
            protein=28.0,
            carbs=20.0,
            fat=18.0,
            timestamp="2024-11-24 18:30"
        )
    ]

    print("\n今日飲食:")
    for meal in daily_meals:
        print(f"  {meal.timestamp} - {meal.food_name}: {meal.calories}大卡")

    # AI 分析
    print("\n正在進行 AI 營養分析...")
    analysis = recommender.analyze_nutrition(daily_meals)

    # 顯示結果
    print(f"\n📊 營養總計:")
    print(f"  熱量: {analysis.total_calories} 大卡")
    print(f"  蛋白質: {analysis.total_protein}g")
    print(f"  碳水化合物: {analysis.total_carbs}g")
    print(f"  脂肪: {analysis.total_fat}g")

    print(f"\n💡 AI 評估:")
    print(f"  {analysis.analysis}")

    print(f"\n📝 改善建議:")
    for i, suggestion in enumerate(analysis.suggestions, 1):
        print(f"  {i}. {suggestion}")


def example_2_personalized_recommendation():
    """範例 2: 個人化餐點推薦"""
    print("\n\n" + "=" * 60)
    print("範例 2: 獲取個人化餐點推薦")
    print("=" * 60)

    # 初始化 AI 服務
    gemini = GeminiService()
    recommender = AIRecommender(gemini)

    # 使用者檔案
    user_profile = UserProfile(
        age=28,
        gender="female",
        height=165,
        weight=58,
        activity_level="moderate",
        goal="lose_weight"
    )

    print(f"\n👤 使用者資料:")
    print(f"  年齡: {user_profile.age}歲")
    print(f"  性別: {user_profile.gender}")
    print(f"  身高: {user_profile.height}cm")
    print(f"  體重: {user_profile.weight}kg")
    print(f"  活動量: {user_profile.activity_level}")
    print(f"  目標: {user_profile.goal}")

    # 獲取推薦
    print("\n正在生成個人化餐點推薦...")
    recommendation = recommender.get_meal_recommendations(
        user_profile,
        preferences="偏好清淡,少油少鹽"
    )

    # 顯示結果
    print(f"\n🎯 每日熱量目標: {recommendation.daily_calorie_target} 大卡")

    print(f"\n🍽️ 今日推薦餐點:")
    for meal in recommendation.recommended_meals:
        print(f"  {meal.get('type', '?')}: {meal.get('meal', '?')}")

    print(f"\n💭 推薦理由:")
    print(f"  {recommendation.reasoning}")


def example_3_nutrition_qa():
    """範例 3: 營養問答"""
    print("\n\n" + "=" * 60)
    print("範例 3: 營養問答諮詢")
    print("=" * 60)

    # 初始化 AI 服務
    gemini = GeminiService()
    recommender = AIRecommender(gemini)

    # 常見問題列表
    questions = [
        "減重期間可以吃水果嗎?",
        "運動後應該吃什麼?",
        "如何增加蛋白質攝取?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n❓ 問題 {i}: {question}")
        print(f"正在諮詢 AI 營養師...")

        answer = recommender.answer_nutrition_question(question)

        print(f"\n💬 AI 營養師回答:")
        # 分段顯示
        paragraphs = answer.split('\n\n')
        for para in paragraphs:
            if para.strip():
                print(f"  {para.strip()}")

        if i < len(questions):
            print("\n" + "-" * 60)


def example_4_complete_workflow():
    """範例 4: 完整工作流程"""
    print("\n\n" + "=" * 60)
    print("範例 4: 完整使用流程")
    print("=" * 60)

    # 初始化
    gemini = GeminiService()
    recommender = AIRecommender(gemini)

    # 步驟 1: 使用者輸入今日飲食
    print("\n步驟 1: 記錄今日飲食")
    breakfast = MealData(
        food_name="燕麥粥",
        calories=150,
        protein=5.0,
        carbs=27.0,
        fat=2.5
    )
    print(f"  ✓ 已記錄: {breakfast.food_name}")

    # 步驟 2: AI 即時分析
    print("\n步驟 2: AI 即時分析")
    analysis = recommender.analyze_nutrition([breakfast])
    print(f"  當前熱量: {analysis.total_calories} 大卡")

    # 步驟 3: 獲取下一餐建議
    print("\n步驟 3: 獲取午餐建議")
    user = UserProfile(
        age=30,
        gender="male",
        height=175,
        weight=75,
        activity_level="active",
        goal="gain_muscle"
    )

    # 使用上下文推薦 (已知早餐攝取)
    prompt = f"""
    使用者今天早餐吃了 {breakfast.food_name} ({breakfast.calories}大卡)。
    請推薦一份適合增肌目標的午餐,要高蛋白。
    """

    lunch_suggestion = gemini.generate_response(
        prompt,
        "你是營養師,請簡短推薦一份午餐並說明理由。使用繁體中文。"
    )

    print(f"  AI 建議:")
    print(f"  {lunch_suggestion[:150]}...")

    # 步驟 4: 使用者詢問問題
    print("\n步驟 4: 詢問營養問題")
    question = "增肌期間需要補充什麼營養品?"
    answer = recommender.answer_nutrition_question(question)
    print(f"  Q: {question}")
    print(f"  A: {answer[:100]}...")

    print("\n✅ 完整流程示範完成")


def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("飲食控管專題 - AI 模組完整使用範例")
    print("=" * 60)

    # 檢查 API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("\n❌ 錯誤: 未設置 GEMINI_API_KEY")
        print("請先設置環境變數:")
        print("  Windows: set GEMINI_API_KEY=你的KEY")
        print("  Linux/Mac: export GEMINI_API_KEY=你的KEY")
        print("\n取得 API Key: https://aistudio.google.com/app/apikey")
        return

    try:
        # 執行各個範例
        example_1_daily_analysis()
        example_2_personalized_recommendation()
        example_3_nutrition_qa()
        example_4_complete_workflow()

        print("\n\n" + "=" * 60)
        print("所有範例執行完成!")
        print("=" * 60)
        print("\n💡 提示:")
        print("  - 查看 AI/README.md 了解更多功能")
        print("  - 查看 api/routers/ai.py 了解 API 整合")
        print("  - 執行 python AI/test_gemini.py 進行完整測試")

    except Exception as e:
        print(f"\n❌ 執行錯誤: {e}")
        print("請檢查:")
        print("  1. GEMINI_API_KEY 是否正確")
        print("  2. 網路連線是否正常")
        print("  3. 是否已安裝所有依賴套件")


if __name__ == "__main__":
    main()
