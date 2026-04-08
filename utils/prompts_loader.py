from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handle import logger

def load_system_prompt():
    """
    加载系统提示语

    :return: 提示语
    """
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompt()] 配置文件缺少，main_prompt_path 字段：{str(e)}")
        raise e

    try:
        with open(system_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_system_prompt()] 配置文件main_prompt_path 字段配置错误：{str(e)}")
        raise e


def load_rag_prompt():
    """
    加载RAG提示语

    :return: 提示语
    """
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompt()] 配置文件缺少，rag_summarize_prompt_path 字段：{str(e)}")
        raise e

    try:
        with open(rag_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_rag_prompt()] 配置文件rag_summarize_prompt_path 字段配置错误：{str(e)}")
        raise e


def load_report_prompt():
    """
    加载报告提示语

    :return: 提示语
    """
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompt()] 配置文件缺少，report_prompt_path 字段：{str(e)}")
        raise e

    try:
        with open(report_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_report_prompt()] 配置文件report_prompt_path 字段配置错误：{str(e)}")
        raise e

if __name__ == '__main__':
    # print(load_system_prompt())
    # print(load_rag_prompt())
    print(load_report_prompt())