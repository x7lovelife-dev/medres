# Pharma Research MCP Server

本目录描述真实数据查询 MCP 服务的入口和工具契约。当前已实现 `search_literature` 的本地 Python 逻辑和 MCP 入口；其余工具仍是接口规划。

## 目标

为 Codex 的 `pharma-research-agent` Skill 提供可复现、可追溯的医药数据查询工具，覆盖多源文献、临床试验、不良事件、药品标签、实体标准化和证据排序。

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

## 工具列表

| 工具 | 目的 | 主要来源 |
| --- | --- | --- |
| `search_literature` | 多源文献检索、合并、去重 | PubMed, Europe PMC, Crossref；OpenAlex/Semantic Scholar/bioRxiv/medRxiv 待扩展 |
| `fetch_publication_detail` | 获取文献详情、摘要、元数据、可用全文标识 | NCBI, Europe PMC, Crossref, OpenAlex |
| `search_clinical_trials` | 查询临床试验设计、阶段、状态、终点 | ClinicalTrials.gov API v2 |
| `search_adverse_events` | 查询药物不良事件报告聚合 | openFDA Drug Event |
| `search_drug_labels` | 查询药品标签、适应症、警告、不良反应 | openFDA Drug Label |
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

失败时返回：

```json
{
  "query": {},
  "retrieved_at": "2026-06-23",
  "source": "source-name",
  "items": [],
  "warnings": ["human readable reason"],
  "error": {
    "code": "RATE_LIMITED",
    "message": "Request exceeded source rate limit."
  }
}
```

## 实现优先级

1. `search_literature`：已接 PubMed、Europe PMC、Crossref；下一步扩展 OpenAlex、Semantic Scholar、bioRxiv/medRxiv。
2. `search_clinical_trials`：接 ClinicalTrials.gov API v2。
3. `search_drug_labels` 和 `search_adverse_events`：接 openFDA。
4. `normalize_entities`：先用本地别名词表和规则。
5. `rank_evidence`：先用 `evidence-quality-rules.md` 的规则实现。

详细字段见 `tool-contracts.md`。
