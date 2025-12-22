# Google Maps API Key 申請教學

## 📝 申請步驟

### 步驟 1: 前往 Google Cloud Console

訪問：https://console.cloud.google.com/

### 步驟 2: 建立新專案

1. 點選左上角「選取專案」
2. 點選「新增專案」
3. 輸入專案名稱：例如「飲食地圖專題」
4. 點選「建立」

### 步驟 3: 啟用 Maps JavaScript API

1. 在左側選單選擇「API 和服務」→「程式庫」
2. 搜尋「Maps JavaScript API」
3. 點選進入後，點擊「啟用」

### 步驟 4: 建立 API 金鑰

1. 左側選單選擇「憑證」
2. 點選上方「建立憑證」→「API 金鑰」
3. 複製產生的 API 金鑰

### 步驟 5: 設定 API 金鑰限制（建議）

1. 點選剛建立的 API 金鑰
2. 在「應用程式限制」選擇「HTTP 參照網址」
3. 新增項目：
   - `http://localhost/*`
   - `http://127.0.0.1/*`
4. 在「API 限制」選擇「限制金鑰」
5. 勾選：
   - Maps JavaScript API
   - Places API
6. 點選「儲存」

---

## 🔧 設定 API Key

### 方法 1: 修改 map.html

在 [map.html](map.html:205) 找到：

```html
<script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE&callback=initMap&libraries=places&language=zh-TW"></script>
```

將 `YOUR_API_KEY_HERE` 替換成你的 API Key：

```html
<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSy...你的KEY&callback=initMap&libraries=places&language=zh-TW"></script>
```

### 方法 2: 修改 map_api.py（可選）

在 [map_api.py](map_api.py:18) 找到：

```python
GOOGLE_MAPS_API_KEY = ""  # 待填入
```

改成：

```python
GOOGLE_MAPS_API_KEY = "AIzaSy...你的KEY"
```

---

## 💰 免費額度

Google Maps 提供免費額度：

- **每月免費額度**: $200 USD
- **Maps JavaScript API**: 每 1000 次載入 $7 USD
- **免費載入次數**: 約 28,000 次/月

對於小型專題來說，**免費額度綽綽有餘**！

---

## ⚠️ 注意事項

### 1. 不要公開 API Key

- ❌ 不要 commit 到 GitHub
- ❌ 不要分享給他人
- ✅ 設定 API 限制

### 2. 監控使用量

在 Google Cloud Console 可以查看使用量，避免超額收費

### 3. 設定費用上限（建議）

1. 前往「帳單」
2. 設定預算警示
3. 當接近 $200 免費額度時會收到通知

---

## 🧪 測試 API Key

建立測試檔案 `test_maps.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>測試 Google Maps</title>
  <style>
    #map { height: 400px; width: 100%; }
  </style>
</head>
<body>
  <h1>Google Maps API 測試</h1>
  <div id="map"></div>

  <script>
    function initMap() {
      const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 25.0330, lng: 121.5654 },
        zoom: 14
      });

      alert('✓ API Key 運作正常！');
    }
  </script>

  <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">
  </script>
</body>
</html>
```

替換 `YOUR_API_KEY` 後用瀏覽器開啟，如果看到地圖就成功了！

---

## 🆘 常見問題

### Q1: 顯示「This page can't load Google Maps correctly」

**A**: API Key 未設定或無效
- 確認 API Key 已複製完整
- 檢查是否已啟用 Maps JavaScript API

### Q2: 顯示「RefererNotAllowedMapError」

**A**: HTTP 參照網址限制問題
- 到憑證設定新增 `http://localhost/*`
- 或暫時移除應用程式限制（僅限開發時）

### Q3: 免費額度用完怎麼辦？

**A**:
- 設定每日請求上限
- 使用快取減少 API 呼叫
- 升級到付費方案（不建議學生專題）

---

## 📚 相關文件

- [Google Maps JavaScript API 文件](https://developers.google.com/maps/documentation/javascript)
- [Places API 文件](https://developers.google.com/maps/documentation/places/web-service)
- [定價說明](https://developers.google.com/maps/billing-and-pricing/pricing)

---

**完成後記得測試！** 🎉
