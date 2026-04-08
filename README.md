# 智扫通机器人智能客服

智扫通是一个基于 LangChain + ReAct Agent 的扫地机器人智能客服系统。它通过检索增强生成（RAG）和多种工具调用能力，为用户提供专业、实时的扫地/扫拖一体机器人咨询、故障排除、选购建议、使用报告生成等服务。系统包含完整的对话管理、知识库向量化、流式交互界面，支持多会话、历史记录持久化。

## ✨ 主要功能

- 🤖 **智能问答**：基于 RAG 检索专业知识库，结合大语言模型生成准确、自然的回答。
- 🧠 **ReAct Agent 架构**：自主思考、调用工具（搜索知识库、获取天气/位置/用户ID/月份、拉取外部使用记录、报告上下文注入等）。
- 📊 **个人使用报告生成**：按固定流程（用户ID → 月份 → 上下文注入 → 获取外部数据）生成月度扫地机器人使用报告。
- 💬 **多会话管理**：支持新建对话、历史会话列表（今天/昨天/更早），自动保存聊天记录。
- 🖥️ **Streamlit Web 界面**：清爽的聊天 UI，流式输出思考过程和最终答案，支持快捷问题建议。
- 📚 **知识库自动加载**：支持 PDF、TXT 文档，自动计算 MD5 去重，分块存入 Chroma 向量库。
- 🔧 **可扩展工具集**：内置天气、位置、用户 ID、当前月份、外部数据获取等工具，并可通过中间件监控、动态切换提示词。

## 🛠️ 技术栈

- **语言 & 环境**：Python 3.10+
- **AI 框架**：LangChain、LangGraph、LangChain Community
- **大模型**：通义千问（DashScope）
- **向量数据库**：Chroma（本地持久化）
- **嵌入模型**：DashScopeEmbeddings
- **前端**：Streamlit
- **配置管理**：YAML
- **日志**：自定义 logger 模块
- **工具中间件**：wrap_tool_call、before_model、dynamic_prompt

## 📁 项目结构
```text
ai-agents/
├── agent/
│ ├── react_agent.py # ReAct Agent 主类，流式执行
│ └── tools/
│ ├── agent_tools.py # 所有工具定义（RAG、天气、位置、ID、月份、外部数据等）
│ └── middleware.py # 工具监控、模型前日志、动态提示词切换
├── rag/
│ ├── vector_store.py # Chroma 向量库管理，文档加载与分块
│ └── rag_service.py # RAG 服务（检索 + 生成总结）
├── model/
│ └── factory.py # 模型工厂（ChatTongyi + DashScopeEmbeddings）
├── utils/
│ ├── config_handler.py # 加载 YAML 配置（agent、chroma、prompts、rag）
│ ├── logger_handle.py # 日志初始化
│ ├── path_tool.py # 获取项目根目录、绝对路径
│ ├── prompts_loader.py # 加载 system / rag / report 提示词
│ ├── file_handler.py # 文件 MD5、目录列表、PDF/TXT 加载
│ └── history_manager.py # 会话历史 JSON 存储
├── config/ # 配置文件目录
│ ├── agent.yml # Agent 相关配置（如 external_data_path）
│ ├── chroma.yml # 向量库配置（collection、路径、分块参数等）
│ ├── prompts.yml # 提示词文件路径配置
│ └── rag.yml # RAG 模型名称配置
├── prompts/ # 提示词文本文件
│ ├── main_prompt.txt # 系统主提示（ReAct 思考准则）
│ ├── rag_summarize.txt # RAG 总结提示
│ └── report_prompt.txt # 报告生成提示
├── data/ # 数据目录
│ ├── history/ # 会话历史 JSON 文件
│ ├── knowledge_base/ # 知识库源文件（PDF/TXT）
│ └── records.csv # 外部用户使用记录（用于报告）
├── logs/ # 日志文件
├── app.py # Streamlit 前端主程序
└── README.md # 本文件
```

## 🚀 安装与配置

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd ai-agents
```
### 2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
# 或 venv\Scripts\activate   # Windows

```
### 3.安装依赖
```bash
pip install -r requirements.txt
```
主要依赖包参考：

- `langchain`, `langchain-community`, `langchain-chroma`

- `streamlit`,`dashscope（阿里云百炼）`

- `pypdf`, `pyyaml`

- `chromadb`

### 4. 配置 API 密钥
系统使用阿里云 DashScope（通义千问 + 嵌入模型）。请设置环境变量：
```bash
export DASHSCOPE_API_KEY="your-api-key"
```
或在启动前配置到 `~/.bashrc`。


## 🧪 使用方式
### 命令行测试 Agent
```bash
python agent/react_agent.py
```
### 启动 Web 界面
```bash
streamlit run app.py
```
## 📝 自定义与扩展
- 添加新工具：在 `agent/tools/agent_tools.py` 中定义函数，使用 @tool 装饰器，并加入 ReactAgent 的 tools 列表。

- 修改提示词：编辑 `prompts/` 下的 .txt 文件，无需重启（动态加载）。

- 更换大模型：修改 `model/factory.py` 中的 ChatModelFactory 和 EmbeddingModelFactory，以及 config/rag.yml 中的模型名称。

- 调整向量库参数：修改 `config/chroma.yml`，重新运行 `vector_store.py`。


## 📄 许可证
本项目仅供学习交流使用，未经许可不得用于商业用途。

## 🤝 贡献
欢迎提交 Issue 或 Pull Request。