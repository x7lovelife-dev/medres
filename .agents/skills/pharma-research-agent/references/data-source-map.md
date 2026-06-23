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
| Google Patents Public Datasets / BigQuery | 结构化专利书目信息、专利族、申请人、CPC、时间趋势和 landscape 统计 | publication number/family ID/BigQuery row | 专利 landscape、批量统计、申请人和技术方向分析 |
| 权威会议与重磅报道网页 | ASCO, ESMO, AACR, ADA, AHA, EHA, WCLC 等会议官网、摘要库、新闻稿和少数重磅媒体报道 | URL/会议摘要号/发布日期 | 最新重要研究、监管前动态、尚未进入文献库的关键更新 |
| 普通网页搜索 | 搜索引擎结果、公司新闻稿、行业媒体、机构页面 | URL/发布日期/发布机构 | 低优先级补充；用于查漏、定位原始来源或发现待验证线索 |
| 用户上传文档 | 内部 PDF、Word、Excel、PPT、图片、表格 | 文件路径/页码/表格名 | 内部资料和非公开材料 |

## 主题到数据源

| 主题 | 必选数据源 | 推荐补充源 |
| --- | --- | --- |
| 靶点竞争格局 | PubMed, ClinicalTrials.gov, OpenAlex | PMC, Europe PMC, Semantic Scholar, 权威会议与重磅报道网页, 用户上传管线表 |
| 药物临床对比 | ClinicalTrials.gov, PubMed, openFDA Label | PMC, Europe PMC, Crossref, ASCO/ESMO/AACR/ADA 等会议摘要, 公司公告, 用户上传临床资料 |
| 不良事件分析 | openFDA FAERS, openFDA Label, PubMed | PMC, Europe PMC, medRxiv, 监管机构或权威会议网页, 用户上传安全性资料 |

## 来源优先级

1. 优先使用可结构化、可稳定追溯的数据源：PubMed/PMC、ClinicalTrials.gov、openFDA、Crossref、OpenAlex、Semantic Scholar、bioRxiv/medRxiv 和用户上传材料。
2. 权威会议和重磅报道网页属于高价值补充源。当 ASCO、ESMO、AACR、ADA、AHA、EHA、WCLC 等会议官网、会议摘要库、期刊同步发布页、监管机构公告或少数重磅媒体报道披露关键更新时，可以提升优先级，并尽量追溯到会议摘要号、NCT ID、DOI、公司公告或监管文件。
3. Google Patents Public Datasets / BigQuery 属于结构化专利补充源，专利 landscape 或批量统计时优先级高于普通网页和 Google Patents 网页核验；使用前应限定查询范围并记录预计扫描量。
4. 普通网页搜索默认低优先级，只用于查漏补缺、发现线索或定位原始来源。网页结果不得单独支撑关键结论，除非来源本身是权威机构、会议官网、监管机构、期刊、公司正式公告或具有明确可追溯 ID 的重磅报道。
5. 使用网页结果时必须记录 URL、发布机构、发布日期和检索日期；如果网页内容无法追溯到原始研究或官方材料，标注为“待补充证据”。

## 检索策略

1. 先用主题词构造核心查询：靶点/药物/适应症/反应术语。
2. 再用同义词和实体别名扩展：通用名、商品名、研发代号、靶点别名、MeSH 词。
3. 临床对比先按“直接头对头试验”检索：药物A + 药物B + 适应症 + 治疗线 + 方案关键词；再按每个核心试验代号/NCT ID 精准检索。
4. 没有成熟直接结果时，建立间接证据集合，并标注为什么纳入：同治疗线、同人群、同组织学、相似方案、或仅背景。
5. 结构化来源检索不足或用户要求最新动态时，再使用网页搜索；优先检索权威会议、监管机构、期刊和公司公告，普通网页结果只作为线索。
6. 专利 landscape 任务优先使用结构化专利源；Google Patents Public Datasets / BigQuery 查询必须避免未限定全表扫描，先按申请人、CPC、关键词、jurisdiction、priority date 或 publication date 缩小范围。
7. 对文献结果按 DOI、PMID、标题标准化去重。
8. 对临床试验按 NCT ID 去重。
9. 对不良事件按药物名和反应术语聚合，保留查询条件。
10. 对网页结果按 URL、标题、发布机构和发布日期去重，并标注是否已追溯到原始研究或官方材料。

## 临床对比核心试验集合规则

| 步骤 | 目的 | 例子 |
| --- | --- | --- |
| 直接试验定位 | 找到同一研究内目标干预 vs 目标对照 | 研究A: 目标干预 vs 目标对照 |
| 同类方案补充 | 找到目标药物在同人群/同治疗线的相近方案 | 研究B: 目标干预 + 相同标准治疗 vs 同类对照 + 相同标准治疗 |
| 标准治疗锚点 | 找到对照药物的标准证据 | 研究C/D: 当前标准治疗或对照方案的关键注册研究 |
| 背景证据 | 记录但不进入核心结论 | 单药研究、后线研究、突变后进展研究 |

临床对比报告必须说明每个研究是直接证据、强间接证据、背景证据还是排除/待补充。

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
| evidence_role | 直接证据/强间接证据/背景证据/排除或待补充 |

### 安全性

| 字段 | 说明 |
| --- | --- |
| source | openFDA FAERS/openFDA Label/文献 |
| drug | 药物名 |
| reaction | 反应术语 |
| count_or_summary | 报告数或文本摘要 |
| seriousness | 严重性字段 |
| source_id | API 查询 URL、PMID、DOI 或标签 ID |
