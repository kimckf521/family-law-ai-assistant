#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
澳大利亚家庭法AI代理 - 快速原型
使用Chroma向量数据库 + Claude API
"""

import json
import os
from typing import List, Dict
import anthropic

print("📦 安装依赖包...")
os.system("pip install chromadb sentence-transformers anthropic --break-system-packages -q")

import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

class FamilyLawAgent:
    def __init__(self, chunks_path: str, db_path: str = "./family_law_db"):
        """初始化家庭法AI代理"""
        self.chunks_path = chunks_path
        self.db_path = db_path
        self.chunks = None
        self.collection = None
        self.model = None
        self.claude_client = None
        
        print("\n🚀 初始化家庭法AI代理...")
        
    def load_chunks(self):
        """加载文本块数据"""
        print("📖 加载知识库...")
        with open(self.chunks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.chunks = data['chunks']
        print(f"✅ 已加载 {len(self.chunks)} 个文本块")
        
    def initialize_embedding_model(self):
        """初始化嵌入模型"""
        print("\n🤖 加载嵌入模型 (首次运行会下载模型，请稍候)...")
        # 使用轻量级但效果好的模型
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ 嵌入模型加载完成")
        
    def create_vector_database(self):
        """创建向量数据库"""
        print("\n💾 创建Chroma向量数据库...")
        
        # 初始化Chroma客户端
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # 删除旧集合（如果存在）
        try:
            self.client.delete_collection("family_law")
            print("  ⚠️  删除旧数据库")
        except:
            pass
        
        # 创建新集合
        self.collection = self.client.create_collection(
            name="family_law",
            metadata={"description": "Australian Family Law Knowledge Base"}
        )
        
        print("  ✓ 数据库创建成功")
        
    def index_documents(self, batch_size: int = 100):
        """索引所有文档到向量数据库"""
        print(f"\n📊 开始索引文档 (共 {len(self.chunks)} 个文本块)...")
        
        total_chunks = len(self.chunks)
        
        for i in range(0, total_chunks, batch_size):
            batch = self.chunks[i:i+batch_size]
            batch_end = min(i+batch_size, total_chunks)
            
            # 准备批次数据
            ids = [chunk['chunk_id'] for chunk in batch]
            documents = [chunk['text'] for chunk in batch]
            metadatas = [{
                'page': chunk['page_number'],
                'chapter': chunk.get('chapter', 'N/A')[:200],  # 限制长度
                'content_type': chunk['content_type'],
                'word_count': chunk['metadata']['word_count']
            } for chunk in batch]
            
            # 生成嵌入并添加到数据库
            embeddings = self.model.encode(documents, show_progress_bar=False)
            
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings.tolist()
            )
            
            print(f"  ✓ 已索引 {batch_end}/{total_chunks} 个文本块 ({batch_end*100//total_chunks}%)")
        
        print("✅ 索引完成!")
        
    def setup_claude(self, api_key: str = None):
        """设置Claude API"""
        print("\n🔑 配置Claude API...")
        
        if api_key is None:
            # 尝试从环境变量获取
            api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        if api_key:
            self.claude_client = anthropic.Anthropic(api_key=api_key)
            print("✅ Claude API配置成功")
        else:
            print("⚠️  未找到API密钥，将只使用检索功能")
            print("   提示: 设置环境变量 ANTHROPIC_API_KEY 或在代码中提供")
        
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """检索相关法律内容"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # 格式化结果
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def ask(self, question: str, n_results: int = 5) -> str:
        """向AI代理提问"""
        
        # 1. 检索相关内容
        print(f"\n🔍 检索相关法律内容...")
        search_results = self.search(question, n_results)
        
        print(f"✓ 找到 {len(search_results)} 个相关段落")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. 页码 {result['metadata']['page']} | 相关度: {1-result['distance']:.2f}")
        
        # 2. 构建上下文
        context = "\n\n---\n\n".join([
            f"[来源: 页码 {r['metadata']['page']}, 章节: {r['metadata']['chapter'][:60]}]\n{r['text']}"
            for r in search_results
        ])
        
        # 3. 如果没有Claude API，只返回检索结果
        if not self.claude_client:
            print("\n⚠️  未配置Claude API，返回原始检索结果:")
            return context
        
        # 4. 调用Claude生成回答
        print("\n🤔 Claude正在分析...")
        
        system_prompt = f"""你是澳大利亚家庭法专家AI助手，基于《The Family Law Book》为用户提供帮助。

【重要规则】
1. 必须引用具体页码（格式: [页码X]）
2. 区分"法律信息"和"法律建议" - 你提供的是信息，不是建议
3. 使用通俗易懂的中英文双语（根据用户语言调整）
4. 强调：这不能替代专业律师咨询

【回答策略】
- 对律师用户：提供精确法条、判例引用、法律论证要点
- 对公众用户：简化解释、提供流程指引、建议何时需要律师

【相关法律内容】
{context}

如果用户问题超出提供的内容范围，请诚实说明，并建议查阅完整的家庭法手册或咨询律师。
"""

        try:
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                temperature=0.3,  # 降低温度使回答更准确
                system=system_prompt,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            answer = message.content[0].text
            print("✅ 回答生成完成\n")
            return answer
            
        except Exception as e:
            print(f"❌ Claude API调用失败: {e}")
            return f"检索到的相关内容:\n\n{context}"
    
    def setup(self):
        """完整设置流程"""
        self.load_chunks()
        self.initialize_embedding_model()
        self.create_vector_database()
        self.index_documents()
        self.setup_claude()
        
        print("\n" + "="*80)
        print("🎉 家庭法AI代理设置完成！")
        print("="*80)

def main():
    """主函数"""
    print("="*80)
    print("🏛️  澳大利亚家庭法AI代理 - 快速原型")
    print("="*80)
    
    # 初始化代理
    agent = FamilyLawAgent(
        chunks_path="/home/claude/family_law_chunks.json",
        db_path="/home/claude/family_law_db"
    )
    
    # 设置系统
    agent.setup()
    
    # 交互式命令行界面
    print("\n💬 进入交互模式（输入 'quit' 或 'exit' 退出）")
    print("   示例问题:")
    print("   - What are the grounds for divorce in Australia?")
    print("   - 离婚需要什么条件?")
    print("   - How is property divided in a divorce?")
    print("   - 如何申请子女抚养权?\n")
    
    while True:
        try:
            print("-" * 80)
            question = input("\n❓ 你的问题: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n👋 再见！")
                break
            
            # 获取回答
            answer = agent.ask(question)
            print("\n💡 回答:")
            print(answer)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            continue

if __name__ == "__main__":
    main()
