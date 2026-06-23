# MedRes 医药研究智能体

本仓库提供一个可在 Codex 中长期使用的医药分析智能体工作流包。它由两部分组成：

- `pharma-research-agent`：Codex Skill，负责问题收窄、多角色分工、按需加载临床或早期项目参考模块、证据质量判断和 Markdown 报告生成。
- `pharma_research` MCP server：为智能体提供真实数据查询工具，覆盖文献、临床试验、药品标签、不良事件和专利检索。

适用场景包括靶点竞争格局、药物临床证据比较、安全性信号分析、早期药物项目第三方尽调、非临床证据评估、管线和专利初筛等内部研究任务。

## 仓库结构

```text
.
├── .agents/skills/pharma-research-agent/  # Codex 可发现的医药研究 Skill
├── .codex/config.example.toml             # Codex MCP 配置示例
├── docs/                                  # 方案、部署记录和使用说明
├── mcp-server/                            # MCP server 启动入口和接口说明
├── mcp_server/                            # MCP 工具实现
├── reports/                               # 默认报告输出目录
├── tests/                                 # 单元测试
├── requirements.txt                       # Python 依赖
└── AGENTS.md                              # 仓库协作约定
```

## 1. 克隆仓库

```bash
git clone https://github.com/x7lovelife-dev/medres.git
cd medres
```

如果已经在 Codex 工作区中打开本仓库，可以跳过这一步。

## 2. 安装 Python 依赖

建议使用 Python 3.10 或更新版本。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell 可使用：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. 在 Codex 中启用智能体 Skill

在 Codex 中打开本仓库根目录后，Codex 会读取仓库内的 `.agents/skills/pharma-research-agent`。

可以直接提出任务，例如：

```text
使用 pharma-research-agent 分析 CLDN18.2 在胃癌中的全球竞争格局，并生成 Markdown 报告。
```

```text
使用 pharma-research-agent 比较药物 A 和药物 B 在某适应症中的临床证据。
```

```text
使用 pharma-research-agent 评估某靶点 ADC 项目在某适应症中的非临床可行性、主要缺陷和失败路径。
```

智能体会先进行研究范围界定，再按任务类型读取必要参考文件。临床任务加载临床/安全性角色和模板；早期项目任务加载靶点生物学、制剂、非临床药效、PK/PD、毒理、项目质疑等专用模块，避免把所有规则一次性放入上下文。

## 4. 在 Codex 中部署 MCP server

MCP server 用于让 Codex 调用本仓库的医药数据查询工具。配置方式有两种：

- 项目级配置：复制 `.codex/config.example.toml` 为 `.codex/config.toml`。
- 用户级配置：把同样内容合并到 `~/.codex/config.toml`。

推荐配置如下，注意把 `cwd` 改成你本机的仓库绝对路径。

```toml
[mcp_servers.pharma_research]
command = "python"
args = ["mcp-server/server.py"]
cwd = "/absolute/path/to/medres"
startup_timeout_sec = 20
tool_timeout_sec = 120

[mcp_servers.pharma_research.env]
HTTP_PROXY = ""
HTTPS_PROXY = ""
ALL_PROXY = ""
http_proxy = ""
https_proxy = ""
all_proxy = ""
NO_PROXY = "*"
no_proxy = "*"
```

如果使用虚拟环境，也可以把 `command` 改为虚拟环境里的 Python 解释器路径，例如：

```toml
command = "/absolute/path/to/medres/.venv/bin/python"
```

Windows 示例：

```toml
[mcp_servers.pharma_research]
command = "C:\\absolute\\path\\to\\medres\\.venv\\Scripts\\python.exe"
args = ["mcp-server/server.py"]
cwd = "C:\\absolute\\path\\to\\medres"
startup_timeout_sec = 20
tool_timeout_sec = 120
```

配置完成后，重启 Codex 或新开一个线程，让 MCP server 重新加载。

## 5. 验证部署

先在终端确认 MCP server 可以启动：

```bash
python mcp-server/server.py
```

在 Codex 新线程中，可以询问可用 MCP 工具，或直接让智能体执行一次小范围检索任务。

当前 MCP server 暴露的工具包括：

| 工具 | 数据源 | 用途 |
| --- | --- | --- |
| `search_literature` | PubMed, Europe PMC, Crossref | 多源文献检索、合并和去重 |
| `search_clinical_trials` | ClinicalTrials.gov API v2 | 查询临床试验设计、阶段、状态、终点和申办方 |
| `search_drug_labels` | openFDA Drug Label | 查询药品标签、适应症、警告、不良反应和剂量信息 |
| `search_adverse_events` | openFDA FAERS | 查询不良事件报告总数和年度趋势 |
| `search_patents` | PatentsView + fallback links | 专利元数据检索和可追溯检索入口；后续 landscape 优先接 Google Patents Public Datasets / BigQuery |

也可以运行单元测试：

```bash
pytest
```

## 6. 推荐使用方式

在 Codex 中优先明确研究主题和输出形式，例如：

```text
使用 pharma-research-agent 调研 HER2 ADC 在乳腺癌中的全球临床竞争格局，输出 reports/YYYY-MM-DD-her2-adc-breast-cancer-research.md。
```

```text
使用 pharma-research-agent 分析某药物相关 ILD 不良事件信号，要求区分 FAERS 报告计数、药品标签和文献证据。
```

```text
使用 pharma-research-agent 对某早期小分子项目做第三方尽调，重点评估靶点有效性、制剂适配性、非临床转化、毒理风险、竞品失败先例和建议补充实验。
```

如果问题范围较宽，智能体应先声明或询问范围。临床任务包括适应症、人群、治疗线、联合方案、对照、地区和优先终点；早期项目任务包括靶点、适应症、modality、项目阶段、已知数据和决策目的。生成报告时，每条关键结论都应保留 PMID、DOI、NCT ID、openFDA 来源、数据库 ID、专利号、URL 或其他可追溯标识。

## 常见问题

### Codex 看不到 MCP 工具

确认以下几点：

- 已重启 Codex 或新开线程。
- `cwd` 是仓库绝对路径。
- `command` 指向能导入 `mcp` 和 `requests` 的 Python。
- 已执行 `pip install -r requirements.txt`。

### 外部 API 请求失败

本仓库默认在 MCP env 中清空代理变量，避免失效代理影响 PubMed、ClinicalTrials.gov 和 openFDA 请求。如果你的网络必须使用代理，请按本机环境调整 `.codex/config.toml` 中的 env 配置。

### 专利工具返回 fallback links

`search_patents` 当前是可调用原型。PatentsView 公共接口不稳定时，工具会返回 `warnings` 和 Google Patents、Espacenet、PatentsView 的检索入口，便于报告保留检索缺口。

## 参考文档

- [docs/使用说明.md](docs/使用说明.md)
- [docs/MCP部署与更新报告.md](docs/MCP部署与更新报告.md)
- [mcp-server/README.md](mcp-server/README.md)
- [mcp-server/tool-contracts.md](mcp-server/tool-contracts.md)
