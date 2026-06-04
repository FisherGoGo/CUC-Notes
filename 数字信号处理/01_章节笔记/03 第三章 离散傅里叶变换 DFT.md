# 离散的傅里叶级数 Discrete Fourier Series

- 我们在信号与系统学过，连续周期信号可以分解为一系列谐波的线性组合：
$$
\tilde{x}(t)=\sum\limits_{k=-\infty}^{\infty} X(jk\Omega_{0})e^{jk\Omega_{0} t}
$$
- 同时离散周期信号也可以分解为一系列谐波的线性组合：
$$
\tilde{x}(n)= \frac{1}{N}\sum\limits_{k=0}^{N-1} \tilde{X}(k)\cdot e^{j \frac{2\pi}{N}k n}
$$
> [!NOTE] 
> - 在连续周期时间信号中，周期为 $T_{0}$ ，假设我们对信号的采样间隔为 $T_{s}$ ，采得 $N$ 个点，他们关系为 $T_{0}=N\cdot T_{s}$
> - 连续域得基频为 $\Omega_{0}=\frac{2\pi}{T_{0}}$
> - 我们对信号进行采样，令 $t=nT_{s}$，那么 $e^{j\Omega_{0}(nT_{s})}=e^{j(\Omega_{0}T_{s})n}$
> - 其中 $\Omega_{0}T_{s}=\omega_{s}$ ，即离散域基频，我们带入 $T_{0}=NT_{s}$ ，得到 $\omega_{0}=\frac{2\pi}{N}$

- 我们容易得到 $e^{jk\omega_{0}n}=e^{j \frac{2\pi}{N}kn}=e^{j \frac{2\pi}{N}(k+iN)n}$ ，所以其谐波也是周期为 $N$ ，所以只有 $0\sim N-1$ 次项谐波
- 那么我们得到 DFS 变换：
$$
\begin{cases}\tilde{X}(k)=DFS[\tilde{x}(n)]=\sum\limits_{n=0}^{N-1}\tilde{x}(n)\cdot e^{-j \frac{2\pi}{N}kn} \\ \\ \tilde{x}(n)=IDFS[\tilde{X}(k)]=\frac{1}{N}\sum\limits_{k=0}^{N-1}\tilde{X}(k)\cdot e^{j \frac{2\pi}{N}kn}\end{cases}
$$
- 我们令 $W_{N}=e^{-j \frac{2\pi}{N}}$ ，那么：
$$
\begin{cases}\tilde{X}(k)=DFS[\tilde{x}(n)]=\sum\limits_{n=0}^{N-1}\tilde{x}(n)\cdot W_{N}^{kn} \\ \\ \tilde{x}(n)=IDFS[\tilde{X}(k)]=\frac{1}{N}\sum\limits_{k=0}^{N-1}\tilde{X}(k)\cdot W_{n}^{-kn}\end{cases}
$$
- DFS 可以视为对 $x(n)$ 的第一个周期做 z 变换，然后将 z 变换在 z 平面单位圆上按间隔角 $\frac{2\pi}{N}$ 等间隔采样得到的
## $W_{N}$ 的性质

- 共轭对称性：$W_{N}^{n}=(W_{N}^{-n})^{*}$
- 周期性：$W_{N}^{n}=W_{N}^{n+iN}$
- 可约性：$W_{N}^{in}=W_{\frac{N}{i}}^{n}$
- 正交性：
$$
\frac{1}{N}\sum\limits_{k=0}^{N-1}W_{N}^{nk}(W_{N}^{mk})^{*}=\frac{1}{N}\sum\limits_{k=0}^{N-1}W_{N}^{(n-m)k}=\begin{cases}1 ,\quad n-m=iN\\ 0,\quad n-m\ne iN\end{cases}
$$

## 性质
### 线性
$$
a\tilde{x}_{1}(n)+b\tilde{x}_{2}(n) \Leftrightarrow a\tilde{X}_{1}(k)+b\tilde{X}_{2}(k)
$$
### 时域移位
$$
\tilde{x}(n+m) \Leftrightarrow \tilde{X}(k)W_{N}^{-mk}
$$
### 频域移位
$$
W_{N}^{nl}\tilde{x}(n)\Leftrightarrow \tilde{X}(k+l)
$$
### 对偶性
$$
\begin{cases}\tilde{x}(n)\Leftrightarrow \tilde{X}(k)\\ \tilde{X}(n)\Leftrightarrow N\tilde{x}(-k)\end{cases}
$$
### 时域卷积
$$
\tilde{X}_{1}(k)\cdot \tilde{X}_{2}(k)\Leftrightarrow \sum\limits_{m=0}^{N-1} \tilde{x}_{1}(m)\tilde{x}_{2}(n-m)
$$
### 频域卷积
$$
\tilde{x}_{1}(n)\cdot \tilde{x}_{2}(n)\Leftrightarrow \frac{1}{N}\sum\limits_{l=0}^{N-1}\tilde{X}_{1}(l)\tilde{X}_{2}(k-l)
$$
- 上述卷积仅在一个周期内进行

# 离散傅里叶变换 Discrete Fourier Transform

- 若我们有有限长序列 $x(n)$ ：
$$
x(n)=\begin{cases}x(n)\quad 0\le n\le N-1\\\\ 0\quad otherwise\end{cases}
$$
- 若我们把 $x(n)$ 看成一个周期为 $N$ 的周期序列 $\tilde{x}(n)$ 的一个周期，那么 $\tilde{x}(n)$ 为 $x(n)$ 的以 $N$ 为周期的周期延拓，即 $\tilde{x}(n)=\sum\limits_{r=-\infty}^{\infty} x(n+rN)$ ，且 $x(n)$ 为 $\tilde{x}(n)$ 的主值区间
- 若我们将区间限制在 $0\sim N-1$ 上，即可从 DFS 得到 N 点 DFT 的定义：
$$
\begin{cases}X(k)=\sum\limits_{n=0}^{N-1}x(n)W_{N}^{nk}\quad 0\le k\le N-1\\\\ x(n)=\frac{1}{N}\sum\limits_{k=0}^{N-1}X(k)W_{N}^{-nk}\quad 0\le n\le N-1\end{cases}
$$
# 离散傅里叶变换的性质
## 线性性质
$$
x_{3}(n)=x_{1}(n)+x_{2}(n)\Leftrightarrow X_{3}(k)=X_{1}(k)+X_{2}(k)
$$
- 其中的 DFT 都要按 $N=\max(N_{1},N_{2})$ 来算
## 圆周移位
$$
x_{m}(n)=x((n+m))_NR_{N}(n)
$$
- 即取周期延拓后移位再取主值
### 时域移位
$$
x((n+m))_{N}R_{N}(n)\Leftrightarrow X(k)W_{N}^{-km}
$$
### 频域移位
$$
x(n)W_{N}^{nl}\Leftrightarrow X((k+l))_{N}R_{N}(k)
$$
- 我们可以推出：
$$
DFT\left[ x(n)\cos\left( \frac{2\pi nl}{N} \right) \right]=\frac{1}{2}[X((k-l))_{N}+X((k+l))_{N}]R_{N}(k)
$$
$$
DFT\left[ x(n)\sin\left( \frac{2\pi nl}{N} \right) \right]=\frac{1}{2}[X((k-l))_{N}-X((k+l))_{N}]R_{N}(k)
$$
## 对偶性
$$
\begin{aligned}x(n)&\Leftrightarrow X(k)\\ X(n)&\Leftrightarrow N\cdot x((-k))_NR_N(k)\end{aligned}
$$
## 帕塞瓦定理
$$
\sum\limits_{n=0}^{N-1}|x(n)|^{2}=\frac{1}{N}\sum\limits_{k=0}^{N-1}|X(k)|^{2}
$$
## 序列的和
$$
\sum\limits_{n=0}^{N-1}x(n)=\left(\sum\limits_{n=0}^{N-1}x(n)W_{N}^{nk}\right)_{k=0}=X(0)
$$
## 序列初始值
$$
x(0)=\left( \frac{1}{N}\sum\limits_{k=0}
^{N-1}X(k)W_{N}^{-nk} \right)_{n=0}=\frac{1}{N}\sum\limits_{k=0}^{N-1}X(k)$$
## 圆周共轭对称性

- 圆周共轭对称分量
$$
x_{ep}(n)=\tilde{x}_{e}(n)R_{N}(n)=\frac{1}{2}[x((n))_{N}+x^{*}((N-n))_N]R_N(n)
$$
- 圆周共轭反对称分量
$$
x_{op}(n)=\tilde{x}_{o}(n)R_{N}(n)=\frac{1}{2}[x((n))_{N}-x^{*}((N-n))_N]R_N(n)
$$
### 共轭对称性
$$
x^{*}(n)\Leftrightarrow X^{*}((N-k))_{N}R_{N}(k)
$$
### 复数序列的 DFT
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
### 虚实序列的 DFT
$$
x(n)=x_{r}(n)\Leftrightarrow X(k)=X_{ep}(k)=X^{*}((N-k))_NR_N(k)
$$
$$
x(n)=jx_{r}(n)\Leftrightarrow X(k)=X_{op}(k)=-X^{*}((N-k))_{N}R_{N}(k)
$$
### 圆周偶/奇对称
$$
x(n)=x((N-n))_{N}R_{N}(n)\Leftrightarrow X(k)=X((N-k))_{N}R_{N}(k)
$$
$$
x(n)=-x((N-n))_{N}R_{N}(n)\Leftrightarrow X(k)=-X((N-k))_{N}R_{N}(k)
$$
## 圆周卷积和
$$
x_1(n) \;\text{Ⓝ}\; x_{2}(n)\Leftrightarrow X_{1}(k)X_{2}(k)
$$
- 其中：
$$
\begin{aligned}x_1(n) \;\text{Ⓝ}\; x_{2}(n)&=\sum\limits_{m=0}^{N-1}x_{1}(m)x_{2}((n-m))_{N}R_{N}(n)\\&=\sum\limits_{m=0}^{N-1}x_{2}(m)x_{1}((n-m))_{N}R_{N}(n)\end{aligned}
$$

