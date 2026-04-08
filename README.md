# 🤖 智扫通机器人智能客服

基于 **RAG + ReAct Agent** 架构的扫地机器人垂直领域智能客服系统，集知识库问答、使用报告生成、多轮对话管理与流式思考可视化于一体。

---

## ✨ 主要功能

- 🤖 **RAG 知识库问答**：PDF / TXT 文档向量化入库，基于语义检索 + 大模型生成，精准回答扫地机器人专业问题
- 🧠 **ReAct Agent 多工具协同**：Agent 自主规划工具调用链路，支持知识库检索、天气查询、外部数据拉取、报告生成等多工具组合
- 📊 **个人使用报告生成**：结构化流程（用户 ID → 月份 → 上下文注入 → 外部数据拉取）自动生成月度使用分析报告
- 🔀 **动态提示词切换**：通过 `@dynamic_prompt` 中间件，根据运行时上下文自动在「客服模式」与「报告模式」之间无缝切换系统提示词
- 💬 **多会话管理**：支持新建 / 切换 / 删除会话，历史记录按今天 / 昨天 / 更早分组，本地 JSON 持久化
- 🔍 **流式思考可视化**：区分工具调用消息与最终回答，逐字打字机效果输出，思考过程展开显示，答案生成后自动折叠
- 🔧 **中间件监控**：统一拦截每次工具调用，记录调用参数、执行结果与异常，便于排查和追踪
- 📚 **文档 MD5 去重**：向量库加载时对文件做 MD5 校验，跳过已处理文档，节省重复向量化开销

---

## 🏗️ 系统架构

```
用户输入
   │
   ▼
┌──────────────────────────────────────────┐
│             Streamlit 前端                │
│   多会话管理 │ 流式打字输出 │ 思考过程展示  │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│          ReAct Agent（LangChain）         │
│                                          │
│  ┌──────────────┐   ┌─────────────────┐  │
│  │   中间件层    │   │  动态提示词切换  │  │
│  │ monitor_tool │   │ report_switch   │  │
│  │ before_model │   │ (客服/报告模式)  │  │
│  └──────────────┘   └─────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │              工具集                 │  │
│  │  rag_summarize   get_weather       │  │
│  │  get_user_id     get_location      │  │
│  │  fetch_external_data               │  │
│  │  fill_context_for_report           │  │
│  └────────────────────────────────────┘  │
└────────────┬─────────────────────────────┘
             │
      ┌──────┴───────┐
      ▼              ▼
┌──────────┐   ┌───────────────┐
│  Chroma  │   │  通义千问      │
│ 向量数据库│   │ Chat + 嵌入   │
└──────────┘   └───────────────┘
```

---

## 🛠️ 技术栈

| 模块 | 技术选型 |
|------|---------|
| 前端界面 | Streamlit |
| 大语言模型 | 通义千问 Qwen（DashScope API）|
| 嵌入模型 | DashScope text-embedding |
| 向量数据库 | Chroma（本地持久化）|
| Agent 框架 | LangChain Agent SDK |
| RAG 框架 | LangChain + PromptTemplate |
| 文档解析 | PyPDF / TXT Loader |
| 配置管理 | YAML |
| 日志 | 自定义 logger 模块 |
| 工具中间件 | wrap_tool_call / before_model / dynamic_prompt |

---

## 📁 项目结构

```
ai-agents/
├── app.py                      # Streamlit 主入口，UI 渲染与流式交互
├── agent/
│   ├── react_agent.py          # ReAct Agent 封装，流式执行（yield 事件类型）
│   └── tools/
│       ├── agent_tools.py      # 工具定义：RAG、天气、位置、外部数据、报告注入
│       └── middleware.py       # 中间件：工具监控、调用日志、动态提示词切换
├── rag/
│   ├── rag_service.py          # RAG 检索 + 生成服务（Chain 封装）
│   └── vector_store.py         # Chroma 向量库管理：文档加载、MD5 去重、分块
├── model/
│   └── factory.py              # 模型工厂（ChatTongyi + DashScopeEmbeddings）
├── utils/
│   ├── config_handler.py       # YAML 配置读取
│   ├── prompts_loader.py       # 系统提示词 / RAG 提示词 / 报告提示词加载
│   ├── history_manager.py      # 会话历史本地持久化（JSON）
│   ├── file_handler.py         # 文件 MD5、目录遍历、PDF/TXT 解析
│   ├── logger_handle.py        # 日志初始化
│   └── path_tool.py            # 项目绝对路径工具
├── config/                     # YAML 配置文件
│   ├── agent.yml               # Agent 配置（外部数据路径等）
│   ├── chroma.yml              # 向量库配置（collection、分块大小、检索 TopK）
│   ├── prompts.yml             # 提示词文件路径映射
│   └── rag.yml                 # 模型名称配置
├── prompts/                    # 提示词文本
│   ├── main_prompt.txt         # 客服系统主提示词
│   ├── rag_summarize.txt       # RAG 总结提示词
│   └── report_prompt.txt       # 报告生成提示词
├── data/
│   ├── history/                # 会话历史 JSON 文件
│   ├── knowledge_base/         # 知识库源文件（PDF / TXT）
│   └── records.csv             # 用户使用记录（外部数据，用于报告）
├── logs/                       # 运行日志
└── requirements.txt
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd ai-agents
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
# venv\Scripts\activate       # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

核心依赖：`langchain` · `langchain-community` · `langchain-chroma` · `streamlit` · `dashscope` · `chromadb` · `pypdf` · `pyyaml`

### 4. 配置 API 密钥

系统使用阿里云 DashScope（通义千问 + 嵌入模型），请设置环境变量：

```bash
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

### 5. 加载知识库

将知识文档（PDF 或 TXT）放入 `config/chroma.yml` 中 `data_path` 指定的目录，然后执行：

```bash
python rag/vector_store.py
```

> 系统会自动对文档进行 MD5 去重，已处理过的文件下次启动不会重复向量化。

### 6. 启动应用

```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501` 即可使用。

---

## 💬 使用说明

- **知识库问答**：直接提问，Agent 自动调用 RAG 工具检索知识库并生成回答
- **使用报告生成**：输入"生成我的使用报告"，系统自动识别场景、切换报告提示词、拉取外部使用数据并生成分析报告
- **思考过程查看**：回答时展开显示 Agent 工具调用链路，最终答案输出后自动折叠为「💭 查看思考过程」
- **多会话**：左侧侧边栏支持新建 / 切换 / 删除对话，历史按今天 / 昨天 / 更早分组

---

## 📌 设计亮点

**动态提示词中间件**：通过 `@dynamic_prompt` 装饰器，在每次模型推理前根据运行时 `context["report"]` 标志动态注入不同系统提示词，实现无侵入式多场景提示词管理，无需修改 Agent 主逻辑。

**工具触发上下文注入**：`fill_context_for_report` 工具调用后，中间件自动将 `context["report"]` 置为 `True`，触发后续推理自动切换到报告生成模式，Agent 的意图识别与模式切换完全解耦。

**MD5 文档去重**：向量库加载时对每个文件计算 MD5 并持久化记录，重启后自动跳过已处理文件，大幅降低重复 API 调用成本。

**流式思考可视化**：在 `execute_stream` 中区分消息类型（`ai` with tool_calls / `tool` / final `ai`），分层渲染思考过程与最终回答，配合逐字输出实现自然的打字机交互体验。

---

## 📝 扩展指南

- **添加新工具**：在 `agent/tools/agent_tools.py` 中用 `@tool` 装饰器定义函数，并将其加入 `ReactAgent` 的 `tools` 列表
- **修改提示词**：直接编辑 `prompts/` 目录下的 `.txt` 文件，每次请求时动态加载，无需重启
- **更换大模型**：修改 `model/factory.py` 的工厂类及 `config/rag.yml` 中的模型名称
- **调整向量库参数**：修改 `config/chroma.yml` 中的 `chunk_size`、`chunk_overlap`、`k` 等参数，重新运行 `vector_store.py`

---

## 📄 许可证

本项目仅供学习与交流，未经许可不得用于商业用途。