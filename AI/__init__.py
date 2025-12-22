"""AI 模組 - Gemini API 整合 V2 (支援對話記憶)"""

from .gemini_service import (
    GeminiServiceV2,
    AIRecommenderV2,
    MealData,
    UserProfile,
    NutritionAnalysis,
    MealRecommendation,
    RestaurantRecommendation
)

# 為了向後兼容,提供別名
GeminiService = GeminiServiceV2
AIRecommender = AIRecommenderV2

__all__ = [
    "GeminiServiceV2",
    "AIRecommenderV2",
    "GeminiService",  # 別名
    "AIRecommender",  # 別名
    "MealData",
    "UserProfile",
    "NutritionAnalysis",
    "MealRecommendation",
    "RestaurantRecommendation"
]
