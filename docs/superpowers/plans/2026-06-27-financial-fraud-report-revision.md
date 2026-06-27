# 紫晶存储案例分析报告优化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 先产出一份约 5000 字、以内部控制目标和五要素为主框架的优化版 Markdown，经用户确认后再生成符合课程格式的 DOCX 与 PDF。

**Architecture:** 内容阶段与排版阶段分离。内容阶段只处理事实、理论、论证、图表数据和人写感；排版阶段读取确认后的 Markdown，生成独立的新 DOCX，并通过 Microsoft Word 导出 PDF、逐页渲染验收。原始报告不覆盖，封面不在本次范围内。

**Tech Stack:** Markdown、Python 3、python-docx、OOXML、Microsoft Word COM、Poppler、humanizer 审校规则。

---

## 文件结构

- 创建：`大二下/选修课/财务舞弊/紫晶存储案例分析报告_理论深化优化版.md`——用户首先审阅的内容定稿。
- 创建：`大二下/选修课/财务舞弊/图表/紫晶存储虚假销售证据链.png`——Word 中的图 1。
- 创建：`大二下/选修课/财务舞弊/紫晶存储案例分析报告_理论深化优化版.docx`——最终 Word 版本，不含封面。
- 创建：`大二下/选修课/财务舞弊/紫晶存储案例分析报告_理论深化优化版.pdf`——由 Word 导出的提交版 PDF。
- 创建：`.codex_tmp/finance_report_revision/build_report.py`——从已确认 Markdown 构建 DOCX 的临时脚本，不作为交付物。
- 读取：`大二下/选修课/财务舞弊/紫晶存储资料索引与事实摘录.md` 与 `资料/紫晶存储/*.pdf`——事实来源。
- 读取：`大二下/选修课/财务舞弊/通识课结课作业要求.pdf`——格式与评分依据。

### Task 1: 建立事实与理论约束清单

- [ ] **Step 1: 提取监管认定的硬事实**

从行政处罚决定书、2021 年年报和先行赔付公告核对：五个报告期虚增收入/利润数据、舞弊手段、责任人员、担保事项、审计意见与赔付主体。不得把推断写成监管结论。

- [ ] **Step 2: 固定理论口径**

内部控制目标采用合规、资产安全、报告及相关信息真实完整、经营效率效果、发展战略五项目标；内部控制五要素采用内部环境、风险评估、控制活动、信息与沟通、内部监督。舞弊三角采用压力、机会、合理化，且合理化部分以“可能的解释路径”表述。

- [ ] **Step 3: 核对写作约束**

记录正文不少于 4000 字、1.5 倍行距、课程规定字体字号、底部居中页码、图表五号宋体、参考文献完整、查重率不高于 30%。确认封面留给用户后加。

### Task 2: 重写优化版 Markdown

**Files:**
- Create: `大二下/选修课/财务舞弊/紫晶存储案例分析报告_理论深化优化版.md`

- [ ] **Step 1: 写标题、摘要与关键词**

标题使用《“证据齐全”何以掩盖虚假交易——紫晶存储销售链舞弊的内控失效与审计反思》。摘要直接交代研究问题、理论框架、核心发现与结论，不复述全文目录。

- [ ] **Step 2: 写引言和案例事实**

将宏观背景压缩至一段；用监管认定、关键日期与虚增比例建立事实基础。正文明确区分“证监会认定”“公司公告披露”“本文据此判断”。

- [ ] **Step 3: 写虚假销售证据链分析**

按合同、物流、验收、回款、收入确认五个环节说明表面证据与真实性缺口，形成全文的“小切口”。

- [ ] **Step 4: 写舞弊三角与内控五要素主体分析**

舞弊三角控制在辅助篇幅；五要素部分逐项落到紫晶存储事实，并明确受损的内控目标。不得恢复为泛化的公司治理教科书段落。

- [ ] **Step 5: 写审计反思、对应建议和结论**

每一条审计程序对应前述证据链中的一个失败点；建议采取“问题—程序—预期获得的独立证据”结构。结论回答标题问题，不再列四点通用启示。

- [ ] **Step 6: 写图表与参考文献**

在 Markdown 中给出表 1 五个期间的虚增数据、表 2 五要素映射，以及图 1 的 Mermaid/文字逻辑。参考文献只保留正文实际使用来源，并统一 `[序号] 责任者. 文献题名[类型]. 日期. URL` 格式。

### Task 3: 执行 humanizer 与质量审校

**Files:**
- Modify: `大二下/选修课/财务舞弊/紫晶存储案例分析报告_理论深化优化版.md`

- [ ] **Step 1: 扫描 AI 写作模式**

检索并逐段处理“首先/其次/再次/最后”“该案例说明”“具有重要意义”“企业层面/监管层面”“综上所述”等高频模板，保留确有逻辑功能的连接词。

- [ ] **Step 2: 做案例替换测试**

逐段判断：若把“紫晶存储”替换为另一家公司，段落是否仍基本成立。若成立，则补入具体数据、控制环节、公告事实或删除该段。

- [ ] **Step 3: 做证据与语气测试**

监管事实使用确定语气；从事实推出的结论使用“表明/可见”；无法直接验证的主观动机使用“可能/可以理解为”，不虚构管理层心理。

- [ ] **Step 4: 运行文本检查**

Run:

```powershell
$f='大二下\选修课\财务舞弊\紫晶存储案例分析报告_理论深化优化版.md'
$text=Get-Content -Raw -Encoding UTF8 $f
"CHARS=" + (($text -replace '\s','').Length)
rg -n "首先|其次|再次|最后|具有重要意义|综上所述|企业层面|监管层面" $f
```

Expected: 去除空白后的全文字符数足以支撑不少于 4000 字正文；检索结果仅保留必要用例。

- [ ] **Step 5: 用户内容确认检查点**

向用户交付 Markdown；在用户确认内容前，不进入 Word 排版阶段。

### Task 4: 生成图形与 DOCX

**Files:**
- Create: `大二下/选修课/财务舞弊/图表/紫晶存储虚假销售证据链.png`
- Create: `.codex_tmp/finance_report_revision/build_report.py`
- Create: `大二下/选修课/财务舞弊/紫晶存储案例分析报告_理论深化优化版.docx`

- [ ] **Step 1: 生成证据链图**

生成横向五节点图：虚构合同→伪造物流→伪造验收→安排回款→确认收入；每个节点下方标出应取得的独立证据。使用黑白/灰色学术风格，保证打印可读。

- [ ] **Step 2: 编写 DOCX 构建脚本**

脚本读取已确认 Markdown，设置 A4、上/下 2.54 cm、左/右 3.18 cm、正文 12 pt 宋体、1.5 倍行距、首行缩进 2 字符；总标题 15 pt 黑体居中；一级标题 12 pt 宋体加粗；二级标题 12 pt 宋体不加粗；图表文字 10.5 pt 宋体；页脚插入居中 PAGE 域。

- [ ] **Step 3: 设置图表几何**

表格使用固定 DXA 列宽、允许自动增高、单元格垂直居中、表头重复；图 1 宽度不超过正文版心，题注置于图下方，表题置于表上方，并标注资料来源。

- [ ] **Step 4: 生成 DOCX 并结构检查**

Run:

```powershell
& 'C:\Users\yyy20\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.codex_tmp\finance_report_revision\build_report.py'
```

Expected: 生成优化版 DOCX；原始两个 DOCX 的时间戳和内容不变。

### Task 5: Word 渲染、PDF 导出与最终验收

**Files:**
- Create: `大二下/选修课/财务舞弊/紫晶存储案例分析报告_理论深化优化版.pdf`
- Create: `.codex_tmp/finance_report_revision/render/page-*.png`

- [ ] **Step 1: 使用 Microsoft Word 导出 PDF**

以只读方式打开优化版 DOCX，更新 PAGE 域并导出 PDF；不接受其他渲染器造成的字体替换作为最终结果。

- [ ] **Step 2: 将 PDF 全部页面渲染为 PNG**

Run:

```powershell
& 'C:\Users\yyy20\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe' -png -r 144 '大二下\选修课\财务舞弊\紫晶存储案例分析报告_理论深化优化版.pdf' '.codex_tmp\finance_report_revision\render\page'
```

Expected: 每页生成一张 `page-N.png`。

- [ ] **Step 3: 逐页视觉检查**

检查全部页面：标题层级、孤行标题、图形清晰度、表格分页、单元格文字截断、页码位置、参考文献换行以及异常空白页。发现问题后修改构建脚本、重新生成并重新渲染。

- [ ] **Step 4: 最终结构审计**

核对 A4 和四边页边距、所有正文 1.5 倍行距、标题和正文中西文字体、图表五号宋体、页脚 PAGE 域、正文字符数、参考文献数量与图表编号。

- [ ] **Step 5: 交付**

仅交付最终 Markdown、DOCX 和 PDF；不交付临时脚本、渲染 PNG 或中间 PDF。

