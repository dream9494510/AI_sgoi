#!/bin/bash

echo "========================================"
echo "飲食控管專題 - 自動安裝與測試"
echo "========================================"
echo ""

# 檢查 Python
echo "[1/5] 檢查 Python 環境..."
if ! command -v python3 &> /dev/null; then
    echo "錯誤: 未找到 Python,請先安裝 Python 3.9+"
    exit 1
fi
python3 --version
echo ""

# 安裝依賴
echo "[2/5] 安裝依賴套件..."
pip3 install -r requirements.txt
echo ""

# 檢查環境變數
echo "[3/5] 檢查環境配置..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo "警告: GEMINI_API_KEY 未設置"
    echo "請執行: export GEMINI_API_KEY=你的KEY"
    echo "或建立 .env 檔案"
else
    echo "✓ GEMINI_API_KEY 已設置"
fi
echo ""

# 測試模組導入
echo "[4/5] 測試模組導入..."
python3 -c "from AI.gemini_service import GeminiService; print('✓ AI 模組導入成功')"
if [ $? -ne 0 ]; then
    echo "✗ 模組導入失敗"
    exit 1
fi
echo ""

# 執行完整測試
echo "[5/5] 執行 AI 模組測試..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo "跳過測試 (未設置 API Key)"
else
    cd AI
    python3 test_gemini.py
    cd ..
fi
echo ""

echo "========================================"
echo "安裝完成!"
echo "========================================"
echo ""
echo "下一步:"
echo "1. 設置 GEMINI_API_KEY (如果尚未設置)"
echo "2. 執行測試: python3 AI/test_gemini.py"
echo "3. 啟動服務: python3 -m api.main"
echo "4. 查看文件: README.md 和 SETUP.md"
echo ""
