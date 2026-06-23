# MCP 部署与更新报告

更新时间：2026-06-23
仓库：x7lovelife-dev/medres

## 本次更新

这次把 `pharma_research` MCP 从单一文献检索原型，扩展成一个可支撑医药调研工作流的基础数据服务。现在同一个 MCP server 暴露五个工具：

| 工具 | 状态 | 数据源 | 用途 |
| --- | --- | --- | --- |
| `search_literature` | 已部署 | PubMed, Europe PMC, Crossref | 多源文献检索、合并和去重 |
| `search_clinical_trials` | 已部署 | ClinicalTrials.gov API v2 | 查询临床试验设计、阶段、状态、终点和申办方 |
| `search_drug_labels` | 已部署 | openFDA Drug Label | 查询药品标签、适应症、警告、不良反应和剂量信息 |
| `search_adverse_events` | 已部署 | openFDA FAERS | 查询不良事件报告总数和年度趋势 |
| `search_patents` | 已部署原型 | PatentsView + fallback links | 尝试结构化专利检索；源不可用时返回 Google Patents、Espacenet、PatentsView 检索入口 |

## 智能体流程更新

`pharma-research-agent` 也做了同步调整。它现在先做问题收窄，再进入检索和报告生成。临床对比会优先找直接头对头证据；如果没有成熟结果，再构建强间接证据和背景证据集合。

新增的 `scope-clarification-rules.md` 是通用规则，不绑定具体药物、靶点或适应症。它要求用 PICO/PECO 明确人群、干预、对照、终点、治疗线、亚型、给药方式和地区。

## 本机部署状态

用户级 Codex 配置已加入：

```toml
[mcp_servers.pharma_research]
command = "python"
args = ["mcp-server/server.py"]
cwd = "C:/Users/ALT147/Documents/多角色分析自动流程拆解"
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

代理覆盖是有必要的。本机环境里存在失效代理变量，外部 API 查询会被截断；清空代理后，PubMed、ClinicalTrials.gov 和 openFDA 查询恢复正常。

## 验证结果

单元测试通过：

```text
7 passed
```

MCP smoke test 结果：

```text
TOOLS=search_literature,search_clinical_trials,search_drug_labels,search_adverse_events,search_patents
search_literature: 1 item, no warning
search_clinical_trials: 1 item, no warning
search_drug_labels: 1 item, no warning
search_adverse_events: 1 item, no warning
search_patents: 1 fallback search link, with PatentsView warning
```

这说明 MCP 注册和四类医药数据源已经可用。专利检索目前是可调用原型，但 PatentsView 结构化接口在当前网络下不稳定，所以工具会返回可追溯检索入口，避免报告里出现“无结果但不知道为什么”的情况。

## 仍需补强

1. 扩展文献源：OpenAlex、Semantic Scholar、bioRxiv、medRxiv。
2. 增强专利检索：接 EPO OPS、Lens 或稳定 PatentsView 新接口；如果需要 API key，可放入 MCP env。
3. 实现 `fetch_publication_detail`，用于 PMID/DOI/NCT 的详情补全。
4. 实现 `normalize_entities` 和 `rank_evidence`，把实体标准化和证据分层从规则文档升级为工具能力。

## 使用提醒

重启 Codex 或新开线程后，才能看到新 MCP 工具。运行报告时，如果某个外部数据源超时，工具会返回 `warnings`；报告应保留这些检索缺口，不要把失败源当成“没有证据”。
