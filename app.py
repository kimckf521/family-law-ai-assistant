#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Australian Family Law AI Assistant - Bilingual Streamlit Web Interface
澳大利亚家庭法AI助手 - 双语Streamlit Web界面
"""

import streamlit as st
import json
import re
import os
from datetime import datetime
from typing import List, Dict

# Language detection and configuration
# 语言检测和配置
LANGUAGES = {
    'en': {
        'name': 'English',
        'flag': '🇬🇧',
        'page_title': 'Australian Family Law AI Assistant',
        'page_icon': '⚖️',
        'title': '⚖️ Australian Family Law AI Assistant',
        'subtitle': 'Instant access to 666 pages of Australian Family Law',
        'search_placeholder': 'Ask about divorce, property, custody, maintenance...',
        'search_button': '🔍 Search',
        'example_questions': 'Example Questions',
        'results_title': 'Search Results',
        'no_results': 'No relevant results found. Try different keywords.',
        'page_label': 'Page',
        'relevance_label': 'Relevance',
        'category_label': 'Category',
        'search_history': 'Recent Searches',
        'clear_history': 'Clear History',
        'about': 'About',
        'about_text': '''
This AI assistant helps you quickly find relevant information from **The Family Law Book** 
(666 pages). It uses advanced search to match your questions with the most relevant legal content.

**Features:**
- 🔍 Smart keyword search
- 📄 Exact page references
- 🏷️ Categorized by topic
- 📊 1,042 searchable chunks

**Disclaimer:** This provides legal information, not legal advice. 
Always consult a qualified lawyer for specific legal matters.
        ''',
        'examples': [
            "What are the requirements for divorce?",
            "How is property divided in separation?",
            "What factors affect child custody decisions?",
            "How is child support calculated?",
            "What is a de facto relationship?",
            "What are parenting orders?",
            "How does spousal maintenance work?",
            "What is the Family Court process?",
            "What are consent orders?",
            "What happens to superannuation in divorce?",
            "What is a binding financial agreement?",
            "How long does divorce take?",
            "What is shared parental responsibility?"
        ],
        'stats_title': 'Knowledge Base Statistics',
        'stats_chunks': 'Text Chunks',
        'stats_pages': 'Pages',
        'stats_words': 'Words',
        'stats_categories': 'Categories',
        'loading': '🔄 Loading knowledge base...',
        'searching': '🔍 Searching...',
        'footer': 'Built with ❤️ for the legal community | Powered by Streamlit',
    },
    'zh': {
        'name': '中文',
        'flag': '🇨🇳',
        'page_title': '澳大利亚家庭法AI助手',
        'page_icon': '⚖️',
        'title': '⚖️ 澳大利亚家庭法AI助手',
        'subtitle': '即时访问666页澳大利亚家庭法内容',
        'search_placeholder': '询问离婚、财产、抚养、赡养费等问题...',
        'search_button': '🔍 搜索',
        'example_questions': '示例问题',
        'results_title': '搜索结果',
        'no_results': '未找到相关结果。请尝试不同的关键词。',
        'page_label': '页码',
        'relevance_label': '相关度',
        'category_label': '类别',
        'search_history': '最近搜索',
        'clear_history': '清空历史',
        'about': '关于',
        'about_text': '''
这个AI助手帮助你快速从《家庭法手册》（666页）中找到相关信息。
它使用先进的搜索技术将你的问题与最相关的法律内容匹配。

**功能特点：**
- 🔍 智能关键词搜索
- 📄 精确页码引用
- 🏷️ 按主题分类
- 📊 1,042个可搜索文本块

**免责声明：** 本系统提供法律信息，不是法律建议。
具体法律问题请咨询专业律师。
        ''',
        'examples': [
            "离婚需要什么条件？",
            "分居时财产如何分割？",
            "哪些因素影响子女抚养权决定？",
            "子女抚养费如何计算？",
            "什么是事实婚姻关系？",
            "什么是育儿令？",
            "配偶赡养费如何运作？",
            "家庭法院的流程是什么？",
            "什么是同意令？",
            "离婚时退休金怎么处理？",
            "什么是有约束力的财务协议？",
            "离婚需要多长时间？",
            "什么是共同父母责任？"
        ],
        'stats_title': '知识库统计',
        'stats_chunks': '文本块',
        'stats_pages': '页数',
        'stats_words': '字数',
        'stats_categories': '类别',
        'loading': '🔄 正在加载知识库...',
        'searching': '🔍 搜索中...',
        'footer': '为法律社区用❤️构建 | 由Streamlit驱动',
    }
}

# Page configuration
st.set_page_config(
    page_title="Family Law AI Assistant | 家庭法AI助手",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        color: #1a1a1a;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
        color: #0d47a1;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 5px solid #4CAF50;
        color: #212121;
    }
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #212121;
    }
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e0e0e0;
    }
    .result-content {
        color: #212121;
        line-height: 1.6;
        margin: 1rem 0;
        font-weight: 400;
    }
    .result-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        font-size: 0.9rem;
        color: #424242;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .example-btn {
        margin: 0.25rem;
    }
    .language-switcher {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


class FamilyLawSearchEngine:
    """Family Law Search Engine | 家庭法搜索引擎"""
    
    def __init__(self, chunks_path: str):
        self.chunks = self._load_chunks(chunks_path)
        self.search_history = []
        
    @st.cache_data
    def _load_chunks(_self, path: str):
        """Load knowledge base (cached) | 加载知识库（使用缓存）"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['chunks']
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Execute search | 执行搜索"""
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


def init_session_state():
    """Initialize session state | 初始化session state"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'search_engine' not in st.session_state:
        with st.spinner(LANGUAGES[st.session_state.language]['loading']):
            # Use relative path for Streamlit Cloud compatibility
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            chunks_path = os.path.join(current_dir, 'family_law_chunks.json')
            st.session_state.search_engine = FamilyLawSearchEngine(chunks_path)
    if 'search_count' not in st.session_state:
        st.session_state.search_count = 0


def detect_language(text: str) -> str:
    """Detect if text contains Chinese characters | 检测文本是否包含中文字符"""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return 'zh' if len(chinese_chars) > len(text) * 0.3 else 'en'


def display_result_card(result: Dict, index: int, lang_data: dict):
    """Display result card | 显示结果卡片"""
    chunk = result['chunk']
    score = result['score']
    
    with st.container():
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 📄 {lang_data['results_title']} #{index + 1}")
        with col2:
            st.markdown(f"**{lang_data['relevance_label']}:** {score}")
        
        # Content
        st.markdown(f'<div class="result-content">{chunk["text"]}</div>', unsafe_allow_html=True)
        
        # Metadata
        meta_parts = []
        if 'page' in chunk:
            meta_parts.append(f"📄 {lang_data['page_label']}: {chunk['page']}")
        if 'category' in chunk:
            meta_parts.append(f"🏷️ {lang_data['category_label']}: {chunk['category']}")
        
        if meta_parts:
            st.markdown(f'<div class="result-meta">{" | ".join(meta_parts)}</div>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    init_session_state()
    
    lang_data = LANGUAGES[st.session_state.language]
    
    # Language switcher in sidebar
    with st.sidebar:
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
        
        # About section
        with st.expander(lang_data['about'], expanded=False):
            st.markdown(lang_data['about_text'])
        
        # Statistics
        st.markdown(f"### 📊 {lang_data['stats_title']}")
        
        stats_data = {
            lang_data['stats_chunks']: "1,042",
            lang_data['stats_pages']: "666",
            lang_data['stats_words']: "295,140",
            lang_data['stats_categories']: "8"
        }
        
        for label, value in stats_data.items():
            st.metric(label, value)
        
        # Search history
        if st.session_state.messages:
            st.markdown("---")
            st.markdown(f"### {lang_data['search_history']}")
            if st.button(lang_data['clear_history'], use_container_width=True):
                st.session_state.messages = []
                st.session_state.search_count = 0
                st.rerun()
            
            for msg in reversed(st.session_state.messages[-5:]):
                if msg['role'] == 'user':
                    st.markdown(f"🔍 {msg['content'][:50]}...")
    
    # Main content
    st.title(lang_data['title'])
    st.markdown(f"*{lang_data['subtitle']}*")
    st.markdown("---")
    
    # Example questions
    with st.expander(f"💡 {lang_data['example_questions']}", expanded=False):
        cols = st.columns(3)
        for idx, example in enumerate(lang_data['examples']):
            with cols[idx % 3]:
                if st.button(example, key=f"example_{idx}", use_container_width=True):
                    st.session_state.messages.append({
                        'role': 'user',
                        'content': example
                    })
                    st.rerun()
    
    # Search input
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "search_input",
            placeholder=lang_data['search_placeholder'],
            label_visibility="collapsed",
            key="search_query"
        )
    with col2:
        search_button = st.button(lang_data['search_button'], use_container_width=True, type="primary")
    
    # Process search
    if search_button and query:
        # Auto-detect language and switch if needed
        detected_lang = detect_language(query)
        if detected_lang != st.session_state.language:
            st.session_state.language = detected_lang
            lang_data = LANGUAGES[detected_lang]
        
        st.session_state.messages.append({
            'role': 'user',
            'content': query
        })
        st.session_state.search_count += 1
        
        with st.spinner(lang_data['searching']):
            results = st.session_state.search_engine.search(query, n_results=5)
        
        if results:
            st.markdown(f"## {lang_data['results_title']}")
            for idx, result in enumerate(results):
                display_result_card(result, idx, lang_data)
        else:
            st.warning(lang_data['no_results'])
    
    # Display search history
    if st.session_state.messages:
        st.markdown("---")
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message">🔍 {msg["content"]}</div>', 
                          unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #666;'>{lang_data['footer']}</div>", 
               unsafe_allow_html=True)


if __name__ == "__main__":
    main()
