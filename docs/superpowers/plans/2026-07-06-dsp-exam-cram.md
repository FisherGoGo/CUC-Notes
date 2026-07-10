# DSP 考前关键知识点 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成一份约 5 页、覆盖 DSP 八章核心考点且只整理低通滤波器设计的考前速查 Markdown。

**Architecture:** 以教师期末复习要点限定考试范围，以八份完善版章节笔记校核公式和条件。正文采用“最后检查清单 + 章节主线 + 题型步骤 + 易错点”的单文件结构，删去长推导、完整例题和低通之外的滤波器设计。

**Tech Stack:** UTF-8 Markdown、Obsidian、LaTeX 数学公式、PowerShell/rg 只读校验。

---

## 文件结构

- Create: `大二下/数字信号处理/02_复习资料/DSP考前关键知识点.md`：唯一交付文件，负责临考快速回忆。
- Read: `大二下/数字信号处理/02_复习资料/老师期末复习要点.md`：限定教师要求的范围。
- Read: `大二下/数字信号处理/01_章节笔记_完善版/*.md`：校核定义、公式、步骤和易错点。

### Task 1: 提取考试范围与必背公式

**Files:**
- Read: `大二下/数字信号处理/02_复习资料/老师期末复习要点.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/01 第一章 离散时间信号与系统.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/02 第二章 Z变换与DTFT变换.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/03 第三章 离散傅里叶变换 DFT.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/04 第四章 快速傅里叶变换.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/05 第五章 序列的抽取、插值与采样率转换.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/06 数字滤波器.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/07 设计IIR滤波器.md`
- Read: `大二下/数字信号处理/01_章节笔记_完善版/08 FIR 滤波器.md`

- [ ] **Step 1: 读取教师范围与八章标题结构**

Run:

```powershell
rg -n '^#|^##|^###|必考|重点|掌握|了解' '大二下/数字信号处理/02_复习资料/老师期末复习要点.md' '大二下/数字信号处理/01_章节笔记_完善版'
```

Expected: 输出教师范围和八章知识标题。

- [ ] **Step 2: 提取公式、步骤和易错提示**

Run:

```powershell
rg -n '^\$\$|^>|步骤|条件|结论|易错' '大二下/数字信号处理/01_章节笔记_完善版'
```

Expected: 每章均有可用于压缩的公式或直接结论。

### Task 2: 编写极简速查正文

**Files:**
- Create: `大二下/数字信号处理/02_复习资料/DSP考前关键知识点.md`

- [ ] **Step 1: 写入最后 10 分钟检查清单**

清单覆盖频率单位、ROC、圆周/线性卷积、FFT 位序、多采样率滤波位置、IIR/FIR 低通设计六类高频失分点。

- [ ] **Step 2: 写入第一至第五章极简条目**

每章只保留定义或判据、必背公式、题型步骤和一组易错点；不得加入完整证明。

- [ ] **Step 3: 写入第六至第八章极简条目**

第六章只保留结构判断；第七章只写数字低通 IIR 设计；第八章只写线性相位 FIR 与窗函数法低通设计，并明确其他滤波器类型不展开。

### Task 3: 范围与公式校验

**Files:**
- Test: `大二下/数字信号处理/02_复习资料/DSP考前关键知识点.md`

- [ ] **Step 1: 检查八章覆盖和低通范围**

Run:

```powershell
rg -n '^## ' '大二下/数字信号处理/02_复习资料/DSP考前关键知识点.md'
rg -n '高通|带通|带阻' '大二下/数字信号处理/02_复习资料/DSP考前关键知识点.md'
```

Expected: 有最后检查清单和八章正文；高通、带通、带阻只在范围声明中出现一次。

- [ ] **Step 2: 检查核心公式关键词**

Run:

```powershell
rg -n 'omega=|ROC|DFT|DIT|DIF|抽取|插值|双线性|窗函数|线性相位' '大二下/数字信号处理/02_复习资料/DSP考前关键知识点.md'
```

Expected: 九类核心内容均有匹配。

- [ ] **Step 3: 检查 Markdown 基本完整性**

Run:

```powershell
$text = Get-Content -Raw -Encoding UTF8 '大二下/数字信号处理/02_复习资料/DSP考前关键知识点.md'; [pscustomobject]@{ Lines=($text -split "`n").Count; DisplayMath=([regex]::Matches($text,'\$\$')).Count; CodeFences=([regex]::Matches($text,'```')).Count }
```

Expected: 行数适合极简速查；`DisplayMath` 和 `CodeFences` 均为偶数。
