# 信源

## 有记忆/无记忆信源

- 消息之间是否有依赖关系
- 无记忆：$P(\overline{X})=P(X_{1}X_{2}\ldots X_{N})=P(X_{1})P(X_{2})\ldots P(X_{N})$
- 有记忆：如有的信息依赖于之前的信息
## 平稳/非平稳信源

- 统计特性是否**保持不变** 
- 若平稳，任意维度的联合概率都与时间起点无关
- $P(X_{i})={(X_{j})}$
- $P(X_{i}X_{i+1}\ldots X_{i+N})={P(X_{j}X_{j+1}\ldots X_{j+N})}$

## 信源

- 我们用随机变量描述信源，本课只讨论离散信源
$$
\begin{bmatrix}X\\P(X)\end{bmatrix}=\begin{bmatrix}X=x_{1}&\ldots& X=x_{i} & \ldots &X=x_{n}\\ p(x_{1})&\ldots & p(x_{i})&\ldots&p(x_{n})\end{bmatrix}
$$
- $\sum\limits p(x_{i})=1$
# 信息熵

## 自信息
$$
I(x_{i})=-\log p(x_{i})=\log \frac{1}{p(x_{i})}
$$
- 物理意义：
	- 事件发生前：事件发生的不确定性的大小
	- 事件发生后：事件中所含有的信息量
	- 理想信道中：收信者接受消息后所获取的信息量
- 单位：比特（bit）

- 联合自信息：
$$
I(x_{i}y_{j})=-\log p(x_{i}y_{j})
$$
- 条件自信息：
$$
I(x_{i}|y_{j})=-\log p(x_{i}|y_{j})
$$
- 我们有：
$$
\begin{aligned}I(x_{i}y_{j})=-\log p(x_{i}y_{j})&=-\log p(x_{i})p(y_{j}|x_{i})=I(x_{i})+I(y_{j}|x_{i})\\&=-\log p(y_{j})p(x_{i}|y_{j})=I(y_{j})+I(x_{i}|y_{j})\end{aligned}
$$
## 信息熵

- 自信息是对一个随机事件而言
- 信息熵是定义整个信源的不确定度，即平均自信息，是信源所有事件自信息的期望
$$
H(X)=E[I(x_{i})]=\sum\limits_{i=1}^{n}p(x_{i})I(x_{i})=-\sum\limits_{i=1}^{n}p(x_{i})\log p(x_{i})
$$
- 单位：比特/符号（bit/symbol）

- 在信源输出前：表示的是信源的平均不确定性
- 在信源输出后：表示的是每个消息符号给出的平均消息量
- 也可以表示变量 $X$ 的随机性的大小、最小描述复杂度
# 信息熵的性质
## 对称性

- 对于概率矢量 $P(p_{1},p_{2},\ldots,p_{q})$ 的其他任意排列，熵函数不变
- 熵只与随机变量的总体结构有关，与信源的总体统计特性有关
- 如果某些信源的统计特性相同（含有的符号数和概率分布相同），那么这些信源的熵就相同
## 确定性
$$
H(1,0)=H(1,0,0)=\ldots=H(1,0,\ldots,0)=0
$$
- 在概率空间中，只要有一个事件是必然发生事件，那么其它事件必然是不可能事件，因此该信源没有不确定性，其熵必为 $0$
## 非负性
$$
H(P)=H(p_{1},p_{2},\ldots,p_{q})\ge 0
$$
## 扩展性
$$
\lim_{\varepsilon \rightarrow 0}H(p_{1},p_{2}\ldots,p_{q}-\varepsilon,\varepsilon)=H(p_{1},p_{2},\ldots,p_{q})
$$
- 增加一个概率接近于零的事件，信源熵保持不变
## 强可加性

- 若我们有两个**相互关联**的随机变量 $X$ 和 $Y$
$$
\begin{bmatrix}X\\P(X)\end{bmatrix}=\begin{bmatrix}x_{1}&x_{2}&\ldots&x_{n}\\p(x_{1})&p(x_{2})&\ldots&p(x_{n})\end{bmatrix}\quad 0\le p(x_{i})\le L \quad \sum\limits_{i=1}^{n}p(x_i)=1 
$$
$$
\begin{bmatrix}Y\\P(Y)\end{bmatrix}=\begin{bmatrix}y_{1}&y_{2}&\ldots&y_{n}\\p(y_{1})&p(y_{2})&\ldots&p(y_{n})\end{bmatrix}\quad 0\le p(y_{i})\le L \quad \sum\limits_{i=1}^{n}p(y_i)=1 
$$
- 相互关联表示 $p(x_{i}y_{j})=p(x_{i})p(y_{j}|x_{i})$
- 我们推导 $H(XY)$ ：
$$
\begin{aligned}
H(XY)&=-\sum\limits_{i}\sum\limits_{j}p(x_{i}y_{j})\log p(x_{i}y_{j})
\\&=-\sum\limits_{i}\sum\limits_{j}p(x_{i}y_{j})\log p(x_{i})-\sum\limits_{i}\sum\limits_{j}p(x_{i}y_{j})\log p(y_{j}|x_{i})
\\&=-\sum\limits_{i}p(x_{i})\log p(x_{i})\sum\limits_{j}p(y_{j}|x_{i})-\sum\limits_{i}p(x_{i})\sum\limits_{j}p(y_{j}|x_{i})\log p(y_{j}|x_{i})
\\&=-\sum\limits_{i}p(x_{i})\log p(x_{i})-\left\{\sum\limits p(x_{i})\left[-\sum\limits_{j}p(y_{j}|x_{i})\log p(y_{j}|x_{i})\right] \right\}
\\&=H(X)+\sum\limits_{i}p(x_{i})H(Y|x_{i})
\\&=H(X)+H(Y|X)
\end{aligned}
$$
- 从上我们可以定义出：
- 联合熵：
$$
H(XY)=E[I(x_{i}y_{j})]=\sum\limits_{XY}p(x_{i}y_{j})\times I(x_{i}y_{j})=-\sum\limits_{XY}p(x_{i}y_{j})\log p(x_{i}y_{j})
$$
- 物理意义：表明在 $X$ 和 $Y$ 相关联的情况下，信源($XY$)每发一个符号所能提供的平均信息量等于信源 $X$ 每发一个符号所能提供的平均信息量，再加上在 $X$ 已知的条件下，信源 $Y$ 再发一个符号所提供的平均信息量

- **条件熵**：
$$
H(Y|X)=E[I(y_{j}|x_{i})]=\sum\limits_{XY}\underline{p(x_{i}y_{j})}\times I(y_{j}|x_{i})=-\sum\limits_{XY}p(x_{i}y_{j})\log p(y_{j}|x_{i})
$$
- 物理意义：从 $X$ 中平均每发一个符号的前提下，从 $Y$ 中平均每发一个符号额外能提供的信息量；已知（已收到）集合 $X$ 后，对集合 $Y$ 仍然存在（或剩余）的平均不确定性

- 对于条件熵，我们也常用这个公式：
$$
H(Y|X)=\sum\limits_{i}p(x_{i})H(Y|x_{i})
$$
- 若 $X$ 与 $Y$ 相互独立：
$$
H(XY)=H(X)+H(Y)
$$
- 链式规则：
$$
H(X_{1}X_{2}\ldots X_{N})=H(X_{1})+H(X_{2}|X_{1})+H(X_{3}|X_{1}X_{2})+\ldots+H(X_{N}|X_{1}X_{2}\ldots X_{N-1})
$$
## 上凸性

- 结论：熵函数是严格上凸函数
### 证明

> [!info] 引理：詹森不等式
> 若 $f(x)$ 是定义在区间 $[a,b]$ 上的实值连续上凸函数，则对于任意一组 $x_1,x_2,\ldots,x_{q}\in [a,b]$ 和任意一组非负实数 $\lambda_{1},\lambda_{2},\ldots,\lambda_{q}$ 满足 $\sum\limits_{k=1}^{q}\lambda_{k}=1$ ，我们有
> $$f\left[\sum\limits_{k=1}^{q}\lambda_{k}x_{k}\right]\ge \sum\limits_{k=1}^{q}\lambda_{k}f(x_{k})$$

- 对于詹森不等式我们也可以这样子解读：对于一个凸函数而言，期望的函数大于等于函数的期望
$$
f(E[x_{i}])\ge E[f(x_{i})]
$$
- 在熵函数中，$f()=\log()$ ，易得 $\log(x)$ 为上凸函数，所以有
$$
\log(E[x])\ge E[\log x]
$$
- 那么我们就可以得到 $H(X)$ 为上凸函数
## 极值性

- 最大离散熵定理：对于一个输出 $n$ 各不同信息符号的离散无记忆信源，当且仅当各个符号出现概率相等时（即 $p_{i}=\frac{1}{n}$），熵最大
$$
H(P)=H(p_{1},p_{2},\ldots,p_{n})\le H\left( \frac{1}{n}, \frac{1}{n},\ldots , \frac{1}{n} \right)=\log n
$$
# 离散无记忆信源
## 扩展信源

- 我们有一个随机矢量/随机序列，我们假定：
	- 符号序列中符号彼此无关（无记忆）
	- 符号序列中各符号取自同一符号集（相同概率空间）
$$
X=X_{1}X_{2}X_{3}\ldots
$$
- 可以建立数学模型：$N$ 次扩展信源模型
$$
\begin{bmatrix}X^{N}\\P(\overrightarrow{X})\end{bmatrix}=\begin{bmatrix}\alpha_{1}&\ldots&\alpha_{q^{N}}\\p(\alpha_{1})&\ldots&p(\alpha_{q^{N}})\end{bmatrix}
$$
- 其中：$p(\alpha_{i})=p(x_{i_{1}})p(x_{i_{2}})\ldots p(x_{i_{N}})=\prod p_{i_{k}}$
- 信源 $X$ 与扩展信源 $X^{N}$ 之间的关系：
$$
H(X^{N})=NH(X)
$$
# 离散平稳信源

- 实际生活中大部分信源为有记忆信源，为了便于研究，我们假定在一个短时间内，信源为平稳信源

## 核心物理量

- **联合熵（矢量熵）**：信源平均每发送一个长度为 $N$ 的消息序列所提供的信息量
$$
H(\vec{X})=H(X_{1}X_{2}\ldots X_{N})
$$
- **平均符号熵**：当序列长度为 $N$ 时，信源平均每发出一个符号提供的信息量
$$
H_{N}(\vec{X})=\frac{1}{N}H(X_{1}X_{2}\ldots X_{N})
$$
- **极限熵（熵率）**：当记忆长度无限延伸时，平均符号熵的极限值
$$
H_{\infty}=\lim_{N\to \infty}H_{N}(\vec{X})
$$

## 三条基本性质

1. 随着已知关联历史（条件）的增长，各阶条件熵单调递减：
$$
H(X_{N}|X_{1}\ldots X_{N-1})\le H(X_{N-1}|X_{1}\ldots X_{N-2})
$$
2. 在记忆长度相同时，平均符号熵大于等于最新一阶的条件熵：
$$
H_{N}(\vec{X})\ge H(X_{N}|X_{1}\ldots X_{N-1})
$$
3. 平均符号熵随 $N$ 增加是非递增的，且有界：
$$
H_{N}(\vec{X})\le H_{N-1}(\vec{X}),\quad 0\le H_{N}(\vec{X})\le H_{1}(X)<\infty
$$

## 极限熵的存在性与求法

- 对于任意离散平稳信源，只要 $H_{1}(X)<\infty$，极限熵必然存在：
$$
H_{\infty}=\lim_{N\to \infty}H_{N}(\vec{X})=\lim_{N\to \infty}H(X_{N}|X_{1}\ldots X_{N-1})
$$
- 若信源的记忆深度为有限的 $m$ 阶（$m+1$ 维平稳信源），当 $N\ge m+1$ 时极限熵退化为有限阶条件熵：
$$
H_{\infty}=H(X_{m+1}|X_{1}X_{2}\ldots X_{m})
$$

# 马尔可夫信源

- 某一时刻发出某一符号的概率，仅与此前发出的有限个符号有关
- $m$ 阶马氏信源：当前符号仅依赖于前 $m$ 个符号

## 马尔可夫链与状态转移矩阵

- **时齐马氏链**：状态转移概率不随时间起点发生改变
$$
p_{ij}(m)=P(X_{m+1}=S_{j}|X_{m}=S_{i})=p_{ij}
$$
- **一步转移概率矩阵** $P$：
$$
P=\begin{bmatrix}p_{11}&p_{12}&\ldots&p_{1J}\\p_{21}&p_{22}&\ldots&p_{2J}\\\vdots&\vdots&\ddots&\vdots\\p_{J1}&p_{J2}&\ldots&p_{JJ}\end{bmatrix}
$$
- 性质：每个元素非负，各行元素之和为 1（$\sum_{j}p_{ij}=1$）

- **C-K 方程**：对于时齐马氏链，$k$ 步转移概率由一步转移概率完全决定
$$
P^{(k)}=P^{k}
$$

## 各态历经性与稳态分布

- **遍历性条件**：有限状态的时齐马氏链不可约、非周期，且存在 $r$ 使 $P^{r}$ 中所有元素均大于 0
- 遍历马氏链在 $n\to\infty$ 时，状态概率收敛到与初始分布无关的稳态分布 $W=[W_{1},W_{2},\ldots,W_{J}]$
- **稳态分布求解**：
$$
\begin{cases}WP=W\\\sum\limits_{j=1}^{J}W_{j}=1\end{cases}
$$

## $m$ 阶马氏信源的极限熵

- $m$ 阶马氏信源等效为有 $q^{m}$ 个状态的时齐马氏链，达到稳态后：
$$
H_{\infty}=-\sum_{i=1}^{J}P(S_{i})\sum_{k=1}^{q}p(x_{k}|S_{i})\log p(x_{k}|S_{i})
$$
- $P(S_{i})$：状态 $S_{i}$ 的平稳概率（由 $WP=W$ 解得）
- $p(x_{k}|S_{i})$：在状态 $S_{i}$ 下输出符号 $x_{k}$ 的条件概率

## 标准解题步骤

1. 由条件概率表写出一步状态转移矩阵 $P$，画出状态转移图
   - 注意区分"符号条件概率"与"状态转移"——状态转移必须满足符号拼接逻辑
2. 验证极限分布是否存在：计算 $P^{2}$ 或 $P^{3}$，检查是否所有元素大于 0
3. 联立 $WP=W$ 与 $\sum W_{i}=1$ 求解稳态概率分布 $W$
4. 套用极限熵公式求 $H_{\infty}$
5. （如需）利用全概率公式计算平稳后的单符号极限分布：
$$
P(x_{k})=\sum_{S_{i}}P(S_{i})P(x_{k}|S_{i})
$$

# 信源的相关性与冗余度

## 相关性对熵的影响

- 不同记忆长度下，同一信源的熵满足：
$$
H_{0}\ge H_{1}\ge H_{2}\ge\ldots\ge H_{m+1}\ge\ldots\ge H_{\infty}
$$
- $H_{0}=\log q$：无记忆等概率下的最大熵
- $H_{1}$：无记忆但考虑符号实际分布概率
- $H_{m}$：考虑前 $m-1$ 个符号关联的条件熵
- $H_{\infty}$：实际信源熵

- **核心结论**：符号间相关性越大，信源的实际有效熵 $H_{\infty}$ 就越小

## 冗余度

- 实际信源存在相关性，若只用 $H_{1}$ 甚至 $H_{0}$ 的方案传输，会造成传输资源的富余——即可压缩空间
- **熵的相对率**：
$$
\eta=\frac{H_{\infty}}{H_{0}}
$$
- **信源冗余度（剩余度）**：
$$
R=1-\eta=\frac{H_{0}-H_{\infty}}{H_{0}}
$$

## 自然语言（英文）冗余度实例

- $q=27$（26 个字母 + 1 个空格）
- $H_{0}=\log_{2}27\approx 4.76\text{ bit/symbol}$
- $H_{1}\approx 4.03\text{ bit/symbol}$（考虑字母出现概率）
- $H_{\infty}\approx 1.4\text{ bit/symbol}$（高阶马氏信源逼近）
- 冗余度：$R=\frac{4.76-1.4}{4.76}\approx 71\%$

- **物理意义**：
  - 英文文章中 $71\%$ 由语言结构规范（语法、拼写习惯）决定，写作者自由选择的部分仅占 $29\%$
  - 通过无失真信源编码，理论上可压缩掉 $71\%$ 的体积
  - **冗余度的双重作用**：降低传输效率，但赋予语言抗干扰能力——收信者可根据上下文纠错