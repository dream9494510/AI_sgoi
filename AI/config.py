"""
AI 模組配置檔案
"""

import os
from typing import Optional


class GeminiConfig:
    """Gemini API 配置類別"""

    # API 設定
    API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

    # 模型選擇
    # gemini-1.5-flash: 快速、經濟,適合大部分任務
    # gemini-1.5-pro: 更強大,適合複雜分析
    DEFAULT_MODEL: str = "gemini-1.5-flash"
    PRO_MODEL: str = "gemini-1.5-pro"

    # 生成參數
    DEFAULT_TEMPERATURE: float = 0.7  # 創意程度 (0-1)
    DEFAULT_MAX_TOKENS: int = 1000    # 最大回應長度

    # 系統提示詞
    NUTRITION_EXPERT_ROLE: str = """你是一位專業的營養師和健康顧問。
你擅長:
1. 分析飲食營養並提供改善建議
2. 根據個人狀況推薦合適的餐點
3. 回答各種營養健康相關問題

請使用繁體中文回應,並確保建議:
- 有科學依據
- 實用且可執行
- 考慮使用者的個人狀況
- 語氣專業但易懂
"""

    @classmethod
    def validate_config(cls) -> bool:
        """
        驗證配置是否完整

        Returns:
            配置是否有效
        """
        if not cls.API_KEY:
            return False
        return True

    @classmethod
    def get_api_key(cls) -> str:
        """
        獲取 API Key,若未設置則拋出錯誤

        Returns:
            API Key

        Raises:
            ValueError: 當 API Key 未設置時
        """
        if not cls.API_KEY:
            raise ValueError(
                "GEMINI_API_KEY 未設置。請設置環境變數或在 .env 檔案中配置。\n"
                "取得 API Key: https://aistudio.google.com/app/apikey"
            )
        return cls.API_KEY


# 營養計算常數
class NutritionConstants:
    """營養計算相關常數"""

    # Harris-Benedict 公式常數 (計算基礎代謝率 BMR)
    MALE_BMR_WEIGHT: float = 13.7
    MALE_BMR_HEIGHT: float = 5.0
    MALE_BMR_AGE: float = 6.8
    MALE_BMR_BASE: float = 66.0

    FEMALE_BMR_WEIGHT: float = 9.6
    FEMALE_BMR_HEIGHT: float = 1.8
    FEMALE_BMR_AGE: float = 4.7
    FEMALE_BMR_BASE: float = 655.0

    # 活動係數
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,      # 久坐,很少運動
        "light": 1.375,        # 輕度活動,每週運動 1-3 天
        "moderate": 1.55,      # 中度活動,每週運動 3-5 天
        "active": 1.725,       # 高度活動,每週運動 6-7 天
        "very_active": 1.9     # 非常活躍,每天高強度運動
    }

    # 目標調整 (每日熱量調整)
    GOAL_ADJUSTMENTS = {
        "lose_weight": -500,   # 減重:每日減少 500 大卡
        "maintain": 0,         # 維持:不調整
        "gain_muscle": 300     # 增肌:每日增加 300 大卡
    }

    # 營養素熱量係數
    PROTEIN_CALORIES_PER_GRAM: float = 4.0
    CARB_CALORIES_PER_GRAM: float = 4.0
    FAT_CALORIES_PER_GRAM: float = 9.0

    # 建議營養素比例 (熱量佔比)
    RECOMMENDED_PROTEIN_RATIO: tuple = (0.20, 0.30)  # 20-30%
    RECOMMENDED_CARB_RATIO: tuple = (0.45, 0.65)     # 45-65%
    RECOMMENDED_FAT_RATIO: tuple = (0.20, 0.35)      # 20-35%
