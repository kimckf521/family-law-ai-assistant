#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
澳大利亚家庭法AI代理 - Streamlit完整版（带Claude API）
"""

import streamlit as st
import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional
import anthropic

# 页面配置
st.set_page_config(
    page_title="家庭法AI助手 Pro",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main {padding: 0rem 1rem;}
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }
    .ai-message {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
    }
    .search-result {
        background-color: #f5f5f5;
        border-left: 5px solid #9E9E9E;
    }
    .page-ref {
        background-color: #1976D2;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: bold;
        margin: 0 4px;
    }
</style>
""", unsafe_allow_html=True)

class FamilyLawAIAgent:
    """家庭法AI代理（完整版）"""
    
    def __init__(self, chunks_path: str, api_key: Optional[str] = None):
        self.chunks = self._load_chunks(chunks_path)
        self.claude_client = None
        if api_key:
            self.claude_client = anthropic.Anthropic(api_key=api_key)
    
    @st.cache_data
    def _load_chunks(_self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['chunks']
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """搜索相关内容"""
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
            
            if score > 0:
                scored_chunks.append({
                    'chunk': chunk,
                    'score': score,
                    'matched_keywords': list(set(matched_keywords))
                })
        
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        return scored_chunks[:n_results]
    
    def generate_answer(self, query: str, search_results: List[Dict]) -> str:
        """使用Claude生成回答"""
        if not self.claude_client:
            return None
        
        # 构建上下文
        context = "\n\n---\n\n".join([
            f"[页码 {r['chunk']['page_number']}] {r['chunk']['text'][:500]}"
            for r in search_results[:3]
        ])
        
        system_prompt = f"""你是澳大利亚家庭法专家AI助手，基于《The Family Law Book》回答问题。

【重要规则】
1. 必须引用具体页码（格式: [页码X]）
2. 区分"法律信息"和"法律建议" - 你提供信息，不是建议
3. 使用清晰、通俗的语言
4. 根据用户语言自动调整（中文或英文）

【相关法律内容】
{context}

【回答格式】
- 直接回答问题
- 引用具体页码
- 提供实用建议
- 最后提醒：这是法律信息，具体情况需咨询律师
"""

        try:
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                temperature=0.3,
                system=system_prompt,
                messages=[{"role": "user", "content": query}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ AI生成失败: {str(e)}"

def init_session_state():
    """初始化session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'agent' not in st.session_state:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        with st.spinner('🔄 正在初始化AI代理...'):
            st.session_state.agent = FamilyLawAIAgent(
                '/home/claude/family_law_chunks.json',
                api_key=api_key
            )
    if 'use_ai' not in st.session_state:
        st.session_state.use_ai = st.session_state.agent.claude_client is not None

def main():
    init_session_state()
    
    # 标题
    st.title("⚖️ 澳大利亚家庭法AI助手 Pro")
    
    # 检查API状态
    if st.session_state.agent.claude_client:
        st.success("✅ AI模式已启用 - 将生成智能回答")
    else:
        st.warning("⚠️ 检索模式 - 仅显示相关法律文本（设置 ANTHROPIC_API_KEY 启用AI回答）")
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 设置")
        
        n_results = st.slider("结果数量", 3, 10, 5)
        
        if st.session_state.agent.claude_client:
            st.session_state.use_ai = st.checkbox("启用AI智能回答", value=True)
        
        st.markdown("---")
        st.subheader("💬 对话历史")
        if st.session_state.messages:
            for i, msg in enumerate(st.session_state.messages[-5:]):
                st.caption(f"{i+1}. {msg['query'][:30]}...")
        else:
            st.caption("暂无历史记录")
        
        if st.button("🗑️ 清除历史", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # 搜索输入
    query = st.text_input(
        "🔍 输入你的问题",
        placeholder="例如: What are the requirements for divorce?",
        key="query_input"
    )
    
    # 快捷按钮
    cols = st.columns(4)
    quick_queries = [
        ("📋 离婚", "divorce requirements"),
        ("💰 财产", "property settlement"),
        ("👶 子女", "child custody"),
        ("📄 表格", "application forms")
    ]
    for col, (label, q) in zip(cols, quick_queries):
        with col:
            if st.button(label, use_container_width=True):
                query = q
    
    # 处理查询
    if query:
        # 记录到历史
        st.session_state.messages.append({
            'query': query,
            'timestamp': datetime.now().isoformat()
        })
        
        # 显示用户问题
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🔍 你的问题:</strong><br>{query}
        </div>
        """, unsafe_allow_html=True)
        
        # 搜索
        with st.spinner('🔍 搜索中...'):
            results = st.session_state.agent.search(query, n_results)
        
        if results:
            # 显示搜索结果摘要
            st.markdown(f"""
            <div class="chat-message search-result">
                <strong>📚 找到 {len(results)} 个相关段落</strong><br>
                页码: {', '.join([str(r['chunk']['page_number']) for r in results[:5]])}
            </div>
            """, unsafe_allow_html=True)
            
            # 如果启用AI，生成回答
            if st.session_state.use_ai and st.session_state.agent.claude_client:
                with st.spinner('🤔 AI正在分析并生成回答...'):
                    answer = st.session_state.agent.generate_answer(query, results)
                
                if answer:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>🤖 AI助手:</strong><br><br>
                        {answer.replace('[页码', '<span class="page-ref">页码').replace(']', '</span>')}
                    </div>
                    """, unsafe_allow_html=True)
            
            # 显示详细结果
            with st.expander("📖 查看详细检索结果"):
                for i, result in enumerate(results, 1):
                    chunk = result['chunk']
                    st.markdown(f"""
                    **结果 {i}** | 页码: {chunk['page_number']} | 相关度: {result['score']}
                    
                    章节: {chunk.get('chapter', 'N/A')[:80]}...
                    
                    {chunk['text'][:400]}...
                    """)
                    st.divider()
            
            # 提示
            st.info("💡 这是法律信息，不是法律建议。具体情况请咨询专业律师。")
        
        else:
            st.warning("❌ 未找到相关内容，请尝试其他关键词")
    
    else:
        # 欢迎页
        st.markdown("""
        ## 👋 欢迎使用家庭法AI助手
        
        ### 🎯 功能特点
        - 🔍 智能语义搜索
        - 🤖 AI生成专业回答（需API密钥）
        - 📄 精确页码引用
        - 🌐 中英文双语支持
        
        ### 🚀 开始使用
        在上方输入框输入问题，或点击快捷按钮！
        """)

if __name__ == "__main__":
    main()
