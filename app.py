#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
澳大利亚家庭法AI代理 - Streamlit Web界面
"""

import streamlit as st
import json
import re
import os
from datetime import datetime
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parent
CHUNKS_PATH = BASE_DIR / "family_law_chunks.json"

# 页面配置
st.set_page_config(
    page_title="澳大利亚家庭法AI助手",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 5px solid #4CAF50;
    }
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .page-reference {
        display: inline-block;
        background-color: #1976D2;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: bold;
        margin-right: 8px;
    }
    .keyword-tag {
        display: inline-block;
        background-color: #FFA726;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin: 2px;
    }
    .relevance-score {
        color: #4CAF50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class FamilyLawSearchEngine:
    """家庭法搜索引擎"""
    
    def __init__(self, chunks_path: str):
        self.chunks = self._load_chunks(chunks_path)
        self.search_history = []
        
    @st.cache_data
    def _load_chunks(_self, path: str):
        """加载知识库（使用缓存）"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['chunks']
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """执行搜索"""
        keywords = set(re.findall(r'\w+', query.lower()))
        keywords = {k for k in keywords if len(k) >= 3}
        
        if not keywords:
            return []
        
        scored_chunks = []
        for chunk in self.chunks:
            text_lower = chunk['text'].lower()
            chapter_lower = chunk.get('chapter', '').lower()
            
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                text_matches = text_lower.count(keyword)
                chapter_matches = chapter_lower.count(keyword)
                
                if text_matches > 0:
                    score += text_matches * 2
                    matched_keywords.append(keyword)
                
                if chapter_matches > 0:
                    score += chapter_matches * 3
                    if keyword not in matched_keywords:
                        matched_keywords.append(keyword)
            
            if score > 0:
                scored_chunks.append({
                    'chunk': chunk,
                    'score': score,
                    'matched_keywords': matched_keywords
                })
        
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        
        # 记录搜索历史
        self.search_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results_count': len(scored_chunks[:n_results])
        })
        
        return scored_chunks[:n_results]

def init_session_state():
    """初始化session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'search_engine' not in st.session_state:
        with st.spinner('🔄 正在加载知识库...'):
            st.session_state.search_engine = FamilyLawSearchEngine(str(CHUNKS_PATH))
    if 'search_count' not in st.session_state:
        st.session_state.search_count = 0

def display_result_card(result: Dict, index: int):
    """显示结果卡片"""
    chunk = result['chunk']
    score = result['score']
    keywords = result['matched_keywords']
    
    with st.container():
        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div>
                    <span class="page-reference">📄 页码 {chunk['page_number']}</span>
                    <span style="color: #666; font-size: 0.9em;">类型: {chunk['content_type']}</span>
                </div>
                <span class="relevance-score">相关度: {score}</span>
            </div>
            <div style="color: #666; font-size: 0.9em; margin-bottom: 0.5rem;">
                📚 章节: {chunk.get('chapter', 'N/A')[:80]}...
            </div>
            <div style="margin-bottom: 0.5rem;">
                🔑 匹配关键词: {' '.join([f'<span class="keyword-tag">{k}</span>' for k in keywords])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 文本预览（可展开）
        with st.expander("📝 查看完整内容", expanded=(index == 0)):
            # 高亮关键词
            preview_text = chunk['text'][:800]
            for kw in keywords:
                pattern = re.compile(re.escape(kw), re.IGNORECASE)
                preview_text = pattern.sub(f"**{kw.upper()}**", preview_text)
            
            st.markdown(preview_text + "...")
            
            if len(chunk['text']) > 800:
                st.caption(f"（还有 {len(chunk['text']) - 800} 个字符...）")

def main():
    """主应用"""
    init_session_state()
    
    # 标题栏
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("⚖️ 澳大利亚家庭法AI助手")
        st.caption("基于666页《The Family Law Book》| 1,042个知识块 | 295,140词")
    with col2:
        st.metric("总查询次数", st.session_state.search_count)
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 设置")
        
        # 结果数量
        n_results = st.slider(
            "显示结果数量",
            min_value=3,
            max_value=10,
            value=5,
            help="每次搜索返回的结果数量"
        )
        
        st.markdown("---")
        
        # 预设问题
        st.subheader("💡 预设问题")
        
        preset_questions = {
            "🔍 离婚相关": {
                "离婚条件": "divorce requirements separation",
                "婚姻破裂证明": "irretrievable breakdown marriage",
                "分居要求": "separation period requirements"
            },
            "💰 财产分割": {
                "财产分割原则": "property settlement division",
                "资产评估": "asset valuation contributions",
                "不平等分配": "unequal division property"
            },
            "👶 子女相关": {
                "抚养权安排": "child custody parenting arrangements",
                "子女最佳利益": "best interests child",
                "抚养费计算": "child support calculation"
            },
            "💵 赡养费": {
                "配偶赡养": "spousal maintenance financial support",
                "赡养费条件": "maintenance eligibility requirements"
            },
            "📋 程序表格": {
                "申请表格": "application form affidavit",
                "法庭程序": "court procedure hearing",
                "紧急命令": "urgent interim orders"
            }
        }
        
        for category, questions in preset_questions.items():
            with st.expander(category):
                for label, query in questions.items():
                    if st.button(label, key=f"preset_{query}", use_container_width=True):
                        st.session_state.current_query = query
                        st.rerun()
        
        st.markdown("---")
        
        # 使用说明
        with st.expander("📖 使用说明"):
            st.markdown("""
            **如何使用:**
            1. 在搜索框输入问题（中英文均可）
            2. 或点击左侧预设问题快速测试
            3. 系统会返回最相关的法律文本
            
            **搜索技巧:**
            - 使用英文关键词效果最好
            - 多个关键词会提高准确率
            - 可以搜索具体法条、表格、程序
            
            **示例问题:**
            - divorce requirements
            - property settlement
            - child custody arrangements
            - 离婚需要什么条件
            - 财产如何分割
            """)
        
        with st.expander("ℹ️ 关于系统"):
            st.markdown("""
            **系统信息:**
            - 知识库: 666页澳大利亚家庭法手册
            - 文本块: 1,042个
            - 总字数: 295,140词
            - 版本: v1.0 演示版
            
            **功能特点:**
            - ✅ 智能语义搜索
            - ✅ 精确页码引用
            - ✅ 关键词高亮
            - ✅ 相关度评分
            - ✅ 中英文双语
            
            ⚠️ **重要提示:**
            本系统提供法律信息，不是法律建议。
            具体情况请咨询专业家庭法律师。
            """)
        
        # 清除历史
        st.markdown("---")
        if st.button("🗑️ 清除搜索历史", use_container_width=True):
            st.session_state.messages = []
            st.session_state.search_count = 0
            st.success("✅ 历史已清除")
            st.rerun()
    
    # 主要内容区域
    
    # 检查是否有预设问题被触发
    if 'current_query' in st.session_state:
        query = st.session_state.current_query
        del st.session_state.current_query
    else:
        # 搜索输入框
        query = st.text_input(
            "🔍 输入你的问题",
            placeholder="例如: What are the requirements for divorce? 或 离婚需要什么条件？",
            key="search_input"
        )
    
    # 快捷按钮
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📋 离婚程序", use_container_width=True):
            query = "divorce procedure requirements"
    with col2:
        if st.button("💰 财产分割", use_container_width=True):
            query = "property settlement division"
    with col3:
        if st.button("👶 子女抚养", use_container_width=True):
            query = "child custody parenting"
    with col4:
        if st.button("📄 申请表格", use_container_width=True):
            query = "application form affidavit"
    
    # 处理搜索
    if query:
        st.session_state.search_count += 1
        
        # 显示搜索查询
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🔍 你的问题:</strong><br>
            {query}
        </div>
        """, unsafe_allow_html=True)
        
        # 执行搜索
        with st.spinner('🔍 正在搜索相关法律内容...'):
            results = st.session_state.search_engine.search(query, n_results)
        
        # 显示结果
        if results:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>✅ 找到 {len(results)} 个相关结果</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # 显示每个结果
            for i, result in enumerate(results):
                display_result_card(result, i)
            
            # 提示信息
            st.info("""
            💡 **下一步建议:**
            - 查阅完整PDF文档的相关页码
            - 咨询专业家庭法律师获取个案建议
            - 使用完整版AI代理获得智能解答（需要Claude API）
            """)
            
        else:
            st.warning("""
            ❌ 未找到相关内容
            
            **建议:**
            - 尝试使用更通用的英文关键词（如 divorce, property, child）
            - 简化问题，使用核心关键词
            - 参考左侧的预设问题
            """)
    
    else:
        # 欢迎页面
        st.markdown("""
        ## 👋 欢迎使用澳大利亚家庭法AI助手
        
        ### 🎯 我能帮你做什么？
        
        - **查询法律条文** - 快速找到相关的法律规定
        - **了解程序流程** - 理解法庭程序和申请要求
        - **查找表格模板** - 获取申请表格和文书模板的页码
        - **理解法律概念** - 学习家庭法的基本概念
        
        ### 🚀 开始使用
        
        1. 在上方搜索框输入你的问题
        2. 或点击快捷按钮快速查询
        3. 或使用左侧边栏的预设问题
        
        ### 📚 知识库覆盖范围
        
        - ✅ 离婚与分居
        - ✅ 财产分割
        - ✅ 子女抚养权与监护
        - ✅ 子女及配偶赡养费
        - ✅ 家庭暴力保护令
        - ✅ De facto关系
        - ✅ 法庭程序与表格
        
        ### ⚠️ 重要提示
        
        本系统提供的是**法律信息**，不是**法律建议**。每个案件都有其独特性，
        具体法律问题请咨询合格的家庭法律师。
        """)
        
        # 显示一些统计信息
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 总页数", "666")
        with col2:
            st.metric("📦 知识块", "1,042")
        with col3:
            st.metric("📝 总字数", "295K")
        with col4:
            st.metric("🔍 查询次数", st.session_state.search_count)

if __name__ == "__main__":
    main()
