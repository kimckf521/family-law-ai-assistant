# 🌐 Streamlit Web界面部署指南

## 📦 包含的文件

1. **app.py** - 演示版（无需API，立即可用）
2. **app_pro.py** - 完整版（需要Claude API，带AI回答）

---

## 🚀 快速开始（本地运行）

### 步骤1: 安装Streamlit

```bash
pip install streamlit
```

### 步骤2: 运行演示版

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

**就这么简单！**

---

## 🎨 功能特点

### 演示版（app.py）
- ✅ 美观的Web界面
- ✅ 智能关键词搜索
- ✅ 预设问题快速查询
- ✅ 相关度评分
- ✅ 关键词高亮
- ✅ 可展开的详细内容
- ✅ 搜索历史记录
- ✅ 响应式设计

### 完整版（app_pro.py）
- 🚀 所有演示版功能
- 🚀 Claude AI智能回答
- 🚀 自动引用页码
- 🚀 中英文自适应
- 🚀 对话历史管理

---

## 💡 使用完整版（带AI）

### 步骤1: 获取API密钥

访问 https://console.anthropic.com/ 获取API密钥

### 步骤2: 设置环境变量

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Windows:**
```bash
set ANTHROPIC_API_KEY=your-api-key-here
```

### 步骤3: 安装依赖

```bash
pip install streamlit anthropic
```

### 步骤4: 运行完整版

```bash
streamlit run app_pro.py
```

---

## 🌐 部署到云端

### 选项1: Streamlit Community Cloud（推荐，免费）

1. **准备代码**
   - 将所有文件上传到GitHub仓库
   - 创建 `requirements.txt`:
     ```
     streamlit
     anthropic
     ```

2. **部署步骤**
   - 访问 https://share.streamlit.io/
   - 连接GitHub账号
   - 选择仓库和分支
   - 选择 `app.py` 作为主文件
   - 在Settings中添加 ANTHROPIC_API_KEY（如需AI功能）

3. **访问应用**
   - 获得公开URL: `https://your-app.streamlit.app`
   - 可分享给任何人使用

**优点:**
- ✅ 完全免费
- ✅ 自动HTTPS
- ✅ 无需服务器管理
- ✅ 自动更新（推送到GitHub即可）

### 选项2: Heroku

```bash
# 创建 Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# 创建 runtime.txt
echo "python-3.11.0" > runtime.txt

# 部署
heroku create your-app-name
git push heroku main
```

### 选项3: AWS/Azure/GCP

使用Docker容器部署:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📱 界面预览

### 主页
- 清晰的标题和说明
- 搜索输入框
- 快捷查询按钮
- 统计信息展示

### 侧边栏
- 设置选项（结果数量等）
- 预设问题分类
  - 离婚相关
  - 财产分割
  - 子女相关
  - 赡养费
  - 程序表格
- 使用说明
- 关于系统

### 搜索结果
- 用户问题展示
- 找到X个结果的提示
- 每个结果卡片包含:
  - 页码标签
  - 章节信息
  - 匹配关键词
  - 相关度评分
  - 可展开的完整内容

### AI回答（完整版）
- 专业的分析和解答
- 自动引用页码
- 通俗易懂的语言
- 法律免责声明

---

## ⚙️ 配置选项

### 自定义配置文件（.streamlit/config.toml）

```toml
[theme]
primaryColor = "#1976D2"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### 环境变量

- `ANTHROPIC_API_KEY` - Claude API密钥
- `STREAMLIT_SERVER_PORT` - 端口号（默认8501）
- `STREAMLIT_SERVER_ADDRESS` - 地址（默认localhost）

---

## 🔧 性能优化

### 1. 使用缓存

代码中已使用 `@st.cache_data` 缓存知识库加载

### 2. 减少重新渲染

使用 `st.session_state` 管理状态

### 3. 异步加载

大型操作使用 `st.spinner` 显示加载状态

### 4. 分页结果

限制每次显示的结果数量（3-10个）

---

## 📊 使用统计

### 内置统计功能
- 总查询次数
- 搜索历史记录
- 最近5次查询

### 添加Google Analytics（可选）

在 `app.py` 中添加:

```python
import streamlit.components.v1 as components

components.html("""
<!-- Google Analytics code -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
""")
```

---

## 🐛 常见问题

### Q: 页面加载很慢？
**A:** 首次加载需要读取2.1MB的知识库，后续会使用缓存。可以考虑使用数据库。

### Q: 如何添加新功能？
**A:** 
- 修改 `app.py` 或 `app_pro.py`
- 重启Streamlit服务
- 或者使用 `st.rerun()` 动态刷新

### Q: 能否添加用户登录？
**A:** 可以使用 `streamlit-authenticator` 库:
```bash
pip install streamlit-authenticator
```

### Q: 如何限制访问？
**A:** 
- 在Streamlit Cloud中设置密码保护
- 或使用反向代理（nginx）添加认证

### Q: API费用如何控制？
**A:**
- 限制每个用户的查询次数
- 使用缓存存储常见问题的回答
- 监控API使用量

---

## 🎯 下一步增强

### 短期（本周）
- [ ] 添加用户反馈按钮（👍 👎）
- [ ] 保存对话历史到文件
- [ ] 添加导出功能（PDF/TXT）
- [ ] 多语言界面切换

### 中期（本月）
- [ ] 用户账号系统
- [ ] 对话历史云端同步
- [ ] 高级搜索过滤
- [ ] 文书生成功能

### 长期（季度）
- [ ] 移动端优化
- [ ] 语音输入
- [ ] 实时协作
- [ ] API接口

---

## 📖 示例使用流程

### 场景1: 律师查询离婚条件

1. 打开应用
2. 点击侧边栏 "离婚相关" → "离婚条件"
3. 系统返回3-5个相关段落
4. AI生成专业解答（完整版）
5. 点击展开查看完整法律文本
6. 记录相关页码（如页码69, 73）

### 场景2: 公众咨询财产分割

1. 在搜索框输入 "财产如何分割"
2. 系统返回相关结果
3. AI用通俗语言解释
4. 提供实用建议
5. 建议咨询专业律师

---

## 💻 开发技巧

### 实时预览

```bash
# 启用自动重载
streamlit run app.py --server.runOnSave true
```

### 调试模式

```python
# 在代码中添加
st.write("Debug info:", variable)
st.json(data)  # 显示JSON数据
```

### 性能分析

```bash
# 使用profiler
streamlit run app.py --server.enableStaticServing=false
```

---

## 🆘 获取帮助

**Streamlit官方资源:**
- 文档: https://docs.streamlit.io/
- 论坛: https://discuss.streamlit.io/
- 示例库: https://streamlit.io/gallery

**本项目支持:**
- 查看代码注释
- 阅读使用说明
- 提出问题

---

## ✅ 快速检查清单

部署前确认:
- [ ] 测试本地运行正常
- [ ] API密钥配置正确（如需AI）
- [ ] 所有文件路径正确
- [ ] requirements.txt 完整
- [ ] 测试各种查询场景
- [ ] 检查移动端显示
- [ ] 确认法律免责声明显示

---

## 🎉 开始使用

**最简单的方式:**

```bash
# 1. 安装Streamlit
pip install streamlit

# 2. 运行应用
streamlit run app.py

# 3. 在浏览器中打开 http://localhost:8501
```

**就这么简单！享受你的Web应用吧！** 🚀

---

**版本**: v1.0  
**更新日期**: 2026-01-09  
**适用于**: Streamlit 1.30+
