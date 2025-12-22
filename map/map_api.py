"""
地圖 API 後端
整合 Google Maps API
優化回應速度和操作流暢度
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from restaurant_data import SAMPLE_RESTAURANTS, Restaurant, MenuItem
from google_places import search_nearby_restaurants, NKUST_LOCATION
import json
from functools import lru_cache
import threading
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Google Maps API Key (免費版)
GOOGLE_MAPS_API_KEY = "AIzaSyDTFcNhyatB-rVRHHX8qjY5tggMZc1Reeg"

# 快取真實餐廳資料及其過期時間
cached_restaurants = None
cache_timestamp = None
CACHE_EXPIRE_SECONDS = 600  # 10分鐘快取

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    """取得所有餐廳 - 使用 Google Places API 真實資料 (優化版)"""
    global cached_restaurants, cache_timestamp

    try:
        category = request.args.get('category', '全部')
        skip_cache = request.args.get('refresh', 'false').lower() == 'true'

        print(f"\n[API] 要求類別: {category}")

        # 檢查快取是否過期
        should_refresh = skip_cache or (
            cached_restaurants is None or 
            cache_timestamp is None or
            datetime.now() - cache_timestamp > timedelta(seconds=CACHE_EXPIRE_SECONDS)
        )

        # 使用快取或重新搜尋
        if not should_refresh and cached_restaurants:
            restaurants = cached_restaurants
            print(f"[API] 使用快取資料，共 {len(restaurants)} 間")
        else:
            # 先從 Google Places 搜尋全部餐廳 - 擴大半徑到3000米
            result = search_nearby_restaurants(
                location=NKUST_LOCATION,
                radius=3000,
                type_filter=None  # 先不用 type_filter，直接搜尋所有餐廳
            )

            if not result['success']:
                if cached_restaurants:
                    restaurants = cached_restaurants
                    print(f"[API] Google Places 失敗，使用舊快取: {len(restaurants)} 間")
                else:
                    return jsonify(result), 500
            else:
                restaurants = result['data']
                cached_restaurants = restaurants
                cache_timestamp = datetime.now()
                print(f"[API] 從 Google Places 取得 {len(restaurants)} 間餐廳")

        # 根據類別進行篩選
        if category and category != '全部':
            original_count = len(restaurants)
            filtered_restaurants = []
            
            category_keywords = {
                '健康餐': ['健康', '輕食', '沙拉', '蔬菜', '素食', '健身', '無糖', '低卡', '雞肉', '健身餐', '超商', 'smoothie', 'bowl'],
                '平價': ['平價', '便當', '小吃', '蚵仔煎', '大腸麵線', '滷肉飯', '麵', '飯', '湯', '拉麵', '牛肉麵', '傳統'],
                '適合聚餐': ['火鍋', '燒肉', '海鮮', '餐廳', '聚餐', '聚', '日式', '義式', '烤', '吃到飽', '和食', '中式', 'bbq'],
                '咖啡廳': ['咖啡', 'cafe', '咖啡館', '手沖', '拿鐵', '卡布奇諾', 'coffee', '咖啡館', '甜點', '烘焙', '冷萃']
            }
            
            keywords = category_keywords.get(category, [])
            
            for restaurant in restaurants:
                name_lower = restaurant.get('name', '').lower()
                category_lower = restaurant.get('category', '').lower()
                tags = [tag.lower() for tag in restaurant.get('tags', [])]
                
                # 檢查名稱或分類是否包含相關關鍵字
                match = any(keyword.lower() in name_lower or keyword.lower() in category_lower for keyword in keywords)
                match = match or any(keyword.lower() in tag for tag in tags for keyword in keywords)
                
                if match:
                    filtered_restaurants.append(restaurant)
            
            # 如果篩選結果太少（少於3家），降低篩選要求，只按分類篩選
            if len(filtered_restaurants) < 3 and category == '咖啡廳':
                filtered_restaurants = [r for r in restaurants if r.get('category', '') == '咖啡廳']
            
            restaurants = filtered_restaurants
            print(f"[API] 篩選 '{category}': {len(restaurants)}/{original_count} 間")

        # 按距離和評分排序
        restaurants = sorted(restaurants, key=lambda r: (r.get('distance_km', float('inf')), -r.get('avg_rating', 0)))

        return jsonify({
            'success': True,
            'data': restaurants,
            'count': len(restaurants),
            'source': 'google_places',
            'cached': not should_refresh,
            'category': category,
            'message': f"成功取得 {len(restaurants)} 間{category if category != '全部' else ''}餐廳"
        })

    except Exception as e:
        print(f"[API ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/restaurant/<restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    """取得單一餐廳詳細資料"""
    try:
        restaurant = next((r for r in SAMPLE_RESTAURANTS if r.restaurant_id == restaurant_id), None)

        if not restaurant:
            return jsonify({
                'success': False,
                'error': '找不到餐廳'
            }), 404

        return jsonify({
            'success': True,
            'data': restaurant.to_dict()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search', methods=['GET'])
def search_restaurants():
    """搜尋餐廳 - 使用 Google Places API 搜尋完整餐廳資料"""
    try:
        query = request.args.get('q', '').strip()

        if not query:
            # 沒有關鍵字就回傳全部
            return get_restaurants()

        # 直接用關鍵字搜尋 Google Places
        print(f"\n[API] 搜尋關鍵字: {query}")
        result = search_nearby_restaurants(
            location=NKUST_LOCATION,
            radius=3000,
            keyword=query
        )

        if not result['success']:
            print(f"[API ERROR] 搜尋失敗: {result['error']}")
            return jsonify(result), 500

        # 排序結果 - 優先顯示距離近的，其次是評分高的
        data = sorted(result['data'], 
                     key=lambda r: (r.get('distance_km', float('inf')), -r.get('avg_rating', 0)))

        print(f"[API] 搜尋成功，找到 {len(data)} 間餐廳")
        
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data),
            'source': 'google_places',
            'query': query,
            'message': f"搜尋到 {len(data)} 間餐廳"
        })

    except Exception as e:
        print(f"[API ERROR] 搜尋異常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/menu/<restaurant_id>', methods=['GET'])
def get_menu(restaurant_id):
    """取得餐廳菜單"""
    try:
        restaurant = next((r for r in SAMPLE_RESTAURANTS if r.restaurant_id == restaurant_id), None)

        if not restaurant:
            return jsonify({
                'success': False,
                'error': '找不到餐廳'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'restaurant_name': restaurant.name,
                'menu': [item.to_dict() for item in restaurant.menu]
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/maps/key', methods=['GET'])
def get_maps_key():
    """取得 Google Maps API Key"""
    return jsonify({
        'success': True,
        'api_key': GOOGLE_MAPS_API_KEY
    })


@app.route('/api/health', methods=['GET'])
def health():
    """健康檢查"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'cache_status': 'cached' if cached_restaurants else 'empty'
    })


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """清除快取 - 用於強制重新載入"""
    global cached_restaurants, cache_timestamp
    cached_restaurants = None
    cache_timestamp = None
    return jsonify({
        'success': True,
        'message': '快取已清除'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Map API Server (Optimized Version)")
    print("=" * 60)
    print("\nServer Configuration:")
    print("   URL: http://localhost:5001")
    print("   CORS: Enabled")
    print("   Cache Strategy: Auto-update every 10 minutes")
    print("\nAvailable API Endpoints:")
    print("   GET  /api/restaurants        - Get all restaurants")
    print("   GET  /api/restaurant/<id>    - Get restaurant details")
    print("   GET  /api/search?q=keyword   - Search restaurants")
    print("   GET  /api/menu/<id>          - Get menu")
    print("   GET  /api/maps/key           - Get Google Maps Key")
    print("   GET  /api/health             - Health check")
    print("   POST /api/cache/clear        - Clear cache")
    print("\nTips:")
    print("   - First load may take 2-3 seconds")
    print("   - Subsequent requests will use cache for faster speed")
    print("   - Search results are sorted by distance")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5001)
