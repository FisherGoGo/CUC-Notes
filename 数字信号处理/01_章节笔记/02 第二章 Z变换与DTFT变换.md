# Z 变换

- 不做详细记载
- [[信号第6章 离散时间系统 Z 变换]]

# 离散时间傅里叶变换 - Discrete-Time Fourier Transform

$$
\begin{cases}X(e^{j\omega})=DTFT[x(n)]=\sum\limits _{n=-\infty}^{\infty}x(n)e^{-j\omega n}\\\\ x(n)=IDTFT[X(e^{j\omega})]=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n} d \omega\end{cases}
$$
$$
\begin{aligned}x(n)& \Leftrightarrow X(e^{j\omega})\\ 离散 &\Leftrightarrow 周期 \\ 非周期 &\Leftrightarrow 连续\end{aligned}
$$
- 可见序列在单位圆上的 $z$ 变换就是序列的傅里叶变换
## 变换存在条件

- 收敛：
	- $\sum\limits|x(n)|<\infty$ ，序列绝对可和
	- $\sum\limits|x(n)|^{2}<\infty$ ，序列平方绝对可和 - 能量有限信号
## DTFT 的性质

- 些许性质证明：[[Proof/DTFT性质证明]]
### 线性
$$
ax(n)\pm by(n)\Leftrightarrow aX(e^{j\omega})\pm bY(e^{j\omega})
$$
### 时移
$$
x(n-m)\Leftrightarrow e^{-j\omega m}X(e^{j\omega})
$$
### 频移
$$
e^{j\omega_{0} n}x(n) \Leftrightarrow X(e^{j(\omega-\omega_{0})})
$$
### 时域卷积
$$
x(n)*h(n)\Leftrightarrow X(e^{j\omega})\cdot H(e^{j\omega})
$$
### 频域卷积
$$
x(n)\cdot h(n) \Leftrightarrow \frac{1}{2\pi} X(e^{j\omega})*H(e^{j\omega})
$$
### 微分
$$
nx(n)\Leftrightarrow j \frac{d}{d\omega}X(e^{j\omega})
$$
### 帕塞瓦定理（能量定理）
$$
\sum\limits|x(n)|^{2}= \frac{1}{2\pi}\int_{-\pi}^{\pi} |X(e^{j\omega})|^{2}d\omega
$$
### 反转
$$
x(-n)\Leftrightarrow X(e^{-j\omega})
$$
### 共轭
$$
x^{*}(n)\Leftrightarrow X^{*}(e^{-j\omega})
$$
## 对称

- 共轭对称序列：
$$
x_{e}(n)=x_{e}^{*}(-n)
$$
- 共轭反对称序列：
$$
x_{0}(n)=-x_{o}^{*}(-n)
$$
- 任意序列总能表示为一个共轭对称序列与一个共轭反对称序列之和
$$
\begin{aligned}&x(n)=x_{e}(n)+x_{o}(n) \\  &\begin{cases}x_{e}(n)= \frac{1}{2}[x(n)+x^{*}(-n)]\\ x_{o}(n)= \frac{1}{2}[x(n)-x^{*}(-n)]\end{cases}\end{aligned}
$$
## DTFT 的对称性
$$
Re[x(n)]= \frac{1}{2}[x(n)+x^{*}(n)] \Leftrightarrow \frac{1}{2}[X(e^j\omega)+X^{*}(e^{-j\omega})]=X_{e}(e^{j\omega})
$$
$$
x_{e}(n)= \frac{1}{2}[x(n)+x^{*}(-n)] \Leftrightarrow \frac{1}{2}[X(e^{j\omega})+X^{*}(e^{j\omega})]=Re[X(e^{j\omega})]
$$
- 我们得到：
	- $Re[x(n)]\leftrightarrow X_{e}(e^{j\omega})$
	- $j\text{Im}[(x(n))]\leftrightarrow X_{o}(e^{j\omega})$
	- $x_{e}(n)\leftrightarrow Re[X(e^{j\omega})]$
	- $x_{o}(n)\leftrightarrow j\text{Im}[X(e^{j\omega})]$
- 若 $x(n)$ 是实数序列，那么傅里叶变换满足：
	- 实部为偶函数
	- 虚部为奇函数
	- 幅度是偶函数
	- 辐角是奇函数
