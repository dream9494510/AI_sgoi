@echo off
echo ========================================
echo 飲食控管專題 - 自動安裝與測試
echo ========================================
echo.

:: 檢查 Python
echo [1/5] 檢查 Python 環境...
python --version
if errorlevel 1 (
    echo 錯誤: 未找到 Python,請先安裝 Python 3.9+
    pause
    exit /b 1
)
echo.

:: 安裝依賴
echo [2/5] 安裝依賴套件...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 部分套件安裝失敗
)
echo.

:: 檢查環境變數
echo [3/5] 檢查環境配置...
if "%GEMINI_API_KEY%"=="" (
    echo 警告: GEMINI_API_KEY 未設置
    echo 請執行: set GEMINI_API_KEY=你的KEY
    echo 或建立 .env 檔案
) else (
    echo ✓ GEMINI_API_KEY 已設置
)
echo.

:: 測試模組導入
echo [4/5] 測試模組導入...
python -c "from AI.gemini_service import GeminiService; print('✓ AI 模組導入成功')"
if errorlevel 1 (
    echo ✗ 模組導入失敗
    pause
    exit /b 1
)
echo.

:: 執行完整測試
echo [5/5] 執行 AI 模組測試...
if "%GEMINI_API_KEY%"=="" (
    echo 跳過測試 (未設置 API Key)
) else (
    cd AI
    python test_gemini.py
    cd ..
)
echo.

echo ========================================
echo 安裝完成!
echo ========================================
echo.
echo 下一步:
echo 1. 設置 GEMINI_API_KEY (如果尚未設置)
echo 2. 執行測試: python AI/test_gemini.py
echo 3. 啟動服務: python -m api.main
echo 4. 查看文件: README.md 和 SETUP.md
echo.
pause
