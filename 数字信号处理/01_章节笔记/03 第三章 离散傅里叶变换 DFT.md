# 第三章 离散傅里叶变换 DFT

本章主线：DTFT 的频率变量是连续的，不方便计算机直接处理；DFT 把有限长序列放到周期框架里，在单位圆上取有限个频率采样点。

## 傅里叶变换的几种形式

| 时域信号 | 频域形式 | 典型变换 |
|---|---|---|
| 连续非周期 | 连续非周期 | 连续时间傅里叶变换 |
| 连续周期 | 离散非周期 | 连续时间傅里叶级数 |
| 离散非周期 | 连续周期 | DTFT |
| 离散周期 | 离散周期 | DFS |

DFT 处理的是有限长序列。它的关键做法是：把有限长序列看作周期序列的一个主值区间。

## 离散傅里叶级数 DFS

### 离散周期序列的表示

离散周期序列 $\tilde{x}(n)$ 的周期为 $N$，可以分解为有限个离散复指数的线性组合：

$$
\tilde{x}(n)=\frac{1}{N}\sum\limits_{k=0}^{N-1}\tilde{X}(k)e^{j\frac{2\pi}{N}kn}
$$

因为：

$$
e^{j\frac{2\pi}{N}(k+iN)n}=e^{j\frac{2\pi}{N}kn}e^{j2\pi in}=e^{j\frac{2\pi}{N}kn}
$$

所以只需要 $0\sim N-1$ 这 $N$ 个谐波。

### DFS 定义

$$
\tilde{X}(k)=DFS[\tilde{x}(n)]
=\sum\limits_{n=0}^{N-1}\tilde{x}(n)e^{-j\frac{2\pi}{N}kn}
$$

$$
\tilde{x}(n)=IDFS[\tilde{X}(k)]
=\frac{1}{N}\sum\limits_{k=0}^{N-1}\tilde{X}(k)e^{j\frac{2\pi}{N}kn}
$$

令：

$$
W_N=e^{-j\frac{2\pi}{N}}
$$

则：

$$
\tilde{X}(k)=\sum\limits_{n=0}^{N-1}\tilde{x}(n)W_N^{kn}
$$

$$
\tilde{x}(n)=\frac{1}{N}\sum\limits_{k=0}^{N-1}\tilde{X}(k)W_N^{-kn}
$$

> 注意：原笔记里 IDFS 的旋转因子应写为 $W_N^{-kn}$，不是 $W_n^{-kn}$。

### $W_N$ 的性质

- 共轭对称性：

$$
W_N^n=(W_N^{-n})^*
$$

- 周期性：

$$
W_N^{n}=W_N^{n+iN}
$$

- 可约性：

$$
W_N^{in}=W_{N/i}^{n}
$$

- 正交性：

$$
\frac{1}{N}\sum\limits_{k=0}^{N-1}W_N^{nk}(W_N^{mk})^*
=
\begin{cases}
1,& n-m=iN\\
0,& n-m\ne iN
\end{cases}
$$

## DFS 的性质

### 线性

$$
a\tilde{x}_1(n)+b\tilde{x}_2(n)
\Leftrightarrow
a\tilde{X}_1(k)+b\tilde{X}_2(k)
$$

### 时域移位

$$
\tilde{x}(n+m)\Leftrightarrow \tilde{X}(k)W_N^{-mk}
$$

### 频域移位

$$
W_N^{nl}\tilde{x}(n)\Leftrightarrow \tilde{X}(k+l)
$$

### 对偶性

$$
\tilde{x}(n)\Leftrightarrow \tilde{X}(k)
$$

$$
\tilde{X}(n)\Leftrightarrow N\tilde{x}(-k)
$$

### 周期卷积

DFS 中的卷积默认在一个周期内进行。

若：

$$
\tilde{y}(n)=\sum\limits_{m=0}^{N-1}\tilde{x}_1(m)\tilde{x}_2(n-m)
$$

则：

$$
\tilde{y}(n)\Leftrightarrow \tilde{X}_1(k)\tilde{X}_2(k)
$$

> 易错点：DFS 里所有序列都是周期序列，所以移位、翻转、卷积都要按周期意义理解。

## 离散傅里叶变换 DFT

### 从 DFS 到 DFT

若有限长序列 $x(n)$ 只在 $0\le n\le N-1$ 内非零：

$$
x(n)=
\begin{cases}
x(n),& 0\le n\le N-1\\
0,& otherwise
\end{cases}
$$

把 $x(n)$ 看成周期为 $N$ 的周期序列 $\tilde{x}(n)$ 的一个主值区间：

$$
\tilde{x}(n)=\sum\limits_{r=-\infty}^{\infty}x(n+rN)
$$

在 $0\sim N-1$ 上使用 DFS，就得到 N 点 DFT：

$$
X(k)=\sum\limits_{n=0}^{N-1}x(n)W_N^{nk},\quad 0\le k\le N-1
$$

$$
x(n)=\frac{1}{N}\sum\limits_{k=0}^{N-1}X(k)W_N^{-nk},\quad 0\le n\le N-1
$$

一句话：DFT 是有限长序列周期延拓后的 DFS 主值。

### DFT 与 DTFT / Z 变换

如果 $x(n)$ 的 DTFT 为 $X(e^{j\omega})$，则 N 点 DFT 可以看成在单位圆上等间隔采样：

$$
X(k)=X(e^{j\omega})|_{\omega=\frac{2\pi}{N}k}
$$

也可以写成：

$$
X(k)=X(z)|_{z=e^{j\frac{2\pi}{N}k}}
$$

> 注意：DFT 不是整个 DTFT，只是 $N$ 个采样点。

## DFT 的性质

### 线性

$$
x_3(n)=ax_1(n)+bx_2(n)
\Leftrightarrow
X_3(k)=aX_1(k)+bX_2(k)
$$

若 $x_1(n)$ 长度为 $N_1$，$x_2(n)$ 长度为 $N_2$，则至少按：

$$
N=\max(N_1,N_2)
$$

补零后计算。

### 圆周移位

长度为 $N$ 的序列圆周移位定义为：

$$
x_m(n)=x((n+m))_NR_N(n)
$$

含义：先周期延拓，再移位，最后取 $0\le n\le N-1$ 的主值区间。

时域圆周移位：

$$
x((n+m))_NR_N(n)\Leftrightarrow X(k)W_N^{-km}
$$

频域圆周移位：

$$
x(n)W_N^{nl}\Leftrightarrow X((k+l))_NR_N(k)
$$

由频移可得：

$$
DFT\left[x(n)\cos\left(\frac{2\pi nl}{N}\right)\right]
=\frac{1}{2}[X((k-l))_N+X((k+l))_N]R_N(k)
$$

$$
DFT\left[x(n)\sin\left(\frac{2\pi nl}{N}\right)\right]
=\frac{1}{2j}[X((k-l))_N-X((k+l))_N]R_N(k)
$$

> 易错点：$x((n+m))_N$ 不是普通移位。移出去的一端会从另一端绕回来。

### 对偶性

$$
x(n)\Leftrightarrow X(k)
$$

$$
X(n)\Leftrightarrow N x((-k))_NR_N(k)
$$

### 帕塞瓦定理

$$
\sum\limits_{n=0}^{N-1}|x(n)|^2
=\frac{1}{N}\sum\limits_{k=0}^{N-1}|X(k)|^2
$$

### 序列的和

$$
X(0)=\sum\limits_{n=0}^{N-1}x(n)
$$

$X(0)$ 是直流分量，也就是一个周期内所有样值之和。

### 序列初始值

$$
x(0)=\frac{1}{N}\sum\limits_{k=0}^{N-1}X(k)
$$

## 圆周共轭对称性

圆周共轭对称分量：

$$
x_{ep}(n)=\frac{1}{2}[x((n))_N+x^*((N-n))_N]R_N(n)
$$

圆周共轭反对称分量：

$$
x_{op}(n)=\frac{1}{2}[x((n))_N-x^*((N-n))_N]R_N(n)
$$

共轭性质：

$$
x^*(n)\Leftrightarrow X^*((N-k))_NR_N(k)
$$

复数序列的 DFT：

$$
Re[x(n)]\Leftrightarrow X_{ep}(k)
$$

$$
jIm[x(n)]\Leftrightarrow X_{op}(k)
$$

$$
x_{ep}(n)\Leftrightarrow Re[X(k)]
$$

$$
x_{op}(n)\Leftrightarrow jIm[X(k)]
$$

若 $x(n)$ 是实序列：

$$
X(k)=X^*((N-k))_NR_N(k)
$$

也就是：

- $Re[X(k)]$ 为圆周偶对称。
- $Im[X(k)]$ 为圆周奇对称。
- $|X(k)|$ 为圆周偶对称。
- $\arg[X(k)]$ 为圆周奇对称。

> 易错点：DTFT 中的 $-\omega$，到 DFT 中对应的是圆周意义下的 $(N-k)_N$。

## 圆周卷积

### 定义

N 点圆周卷积：

$$
y(n)=x_1(n)\circledast_N x_2(n)
$$

$$
y(n)=\sum\limits_{m=0}^{N-1}x_1(m)x_2((n-m))_NR_N(n)
$$

DFT 对应关系：

$$
x_1(n)\circledast_N x_2(n)\Leftrightarrow X_1(k)X_2(k)
$$

### 圆周卷积与线性卷积

若 $x_1(n)$ 长度为 $N_1$，$x_2(n)$ 长度为 $N_2$，线性卷积长度为：

$$
N_1+N_2-1
$$

要让 N 点圆周卷积等于线性卷积，需要补零使：

$$
N\ge N_1+N_2-1
$$

若 $N$ 不足，线性卷积的尾部会折回前面，产生时域混叠。

### 用 DFT 计算线性卷积

1. 确定线性卷积长度 $L=N_1+N_2-1$。
2. 选取 $N\ge L$，通常取便于 FFT 的长度。
3. 将两个序列都补零到 $N$ 点。
4. 分别做 DFT，频域相乘。
5. 做 IDFT 得到线性卷积结果。

## 抽样 Z 变换与频域抽样理论

### 频域采样

对 $X(z)$ 在单位圆上等间隔采样：

$$
X(k)=X(z)|_{z=e^{j\frac{2\pi}{N}k}},\quad k=0,1,\ldots,N-1
$$

这就是 DFT 的频域采样观点。

### 频域采样定理

若对序列 $x(n)$ 的 DTFT 进行 N 点频域采样，再做 IDFT，得到：

$$
x_N(n)=\sum\limits_{r=-\infty}^{\infty}x(n+rN)
$$

也就是时域的周期叠加。

若 $x(n)$ 长度为 $M$，且：

$$
N\ge M
$$

则一个周期内不会发生时域混叠，可以由 $X(k)$ 恢复原有限长序列。

> 易错点：频域采样会导致时域周期延拓。采样点数不够时，时域会混叠。

## DFT 的应用

### 频谱分析

用 DFT 分析连续信号通常经历：

$$
x_a(t)\rightarrow x(n)\rightarrow x_N(n)\rightarrow X(k)
$$

也就是：

1. 连续信号采样。
2. 截取有限长度数据。
3. 对有限长序列做 DFT。

常见误差：

| 误差 | 原因 | 改进 |
|---|---|---|
| 混叠 | 采样频率不足 | 提高 $f_s$，采样前加抗混叠低通滤波 |
| 泄漏 | 截断导致频谱扩散 | 增加记录长度，选合适窗函数 |
| 栅栏效应 | 频域只观察有限个采样点 | 补零增大 DFT 点数，提高频率采样密度 |

### 补零的作用

- 时域补零不会增加原始信息量。
- 补零会增加 DFT 频率采样点数，使频谱曲线看起来更细。
- 补零到足够长度可以避免圆周卷积中的时域混叠。

## 本章自查问题

1. DFS 和 DFT 的区别是什么？
2. 为什么 DFT 隐含周期延拓？
3. $W_N$ 的周期性、共轭对称性、可约性分别有什么用？
4. 圆周移位和普通移位有什么区别？
5. $X(0)$ 和 $x(0)$ 分别可以由 DFT 怎样求？
6. 实序列的 DFT 为什么满足圆周共轭对称？
7. 圆周卷积等于线性卷积的补零条件是什么？
8. 频域采样为什么会导致时域周期延拓？
9. 混叠、泄漏、栅栏效应分别来自哪里？

## 待补位置

- 圆周移位的画图例题。
- 圆周卷积的矩阵法或列表法例题。
- 频域采样定理的推导细节。
- DFT 频谱分析的 MATLAB / Python 小例子。
