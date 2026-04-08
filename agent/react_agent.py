from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompts_loader import load_system_prompt
from agent.tools.agent_tools import (rag_summarize,get_weather,get_user_location,get_user_id,
                                     get_current_month,fetch_external_data,fill_context_for_report)
from agent.tools.middleware import monitor_tool,log_before_model,report_prompt_switch



class ReactAgent:

    def __init__(self):
        self.agent = create_agent(
            model= chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize,get_weather,get_user_location,get_user_id,
                   get_current_month,fetch_external_data,fill_context_for_report],
            middleware=[monitor_tool,log_before_model,report_prompt_switch],
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk['messages'][-1]
            msg_type = getattr(latest_message, 'type', '')

            if msg_type == 'tool':
                # 工具返回结果 → 属于思考过程
                if latest_message.content:
                    yield ("thinking", f"📋 **工具返回：**\n```\n{latest_message.content.strip()}\n```\n\n")

            elif msg_type == 'ai':
                tool_calls = getattr(latest_message, 'tool_calls', None)
                if tool_calls:
                    # 正在调用工具 → 属于思考过程
                    for tc in tool_calls:
                        yield ("thinking", f"🔧 **调用工具 `{tc['name']}`：**\n```json\n{tc['args']}\n```\n\n")
                elif latest_message.content:
                    # 最终回答
                    yield ("answer", latest_message.content.strip() + "\n")

if __name__ == '__main__':
    agent = ReactAgent()

    for chunk in  agent.execute_stream("给我生成我的使用报告"):
       print(chunk,end="",flush=True)

