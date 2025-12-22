"""
Gemini API 測試腳本
用於驗證 AI 模組是否正常運作
"""

import os
from gemini_service import GeminiService, AIRecommender, MealData, UserProfile


def test_basic_connection():
    """測試基本連線"""
    print("=" * 50)
    print("測試 1: 檢查 Gemini API 連線")
    print("=" * 50)

    try:
        gemini = GeminiService()
        print("✓ Gemini 服務初始化成功")
        print(f"  使用模型: {gemini.model}")
        return gemini
    except ValueError as e:
        print(f"✗ 初始化失敗: {e}")
        print("\n請確認:")
        print("1. 已設置 GEMINI_API_KEY 環境變數")
        print("2. API Key 正確且有效")
        print("3. 取得 API Key: https://aistudio.google.com/app/apikey")
        return None


def test_simple_query(gemini: GeminiService):
    """測試簡單查詢"""
    print("\n" + "=" * 50)
    print("測試 2: 簡單 AI 查詢")
    print("=" * 50)

    try:
        response = gemini.generate_response(
            "用一句話說明什麼是健康飲食",
            "你是一位營養師,請用繁體中文簡潔回答。"
        )
        print("✓ AI 回應成功")
        print(f"  回應: {response[:100]}...")
        return True
    except Exception as e:
        print(f"✗ 查詢失敗: {e}")
        return False


def test_nutrition_analysis():
    """測試營養分析"""
    print("\n" + "=" * 50)
    print("測試 3: 營養分析功能")
    print("=" * 50)

    try:
        gemini = GeminiService()
        recommender = AIRecommender(gemini)

        # 建立測試飲食紀錄
        meals = [
            MealData(
                food_name="雞胸肉",
                calories=165,
                protein=31.0,
                carbs=0.0,
                fat=3.6
            ),
            MealData(
                food_name="糙米飯",
                calories=216,
                protein=5.0,
                carbs=45.0,
                fat=1.8
            ),
            MealData(
                food_name="花椰菜",
                calories=55,
                protein=3.7,
                carbs=11.0,
                fat=0.6
            )
        ]

        print("分析以下飲食:")
        for meal in meals:
            print(f"  - {meal.food_name}: {meal.calories}大卡")

        analysis = recommender.analyze_nutrition(meals)

        print("\n✓ 分析成功")
        print(f"  總熱量: {analysis.total_calories} 大卡")
        print(f"  總蛋白質: {analysis.total_protein}g")
        print(f"  總碳水: {analysis.total_carbs}g")
        print(f"  總脂肪: {analysis.total_fat}g")
        print(f"\n  AI 評估: {analysis.analysis[:100]}...")
        print(f"\n  建議數量: {len(analysis.suggestions)} 個")

        return True
    except Exception as e:
        print(f"✗ 分析失敗: {e}")
        return False


def test_meal_recommendation():
    """測試餐點推薦"""
    print("\n" + "=" * 50)
    print("測試 4: 餐點推薦功能")
    print("=" * 50)

    try:
        gemini = GeminiService()
        recommender = AIRecommender(gemini)

        # 建立測試使用者檔案
        user = UserProfile(
            age=25,
            gender="male",
            height=175,
            weight=70,
            activity_level="moderate",
            goal="maintain"
        )

        print("使用者資料:")
        print(f"  年齡: {user.age}歲")
        print(f"  性別: {user.gender}")
        print(f"  身高: {user.height}cm")
        print(f"  體重: {user.weight}kg")
        print(f"  活動量: {user.activity_level}")
        print(f"  目標: {user.goal}")

        recommendation = recommender.get_meal_recommendations(
            user,
            preferences="高蛋白"
        )

        print("\n✓ 推薦成功")
        print(f"  每日熱量目標: {recommendation.daily_calorie_target} 大卡")
        print(f"  推薦餐點數: {len(recommendation.recommended_meals)} 個")
        if recommendation.recommended_meals:
            print("\n  餐點推薦:")
            for meal in recommendation.recommended_meals:
                print(f"    {meal.get('type', '?')}: {meal.get('meal', '?')}")

        return True
    except Exception as e:
        print(f"✗ 推薦失敗: {e}")
        return False


def test_nutrition_question():
    """測試營養問答"""
    print("\n" + "=" * 50)
    print("測試 5: 營養問答功能")
    print("=" * 50)

    try:
        gemini = GeminiService()
        recommender = AIRecommender(gemini)

        question = "減重期間晚餐應該怎麼吃?"
        print(f"問題: {question}")

        answer = recommender.answer_nutrition_question(question)

        print("\n✓ 回答成功")
        print(f"  回答: {answer[:200]}...")

        return True
    except Exception as e:
        print(f"✗ 回答失敗: {e}")
        return False


def main():
    """主測試流程"""
    print("\n" + "=" * 50)
    print("Gemini AI 模組測試")
    print("=" * 50)

    # 檢查環境變數
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  警告: 未設置 GEMINI_API_KEY 環境變數")
        print("部分測試將會失敗\n")

    results = []

    # 測試 1: 基本連線
    gemini = test_basic_connection()
    results.append(("基本連線", gemini is not None))

    if gemini:
        # 測試 2: 簡單查詢
        results.append(("簡單查詢", test_simple_query(gemini)))

        # 測試 3: 營養分析
        results.append(("營養分析", test_nutrition_analysis()))

        # 測試 4: 餐點推薦
        results.append(("餐點推薦", test_meal_recommendation()))

        # 測試 5: 營養問答
        results.append(("營養問答", test_nutrition_question()))

    # 總結
    print("\n" + "=" * 50)
    print("測試總結")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"{status} - {name}")

    print(f"\n總計: {passed}/{total} 個測試通過")

    if passed == total:
        print("\n🎉 所有測試通過! AI 模組運作正常")
    else:
        print("\n⚠️  部分測試失敗,請檢查配置")


if __name__ == "__main__":
    main()
