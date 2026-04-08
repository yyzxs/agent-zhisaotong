"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from sympy import print_rcode

from model.factory import chat_model
from rag.vector_store import VectorStoreService
from utils.prompts_loader import load_rag_prompt

def print_prompt(prompt):
    print("=" * 20 )
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagSummarizeService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retrieve()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self.__init__chain()

    def __init__chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain
    def retriever_docs(self,query:str)->list[Document]:
        """
        根据query搜索参考资料
        :param query:
        :return:
        """
        docs = self.retriever.invoke(query)
        return docs

    def rag_summarize(self,query:str)->str:
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"[参考资料{counter}:参考资料{doc.page_content}] | 参考原数据：{doc.metadata}\n"
        return self.chain.invoke(
            {
                "input" : query,
                "context" : context
            }
        )

if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize("小户型适合哪些扫地机器人？"))
