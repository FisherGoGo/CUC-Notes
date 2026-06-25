# 第二章 Z 变换与 DTFT 变换

本章主线：Z 变换从整个复平面观察序列，DTFT 是在单位圆上观察序列的频率成分；系统函数、收敛域和频率响应都围绕这条关系展开。

## Z 变换

### 定义

双边 Z 变换：

$$
X(z)=Z[x(n)]=\sum\limits_{n=-\infty}^{\infty}x(n)z^{-n}
$$

反变换：

$$
x(n)=Z^{-1}[X(z)]
$$

其中 $z$ 是复变量，常写为：

$$
z=re^{j\omega}
$$

所以：

$$
z^{-n}=r^{-n}e^{-j\omega n}
$$

- $r$ 控制收敛半径。
- $\omega$ 控制频率角度。

### 收敛域 ROC

Z 变换不仅要写 $X(z)$，还要说明收敛域 ROC。

- 右边序列的 ROC 通常在最外极点之外。
- 左边序列的 ROC 通常在最内极点之内。
- 双边序列的 ROC 通常在两个极点之间。
- ROC 内不能包含极点。

> 易错点：同一个代数表达式 $X(z)$，如果 ROC 不同，对应的时域序列可能不同。

### Z 变换与 DTFT 的关系

当单位圆 $|z|=1$ 位于 ROC 内时，可以令：

$$
z=e^{j\omega}
$$

得到：

$$
X(e^{j\omega})=X(z)|_{z=e^{j\omega}}
$$

也就是说，DTFT 是 Z 变换在单位圆上的取值。

## 离散时间傅里叶变换 DTFT

### 定义

$$
X(e^{j\omega})=DTFT[x(n)]=\sum\limits_{n=-\infty}^{\infty}x(n)e^{-j\omega n}
$$

$$
x(n)=IDTFT[X(e^{j\omega})]=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}d\omega
$$

对应关系：

| 时域 | 频域 |
|---|---|
| 离散 | $2\pi$ 周期 |
| 非周期 | 连续 |

因为：

$$
e^{-j(\omega+2\pi)n}=e^{-j\omega n}e^{-j2\pi n}=e^{-j\omega n}
$$

所以：

$$
X(e^{j(\omega+2\pi)})=X(e^{j\omega})
$$

> 注意：DTFT 的频率变量 $\omega$ 是连续变量，但频谱以 $2\pi$ 为周期。

### 变换存在条件

常用充分条件：

$$
\sum\limits_{n=-\infty}^{\infty}|x(n)|<\infty
$$

即序列绝对可和。

能量有限条件：

$$
\sum\limits_{n=-\infty}^{\infty}|x(n)|^2<\infty
$$

能量有限序列的 DTFT 可按能量意义讨论，考试中一般优先记绝对可和这个充分条件。

## DTFT 的性质

些许性质证明：[[Proof/DTFT性质证明]]

| 性质 | 时域 | 频域 |
|---|---|---|
| 线性 | $ax(n)+by(n)$ | $aX(e^{j\omega})+bY(e^{j\omega})$ |
| 时移 | $x(n-m)$ | $e^{-j\omega m}X(e^{j\omega})$ |
| 频移 | $e^{j\omega_0n}x(n)$ | $X(e^{j(\omega-\omega_0)})$ |
| 反转 | $x(-n)$ | $X(e^{-j\omega})$ |
| 共轭 | $x^*(n)$ | $X^*(e^{-j\omega})$ |

### 时域卷积

$$
x(n)*h(n)\Leftrightarrow X(e^{j\omega})H(e^{j\omega})
$$

### 时域相乘

$$
x(n)h(n)\Leftrightarrow \frac{1}{2\pi}X(e^{j\omega})*H(e^{j\omega})
$$

这里右边的卷积是关于频率变量 $\omega$ 的周期卷积。

### 微分性质

$$
nx(n)\Leftrightarrow j\frac{d}{d\omega}X(e^{j\omega})
$$

推导直觉：

$$
\frac{d}{d\omega}e^{-j\omega n}=-jne^{-j\omega n}
$$

所以乘上 $n$ 会转化为频域微分。

### 帕塞瓦定理

$$
\sum\limits_{n=-\infty}^{\infty}|x(n)|^2=
\frac{1}{2\pi}\int_{-\pi}^{\pi}|X(e^{j\omega})|^2d\omega
$$

含义：时域能量和频域能量一致，只是频域积分前有归一化因子 $\dfrac{1}{2\pi}$。

## 对称性

### 共轭对称与共轭反对称序列

共轭对称序列：

$$
x_e(n)=x_e^*(-n)
$$

共轭反对称序列：

$$
x_o(n)=-x_o^*(-n)
$$

任意序列总能分解为：

$$
x(n)=x_e(n)+x_o(n)
$$

其中：

$$
x_e(n)=\frac{1}{2}[x(n)+x^*(-n)]
$$

$$
x_o(n)=\frac{1}{2}[x(n)-x^*(-n)]
$$

### DTFT 的对称关系

我们结合对称性和 DTFT 的共轭性质：

$$
x^{*}(n) \leftrightarrow X^{*}(e^{-j\omega}) \quad x^{*}(-n) \leftrightarrow X^{*}(e^{j\omega})
$$

我们可以推导出：

$$
\begin{aligned}x_{e}(n)&=\frac{1}{2}[x(n)+x^{*}(-n)]
\\&\leftrightarrow \frac{1}{2}[X(e^{j\omega})+X^{*}(e^{j\omega})]=Re[X(e^{j\omega} )]\end{aligned}
$$
$$
\begin{aligned}x_{o}(n)&=\frac{1}{2}[x(n)-x^{*}(-n)]
\\&\leftrightarrow \frac{1}{2}[X(e^{j\omega})-X^{*}(e^{j\omega})]=jIm[X(e^{j\omega} )]\end{aligned}
$$

同上有：

$$
X_{e}(e^{j\omega})\leftrightarrow Re[x(n)] \quad X_{o}(e^{j\omega})\leftrightarrow jIm[x(n)]
$$


## 离散系统的系统函数与频率响应

### 系统函数

对于 LTI 系统，单位冲激响应为 $h(n)$，系统函数为：

$$
H(z)=Z[h(n)]
$$

若差分方程为：

$$
y(n)-\sum\limits_{k=1}^{N}a_ky(n-k)=\sum\limits_{r=0}^{M}b_rx(n-r)
$$

在零初始条件下做 Z 变换：

$$
Y(z)\left(1-\sum\limits_{k=1}^{N}a_kz^{-k}\right)=X(z)\sum\limits_{r=0}^{M}b_rz^{-r}
$$

因此：

$$
H(z)=\frac{Y(z)}{X(z)}
=\frac{\sum\limits_{r=0}^{M}b_rz^{-r}}
{1-\sum\limits_{k=1}^{N}a_kz^{-k}}
$$

### 频率响应

如果单位圆在 $H(z)$ 的 ROC 内，则系统频率响应为：

$$
H(e^{j\omega})=H(z)|_{z=e^{j\omega}}
$$

输入为复指数时：

$$
x(n)=e^{j\omega n}
$$

输出为：

$$
y(n)=H(e^{j\omega})e^{j\omega n}
$$

所以复指数是 LTI 系统的特征函数，$H(e^{j\omega})$ 是对应特征值。

### 因果性与稳定性

对于 LTI 系统：

- 因果：$h(n)=0,\;n<0$。
- 稳定：$\sum\limits_{n=-\infty}^{\infty}|h(n)|<\infty$。

用系统函数判断时：

- 因果有理系统的 ROC 在最外极点之外。
- 稳定要求单位圆位于 ROC 内。
- 因果稳定有理系统要求全部极点在单位圆内。

## 与连续信号变换的关系

连续时间拉普拉斯变换：

$$
X_a(s)=\int_{-\infty}^{\infty}x_a(t)e^{-st}dt
$$

离散时间 Z 变换：

$$
X(z)=\sum\limits_{n=-\infty}^{\infty}x(n)z^{-n}
$$

若由 $t=nT$ 采样得到序列，则常见映射关系为：

$$
z=e^{sT}
$$

令 $s=j\Omega$，则：

$$
z=e^{j\Omega T}=e^{j\omega}
$$

因此：

$$
\omega=\Omega T
$$

这说明数字角频率是模拟角频率按采样间隔归一化后的结果。

## 本章自查问题

1. 为什么只写 $X(z)$ 而不写 ROC 可能不完整？
2. DTFT 为什么一定以 $2\pi$ 为周期？
3. DTFT 和 Z 变换的关系是什么？
4. $x(n-m)$、$e^{j\omega_0n}x(n)$、$x(n)*h(n)$ 分别对应什么频域操作？
5. 实序列的 DTFT 有哪些共轭对称性质？
6. 系统函数 $H(z)$ 和单位冲激响应 $h(n)$ 的关系是什么？
7. 因果稳定有理系统的极点应位于哪里？

## 待补位置

- 常见序列的 Z 变换表。
- 部分分式展开求反 Z 变换例题。
- ROC 判断时域序列方向的练习题。
