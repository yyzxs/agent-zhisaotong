import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from networkx.algorithms.similarity import optimal_edit_paths

from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import pdf_loader, listdir_with_allowed_types, get_file_md5_hex, text_loader
from utils.logger_handle import logger


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf['collection_name'],
            embedding_function=embed_model,
            persist_directory=chroma_conf['persist_directory']
        )

        # 文本分割器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size= chroma_conf['chunk_size'],
            chunk_overlap= chroma_conf['chunk_overlap'],
            separators=chroma_conf['separators'],
            length_function=len,
        )

    def get_retrieve(self):
        return self.vector_store.as_retriever(search_kwargs = {'k':chroma_conf['k']})

    def load_document(self):
        """
        从数据文件夹中读取数据文件，转为向量存入向量库
        要计算md5文件做去重
        :return: None
        """

        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_conf['md5_hex_store'])):
                # 创建文件
                open(get_abs_path(chroma_conf['md5_hex_store']),'w',encoding='utf-8').close()
                return False
            with open(get_abs_path(chroma_conf['md5_hex_store']),'r',encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True

                return False

        def save_md5_hex(md5_for_check:str):

            with open(get_abs_path(chroma_conf['md5_hex_store']),'a',encoding='utf-8') as f:
                f.write(md5_for_check + '\n')


        def get_file_documents(read_path:str):
            if read_path.endswith('txt'):
                return text_loader(read_path)
            if read_path.endswith('pdf'):
                return pdf_loader(read_path)
            return []

        allowed_file_path = listdir_with_allowed_types(get_abs_path(chroma_conf['data_path'])
                                                       ,tuple(chroma_conf['allowed_files']))
        for path in allowed_file_path:
            # 获取文件的md5
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库] 内容已经存在知识库，跳过文件：{path}")
                continue
            try:
                documents:list[Document] = get_file_documents( path)
                if not documents:
                    logger.warning(f"[加载知识库] 文件内容为空，跳过文件：{path}")
                    continue
                split_document:list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库] 文件内容已经过分割，但分割后的内容为空，跳过文件：{path}")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 将记录这个已经处理好的文件md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库] 成功加载文件{path}")
            except Exception as e:
                logger.error(f"[加载知识库] 加载文件{path}失败：{str(e)}",exc_info=True)
                continue


if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()

    retrieve = vs.get_retrieve()
    res = retrieve.invoke("迷路")
    for r in res:
        print(r.page_content)
        print('-' * 20)

