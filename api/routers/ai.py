"""
AI 相關 API 路由
整合 Gemini API 提供智慧飲食分析與推薦
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from AI.gemini_service import GeminiService, AIRecommender, MealData, UserProfile

router = APIRouter()

# 初始化 Gemini 服務
try:
    gemini_service = GeminiService()
    ai_recommender = AIRecommender(gemini_service)
except ValueError as e:
    print(f"警告: Gemini API 未正確配置 - {e}")
    gemini_service = None
    ai_recommender = None


# === Request/Response 模型 ===

class AnalyzeRequest(BaseModel):
    """營養分析請求"""
    meals: List[MealData]


class RecommendRequest(BaseModel):
    """餐點推薦請求"""
    user_profile: UserProfile
    preferences: Optional[str] = None


class QuestionRequest(BaseModel):
    """營養問題請求"""
    question: str


# === API 端點 ===

@router.post("/analyze")
async def analyze_nutrition(request: AnalyzeRequest):
    """
    分析飲食營養

    Args:
        request: 包含飲食紀錄的分析請求

    Returns:
        營養分析結果,包含總營養素、評估和建議
    """
    if not ai_recommender:
        raise HTTPException(
            status_code=503,
            detail="AI 服務未啟用,請檢查 GEMINI_API_KEY 環境變數"
        )

    try:
        analysis = ai_recommender.analyze_nutrition(request.meals)
        return {
            "success": True,
            "data": {
                "total_calories": analysis.total_calories,
                "total_protein": analysis.total_protein,
                "total_carbs": analysis.total_carbs,
                "total_fat": analysis.total_fat,
                "analysis": analysis.analysis,
                "suggestions": analysis.suggestions
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗: {str(e)}")


@router.post("/recommend")
async def get_meal_recommendation(request: RecommendRequest):
    """
    獲取個人化餐點推薦

    Args:
        request: 包含使用者檔案和偏好的推薦請求

    Returns:
        餐點推薦結果,包含推薦餐點、理由和每日熱量目標
    """
    if not ai_recommender:
        raise HTTPException(
            status_code=503,
            detail="AI 服務未啟用,請檢查 GEMINI_API_KEY 環境變數"
        )

    try:
        recommendation = ai_recommender.get_meal_recommendations(
            request.user_profile,
            request.preferences
        )
        return {
            "success": True,
            "data": {
                "recommended_meals": recommendation.recommended_meals,
                "reasoning": recommendation.reasoning,
                "daily_calorie_target": recommendation.daily_calorie_target
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推薦失敗: {str(e)}")


@router.post("/question")
async def ask_nutrition_question(request: QuestionRequest):
    """
    詢問營養相關問題

    Args:
        request: 包含使用者問題的請求

    Returns:
        AI 營養師的回答
    """
    if not ai_recommender:
        raise HTTPException(
            status_code=503,
            detail="AI 服務未啟用,請檢查 GEMINI_API_KEY 環境變數"
        )

    try:
        answer = ai_recommender.answer_nutrition_question(request.question)
        return {
            "success": True,
            "data": {
                "question": request.question,
                "answer": answer
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"回答失敗: {str(e)}")


@router.get("/health")
async def check_ai_health():
    """
    檢查 AI 服務健康狀態

    Returns:
        服務狀態資訊
    """
    if not gemini_service:
        return {
            "status": "unavailable",
            "message": "Gemini API 未配置",
            "configured": False
        }

    return {
        "status": "healthy",
        "message": "AI 服務運作正常",
        "configured": True,
        "model": gemini_service.model
    }
