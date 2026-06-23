# 早期药物项目数据源地图

## 数据源优先级

| 数据类别 | 主要来源 | 关键 ID | 用途 |
| --- | --- | --- | --- |
| 文献与全文 | PubMed, PubMed Central, Europe PMC, Crossref, bioRxiv, medRxiv | PMID/PMCID/DOI | 机制、非临床、转化、毒理和早期临床线索 |
| 靶点-疾病证据 | Open Targets, GWAS Catalog, ClinVar, OMIM, DisGeNET | target ID/trait ID/variant ID | 人类遗传学、疾病关联和靶点验证 |
| 蛋白与功能 | UniProt, NCBI Gene, Ensembl | UniProt ID/Gene ID/Ensembl ID | 蛋白功能、结构域、亚细胞定位、同源性 |
| 表达与组织分布 | Human Protein Atlas, GTEx, Bgee, ENCODE, 单细胞公开数据 | tissue/cell type/dataset ID | 正常组织表达、患者样本、潜在 on-target 毒性 |
| 通路与互作 | Reactome, GO, STRING, KEGG | pathway ID/GO ID/STRING ID | 机制位置、通路冗余、上下游补偿 |
| 活性与化学 | ChEMBL, BindingDB, PubChem | ChEMBL ID/BindingDB ID/CID | 已知配体、活性、选择性、成药性线索 |
| 结构与可成药性 | RCSB PDB, AlphaFold, UniProt structure annotations | PDB ID/AlphaFold ID | 结合口袋、结构域、抗体表位、构象可及性 |
| 临床与管线 | ClinicalTrials.gov, WHO ICTRP, 公司公告, 权威会议摘要 | NCT ID/registry ID/abstract ID | 竞品、转化进度、失败或成功先例 |
| 安全性与标签 | openFDA Label, openFDA FAERS, 药品说明书, 监管文件 | set ID/query URL/regulatory ID | 同类安全性、标签风险、信号线索 |
| 专利 | PatentsView, Google Patents Public Datasets / BigQuery, EPO OPS / Espacenet, Lens, Google Patents 网页 | patent number/publication number/family ID/BigQuery row | 核心结构、用途、组合、制剂、给药、同族、引用、申请人和绕开空间 |
| 权威会议与网页 | ASCO, AACR, ESMO, ADA, AHA, EHA, WCLC, 监管机构, 期刊新闻页 | URL/摘要号/发布日期 | 最新进展、尚未入库数据、关键公告 |
| 用户上传材料 | PDF, Word, Excel, PPT, 图片, 表格 | 文件路径/页码/表格名 | 内部数据、项目资料、未公开研究 |

## 主题到数据源

| 评估主题 | 必选数据源 | 推荐补充源 |
| --- | --- | --- |
| 靶点有效性 | PubMed/PMC, Open Targets, UniProt, HPA/GTEx | GWAS Catalog, Reactome, STRING, 单细胞数据 |
| 制剂/技术路线 | PubMed/PMC, UniProt, HPA/GTEx, PDB/AlphaFold | ChEMBL, BindingDB, 同 modality 竞品公告 |
| 非临床药效 | PubMed/PMC, bioRxiv/medRxiv, 用户上传资料 | 会议摘要、公司公告、补充材料 |
| PK/PD 与暴露 | 文献全文、用户上传资料、标签/同类药物资料 | 会议摘要、监管文件 |
| 毒理风险 | HPA/GTEx, openFDA Label, 文献全文, 同类药物标签 | FAERS, 监管文件, 物种表达数据 |
| 竞品与失败先例 | ClinicalTrials.gov, PubMed, 公司公告, 会议摘要 | 网页搜索、监管文件、专利 |
| 专利与差异化 | PatentsView, Google Patents Public Datasets / BigQuery, Lens, EPO OPS / Espacenet | Google Patents 网页核验、公司公告、文献结构信息 |

## 检索策略

1. 先标准化实体：靶点名、基因名、蛋白名、药物名、研发代号、公司名、适应症和 modality。
2. 对靶点先查人类证据，再查模型证据：人类遗传学、患者组织/表达、临床相关性优先于细胞和动物模型。
3. 对 modality 先判断基本适配性：靶点定位、组织可及性、递送方式、分子大小、内吞/释放需求、免疫原性和同类 precedent。
4. 对非临床证据记录模型类型、物种、细胞系、是否过表达、剂量、暴露、终点、阳性/阴性对照和重复性。
5. 对毒理风险优先查正常组织表达、同类药物标签、物种差异和已知 on-target/off-target 风险。
6. 对竞品和失败案例同时检索成功和终止项目，区分靶点失败、分子失败、剂量失败、毒性失败和临床设计失败。
7. 对专利和 landscape 任务，优先使用 PatentsView、Google Patents Public Datasets / BigQuery、Lens、EPO OPS 等结构化来源；Google Patents 网页和 Espacenet 网页只作低频核验和链接入口。
8. 使用 Google Patents Public Datasets / BigQuery 前，应先用限定条件缩小查询范围，并记录预计扫描量、查询日期和 SQL 条件；不要使用未限定的全表扫描或 `SELECT *` 作为默认检索。
9. 网页搜索只作补充，优先权威会议、监管机构、期刊和公司正式公告；普通网页结果必须追溯到原始来源后才能支撑关键结论。

## 最小输出字段

### 靶点证据

| 字段 | 说明 |
| --- | --- |
| target | 靶点/基因/蛋白 |
| disease | 疾病或适应症 |
| evidence_type | 遗传学/表达/机制/患者样本/模型/临床 |
| source | 数据源 |
| source_id | PMID/DOI/数据库 ID/URL |
| evidence_direction | 支持/反对/不确定 |
| note | 与项目假设的关系 |

### 非临床证据

| 字段 | 说明 |
| --- | --- |
| model | 细胞系/类器官/动物/体内外系统 |
| intervention | 分子、制剂或处理方式 |
| endpoint | 药效、PD biomarker、毒理或 PK 指标 |
| exposure_or_dose | 剂量、浓度、暴露或给药方案 |
| result_summary | 结果摘要 |
| limitation | 模型和外推限制 |
| source_id | PMID/DOI/文件页码/URL |

### 风险与失败路径

| 字段 | 说明 |
| --- | --- |
| risk_area | 靶点/制剂/药效/PKPD/毒理/竞品/专利 |
| risk_statement | 风险描述 |
| evidence | 来源 ID 或待补充证据 |
| impact | 高/中/低 |
| de_risking_step | 建议补充实验或资料 |
