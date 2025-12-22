# ⚠️ 重要！啟用 Places API

## 🔴 目前狀態：REQUEST_DENIED

你的 API Key 需要啟用 **Places API** 才能搜尋真實餐廳！

---

## 📝 啟用步驟（5 分鐘完成）

### 步驟 1: 前往 Google Cloud Console

https://console.cloud.google.com/

### 步驟 2: 啟用 Places API

1. 左側選單 → 「API 和服務」→「程式庫」
2. 搜尋框輸入：**Places API**
3. 選擇「**Places API**」（不是 Places API (New)）
4. 點選「**啟用**」按鈕

### 步驟 3: 確認已啟用

前往「API 和服務」→「已啟用的 API 和服務」

應該看到：
- ✅ Maps JavaScript API
- ✅ Places API ⭐ 新增的

---

## 💰 費用說明（不用擔心！）

### Places API 免費額度：

```
每月免費: $200 USD
Places API - Nearby Search: $32/1000 次
免費搜尋次數: 約 6,250 次/月
```

### 我們的專題用量估算：

```
每次開啟網頁 = 1 次搜尋
每天測試 20 次 = 20 次搜尋
每月 30 天 = 600 次搜尋

費用: 600 次 × $32/1000 = $19.2 USD
結論: 仍在 $200 免費額度內！✅
```

---

## 🛡️ 安全設定（確保不扣錢）

### 1. 設定每日配額

前往：https://console.cloud.google.com/google/maps-apis/quotas

找到「Places API - Nearby Search」，設定：
```
每日請求數上限: 200 次/日
```

計算：200 次/日 × 30 天 = 6,000 次/月（仍在免費範圍內）

### 2. 更新 API 限制

前往：https://console.cloud.google.com/apis/credentials

點選你的 API Key，在「API 限制」中勾選：
- ✅ Maps JavaScript API
- ✅ **Places API** ⭐ 新增這個

---

## ✅ 完成後測試

### 測試 1: Python 測試

```bash
cd map
python google_places.py
```

應該看到：
```
找到 10 家餐廳:

📍 麥當勞建工店
   類別: 速食 | 評分: 8.2/10
   ...
```

### 測試 2: 網頁測試

打開 `map/map.html`

應該看到：
- ✅ Google 地圖
- ✅ 真實的餐廳卡片（不是範例資料）
- ✅ 可以搜尋和篩選

---

## 🔍 確認是否使用真實資料

打開 `map/map.html` 後，按 F12 開啟開發者工具，在 Console 看到：

```
✓ 地圖 API 連線成功: {status: "ok"}
```

然後餐廳卡片應該顯示真實的高雄科大建工校區附近餐廳！

---

## ⚠️ 如果還是 REQUEST_DENIED

### 檢查清單：

1. ⬜ 已啟用 Places API（不是 Places API (New)）
2. ⬜ API Key 的「API 限制」中有勾選 Places API
3. ⬜ 等待 5 分鐘（Google 需要時間同步設定）
4. ⬜ 重新整理網頁

### 如果以上都做了還是不行：

建立新的 API Key：
1. 前往憑證頁面
2. 點選「建立憑證」→「API 金鑰」
3. 複製新的 Key
4. 在「應用程式限制」選擇「HTTP 參照網址」
5. 新增：`http://localhost/*` 和 `file:///*`
6. 在「API 限制」勾選：Maps JavaScript API 和 Places API
7. 儲存

然後更新 [map/map.html](map/map.html:141) 和 [map/map_api.py](map/map_api.py:16) 的 API Key

---

## 📞 還有問題？

如果啟用後還是無法使用，告訴我你看到什麼錯誤訊息！

**記住**: 只要不綁信用卡 + 設定配額上限，就絕對不會扣錢！🛡️
