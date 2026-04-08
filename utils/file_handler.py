import os
import hashlib

from gitdb.fun import chunk_size

from utils.logger_handle import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader

def get_file_md5_hex(file_path:str):
    """
    获取文件的md5值

    :param file_path: 文件路径
    :return: md5值
    """
    if not os.path.exists(file_path):
        logger.error(f"[get_file_md5_hex()] 文件不存在：{file_path}")
        return None

    if not os.path.isfile(file_path):
        logger.error(f"[get_file_md5_hex()] 不是文件：{file_path}")
        return None
    md5_obj = hashlib.md5()

    chunk_size = 4096

    try:
        with open(file_path, "rb") as f: # 必须二进制读取
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
                """
                chunk = f.read(chunk_size)
                while chunk:
                    md5_obj.update(chunk)
                    chunk = f.read(chunk_size)
                """
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[get_file_md5_hex()] 获取文件md5值失败：{file_path}")
        return None


def listdir_with_allowed_types(path: str, allowed_types: tuple[str,...]): # 返回文件夹的文件列表
    """
    列出指定目录下的所有文件，并筛选出指定类型的文件

    :param path: 目录路径
    :param allowed_types: 允许的文件类型列表
    :return: 筛选后的文件列表
    """
    files = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_types()] 路径不是目录：{path}")
        return ()
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))
    return tuple(files)

def pdf_loader(file_path:str,passwd = None):
    return PyPDFLoader(file_path,passwd).load()

def text_loader(file_path:str):
    return TextLoader(file_path).load()

