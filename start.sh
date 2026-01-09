#!/bin/bash
# 家庭法AI助手 - 一键启动脚本

echo "=================================="
echo "🏛️  家庭法AI助手 - Web版"
echo "=================================="
echo ""

# 检查Streamlit是否安装
if ! command -v streamlit &> /dev/null
then
    echo "📦 Streamlit未安装，正在安装..."
    pip install streamlit
    echo "✅ 安装完成"
    echo ""
fi

# 检查API密钥
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  未设置ANTHROPIC_API_KEY"
    echo "   运行演示版（仅搜索功能）"
    echo ""
    echo "💡 如需AI回答功能，请先设置API密钥:"
    echo "   export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    APP_FILE="app.py"
else
    echo "✅ 检测到API密钥，运行完整版（含AI回答）"
    echo ""
    
    # 询问使用哪个版本
    read -p "使用完整版？(y/n，默认y): " choice
    choice=${choice:-y}
    
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        APP_FILE="app_pro.py"
        
        # 检查anthropic是否安装
        if ! python3 -c "import anthropic" &> /dev/null; then
            echo "📦 安装anthropic库..."
            pip install anthropic
        fi
    else
        APP_FILE="app.py"
    fi
fi

echo "🚀 启动 $APP_FILE ..."
echo ""
echo "=================================="
echo "浏览器将自动打开应用"
echo "或手动访问: http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止服务"
echo "=================================="
echo ""

# 启动Streamlit
streamlit run $APP_FILE
