from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REVIEW_DIR = ROOT / "02_复习资料"
HTML_DIR = ROOT / "03_交互测试"


KNOWLEDGE_MD = r"""# 信息论与编码第 1-3 章期末复习清单

## 第一章 绪论：信息论到底在解决什么问题？

本章不是计算重点，但它给后面所有公式定了主线：通信系统面对噪声和资源限制，必须同时追求有效性、可靠性、保密性和认证性。香农信息论关心的是「理论极限」：最多能压缩到多短、最可靠能传到什么程度、信道最多能承载多少信息。

### 信息、消息与香农信息 <span class="tag-key">重点</span>

<span class="kp">消息</span><span class="exp">是通信系统中被传送的具体载体，如文字、语音、图像或符号序列。</span><span class="kp">信息</span><span class="exp">是消息消除不确定性的能力。香农把信息放在概率框架里度量：越不容易发生的事件，发生后带来的信息量越大。</span>

为什么需要这样定义？因为工程上要比较「不同消息到底带来多少不确定性减少」，只说语义价值无法做编码和信道容量计算。香农信息的优点是可计算、可优化；局限是它不讨论消息对人的意义和价值。

<blockquote>易错：信息论中「信息量大」不是「内容重要」，而是「先验概率小、出现后消除的不确定性大」。考试常把语义价值和香农信息量混在一起考。</blockquote>

### 通信系统模型 <span class="tag-must">必考</span>

通信系统主线是：<span class="kp">信源 --&gt; 编码器 --&gt; 信道 --&gt; 译码器 --&gt; 信宿</span>，噪声主要作用在信道。信息论研究的是从信源到信宿的全过程，但重点落在编译码和信道极限上。

| 环节 | 是什么 | 为什么重要 | 考试抓手 |
|---|---|---|---|
| 信源 | 产生消息或消息序列 | 决定原始不确定性和冗余 | 信源熵、剩余度 |
| 信源编码器 | 去冗余、压缩表示 | 提高有效性 | 无失真信源编码定理 |
| 信道编码器 | 加冗余、抗噪声 | 提高可靠性 | 有噪信道编码、纠错码 |
| 信道 | 传输信号的媒介 | 决定传输能力上限 | 平均互信息、信道容量 |
| 译码器 | 从接收信号恢复消息 | 连接理论极限和实际接收 | 差错、疑义度 |

### 有效性与可靠性的矛盾 <span class="tag-key">重点</span>

<span class="kp">有效性</span><span class="exp">要求传得快、码率高、冗余少；信源编码主要服务于有效性。</span><span class="kp">可靠性</span><span class="exp">要求差错少、抗干扰强，信道编码通常通过增加冗余实现。</span>

这两个目标看似冲突：去冗余能提高效率，加冗余能对抗噪声。信息论的价值在于给出可量化边界：哪些冗余是信源内部可去掉的，哪些冗余是为了信道可靠传输必须加回来的。

<blockquote>易错：信源编码和信道编码对冗余的态度相反，不是矛盾操作，而是分别处理「源的冗余」和「抗噪声所需冗余」。</blockquote>

## 第二章 离散信源及其信息测度：怎么度量信源含有多少信息？

第二章的核心问题是：信源还没输出时有多少不确定性？输出后每个符号平均提供多少信息？从自信息到熵，再到联合熵、条件熵、扩展信源和马尔可夫信源，本质上都是在回答「不确定性如何计算、如何分解、如何随记忆性变化」。

### 信源分类与数学模型 <span class="tag-freq">高频</span>

离散信源可以用随机变量及其概率分布描述：

$$
X=\{x_1,x_2,\ldots,x_n\},\quad P(X)=\{p(x_1),p(x_2),\ldots,p(x_n)\}
$$

其中 $p(x_i)\ge 0$ 且 $\sum_i p(x_i)=1$。它解决的问题是：在计算信息量前，先把信源输出的不确定性变成概率空间。

| 分类标准 | 类型 | 关键区别 |
|---|---|---|
| 符号间是否独立 | 无记忆 / 有记忆 | 无记忆满足 $P(X_1\cdots X_N)=\prod_iP(X_i)$ |
| 统计特性是否随时间变 | 平稳 / 非平稳 | 平稳信源的联合概率与时间起点无关 |
| 取值与时间形态 | 离散 / 连续 | 本阶段重点是离散信源 |

<blockquote>易错：无记忆强调符号之间独立；平稳强调统计规律不随时间平移改变。二者不是同一个概念。</blockquote>

### 自信息、联合自信息、条件自信息 <span class="tag-must">必考</span>

<span class="kp">自信息</span>衡量某个事件发生前的不确定性，或发生后提供的信息量：

$$
I(x_i)=-\log p(x_i)=\log \frac{1}{p(x_i)}
$$

对数以 2 为底时单位是 bit。公式直观含义是：概率越小，倒数越大，取对数后信息量越大。

二维联合空间中：

$$
I(x_i y_j)=-\log p(x_i y_j),\qquad I(x_i|y_j)=-\log p(x_i|y_j)
$$

链式关系为：

$$
I(x_i y_j)=I(x_i)+I(y_j|x_i)=I(y_j)+I(x_i|y_j)
$$

它说明一个联合事件的信息量可以拆成「先知道一个事件的信息量」加上「在此前提下另一个事件的条件信息量」。

<blockquote>易错：自信息是随机事件级别的量；熵才是对整个信源求平均后的量。题目问某个具体符号序列的信息量时，不能直接写 $H(X)$。</blockquote>

### 信息熵与熵函数性质 <span class="tag-must">必考</span>

<span class="kp">信息熵</span>是自信息的数学期望，用来衡量整个信源平均不确定性：

$$
H(X)=E[I(x_i)]=-\sum_{i=1}^{n}p(x_i)\log p(x_i)
$$

它在算「信源平均每发一个符号提供多少信息」。输出前看，它是不确定性；输出后看，它是每个符号平均给出的信息量。

| 性质 | 公式或结论 | 直观理解 |
|---|---|---|
| 对称性 | 概率分量换序，熵不变 | 熵只看概率结构，不看符号名字 |
| 确定性 | $H(1,0,\ldots,0)=0$ | 必然事件没有不确定性 |
| 非负性 | $H(X)\ge 0$ | 平均信息量不能为负 |
| 扩展性 | 加入概率趋近 0 的事件，熵极限不变 | 几乎不发生的符号不改变整体 |
| 上凸性 | 熵是概率分布的上凸函数 | 分布越均匀，不确定性越大 |
| 极值性 | $H(X)\le \log n$，等概时取等号 | $n$ 个符号等可能时熵最大 |

二进制信源常用：

$$
H(p)=-p\log p-(1-p)\log(1-p)
$$

当 $p=0$ 或 $1$ 时熵为 0；当 $p=1/2$ 时熵最大，为 1 bit/符号。

<blockquote>易错：熵相同不代表信源内容相同；它只说明概率分布结构带来的平均不确定性相同。</blockquote>

### 联合熵、条件熵与链规则 <span class="tag-must">必考</span>

联合熵：

$$
H(XY)=-\sum_i\sum_j p(x_i y_j)\log p(x_i y_j)
$$

条件熵：

$$
H(Y|X)=-\sum_i p(x_i)\sum_j p(y_j|x_i)\log p(y_j|x_i)
$$

强可加性：

$$
H(XY)=H(X)+H(Y|X)=H(Y)+H(X|Y)
$$

条件熵的动机是：当 $X$ 已经知道后，$Y$ 还剩多少平均不确定性。联合熵的动机是：把 $X$ 和 $Y$ 看成一个整体时总不确定性是多少。

<blockquote>易错：条件熵不是简单地对 $H(Y|x_i)$ 求算术平均，必须用 $p(x_i)$ 加权。</blockquote>

### 离散无记忆扩展信源 <span class="tag-key">重点</span>

实际消息常由多个符号组成，所以要把单符号信源扩展成长度为 $N$ 的序列信源。若原信源无记忆，则每个序列概率为各符号概率乘积：

$$
P(\alpha)=P(x_{i1}x_{i2}\cdots x_{iN})=\prod_{k=1}^{N}p(x_{ik})
$$

无记忆扩展信源的熵满足：

$$
H(X^N)=NH(X)
$$

这说明独立重复 $N$ 次时，总不确定性线性相加，平均到每个符号仍是 $H(X)$。

<blockquote>易错：$H(X^N)=NH(X)$ 依赖「无记忆/独立」条件。有记忆信源不能直接这样乘。</blockquote>

### 平稳信源、马尔可夫信源与剩余度 <span class="tag-key">重点</span>

平稳有记忆信源的联合熵可按链规则展开：

$$
H(X_1X_2\cdots X_N)=H(X_1)+H(X_2|X_1)+\cdots+H(X_N|X_1\cdots X_{N-1})
$$

平均符号熵：

$$
H_N(X)=\frac{1}{N}H(X_1X_2\cdots X_N)
$$

随着 $N$ 增大，平均符号熵非递增，极限熵表示长期平均每个符号提供的信息量。

<span class="kp">马尔可夫信源</span><span class="exp">是一类有限记忆信源：当前输出只与此前有限个符号有关。$m$ 阶马尔可夫信源只依赖前 $m$ 个符号。</span>若齐次、遍历并进入稳态，其极限熵可由稳态状态概率与符号条件概率计算。

剩余度用于衡量信源还剩多少可压缩冗余：

$$
R=1-\frac{H_\infty}{H_0}
$$

其中 $H_0$ 常表示最大可能熵，$H_\infty$ 表示考虑长期相关后的极限熵。相关性越强，极限熵越低，剩余度越高。

<blockquote>易错：齐次马尔可夫链只说明转移概率不随时间变；它本身不必然是平稳过程。进入稳态后才可按平稳信源处理。</blockquote>

## 第三章 离散信道：信道到底能传多少信息？

第三章从「信源含多少信息」转向「信道传过去多少信息」。核心逻辑是：信道用转移概率描述噪声；输出减少了输入的不确定性，减少的部分就是互信息；在所有输入分布中让互信息最大，就得到信道容量。

### 离散信道模型与信道矩阵 <span class="tag-must">必考</span>

信道数学模型是：

$$
\{X,\;P(Y|X),\;Y\}
$$

其中 $X$ 是输入随机变量，$Y$ 是输出随机变量，$P(Y|X)$ 是信道转移概率，描述输入和输出之间的统计依赖关系。

单符号离散信道的信道矩阵为：

$$
P=
\begin{bmatrix}
p(b_1|a_1)&p(b_2|a_1)&\cdots&p(b_s|a_1)\\
p(b_1|a_2)&p(b_2|a_2)&\cdots&p(b_s|a_2)\\
\vdots&\vdots&\ddots&\vdots\\
p(b_1|a_r)&p(b_2|a_r)&\cdots&p(b_s|a_r)
\end{bmatrix}
$$

每一行对应一个输入符号，行内概率必须相加为 1。

<blockquote>易错：信道矩阵通常是「行表示输入、列表示输出」。行和为 1，不是列和为 1。</blockquote>

### BSC、BEC 与常见信道分类 <span class="tag-freq">高频</span>

二元对称信道 BSC 的矩阵常写为：

$$
P=
\begin{bmatrix}
1-p&p\\
p&1-p
\end{bmatrix}
$$

$p$ 是交叉错误概率。它的特点是两个输入符号被翻转的概率相同。

二元删除信道 BEC 的输出含删除符号「?」：

$$
P=
\begin{bmatrix}
1-p&p&0\\
0&p&1-p
\end{bmatrix}
$$

$p$ 是删除概率，接收端知道「这个符号丢了」，但不知道原来是 0 还是 1。

| 信道类型 | 特点 | 容量抓手 |
|---|---|---|
| 无噪无损 | 输入输出一一对应 | $C=\log r$ |
| 有噪无损 | 一个输入可到多个输出，但不同输入输出集合不交 | $C=\log r$ |
| 无噪有损 | 多个输入可能映射到同一输出 | $C=\log s$ |
| 对称信道 | 每行、每列分别互为排列 | 等概输入达容量 |

### 信道疑义度、噪声熵与平均互信息 <span class="tag-must">必考</span>

<span class="kp">信道疑义度</span>是 $H(X|Y)$，表示接收端收到输出符号后，对输入仍然存在的平均不确定性。它也叫后验熵或损失熵。

<span class="kp">噪声熵</span>是 $H(Y|X)$，表示已知输入后，输出仍因噪声产生的平均不确定性。

平均互信息定义为：

$$
I(X;Y)=\sum_i\sum_j p(x_i y_j)\log\frac{p(x_i y_j)}{p(x_i)p(y_j)}
$$

常用等价形式：

$$
I(X;Y)=H(X)-H(X|Y)=H(Y)-H(Y|X)=H(X)+H(Y)-H(XY)
$$

三种观察角度：

| 角度 | 公式 | 物理意义 |
|---|---|---|
| 接收端看输入 | $I(X;Y)=H(X)-H(X|Y)$ | 收到 $Y$ 后，关于 $X$ 的不确定性减少量 |
| 发送端看输出 | $I(X;Y)=H(Y)-H(Y|X)$ | 输出中扣掉噪声后真正来自输入的信息 |
| 系统整体 | $I(X;Y)=H(X)+H(Y)-H(XY)$ | 系统总不确定性的减少量 |

<blockquote>易错：$H(X|Y)$ 是损失熵/疑义度，$H(Y|X)$ 是噪声熵。二者一般不相等，名字不能互换。</blockquote>

### 平均互信息性质 <span class="tag-key">重点</span>

平均互信息具有：

$$
I(X;Y)\ge 0,\qquad I(X;Y)=I(Y;X)
$$

并且：

$$
I(X;Y)\le H(X),\qquad I(X;Y)\le H(Y)
$$

对固定信道，$I(X;Y)$ 是输入分布 $p(x)$ 的上凸函数，所以存在最优输入分布让它最大；对固定信源，它是信道转移概率的下凸函数。

<blockquote>易错：互信息对 $X,Y$ 是对称的，但信道本身 $P(Y|X)$ 不是对称概念。不要把 $I(X;Y)=I(Y;X)$ 误解成 $P(Y|X)=P(X|Y)$。</blockquote>

### 信道容量 <span class="tag-must">必考</span>

信息传输率定义为：

$$
R=I(X;Y)
$$

在信道确定时，遍历所有可能输入分布，使平均互信息最大：

$$
C=\max_{p(x)} I(X;Y)
$$

<span class="kp">信道容量</span><span class="exp">是信道本身能传输的最大平均信息量，是信道属性，不依赖某一个具体信源分布。</span>

BSC 的容量：

$$
C=1-H(p)
$$

其中 $H(p)=-p\log p-(1-p)\log(1-p)$。当 $p=0$ 时容量为 1；当 $p=1/2$ 时输出与输入无关，容量为 0。

对称信道在输入等概时达到容量，若输出符号数为 $s$，任一行概率为 $(p_1,\ldots,p_s)$：

$$
C=\log s-H(p_1,p_2,\ldots,p_s)
$$

<blockquote>易错：容量是对输入分布取最大值后的结果；某个给定输入分布下算出的 $I(X;Y)$ 不一定等于容量。</blockquote>

### 离散无记忆扩展信道与信道组合 <span class="tag-key">重点</span>

无记忆信道的 $N$ 次扩展中，序列转移概率可分解：

$$
p(\beta|\alpha)=\prod_{k=1}^{N}p(b_k|a_k)
$$

若信源、信道都无记忆：

$$
I(X^N;Y^N)=\sum_{k=1}^{N}I(X_k;Y_k)
$$

若信源有记忆、信道无记忆，则整体互信息不超过逐符号互信息之和；若信源无记忆、信道有记忆，则整体互信息可能大于逐符号互信息之和。

串联信道满足信息不增原则：

$$
H(X)\ge I(X;Y)\ge I(X;Z)\ge \cdots
$$

通过后续信道或数据处理，一般只会增加信息损失，最多保持原有信息，不会凭空增加关于原始输入的信息。

<blockquote>易错：串联信道会让质量变差或不变，不会让关于原输入的平均互信息增加。题目中看到「数据处理后信息更多」通常是陷阱。</blockquote>

### 信源与信道匹配、信道剩余度 <span class="tag-freq">高频</span>

当信源接入信道后，如果实际信息传输率达到信道容量，即：

$$
I(X;Y)=C
$$

就称信源与信道匹配。若达不到，信道存在剩余：

$$
\text{信道剩余度}=C-I(X;Y),\qquad
\text{相对剩余度}=1-\frac{I(X;Y)}{C}
$$

无损信道中，相对剩余度可和信源冗余联系起来：

$$
1-\frac{H(X)}{\log r}
$$

<blockquote>易错：信源剩余度关注源自身冗余；信道剩余度关注实际输入分布有没有把信道容量用满。</blockquote>
"""


QUESTIONS = [
    {"type": "choice", "points": 2, "question": "香农信息论中，一个事件的信息量主要取决于什么？", "options": ["事件发生概率的大小", "事件语义价值的高低", "事件文字描述的长度", "事件是否来自模拟信号"], "answer": 0, "explanation": "<strong>正确答案</strong>：事件发生概率的大小。<br><br><strong>解析</strong>：自信息 $I(x)=-\\log p(x)$，概率越小，发生后消除的不确定性越大。", "pitfall": "不要把语义重要性当成香农信息量。"},
    {"type": "choice", "points": 2, "question": "信源编码器和信道编码器对冗余的基本态度分别是？", "options": ["信源编码去冗余，信道编码加冗余", "二者都尽量去冗余", "二者都尽量加冗余", "信源编码加冗余，信道编码去冗余"], "answer": 0, "explanation": "<strong>正确答案</strong>：信源编码去冗余，信道编码加冗余。<br><br><strong>解析</strong>：前者服务有效性，后者服务可靠性。", "pitfall": "两类冗余服务不同目标，不是互相矛盾。"},
    {"type": "choice", "points": 2, "question": "若 $p(x)=1/8$，以 2 为底时 $I(x)$ 等于多少？", "options": ["3 bit", "1/8 bit", "8 bit", "$-3$ bit"], "answer": 0, "explanation": "<strong>正确答案</strong>：3 bit。<br><br><strong>解析</strong>：$I(x)=-\\log_2(1/8)=3$。", "pitfall": "自信息单位要跟对数底一致。"},
    {"type": "choice", "points": 2, "question": "关于熵 $H(X)$，下列说法最准确的是？", "options": ["它是信源平均自信息", "它是某个具体符号的信息量", "它只由符号名称决定", "它一定等于信宿获得的信息量"], "answer": 0, "explanation": "<strong>正确答案</strong>：它是信源平均自信息。<br><br><strong>解析</strong>：$H(X)=E[I(x_i)]$，刻画整个概率分布的平均不确定性。", "pitfall": "具体符号用自信息，整个信源用熵。"},
    {"type": "choice", "points": 2, "question": "二进制信源何时熵最大？", "options": ["两个符号等概率", "一个符号概率为 1", "两个符号概率都为 0", "概率越偏越大"], "answer": 0, "explanation": "<strong>正确答案</strong>：两个符号等概率。<br><br><strong>解析</strong>：熵函数上凸，分布越均匀不确定性越大，二进制时最大值为 1 bit/符号。", "pitfall": "确定输出时熵为 0，不是最大。"},
    {"type": "choice", "points": 2, "question": "$H(XY)=H(X)+H(Y|X)$ 体现的是熵函数的哪种性质？", "options": ["强可加性", "确定性", "扩展性", "非负性"], "answer": 0, "explanation": "<strong>正确答案</strong>：强可加性。<br><br><strong>解析</strong>：联合熵可拆成先描述 $X$ 的不确定性，再描述已知 $X$ 后 $Y$ 的剩余不确定性。", "pitfall": "独立时才可进一步写成 $H(XY)=H(X)+H(Y)$。"},
    {"type": "choice", "points": 2, "question": "离散无记忆信源的 $N$ 次扩展熵满足什么关系？", "options": ["$H(X^N)=NH(X)$", "$H(X^N)=H(X)/N$", "$H(X^N)=H(X)$", "$H(X^N)=\\log N$"], "answer": 0, "explanation": "<strong>正确答案</strong>：$H(X^N)=NH(X)$。<br><br><strong>解析</strong>：无记忆意味着各符号独立，序列总熵为各次熵之和。", "pitfall": "有记忆信源不能直接乘 $N$。"},
    {"type": "choice", "points": 2, "question": "单符号离散信道矩阵中，每一行概率之和应为多少？", "options": ["1", "0", "输入符号数 $r$", "输出符号数 $s$"], "answer": 0, "explanation": "<strong>正确答案</strong>：1。<br><br><strong>解析</strong>：每行是在给定某个输入 $a_i$ 后所有可能输出的条件概率分布。", "pitfall": "通常行对应输入，列对应输出；不要检查成列和为 1。"},
    {"type": "choice", "points": 2, "question": "信道疑义度通常指哪个量？", "options": ["$H(X|Y)$", "$H(Y|X)$", "$H(XY)$", "$H(X)-H(Y)$"], "answer": 0, "explanation": "<strong>正确答案</strong>：$H(X|Y)$。<br><br><strong>解析</strong>：收到输出 $Y$ 后，对输入 $X$ 仍存在的不确定性称为疑义度或损失熵。", "pitfall": "$H(Y|X)$ 是噪声熵。"},
    {"type": "choice", "points": 2, "question": "信道容量 $C$ 的定义是？", "options": ["对输入分布取最大值的平均互信息", "任意输入分布下的熵 $H(X)$", "信道矩阵所有元素之和", "噪声熵 $H(Y|X)$"], "answer": 0, "explanation": "<strong>正确答案</strong>：对输入分布取最大值的平均互信息。<br><br><strong>解析</strong>：$C=\\max_{p(x)}I(X;Y)$，是信道属性。", "pitfall": "给定分布算出的 $I(X;Y)$ 不一定等于容量。"},
    {"type": "tf", "points": 1, "question": "信息论中的信息量越大，表示消息的语义价值一定越高。", "options": [], "answer": False, "explanation": "<strong>正确答案</strong>：错误。<br><br><strong>解析</strong>：香农信息量只度量概率不确定性的减少，不度量语义价值。", "pitfall": "香农信息的适用范围是概率与通信极限。"},
    {"type": "tf", "points": 1, "question": "无记忆信源一定满足符号序列概率可分解为各符号概率乘积。", "options": [], "answer": True, "explanation": "<strong>正确答案</strong>：正确。<br><br><strong>解析</strong>：这是无记忆信源的核心定义。", "pitfall": "平稳不等于无记忆。"},
    {"type": "tf", "points": 1, "question": "自信息是对整个信源所有事件的信息量求平均。", "options": [], "answer": False, "explanation": "<strong>正确答案</strong>：错误。<br><br><strong>解析</strong>：自信息对应单个事件；熵才是平均自信息。", "pitfall": "看到「平均」优先想到熵。"},
    {"type": "tf", "points": 1, "question": "若一个信源输出完全确定，则它的信息熵为 0。", "options": [], "answer": True, "explanation": "<strong>正确答案</strong>：正确。<br><br><strong>解析</strong>：$H(1,0,\\ldots,0)=0$。", "pitfall": "确定事件自信息也是 0。"},
    {"type": "tf", "points": 1, "question": "$H(Y|X)$ 计算时需要按 $p(x_i)$ 对各条件熵加权。", "options": [], "answer": True, "explanation": "<strong>正确答案</strong>：正确。<br><br><strong>解析</strong>：$H(Y|X)=\\sum_i p(x_i)H(Y|x_i)$。", "pitfall": "不是简单算术平均。"},
    {"type": "tf", "points": 1, "question": "齐次马尔可夫链一定是平稳随机过程。", "options": [], "answer": False, "explanation": "<strong>正确答案</strong>：错误。<br><br><strong>解析</strong>：齐次只说明转移概率与时间起点无关，不保证状态分布已平稳。", "pitfall": "平稳通常可推出齐次条件概率，但反过来不一定。"},
    {"type": "tf", "points": 1, "question": "平均互信息满足 $I(X;Y)=I(Y;X)$。", "options": [], "answer": True, "explanation": "<strong>正确答案</strong>：正确。<br><br><strong>解析</strong>：互信息具有对称性。", "pitfall": "互信息对称不代表信道转移概率对称。"},
    {"type": "tf", "points": 1, "question": "信道容量是信道本身的属性，与具体输入分布无关。", "options": [], "answer": True, "explanation": "<strong>正确答案</strong>：正确。<br><br><strong>解析</strong>：容量已经对输入分布取最大值。", "pitfall": "实际传输率 $I(X;Y)$ 仍依赖输入分布。"},
    {"type": "tf", "points": 1, "question": "BSC 当交叉概率 $p=1/2$ 时容量为 1 bit/符号。", "options": [], "answer": False, "explanation": "<strong>正确答案</strong>：错误。<br><br><strong>解析</strong>：$C=1-H(p)$，$p=1/2$ 时 $H(p)=1$，容量为 0。", "pitfall": "$p=0$ 时才是无噪容量 1。"},
    {"type": "tf", "points": 1, "question": "串联信道或数据处理通常不会增加关于原始输入的平均互信息。", "options": [], "answer": True, "explanation": "<strong>正确答案</strong>：正确。<br><br><strong>解析</strong>：这是信息不增原则或数据处理定理的直观含义。", "pitfall": "处理可以改变表示，但不能凭空增加关于原输入的信息。"},
    {"type": "short", "points": 6, "question": "解释「自信息」和「信息熵」的区别，并写出对应公式。", "options": [], "answer": "自信息 $I(x_i)=-\\log p(x_i)$ 是单个事件发生前的不确定性或发生后提供的信息量；信息熵 $H(X)=-\\sum_i p(x_i)\\log p(x_i)$ 是整个信源的平均自信息，刻画平均不确定性。", "explanation": "<strong>参考答案</strong>：要点是「事件级」和「信源平均级」的区别，并写出两个公式。", "pitfall": "只写公式不解释层级，简答题容易丢分。"},
    {"type": "short", "points": 6, "question": "为什么无记忆扩展信源满足 $H(X^N)=NH(X)$？", "options": [], "answer": "无记忆表示各次输出相互独立，序列概率可分解为单符号概率乘积。由联合熵链规则，独立时联合熵等于各随机变量熵之和；若每次同分布，则 $N$ 项都等于 $H(X)$，所以 $H(X^N)=NH(X)$。", "explanation": "<strong>参考答案</strong>：必须同时说出独立、链规则、同分布三个逻辑点。", "pitfall": "不能脱离无记忆条件直接套公式。"},
    {"type": "short", "points": 6, "question": "区分信道疑义度 $H(X|Y)$ 和噪声熵 $H(Y|X)$。", "options": [], "answer": "$H(X|Y)$ 是收到输出 $Y$ 后，对输入 $X$ 仍然存在的平均不确定性，表示信道中损失的信息；$H(Y|X)$ 是已知输入 $X$ 后，输出 $Y$ 仍因噪声而存在的不确定性，表示噪声带来的随机性。", "explanation": "<strong>参考答案</strong>：接收端看输入是疑义度，发送端看输出是噪声熵。", "pitfall": "两个条件熵方向相反，名称不能互换。"},
    {"type": "short", "points": 6, "question": "写出信道容量定义，并说明它为什么是信道属性。", "options": [], "answer": "$C=\\max_{p(x)}I(X;Y)$。对固定信道，平均互信息随输入概率分布变化；容量是在所有输入分布中取到的最大信息传输率，因此只由信道转移概率所决定，不依赖某一个实际信源分布。", "explanation": "<strong>参考答案</strong>：要写出最大化对象和「固定信道」这个前提。", "pitfall": "不要把 $I(X;Y)$ 和 $C$ 直接画等号。"},
    {"type": "essay", "points": 8, "question": "从通信系统模型说明有效性和可靠性为什么会产生矛盾，以及信源编码、信道编码分别如何处理冗余。", "options": [], "answer": "通信系统中信源产生消息，编码器把消息变成适合信道传输的形式，信道中存在噪声。有效性要求单位资源传更多信息，因此希望去掉信源内部可预测、重复的冗余，信源编码负责压缩。可靠性要求在噪声下仍能恢复消息，因此需要加入校验或纠错冗余，信道编码负责抗干扰。二者看似一个去冗余一个加冗余，但处理的是不同层面的冗余：源冗余应压缩，抗噪冗余是可靠传输的代价。", "explanation": "<strong>参考答案</strong>：逻辑链应包含噪声、有效性、可靠性、信源编码、信道编码。", "pitfall": "不要简单说「编码器提高性能」，要说明两个编码器目标不同。"},
    {"type": "essay", "points": 8, "question": "用熵、条件熵和联合熵解释链规则 $H(XY)=H(X)+H(Y|X)$ 的含义。", "options": [], "answer": "$H(XY)$ 是把 $X,Y$ 作为整体时的平均不确定性。若按顺序描述这个整体，可以先描述 $X$，平均需要 $H(X)$ 的信息量；在 $X$ 已知后，$Y$ 的剩余不确定性为 $H(Y|X)$。两部分相加就是完整描述联合变量所需的平均信息量。若 $X,Y$ 独立，则知道 $X$ 不减少 $Y$ 的不确定性，所以 $H(Y|X)=H(Y)$，链规则退化为 $H(XY)=H(X)+H(Y)$。", "explanation": "<strong>参考答案</strong>：重点是「先描述 X，再描述已知 X 后的 Y」。", "pitfall": "独立是特例，不是链规则成立的前提。"},
    {"type": "essay", "points": 10, "question": "说明平均互信息、信道疑义度、噪声熵和信道容量之间的逻辑关系。", "options": [], "answer": "平均互信息 $I(X;Y)$ 衡量信道实际传过去的平均信息量。站在接收端，$I(X;Y)=H(X)-H(X|Y)$，其中 $H(X|Y)$ 是信道疑义度，表示收到输出后关于输入仍损失的信息；站在发送端，$I(X;Y)=H(Y)-H(Y|X)$，其中 $H(Y|X)$ 是噪声熵，表示已知输入后输出中由噪声造成的不确定性。对固定信道，改变输入分布会改变 $I(X;Y)$；把 $I(X;Y)$ 对所有输入分布取最大，就得到信道容量 $C=\\max_{p(x)}I(X;Y)$。所以互信息是实际传输率，容量是信道可达到的最大传输率。", "explanation": "<strong>参考答案</strong>：应把三个等价公式和最大化定义串起来。", "pitfall": "不要把疑义度和噪声熵混淆，也不要把互信息直接等同容量。"},
    {"type": "comprehensive", "points": 20, "question": "某二元对称信道 BSC 的交叉概率为 $p$，输入等概。请回答：1. 写出信道矩阵；2. 写出平均互信息表达式；3. 求信道容量；4. 分析 $p=0$ 与 $p=1/2$ 两种极端情况；5. 说明为什么输入等概是达到容量的分布。", "options": [], "answer": "1. 信道矩阵为 $P=\\begin{bmatrix}1-p&p\\\\p&1-p\\end{bmatrix}$。2. 输入等概时输出也等概，$H(Y)=1$，噪声熵 $H(Y|X)=H(p)$，所以 $I(X;Y)=1-H(p)$。3. BSC 是强对称信道，等概输入达到容量，因此 $C=1-H(p)$。4. 当 $p=0$ 时无差错，$H(p)=0$，容量为 1 bit/符号；当 $p=1/2$ 时输出与输入独立，$H(p)=1$，容量为 0。5. 对称信道在输入等概时使输出等概，从而 $H(Y)$ 最大，同时每行噪声熵相同，所以平均互信息达到最大。", "explanation": "<strong>参考答案</strong>：综合题应覆盖矩阵、互信息、容量、极端情况和等概最优原因。", "pitfall": "常见错误是把 $p=1/2$ 当成「最随机所以容量最大」，实际此时输入信息全部被噪声淹没。"},
]


CSS = r"""
:root {
  --paper: #fdf6e3;
  --paper-dark: #f5ecd7;
  --ink: #262626;
  --ink-light: #5f6368;
  --accent: #2563eb;
  --divider: #d8c8a8;
  --card-bg: #fffaf0;
  --card-border: #e7d8bf;
  --correct: #15803d;
  --correct-bg: #ecfdf3;
  --wrong: #b91c1c;
  --wrong-bg: #fef2f2;
  --radius: 6px;
}
* { box-sizing: border-box; }
body {
  margin: auto;
  max-width: 900px;
  padding: 24px 20px 64px;
  background: var(--paper);
  color: var(--ink);
  font-family: "Microsoft YaHei", "Noto Sans SC", "SimSun", sans-serif;
  font-size: 12pt;
  line-height: 1.75;
}
h1 { font-size: 1.9rem; line-height: 1.25; margin: 18px 0 20px; }
h2 { margin-top: 34px; padding-bottom: 8px; border-bottom: 1px solid var(--divider); font-size: 1.45rem; }
h3 { margin-top: 24px; font-size: 1.14rem; }
table { width: 100%; border-collapse: collapse; margin: 14px 0; background: var(--card-bg); }
th, td { border: 1px solid var(--card-border); padding: 8px 10px; vertical-align: top; }
th { background: var(--paper-dark); text-align: left; }
blockquote { margin: 14px 0; padding: 10px 14px; border-left: 4px solid #d97706; background: #fff7ed; color: #5f370e; }
.kp { font-weight: 700; color: #111827; }
.exp { color: var(--ink-light); }
.tag-must, .tag-key, .tag-freq, .tag-info {
  display: inline-block; margin-left: 8px; padding: 1px 7px; border-radius: 999px;
  font-size: 0.74em; font-weight: 700; vertical-align: middle;
}
.tag-must { color: #991b1b; background: #fee2e2; }
.tag-key { color: #1d4ed8; background: #dbeafe; }
.tag-freq { color: #166534; background: #dcfce7; }
.tag-info { color: #475569; background: #e2e8f0; }
.topbar { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid var(--divider); padding-bottom: 10px; color: var(--ink-light); }
.brand { font-weight: 700; color: #111827; }
.toc { background: var(--card-bg); border: 1px solid var(--card-border); padding: 12px 16px; border-radius: var(--radius); }
.toc a { color: var(--accent); text-decoration: none; display: block; margin: 2px 0; }
.question-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: var(--radius); padding: 16px; margin: 14px 0; }
.question-card.correct { border-color: var(--correct); background: var(--correct-bg); }
.question-card.wrong { border-color: var(--wrong); background: var(--wrong-bg); }
.q-meta { color: var(--ink-light); font-size: 0.86em; margin-bottom: 6px; }
.option { display: block; border: 1px solid var(--card-border); border-radius: var(--radius); padding: 8px 10px; margin: 8px 0; background: white; cursor: pointer; }
.option.correct-answer { border-color: var(--correct); background: var(--correct-bg); }
.option.wrong-answer { border-color: var(--wrong); background: var(--wrong-bg); }
textarea { width: 100%; min-height: 96px; border: 1px solid var(--card-border); border-radius: var(--radius); padding: 10px; font: inherit; background: white; }
.answer-box { display: none; margin-top: 12px; padding: 10px 12px; border-radius: var(--radius); background: #fff; border: 1px solid var(--card-border); }
.controls { position: sticky; bottom: 0; padding: 12px 0; background: linear-gradient(to top, var(--paper), rgba(253,246,227,0.92)); }
button { border: 0; border-radius: var(--radius); background: var(--accent); color: white; padding: 10px 16px; font-weight: 700; cursor: pointer; }
#score-box { display: none; background: var(--paper-dark); padding: 14px 16px; border-radius: var(--radius); margin: 14px 0; }
#score-num { font-size: 2rem; font-weight: 800; }
@media print {
  body { background: white; font-size: 10.5pt; }
  .no-print, .controls { display: none !important; }
  h1, h2, h3 { page-break-after: avoid; }
}
"""


def slug(text: str) -> str:
    return "".join(ch for ch in text if ch.isalnum())[:24] or "section"


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_ul = False
    in_table = False
    headings: list[tuple[str, str]] = []

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    for raw in lines:
        line = raw.rstrip()
        if not line:
            close_ul()
            close_table()
            continue
        if line.startswith("# "):
            close_ul()
            close_table()
            out.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            close_ul()
            close_table()
            title = line[3:]
            sid = slug(title)
            headings.append((sid, title))
            out.append(f'<h2 id="{sid}">{title}</h2>')
        elif line.startswith("### "):
            close_ul()
            close_table()
            out.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("|"):
            close_ul()
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= {"-", ":"} for c in cells):
                continue
            if not in_table:
                out.append("<table><tbody>")
                in_table = True
                out.append("<tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        elif line.startswith("- "):
            close_table()
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{line[2:]}</li>")
        elif line.startswith("<blockquote>"):
            close_ul()
            close_table()
            out.append(line)
        elif line.startswith("$$"):
            close_ul()
            close_table()
            out.append(line)
        else:
            close_ul()
            close_table()
            out.append(f"<p>{line}</p>")

    close_ul()
    close_table()
    toc = '<div class="toc"><strong>目录</strong>' + "".join(
        f'<a href="#{sid}">{title}</a>' for sid, title in headings
    ) + "</div>"
    body = "\n".join(out)
    return body.replace("<h1>", toc + "\n<h1>", 1)


def page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{html.escape(title)}</title>
<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
  }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"></script>
<style>{CSS}</style>
</head>
<body>
<div class="topbar"><span class="brand">ExamPass</span><span>信息论与编码 | 第 1-3 章</span></div>
{body}
</body>
</html>
"""


def quiz_html() -> str:
    q_json = json.dumps(QUESTIONS, ensure_ascii=False)
    body = f"""
<h1>信息论与编码第 1-3 章章节测试</h1>
<p>满分 100 分。选择题和判断题自动批改 30 分；简答、问答、综合题展示参考答案，用于自评剩余 70 分。</p>
<div id="score-box"><div><span id="score-num">0</span> / 30</div><div>客观题得分</div></div>
<div id="questions-container"></div>
<div class="controls no-print"><button onclick="gradeAll()">提交批改并显示参考答案</button></div>
<script>
const Q = {q_json};
const sections = {{
  choice: '一、选择题',
  tf: '二、判断题',
  short: '三、简答题',
  essay: '四、问答题',
  comprehensive: '五、综合题'
}};
const order = ['choice', 'tf', 'short', 'essay', 'comprehensive'];
function label(i) {{ return String.fromCharCode(65 + i); }}
function refAnswer(q) {{
  if (q.type === 'choice') return label(q.answer) + '. ' + q.options[q.answer];
  if (q.type === 'tf') return q.answer ? '正确' : '错误';
  return q.answer;
}}
function render() {{
  const root = document.getElementById('questions-container');
  let n = 1;
  for (const type of order) {{
    const items = Q.filter(q => q.type === type);
    if (!items.length) continue;
    const h = document.createElement('h2');
    h.textContent = sections[type];
    root.appendChild(h);
    for (const q of items) {{
      const idx = Q.indexOf(q);
      const card = document.createElement('div');
      card.className = 'question-card';
      card.id = 'q-' + idx;
      let inner = `<div class="q-meta">第 ${{n++}} 题 | ${{q.points}} 分</div><div><strong>${{q.question}}</strong></div>`;
      if (q.type === 'choice') {{
        q.options.forEach((opt, oi) => {{
          inner += `<label class="option" id="opt-${{idx}}-${{oi}}"><input type="radio" name="q${{idx}}" value="${{oi}}"> ${{label(oi)}}. ${{opt}}</label>`;
        }});
      }} else if (q.type === 'tf') {{
        inner += `<label class="option" id="opt-${{idx}}-true"><input type="radio" name="q${{idx}}" value="true"> 正确</label>`;
        inner += `<label class="option" id="opt-${{idx}}-false"><input type="radio" name="q${{idx}}" value="false"> 错误</label>`;
      }} else {{
        inner += '<textarea placeholder="在此作答..."></textarea>';
      }}
      inner += `<div class="answer-box" id="ans-${{idx}}"><div>${{q.explanation}}</div><div><strong>参考答案</strong>：${{refAnswer(q)}}</div><blockquote>易错提醒：${{q.pitfall}}</blockquote></div>`;
      card.innerHTML = inner;
      root.appendChild(card);
    }}
  }}
  if (window.MathJax) MathJax.typesetPromise();
}}
function gradeAll() {{
  let score = 0;
  Q.forEach((q, idx) => {{
    const card = document.getElementById('q-' + idx);
    card.classList.remove('correct', 'wrong');
    const ans = document.getElementById('ans-' + idx);
    ans.style.display = 'block';
    if (q.type === 'choice' || q.type === 'tf') {{
      const selected = document.querySelector(`input[name="q${{idx}}"]:checked`);
      const expected = String(q.answer);
      const correctId = q.type === 'choice' ? `opt-${{idx}}-${{q.answer}}` : `opt-${{idx}}-${{expected}}`;
      const correctEl = document.getElementById(correctId);
      if (correctEl) correctEl.classList.add('correct-answer');
      if (selected && selected.value === expected) {{
        score += q.points;
        card.classList.add('correct');
      }} else {{
        card.classList.add('wrong');
        if (selected) {{
          const wrongEl = document.getElementById(q.type === 'choice' ? `opt-${{idx}}-${{selected.value}}` : `opt-${{idx}}-${{selected.value}}`);
          if (wrongEl) wrongEl.classList.add('wrong-answer');
        }}
      }}
    }}
  }});
  document.getElementById('score-num').textContent = score;
  document.getElementById('score-box').style.display = 'block';
  if (window.MathJax) MathJax.typesetPromise();
}}
render();
</script>
"""
    return page("信息论与编码第 1-3 章章节测试", body)


def main() -> None:
    REVIEW_DIR.mkdir(exist_ok=True)
    HTML_DIR.mkdir(exist_ok=True)
    (REVIEW_DIR / "信息论与编码第1-3章期末复习清单.md").write_text(KNOWLEDGE_MD, encoding="utf-8")
    knowledge_body = markdown_to_html(KNOWLEDGE_MD)
    (HTML_DIR / "第1-3章知识清单.html").write_text(page("信息论与编码第 1-3 章知识清单", knowledge_body), encoding="utf-8")
    (HTML_DIR / "第1-3章章节测试.html").write_text(quiz_html(), encoding="utf-8")


if __name__ == "__main__":
    main()
