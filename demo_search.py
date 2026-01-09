#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
家庭法AI代理 - 轻量级演示
使用基础关键词匹配（无需额外依赖）
"""

import json
import re
from typing import List, Dict

class SimpleLegalSearch:
    def __init__(self, chunks_path: str):
        """初始化搜索系统"""
        print("📖 加载知识库...")
        with open(chunks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.chunks = data['chunks']
        print(f"✅ 已加载 {len(self.chunks)} 个文本块\n")
        
    def simple_search(self, query: str, n: int = 5) -> List[Dict]:
        """简单的关键词+相关性搜索"""
        
        # 提取查询关键词
        keywords = set(re.findall(r'\w+', query.lower()))
        
        # 计算每个chunk的相关性得分
        scored_chunks = []
        for chunk in self.chunks:
            text_lower = chunk['text'].lower()
            chapter_lower = chunk.get('chapter', '').lower()
            
            # 计算匹配得分
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                if len(keyword) < 3:  # 忽略太短的词
                    continue
                    
                # 在文本中查找
                text_matches = text_lower.count(keyword)
                chapter_matches = chapter_lower.count(keyword)
                
                if text_matches > 0:
                    score += text_matches * 2  # 文本匹配权重更高
                    matched_keywords.append(keyword)
                
                if chapter_matches > 0:
                    score += chapter_matches * 3  # 章节匹配权重最高
                    if keyword not in matched_keywords:
                        matched_keywords.append(keyword)
            
            if score > 0:
                scored_chunks.append({
                    'chunk': chunk,
                    'score': score,
                    'matched_keywords': matched_keywords
                })
        
        # 按得分排序
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_chunks[:n]
    
    def display_results(self, results: List[Dict], query: str):
        """显示搜索结果"""
        if not results:
            print("❌ 未找到相关内容")
            print("💡 建议:")
            print("   - 使用更通用的关键词（如 divorce, property, child）")
            print("   - 尝试英文查询以获得更好的结果")
            return
        
        print(f"\n🔍 搜索: '{query}'")
        print(f"✅ 找到 {len(results)} 个相关结果\n")
        print("="*80)
        
        for i, result in enumerate(results, 1):
            chunk = result['chunk']
            score = result['score']
            keywords = result['matched_keywords']
            
            print(f"\n【结果 #{i}】 相关度得分: {score}")
            print(f"📄 页码: {chunk['page_number']}")
            print(f"📚 章节: {chunk.get('chapter', 'N/A')[:70]}...")
            print(f"🏷️  类型: {chunk['content_type']}")
            print(f"🔑 匹配关键词: {', '.join(keywords)}")
            print(f"\n📝 内容预览:")
            
            # 高亮显示关键词
            preview = chunk['text'][:400]
            for kw in keywords:
                pattern = re.compile(re.escape(kw), re.IGNORECASE)
                preview = pattern.sub(f"**{kw.upper()}**", preview)
            
            print(f"{preview}...")
            print("\n" + "-"*80)

def main():
    print("="*80)
    print("🏛️  澳大利亚家庭法智能检索系统 - 演示版")
    print("   (基于关键词匹配，无需额外依赖)")
    print("="*80)
    print()
    
    # 初始化搜索系统
    searcher = SimpleLegalSearch('/home/claude/family_law_chunks.json')
    
    # 预设测试问题
    test_queries = {
        '1': 'divorce requirements separation',
        '2': 'property settlement division assets',
        '3': 'child custody parenting arrangements',
        '4': 'spousal maintenance financial support',
        '5': 'family violence protection order',
        '6': 'application form affidavit',
        '7': 'court procedure hearing trial',
        '8': 'de facto relationship',
    }
    
    print("📋 预设测试问题（输入数字快速测试）:")
    print("  1. Divorce requirements")
    print("  2. Property settlement")
    print("  3. Child custody")
    print("  4. Spousal maintenance")
    print("  5. Family violence protection")
    print("  6. Application forms")
    print("  7. Court procedures")
    print("  8. De facto relationships")
    print()
    print("💬 或直接输入你的问题（输入 'quit' 退出）")
    print("   建议使用英文关键词以获得最佳结果\n")
    
    while True:
        try:
            print("="*80)
            user_input = input("\n❓ 你的问题（或输入数字1-8）: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n👋 再见！")
                break
            
            # 检查是否是预设问题
            if user_input in test_queries:
                query = test_queries[user_input]
                print(f"📌 使用预设: {query}")
            else:
                query = user_input
            
            # 执行搜索
            results = searcher.simple_search(query, n=3)
            searcher.display_results(results, query)
            
            print("\n💡 提示: 基于检索结果，如需详细解答请:")
            print("   1. 查阅完整的PDF文档相关页码")
            print("   2. 咨询专业家庭法律师")
            print("   3. 使用完整版AI代理（需要Claude API）获得智能解答")
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            continue

if __name__ == "__main__":
    main()
