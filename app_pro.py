#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Australian Family Law AI Agent Pro - Bilingual with Claude API
澳大利亚家庭法AI代理专业版 - 双语版带Claude API
"""

import streamlit as st
import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional
import anthropic

# Language configurations
LANGUAGES = {
    'en': {
        'page_title': 'Family Law AI Assistant Pro',
        'title': '⚖️ Australian Family Law AI Assistant Pro',
        'subtitle': 'AI-powered legal assistant with intelligent answers',
        'search_placeholder': 'Ask your question about family law...',
        'search_button': '🤖 Ask AI',
        'loading': '🔄 Loading AI agent...',
        'thinking': '🤔 AI is thinking...',
        'searching': '🔍 Searching knowledge base...',
        'results_title': 'Relevant Content',
        'ai_answer_title': '💡 AI Answer',
        'no_api_key': '⚠️ No API key configured. Using search-only mode.',
        'about': 'About',
        'about_text': '''
**Pro Version Features:**
- 🤖 AI-powered intelligent answers
- 🔍 Advanced semantic search
- 📄 Automatic citations with page numbers
- 💬 Natural language understanding

**Powered by:**
- Claude Sonnet 4 AI
- 666-page Family Law knowledge base
- 1,042 searchable content chunks

**Note:** This is the Pro version with AI capabilities. Requires Anthropic API key.
        ''',
        'search_mode': 'Search Only Mode',
        'ai_mode': 'AI Mode',
        'toggle_mode': 'Mode',
        'page_label': 'Page',
        'category_label': 'Category',
        'clear_chat': 'Clear Chat',
        'search_history': 'Chat History',
        'footer': 'Pro version with AI | Built with ❤️ for the legal community'
    },
    'zh': {
        'page_title': '家庭法AI助手专业版',
        'title': '⚖️ 澳大利亚家庭法AI助手专业版',
        'subtitle': 'AI驱动的法律助手，提供智能回答',
        'search_placeholder': '询问您的家庭法问题...',
        'search_button': '🤖 询问AI',
        'loading': '🔄 正在加载AI代理...',
        'thinking': '🤔 AI正在思考...',
        'searching': '🔍 搜索知识库中...',
        'results_title': '相关内容',
        'ai_answer_title': '💡 AI回答',
        'no_api_key': '⚠️ 未配置API密钥。使用纯搜索模式。',
        'about': '关于',
        'about_text': '''
**专业版功能：**
- 🤖 AI驱动的智能回答
- 🔍 高级语义搜索
- 📄 自动引用页码
- 💬 自然语言理解

**技术支持：**
- Claude Sonnet 4 AI
- 666页家庭法知识库
- 1,042个可搜索内容块

**注意：** 这是带AI功能的专业版。需要Anthropic API密钥。
        ''',
        'search_mode': '纯搜索模式',
        'ai_mode': 'AI模式',
        'toggle_mode': '模式',
        'page_label': '页码',
        'category_label': '类别',
        'clear_chat': '清空对话',
        'search_history': '对话历史',
        'footer': 'AI专业版 | 为法律社区用❤️构建'
    }
}

# Page configuration
st.set_page_config(
    page_title="Family Law AI Pro | 家庭法AI专业版",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
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
    """Family Law AI Agent Pro | 家庭法AI代理专业版"""
    
    def __init__(self, chunks_path: str, api_key: Optional[str] = None):
        self.chunks = self._load_chunks(chunks_path)
        self.claude_client = None
        if api_key:
            try:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
            except Exception as e:
                st.error(f"Failed to initialize Claude API: {str(e)}")
    
    @st.cache_data
    def _load_chunks(_self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['chunks']
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search relevant content | 搜索相关内容"""
        query_lower = query.lower()
        query_terms = set(re.findall(r'\b\w+\b', query_lower))
        
        scored_chunks = []
        for chunk in self.chunks:
            text_lower = chunk['text'].lower()
            score = 0
            
            # Exact phrase match
            if query_lower in text_lower:
                score += 10
            
            # Term matching
            text_terms = set(re.findall(r'\b\w+\b', text_lower))
            matching_terms = query_terms & text_terms
            score += len(matching_terms) * 2
            
            # Boost by term frequency
            for term in matching_terms:
                score += text_lower.count(term)
            
            if score > 0:
                scored_chunks.append({
                    'chunk': chunk,
                    'score': score
                })
        
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        return scored_chunks[:n_results]
    
    def generate_ai_answer(self, query: str, context_chunks: List[Dict], language: str = 'en') -> str:
        """Generate AI answer | 生成AI回答"""
        if not self.claude_client:
            return None
        
        context_text = "\n\n".join([
            f"[Page {chunk['chunk']['page']}] {chunk['chunk']['text']}"
            for chunk in context_chunks[:5]
        ])
        
        if language == 'zh':
            system_prompt = """你是一个澳大利亚家庭法专家助手。基于提供的法律文本，用中文回答用户的问题。

要求：
1. 只使用提供的文本内容回答
2. 明确引用页码（如"根据第123页..."）
3. 如果文本中没有相关信息，诚实地说明
4. 使用清晰、专业但易懂的语言
5. 提供具体、实用的信息
6. 提醒这是法律信息，不是法律建议"""

            user_prompt = f"""基于以下法律文本回答问题。

法律文本：
{context_text}

用户问题：{query}

请用中文提供清晰、专业的回答，并引用相关页码。"""
        else:
            system_prompt = """You are an Australian Family Law expert assistant. Answer questions based on the provided legal text.

Requirements:
1. Only use the provided text content
2. Clearly cite page numbers (e.g., "According to page 123...")
3. If information is not in the text, honestly state this
4. Use clear, professional but accessible language
5. Provide specific, practical information
6. Remind that this is legal information, not legal advice"""

            user_prompt = f"""Answer the question based on the following legal text.

Legal Text:
{context_text}

Question: {query}

Provide a clear, professional answer with page citations."""
        
        try:
            response = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating AI response: {str(e)}"


def detect_language(text: str) -> str:
    """Detect if text contains Chinese | 检测是否包含中文"""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return 'zh' if len(chinese_chars) > len(text) * 0.3 else 'en'


def init_session_state():
    """Initialize session state | 初始化状态"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'agent' not in st.session_state:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        with st.spinner(LANGUAGES[st.session_state.language]['loading']):
            # Use relative path for Streamlit Cloud
            current_dir = os.path.dirname(os.path.abspath(__file__))
            chunks_path = os.path.join(current_dir, 'family_law_chunks.json')
            st.session_state.agent = FamilyLawAIAgent(chunks_path, api_key=api_key)
    if 'use_ai' not in st.session_state:
        st.session_state.use_ai = st.session_state.agent.claude_client is not None


def main():
    init_session_state()
    
    lang_data = LANGUAGES[st.session_state.language]
    
    # Sidebar
    with st.sidebar:
        # Language switcher
        st.markdown("### 🌐 Language | 语言")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇬🇧 English", use_container_width=True,
                        type="primary" if st.session_state.language == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        with col2:
            if st.button("🇨🇳 中文", use_container_width=True,
                        type="primary" if st.session_state.language == 'zh' else "secondary"):
                st.session_state.language = 'zh'
                st.rerun()
        
        st.markdown("---")
        
        # Mode toggle
        if st.session_state.agent.claude_client:
            st.markdown(f"### {lang_data['toggle_mode']}")
            use_ai = st.toggle(
                lang_data['ai_mode'] if st.session_state.use_ai else lang_data['search_mode'],
                value=st.session_state.use_ai,
                key="ai_toggle"
            )
            st.session_state.use_ai = use_ai
        else:
            st.warning(lang_data['no_api_key'])
        
        st.markdown("---")
        
        # About
        with st.expander(lang_data['about'], expanded=False):
            st.markdown(lang_data['about_text'])
        
        # Chat controls
        if st.session_state.messages:
            st.markdown("---")
            if st.button(lang_data['clear_chat'], use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    # Main content
    st.title(lang_data['title'])
    st.markdown(f"*{lang_data['subtitle']}*")
    st.markdown("---")
    
    # Chat interface
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 {message["content"]}</div>',
                       unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f'<div class="chat-message ai-message">🤖 {message["content"]}</div>',
                       unsafe_allow_html=True)
        elif message["role"] == "search":
            st.markdown(f'<div class="chat-message search-result">🔍 {message["content"]}</div>',
                       unsafe_allow_html=True)
    
    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "query_input",
            placeholder=lang_data['search_placeholder'],
            label_visibility="collapsed",
            key="user_query"
        )
    with col2:
        search_button = st.button(lang_data['search_button'], use_container_width=True, type="primary")
    
    # Process query
    if search_button and query:
        # Auto-detect language
        detected_lang = detect_language(query)
        if detected_lang != st.session_state.language:
            st.session_state.language = detected_lang
            lang_data = LANGUAGES[detected_lang]
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })
        
        # Search
        with st.spinner(lang_data['searching']):
            results = st.session_state.agent.search(query, n_results=5)
        
        # Display search results
        if results:
            search_summary = f"{lang_data['results_title']}:\n"
            for idx, result in enumerate(results[:3]):
                chunk = result['chunk']
                page = chunk.get('page', 'N/A')
                text_preview = chunk['text'][:150] + "..."
                search_summary += f"\n📄 {lang_data['page_label']} {page}: {text_preview}"
            
            st.session_state.messages.append({
                "role": "search",
                "content": search_summary
            })
        
        # Generate AI answer if enabled
        if st.session_state.use_ai and results:
            with st.spinner(lang_data['thinking']):
                ai_answer = st.session_state.agent.generate_ai_answer(
                    query, results, st.session_state.language
                )
                if ai_answer:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_answer
                    })
        
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #666;'>{lang_data['footer']}</div>",
               unsafe_allow_html=True)


if __name__ == "__main__":
    main()
