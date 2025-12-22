"""
餐廳資料結構定義
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MenuItem:
    """食物項目"""
    name: str                    # 名稱
    price: float                 # 價格
    rating: float                # 評分 (0-10)
    calories: Optional[int] = None      # 卡路里
    protein: Optional[float] = None     # 蛋白質(g)
    carbs: Optional[float] = None       # 碳水化合物(g)
    fat: Optional[float] = None         # 脂肪(g)

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "rating": self.rating,
            "calories": self.calories,
            "protein": self.protein,
            "carbs": self.carbs,
            "fat": self.fat
        }


@dataclass
class Restaurant:
    """餐廳資料"""
    restaurant_id: str           # 店家ID
    name: str                    # 名稱
    latitude: float              # 緯度
    longitude: float             # 經度
    address: str                 # 地址
    avg_rating: float            # 平均評分 (0-10)
    nutrition_score: float       # 營養評分 (0-10)
    category: str                # 類別 (義式、咖啡廳、海鮮等)
    price_level: int             # 價格等級 (1-3: $, $$, $$$)
    distance_km: float           # 距離(公里)
    menu: List[MenuItem]         # 菜單
    tags: List[str]              # 標籤
    image_url: Optional[str] = None     # 圖片

    def to_dict(self):
        return {
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "avg_rating": self.avg_rating,
            "nutrition_score": self.nutrition_score,
            "category": self.category,
            "price_level": self.price_level,
            "distance_km": self.distance_km,
            "menu": [item.to_dict() for item in self.menu],
            "tags": self.tags,
            "image_url": self.image_url
        }


# 示範資料
SAMPLE_RESTAURANTS = [
    Restaurant(
        restaurant_id="green_leaf_001",
        name="綠葉輕食 Green Leaf",
        latitude=25.0330,
        longitude=121.5654,
        address="台北市大安區信義路四段100號",
        avg_rating=8.5,
        nutrition_score=9.2,
        category="義式",
        price_level=2,
        distance_km=1.2,
        menu=[
            MenuItem("凱薩沙拉", 280, 8.8, 350, 15, 25, 20),
            MenuItem("烤雞胸義大利麵", 320, 8.5, 520, 35, 55, 15),
            MenuItem("藜麥蔬菜碗", 260, 9.0, 380, 18, 45, 12),
        ],
        tags=["蔬菜多樣", "適合聚餐"],
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCMGfHSh9kLJZfHpcC_EaLfW3BMWFBlhC1COxyvuEui9pelQ9lYTrCEeYJXCZxq2fqOakYVgIJNTCMsM1WooH8ppbfN3XZj9MOH-b3rTOm6quCksYwBD8M-awj32LzRAssF17Y5rt2wq_q6l8E7qR6pWERPSvJ2dDeCAxgpKSn8DH1-CBYboHcXkHnox1IFS--zO0dQ4bpmrGUfm53RtXqRiqf_rnDZ-pExLSiiWKaDLF7CFqM5DEW_1V4zSnTSsPWQSQw4nEDj6wOr"
    ),
    Restaurant(
        restaurant_id="daily_grind_002",
        name="每日研磨 Daily Grind",
        latitude=25.0420,
        longitude=121.5700,
        address="台北市大安區敦化南路一段50號",
        avg_rating=9.2,
        nutrition_score=7.5,
        category="咖啡廳",
        price_level=1,
        distance_km=0.8,
        menu=[
            MenuItem("美式咖啡", 120, 9.0, 10, 0, 2, 0),
            MenuItem("香蕉核桃燕麥", 180, 8.8, 420, 12, 65, 15),
            MenuItem("雞胸酪梨吐司", 240, 9.3, 480, 30, 40, 18),
        ],
        tags=["咖啡/讀書", "高蛋白"],
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuAoew7BTI3NvvbwKWmES083CcZNgy5Mh5OgyGcp9ZcB6e48dJ6fa6UUoX-trC7uO8JZkGNikYWVPjLFEKolDuiIyu0bZaKQnD271MgF0XsOgJvkdE-gG7dLHdBHTyIOXrTIULidoUsRyp9586eBrGuzzSU8x-C1l2PWzUr_WwSEA6TbvTnTBxo_ekbboXPSkJmVCAahvwGXJLq-AIWrQko2sPk7obMPrBWo-zScZL89qYaZ-6L6M6eWLKE1h7ATLS_KTIr8MehdIQ7J"
    ),
    Restaurant(
        restaurant_id="oceans_bounty_003",
        name="海洋之炊 Ocean's Bounty",
        latitude=25.0280,
        longitude=121.5500,
        address="台北市大安區復興南路二段200號",
        avg_rating=8.9,
        nutrition_score=8.0,
        category="海鮮",
        price_level=3,
        distance_km=2.5,
        menu=[
            MenuItem("烤鮭魚排", 480, 9.2, 380, 42, 5, 20),
            MenuItem("海鮮總匯湯", 420, 8.7, 280, 35, 15, 8),
            MenuItem("清蒸鱸魚", 550, 9.0, 320, 45, 3, 12),
        ],
        tags=["食材多樣"],
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCVLbRMPcZ8omhha-oE4b3BdGMPABLjjzCc7YrspWCcVfmqflcIFQKuTRxCxylX6VZgN69vsJDNabSZSsub7mGmJjZIaQeWjnLG8YyCZigu2-odITJDWf2lehPCNJYueLIQhfasYddnDWEdW-iTSRM2avaxKW2xdBey8f4lwsIaq-GHJeEPNzXXjarJEosQMe8hTEeC5ZE9uZLrCM4kAGw1QdjaUfEZxuVw_NWWIfsFbdmfnTWKeoh6O9koYUSTqXFX94Cen_2GxQV5"
    ),
]
