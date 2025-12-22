"""
Google Places API 整合
抓取真實餐廳資料
"""

import requests
import json

GOOGLE_MAPS_API_KEY = "AIzaSyDTFcNhyatB-rVRHHX8qjY5tggMZc1Reeg"
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# 高雄科技大學建工校區座標
NKUST_LOCATION = {
    'lat': 22.6273,
    'lng': 120.3014
}

def search_nearby_restaurants(location=None, radius=1500, keyword=None, type_filter=None):
    """
    搜尋附近餐廳

    Args:
        location: {'lat': float, 'lng': float}
        radius: 搜尋半徑(公尺)，預設1500m
        keyword: 關鍵字
        type_filter: 類型篩選 (健康餐、平價、咖啡廳等)
    """
    if location is None:
        location = NKUST_LOCATION

    params = {
        'location': f"{location['lat']},{location['lng']}",
        'radius': radius,
        'type': 'restaurant',
        'key': GOOGLE_MAPS_API_KEY,
        'language': 'zh-TW'
    }

    # 根據類型篩選加入關鍵字
    if type_filter:
        keyword_map = {
            '健康餐': '健康 輕食 沙拉',
            '平價': '小吃 平價 便當',
            '適合聚餐': '餐廳 聚餐 火鍋',
            '咖啡廳': '咖啡 cafe'
        }
        params['keyword'] = keyword_map.get(type_filter, type_filter)
    elif keyword:
        params['keyword'] = keyword

    try:
        response = requests.get(PLACES_API_URL, params=params)
        data = response.json()

        if data['status'] == 'OK':
            restaurants = []
            for place in data['results'][:20]:  # 增加到20家
                restaurant = parse_place_to_restaurant(place, location)
                restaurants.append(restaurant)

            return {
                'success': True,
                'data': restaurants,
                'count': len(restaurants)
            }
        else:
            return {
                'success': False,
                'error': f"Google Places API 錯誤: {data['status']}"
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def parse_place_to_restaurant(place, center_location):
    """將 Google Place 轉換成餐廳格式"""

    # 計算距離
    distance = calculate_distance(
        center_location['lat'], center_location['lng'],
        place['geometry']['location']['lat'],
        place['geometry']['location']['lng']
    )

    # 價格等級
    price_level = place.get('price_level', 2)

    # 評分 (Google 是 0-5，直接使用)
    avg_rating = round(place.get('rating', 4.0), 1)

    # 營養評分 (根據類別估算)
    nutrition_score = estimate_nutrition_score(place)

    # 標籤
    tags = generate_tags(place)

    # 圖片
    image_url = None
    if 'photos' in place and len(place['photos']) > 0:
        photo_reference = place['photos'][0]['photo_reference']
        image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_MAPS_API_KEY}"

    return {
        'restaurant_id': place['place_id'],
        'name': place['name'],
        'latitude': place['geometry']['location']['lat'],
        'longitude': place['geometry']['location']['lng'],
        'address': place.get('vicinity', '地址未提供'),
        'avg_rating': avg_rating,
        'nutrition_score': nutrition_score,
        'category': parse_category(place),
        'price_level': price_level,
        'distance_km': round(distance, 1),
        'tags': tags,
        'image_url': image_url,
        'is_open': place.get('opening_hours', {}).get('open_now', None)
    }


def calculate_distance(lat1, lng1, lat2, lng2):
    """計算兩點距離(公里)"""
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # 地球半徑(公里)

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lng2 - lng1)

    a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


def estimate_nutrition_score(place):
    """估算營養評分"""
    types = place.get('types', [])
    name = place['name'].lower()

    # 健康關鍵字
    healthy_keywords = ['沙拉', '輕食', '健康', '蔬食', '素食', '有機']
    unhealthy_keywords = ['炸', '燒烤', '速食', '鹽酥雞']

    score = 6.0  # 基礎分

    # 根據類型
    if 'cafe' in types:
        score += 0.5
    if 'meal_takeaway' in types:
        score -= 0.5

    # 根據名稱
    for keyword in healthy_keywords:
        if keyword in name:
            score += 1.5
            break

    for keyword in unhealthy_keywords:
        if keyword in name:
            score -= 2.0
            break

    return round(min(max(score, 3.0), 10.0), 1)


def parse_category(place):
    """解析類別"""
    types = place.get('types', [])
    name = place['name'].lower()

    # 類別對應
    if 'cafe' in types or '咖啡' in name:
        return '咖啡廳'
    elif 'meal_takeaway' in types or '便當' in name:
        return '便當'
    elif 'bar' in types:
        return '酒吧'
    elif any(t in name for t in ['日式', '日本', '壽司', '拉麵']):
        return '日式'
    elif any(t in name for t in ['義式', '義大利', '披薩']):
        return '義式'
    elif any(t in name for t in ['火鍋', '鍋物']):
        return '火鍋'
    elif any(t in name for t in ['早餐', '早午餐']):
        return '早午餐'
    else:
        return '餐廳'


def generate_tags(place):
    """生成標籤 - 確保至少有1個標籤"""
    tags = []
    types = place.get('types', [])
    name = place['name'].lower()
    price_level = place.get('price_level', 2)
    rating = place.get('rating', 0)

    # 價格標籤
    if price_level <= 1:
        tags.append('平價')
    elif price_level >= 3:
        tags.append('高檔')
    else:
        tags.append('中等價位')

    # 健康標籤
    healthy_keywords = ['沙拉', '輕食', '健康', '蔬食', '素食', '有機']
    if any(k in name for k in healthy_keywords):
        tags.append('健康餐')
    
    # 評價標籤
    if rating >= 4.5:
        tags.append('高評價 ⭐⭐⭐')
    elif rating >= 4.0:
        tags.append('好評')

    # 咖啡廳標籤
    if 'cafe' in types or '咖啡' in name:
        tags.append('咖啡/讀書')
    
    # 火鍋標籤
    if '火鍋' in name or 'hot pot' in name.lower():
        tags.append('火鍋')

    # 聚餐標籤
    if any(k in name for k in ['火鍋', '燒肉', '海鮮', '聚餐']):
        tags.append('適合聚餐')

    # 營業中標籤
    if place.get('opening_hours', {}).get('open_now', False):
        tags.append('營業中')

    # 如果標籤為空，根據類別添加預設標籤
    if not tags:
        if 'cafe' in types:
            tags.append('咖啡')
        elif 'restaurant' in types:
            tags.append('推薦')
        else:
            tags.append('新發現')

    return tags[:4]  # 最多4個標籤


# 測試
if __name__ == '__main__':
    print("搜尋高雄科大建工校區附近餐廳...")
    result = search_nearby_restaurants()

    if result['success']:
        print(f"\n找到 {result['count']} 家餐廳:\n")
        for r in result['data']:
            print(f"📍 {r['name']}")
            print(f"   類別: {r['category']} | 評分: {r['avg_rating']}/10")
            print(f"   距離: {r['distance_km']} 公里 | 價格: {'$' * r['price_level']}")
            print(f"   標籤: {', '.join(r['tags'])}")
            print()
    else:
        print(f"錯誤: {result['error']}")
