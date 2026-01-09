#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
家庭法AI代理 - 简单测试（无需API密钥）
仅使用向量检索功能
"""

import json
import os
import sys

# 添加主脚本路径
sys.path.insert(0, '/home/claude')

print("📦 安装依赖...")
os.system("pip install chromadb sentence-transformers --break-system-packages -q")

import chromadb
from sentence_transformers import SentenceTransformer

class SimpleFamilyLawSearch:
    def __init__(self):
        self.chunks = None
        self.collection = None
        self.model = None
        
    def load_data(self):
        """加载数据"""
        print("\n📖 加载知识库...")
        with open('/home/claude/family_law_chunks.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.chunks = data['chunks']
        print(f"✅ 已加载 {len(self.chunks)} 个文本块")
        
    def load_model(self):
        """加载嵌入模型"""
        print("\n🤖 加载嵌入模型...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ 模型加载完成")
        
    def create_database(self):
        """创建向量数据库"""
        print("\n💾 创建向量数据库...")
        
        self.client = chromadb.PersistentClient(path="/home/claude/family_law_db_test")
        
        try:
            self.collection = self.client.get_collection("family_law")
            print("✅ 找到现有数据库")
            return
        except:
            pass
        
        print("  创建新数据库并索引文档...")
        self.collection = self.client.create_collection(name="family_law")
        
        # 分批索引
        batch_size = 100
        for i in range(0, len(self.chunks), batch_size):
            batch = self.chunks[i:i+batch_size]
            
            ids = [c['chunk_id'] for c in batch]
            docs = [c['text'] for c in batch]
            metas = [{
                'page': c['page_number'],
                'chapter': c.get('chapter', '')[:200],
                'type': c['content_type']
            } for c in batch]
            
            embeddings = self.model.encode(docs, show_progress_bar=False)
            
            self.collection.add(
                ids=ids,
                documents=docs,
                metadatas=metas,
                embeddings=embeddings.tolist()
            )
            
            print(f"  ✓ {min(i+batch_size, len(self.chunks))}/{len(self.chunks)}")
        
        print("✅ 索引完成")
        
    def search(self, query: str, n: int = 5):
        """搜索相关内容"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n
        )
        
        print(f"\n🔍 找到 {len(results['documents'][0])} 个相关结果:\n")
        
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            distance = results['distances'][0][i] if 'distances' in results else 0
            
            print("="*80)
            print(f"【结果 #{i+1}】相关度: {(1-distance)*100:.1f}%")
            print(f"页码: {meta['page']} | 类型: {meta['type']}")
            print(f"章节: {meta['chapter'][:70]}...")
            print(f"\n{doc[:500]}...")
            print()

def main():
    print("="*80)
    print("🏛️  家庭法AI检索系统 - 测试版")
    print("   (不需要API密钥，仅语义搜索)")
    print("="*80)
    
    searcher = SimpleFamilyLawSearch()
    searcher.load_data()
    searcher.load_model()
    searcher.create_database()
    
    print("\n" + "="*80)
    print("✅ 系统就绪！")
    print("="*80)
    
    # 预设测试问题
    test_queries = [
        "What are the requirements for divorce in Australia?",
        "How is property divided in divorce?",
        "Child custody arrangements",
        "离婚财产分割",
        "子女抚养权"
    ]
    
    print("\n📋 预设测试问题:")
    for i, q in enumerate(test_queries, 1):
        print(f"  {i}. {q}")
    
    print("\n💬 输入问题进行搜索 (输入 'quit' 退出)")
    print("   或输入数字 1-5 测试预设问题\n")
    
    while True:
        try:
            user_input = input("❓ 你的问题: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            # 检查是否是数字选择
            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(test_queries):
                    query = test_queries[idx]
                    print(f"\n使用预设问题: {query}")
                else:
                    print("❌ 无效的选项")
                    continue
            else:
                query = user_input
            
            searcher.search(query, n=3)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
