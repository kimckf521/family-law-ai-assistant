# 🌐 家庭法AI助手 - Web版快速开始

## 📦 文件清单

```
streamlit-app/
├── app.py                      # 演示版（无需API）⭐ 推荐先试用
├── app_pro.py                  # 完整版（需要API）
├── start.sh                    # Mac/Linux 启动脚本
├── start.bat                   # Windows 启动脚本
├── requirements.txt            # Python依赖
├── STREAMLIT部署指南.md        # 详细部署文档
├── family_law_chunks.json      # 知识库数据（2.1MB）
└── README_STREAMLIT.md         # 本文件
```

---

## 🚀 最快速启动（3步）

### Mac / Linux

```bash
# 1. 确保在正确目录
cd /path/to/your/files

# 2. 给启动脚本执行权限
chmod +x start.sh

# 3. 运行
./start.sh
```

### Windows

```bash
# 直接双击 start.bat
# 或在命令行中运行:
start.bat
```

### 手动启动

```bash
# 安装Streamlit
pip install streamlit

# 运行演示版
streamlit run app.py

# 或运行完整版（需要API密钥）
export ANTHROPIC_API_KEY='your-key'
streamlit run app_pro.py
```

浏览器会自动打开 http://localhost:8501

---

## 🎯 两个版本对比

| 功能 | 演示版 (app.py) | 完整版 (app_pro.py) |
|------|----------------|-------------------|
| 智能搜索 | ✅ | ✅ |
| 页码引用 | ✅ | ✅ |
| 关键词高亮 | ✅ | ✅ |
| AI智能回答 | ❌ | ✅ |
| 需要API密钥 | ❌ | ✅ |
| 中英文自适应 | 部分 | ✅ |
| 启动速度 | 快 | 稍慢 |
| 推荐用于 | 测试/演示 | 生产使用 |

---

## 💡 演示版功能展示

### ✨ 主要功能

1. **智能搜索**
   - 输入问题自动搜索
   - 关键词匹配和高亮
   - 相关度评分

2. **预设问题**
   - 离婚相关（3个问题）
   - 财产分割（3个问题）
   - 子女相关（3个问题）
   - 赡养费（2个问题）
   - 程序表格（2个问题）

3. **搜索结果**
   - 精美的卡片式展示
   - 页码、章节、类型标签
   - 匹配关键词展示
   - 可展开的完整内容

4. **用户体验**
   - 快捷查询按钮
   - 搜索历史记录
   - 响应式设计
   - 清晰的使用说明

### 📸 界面预览

**主页面:**
- 标题和统计信息
- 搜索输入框
- 4个快捷按钮
- 欢迎信息和使用指南

**侧边栏:**
- 结果数量设置
- 预设问题分类列表
- 使用说明
- 关于系统信息
- 清除历史按钮

**搜索结果:**
- 用户问题显示（蓝色背景）
- 找到X个结果提示（灰色背景）
- 结果卡片（白色，带阴影）
  - 页码标签（蓝色）
  - 相关度得分（绿色）
  - 章节信息
  - 匹配关键词（橙色标签）
  - 可展开的完整内容

---

## 🚀 完整版额外功能

启用完整版需要：

1. **获取API密钥**
   - 访问 https://console.anthropic.com/
   - 创建账号并生成API密钥

2. **设置环境变量**
   ```bash
   # Mac/Linux
   export ANTHROPIC_API_KEY='sk-ant-api03-...'
   
   # Windows
   set ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

3. **运行完整版**
   ```bash
   streamlit run app_pro.py
   ```

**新增功能:**
- 🤖 Claude AI生成专业回答
- 📝 自动引用法条和页码
- 🌐 中英文自动适应
- 💬 对话历史管理
- ⚙️ AI开关控制

---

## 📖 使用示例

### 示例1: 查询离婚条件

**操作:**
1. 在搜索框输入 "divorce requirements"
2. 或点击侧边栏预设问题

**结果:**
- 显示3-5个相关段落
- 包含页码69, 68, 73等
- 关键词 "divorce", "separation", "requirements" 高亮
- （完整版）AI生成详细解答

### 示例2: 快速查询

**操作:**
点击主页面的快捷按钮 "📋 离婚"

**结果:**
自动执行搜索 "divorce requirements"

### 示例3: 浏览预设问题

**操作:**
在侧边栏展开 "🔍 离婚相关"，点击 "婚姻破裂证明"

**结果:**
搜索 "irretrievable breakdown marriage"

---

## 🔧 自定义配置

### 修改端口

```bash
streamlit run app.py --server.port 8080
```

### 禁用自动打开浏览器

```bash
streamlit run app.py --server.headless true
```

### 允许外部访问

```bash
streamlit run app.py --server.address 0.0.0.0
```

### 配置文件

创建 `.streamlit/config.toml`:

```toml
[server]
port = 8501
enableCORS = false

[theme]
primaryColor = "#1976D2"
backgroundColor = "#FFFFFF"
```

---

## 🌐 部署到互联网

### 最简单：Streamlit Community Cloud（免费）

1. **准备GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/family-law-ai.git
   git push -u origin main
   ```

2. **部署**
   - 访问 https://share.streamlit.io/
   - 连接GitHub
   - 选择仓库和app.py
   - 点击Deploy

3. **配置API密钥（如需完整版）**
   - 在Streamlit Cloud设置中
   - Secrets → 添加 ANTHROPIC_API_KEY

4. **获取公开URL**
   - `https://your-app-name.streamlit.app`
   - 可分享给任何人

**优点:**
- ✅ 完全免费
- ✅ 自动HTTPS
- ✅ 无需服务器
- ✅ 自动更新

详见 `STREAMLIT部署指南.md`

---

## 🐛 常见问题

### Q1: ModuleNotFoundError: No module named 'streamlit'

**A:** 安装Streamlit
```bash
pip install streamlit
```

### Q2: 页面空白或加载失败

**A:** 检查：
1. 确认 `family_law_chunks.json` 在同一目录
2. 查看终端错误信息
3. 尝试刷新浏览器

### Q3: API相关错误

**A:** 
1. 确认API密钥正确
2. 检查网络连接
3. 验证API有余额

### Q4: 搜索没有结果

**A:**
- 使用英文关键词
- 尝试更通用的词汇
- 参考预设问题

### Q5: 如何停止服务？

**A:** 在终端按 `Ctrl + C`

---

## 📊 性能说明

### 首次启动
- 加载知识库: ~3秒
- 启动服务: ~2秒
- **总计: ~5秒**

### 搜索速度
- 演示版: <1秒
- 完整版: 3-6秒（含AI生成）

### 内存使用
- 演示版: ~150MB
- 完整版: ~200MB

### 并发支持
- 本地运行: 单用户
- 云端部署: 支持多用户

---

## 🎓 学习资源

**Streamlit官方:**
- 文档: https://docs.streamlit.io/
- 教程: https://docs.streamlit.io/get-started
- 示例: https://streamlit.io/gallery

**本项目:**
- 查看 `STREAMLIT部署指南.md` 了解详细功能
- 阅读代码注释理解实现
- 测试各种查询场景

---

## ✅ 快速检查

启动前确认:
- [ ] Python 3.8+ 已安装
- [ ] Streamlit 已安装
- [ ] family_law_chunks.json 在同一目录
- [ ] （完整版）API密钥已设置
- [ ] （完整版）anthropic库已安装

---

## 🎉 现在开始！

**推荐流程:**

```bash
# 1. 确保文件就绪
ls -l *.py *.json

# 2. 运行启动脚本（最简单）
./start.sh    # Mac/Linux
start.bat     # Windows

# 或手动运行
streamlit run app.py

# 3. 在浏览器中测试
```

**访问:** http://localhost:8501

**第一次使用:**
1. 尝试快捷按钮
2. 测试预设问题
3. 输入自己的问题
4. 查看详细结果
5. 体验用户界面

---

## 💬 需要帮助？

1. 查看 `STREAMLIT部署指南.md` 
2. 阅读错误提示信息
3. 检查终端日志
4. 访问Streamlit官方文档

---

**版本**: v1.0  
**最后更新**: 2026-01-09  
**Streamlit版本要求**: 1.30+

祝你使用愉快！🚀
