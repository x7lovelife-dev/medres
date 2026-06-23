# 数据源地图

## 多源文献

| 数据源 | 用途 | 关键 ID | 优先场景 |
| --- | --- | --- | --- |
| PubMed / NCBI E-utilities | 医学文献检索、摘要、MeSH、PMID 溯源 | PMID | 所有主题 |
| PubMed Central | 开放全文、正文证据、图表和补充材料 | PMCID | 机制、临床、安全性深读 |
| Europe PMC | 欧洲文献、开放全文、预印本补充 | PMID/PMCID/DOI | 多源补充和全文查找 |
| Crossref | DOI、出版元数据、期刊、出版日期 | DOI | 去重和元数据补全 |
| OpenAlex | 学术图谱、作者、机构、引用关系 | OpenAlex ID/DOI | 领域趋势、机构和引用分析 |
| Semantic Scholar | 引用、相关论文、影响力指标 | S2 ID/DOI | 相关文献扩展 |
| bioRxiv / medRxiv | 生命科学和医学预印本 | DOI | 最新机制和临床前沿 |
| 用户上传文档 | 内部 PDF、Word、Excel、PPT、图片、表格 | 文件路径/页码/表格名 | 内部资料和非公开材料 |

## 主题到数据源

| 主题 | 必选数据源 | 推荐补充源 |
| --- | --- | --- |
| 靶点竞争格局 | PubMed, ClinicalTrials.gov, OpenAlex | PMC, Europe PMC, Semantic Scholar, 用户上传管线表 |
| 药物临床对比 | ClinicalTrials.gov, PubMed, openFDA Label | PMC, Europe PMC, Crossref, 用户上传临床资料 |
| 不良事件分析 | openFDA FAERS, openFDA Label, PubMed | PMC, Europe PMC, medRxiv, 用户上传安全性资料 |

## 检索策略

1. 先用主题词构造核心查询：靶点/药物/适应症/反应术语。
2. 再用同义词和实体别名扩展：通用名、商品名、研发代号、靶点别名、MeSH 词。
3. 对文献结果按 DOI、PMID、标题标准化去重。
4. 对临床试验按 NCT ID 去重。
5. 对不良事件按药物名和反应术语聚合，保留查询条件。

## 最小输出字段

### 文献

| 字段 | 说明 |
| --- | --- |
| source | PubMed/PMC/Europe PMC/Crossref/OpenAlex/Semantic Scholar/bioRxiv/medRxiv |
| id | PMID/PMCID/DOI/OpenAlex ID/S2 ID |
| title | 标题 |
| authors | 作者 |
| journal_or_server | 期刊或预印本平台 |
| publication_date | 发表日期 |
| abstract | 摘要 |
| url | 来源链接 |
| evidence_note | 与研究问题的关系 |

### 临床试验

| 字段 | 说明 |
| --- | --- |
| nct_id | ClinicalTrials.gov ID |
| title | 试验标题 |
| phase | 临床阶段 |
| condition | 适应症 |
| intervention | 干预 |
| sponsor | 申办方 |
| enrollment | 入组人数 |
| primary_outcomes | 主要终点 |
| status | 招募/完成状态 |

### 安全性

| 字段 | 说明 |
| --- | --- |
| source | openFDA FAERS/openFDA Label/文献 |
| drug | 药物名 |
| reaction | 反应术语 |
| count_or_summary | 报告数或文本摘要 |
| seriousness | 严重性字段 |
| source_id | API 查询 URL、PMID、DOI 或标签 ID |
