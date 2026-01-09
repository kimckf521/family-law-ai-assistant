@echo off
REM 家庭法AI助手 - Windows一键启动脚本

echo ==================================
echo 🏛️  家庭法AI助手 - Web版
echo ==================================
echo.

REM 检查Streamlit是否安装
streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Streamlit未安装，正在安装...
    pip install streamlit
    echo ✅ 安装完成
    echo.
)

REM 检查API密钥
if "%ANTHROPIC_API_KEY%"=="" (
    echo ⚠️  未设置ANTHROPIC_API_KEY
    echo    运行演示版（仅搜索功能）
    echo.
    echo 💡 如需AI回答功能，请先设置API密钥:
    echo    set ANTHROPIC_API_KEY=your-key-here
    echo.
    set APP_FILE=app.py
) else (
    echo ✅ 检测到API密钥，运行完整版（含AI回答）
    echo.
    
    REM 检查anthropic是否安装
    python -c "import anthropic" >nul 2>&1
    if %errorlevel% neq 0 (
        echo 📦 安装anthropic库...
        pip install anthropic
    )
    
    set APP_FILE=app_pro.py
)

echo 🚀 启动 %APP_FILE% ...
echo.
echo ==================================
echo 浏览器将自动打开应用
echo 或手动访问: http://localhost:8501
echo.
echo 按 Ctrl+C 停止服务
echo ==================================
echo.

REM 启动Streamlit
streamlit run %APP_FILE%
