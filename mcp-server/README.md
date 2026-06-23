# Pharma Research MCP Server

本目录是 `pharma-research-agent` 的真实数据查询入口。当前 MCP server 已实现并挂载五个工具：文献检索、临床试验检索、药品标签检索、不良事件检索和专利检索。

## 目标

为 Codex 的 `pharma-research-agent` Skill 提供可复现、可追溯的医药数据查询工具，覆盖多源文献、临床试验、不良事件、药品标签和早期专利信息。

## 本地启动

先安装依赖：

```powershell
pip install -r requirements.txt
```

再启动 MCP 服务：

```powershell
python mcp-server/server.py
```

Codex 配置示例见 `.codex/config.example.toml`。复制到项目级 `.codex/config.toml` 或合并到用户级 `~/.codex/config.toml` 后，重启 Codex 或新开线程。

## 已实现工具

| 工具 | 状态 | 主要来源 | 说明 |
| --- | --- | --- | --- |
| `search_literature` | 已实现 | PubMed, Europe PMC, Crossref | 多源文献检索、合并、去重 |
| `search_clinical_trials` | 已实现 | ClinicalTrials.gov API v2 | 查询试验设计、阶段、状态、终点、申办方 |
| `search_drug_labels` | 已实现 | openFDA Drug Label | 查询适应症、警告、不良反应、剂量等标签字段 |
| `search_adverse_events` | 已实现 | openFDA Drug Event / FAERS | 查询报告总数和年度趋势；只作安全性信号，不作因果判断 |
| `search_patents` | 已实现原型 | PatentsView | 查询美国专利元数据；当前公共源偶发超时，失败时返回 warning |

## 规划中工具

| 工具 | 目的 | 来源 |
| --- | --- | --- |
| `fetch_publication_detail` | 获取文献详情、摘要、元数据、可用全文标识 | NCBI, Europe PMC, Crossref, OpenAlex |
| `normalize_entities` | 标准化药物、靶点、适应症、反应术语 | 本地规则表/后续实体服务 |
| `rank_evidence` | 按研究问题对证据排序和标注 | 本地规则/后续模型辅助 |

## 通用响应约定

所有工具返回 JSON 对象：

```json
{
  "query": {},
  "retrieved_at": "2026-06-23",
  "source": "source-name",
  "items": [],
  "warnings": [],
  "next_page": null
}
```

失败或外部源超时时，不抛出致命错误，返回空 `items` 和可读 `warnings`，便于报告里保留检索缺口。

## 实现优先级

1. 扩展 `search_literature`：接 OpenAlex、Semantic Scholar、bioRxiv/medRxiv。
2. 增强 `search_patents`：接 EPO OPS、Google Patents 或 Lens 等更完整来源；如需账号/API key，再放入 MCP env。
3. 实现 `fetch_publication_detail`。
4. 实现 `normalize_entities` 和 `rank_evidence`。

详细字段见 `tool-contracts.md`。
