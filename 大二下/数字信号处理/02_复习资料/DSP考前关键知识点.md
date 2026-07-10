# DSP 考前关键知识点（极简版）

> 用法：先看“最后 10 分钟”，再按薄弱章节回查。滤波器设计只整理低通，其他选频类型不展开。

## 最后 10 分钟检查

- [ ] 频率没混：$\omega=\Omega T=2\pi f/f_s$；数字角频率无 rad/s。
- [ ] 周期会判：$\omega_0/(2\pi)$ 为有理数才是周期序列。
- [ ] ROC 没漏：因果看最外极点外侧，稳定要求单位圆在 ROC 内。
- [ ] 符号没反：时移 $x(n-n_0)\leftrightarrow e^{-j\omega n_0}X(e^{j\omega})$。
- [ ] 卷积没混：DFT 相乘对应圆周卷积；想得到线性卷积，$N\ge N_1+N_2-1$。
- [ ] FFT 位序没反：DIT 输入倒位序、输出自然序；DIF 相反。
- [ ] 多采样率顺序没反：抽取前抗混叠，插值后抗镜像；有理数转换先插值后抽取。
- [ ] 双线性变换先预畸变：$\Omega=(2/T)\tan(\omega/2)$。
- [ ] FIR 长度和阶数没混：长度 $N$，阶数 $N-1$，群延迟 $(N-1)/2$。
- [ ] 窗函数选法没反：阻带衰减选窗，过渡带宽定长度。

## 1 离散时间信号与系统

### 必背关系

$$
x(n)=x_a(nT),\qquad f_s=\frac1T,\qquad
\omega=\Omega T=2\pi\frac{f}{f_s}
$$

- $\Omega$：模拟角频率（rad/s）；$\omega$：数字角频率（rad），以 $2\pi$ 为周期。
- 防止模拟采样混叠：$f_s\ge 2f_h$，实际还要留过渡带并在采样前低通。

### 序列周期

对 $e^{j\omega_0n}$ 或 $\sin(\omega_0n+\varphi)$：

$$
\omega_0N=2\pi k,\quad N\in\mathbb Z^+,\ k\in\mathbb Z
$$

即 $\omega_0/(2\pi)\in\mathbb Q$。满足条件的最小正整数 $N$ 是基本周期。

### 卷积与 LTI

$$
y(n)=x(n)*h(n)=\sum_{m=-\infty}^{\infty}x(m)h(n-m)
$$

手算顺序：翻转 $h(m)$ → 平移成 $h(n-m)$ → 逐点乘 → 对 $m$ 求和。

| 性质 | 判据 |
|---|---|
| 线性 | $T[ax_1+bx_2]=aT[x_1]+bT[x_2]$ |
| 时不变 | $x(n-n_0)$ 的输出为 $y(n-n_0)$ |
| LTI 因果 | $h(n)=0,\ n<0$ |
| LTI 稳定 | $\sum_{n=-\infty}^{\infty}\lvert h(n)\rvert<\infty$ |

> 易错：因果只允许依赖当前和过去输入；看到 $x(n+1)$ 通常就是非因果。卷积中的 $m$ 是求和变量，$n$ 是输出下标。

## 2 Z 变换与 DTFT

### 定义与关系

$$
X(z)=\sum_{n=-\infty}^{\infty}x(n)z^{-n}
$$

$$
X(e^{j\omega})=\sum_{n=-\infty}^{\infty}x(n)e^{-j\omega n},\qquad
x(n)=\frac1{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}\,\mathrm d\omega
$$

$$
X(e^{j\omega})=X(z)\big|_{z=e^{j\omega}}
$$

DTFT 存在的关键：Z 变换的 ROC 包含单位圆。

### ROC 速判

| 序列 / 系统 | ROC |
|---|---|
| 右边序列、因果有理系统 | 最外极点之外 |
| 左边序列 | 最内极点之内 |
| 双边序列 | 两圈极点之间 |
| 稳定系统 | ROC 包含单位圆 |
| 因果且稳定有理系统 | 全部极点在单位圆内 |

ROC 不含极点；同一个代数式配不同 ROC，可对应不同序列。

### 高频性质

$$
x(n-n_0)\longleftrightarrow e^{-j\omega n_0}X(e^{j\omega})
$$

$$
e^{j\omega_0n}x(n)\longleftrightarrow X(e^{j(\omega-\omega_0)})
$$

$$
x(n)*h(n)\longleftrightarrow X(e^{j\omega})H(e^{j\omega})
$$

$$
x(n)h(n)\longleftrightarrow
\frac1{2\pi}\int_{-\pi}^{\pi}X(e^{j\theta})H(e^{j(\omega-\theta)})\,\mathrm d\theta
$$

$$
\sum_{n=-\infty}^{\infty}|x(n)|^2
=\frac1{2\pi}\int_{-\pi}^{\pi}|X(e^{j\omega})|^2\,\mathrm d\omega
$$

实序列满足：

$$
X(e^{-j\omega})=X^*(e^{j\omega})
$$

所以实部为偶函数、虚部为奇函数，幅度为偶函数、相位为奇函数（忽略相位跳变）。

### 系统函数

$$
H(z)=\frac{Y(z)}{X(z)},\qquad
H(e^{j\omega})=H(z)\big|_{z=e^{j\omega}}
$$

差分方程题：零初始条件下做 Z 变换 → 整理 $Y(z)/X(z)$ → 因果性定 ROC → 极点判断稳定性。

## 3 离散傅里叶变换 DFT

### 四种傅里叶形式

| 时域 | 频域 | 变换 |
|---|---|---|
| 连续、非周期 | 连续、非周期 | CTFT |
| 连续、周期 | 离散、非周期 | CTFS |
| 离散、非周期 | 连续、周期 | DTFT |
| 离散、周期 | 离散、周期 | DFS |

DFT 是有限长序列的有限点表示，但运算隐含时、频域的周期延拓。

### 定义

令 $W_N=e^{-j2\pi/N}$：

$$
X(k)=\sum_{n=0}^{N-1}x(n)W_N^{nk}
$$

$$
x(n)=\frac1N\sum_{k=0}^{N-1}X(k)W_N^{-nk}
$$

$$
X(k)=X(e^{j\omega})\big|_{\omega=2\pi k/N}
$$

两条秒算：

$$
X(0)=\sum_{n=0}^{N-1}x(n),\qquad
x(0)=\frac1N\sum_{k=0}^{N-1}X(k)
$$

若 $x(n)$ 为实序列，则 $X(N-k)=X^*(k)$。

对偶性与帕塞瓦：

$$
x(n)\xleftrightarrow{\mathrm{DFT}}X(k)
\quad\Longrightarrow\quad
X(n)\xleftrightarrow{\mathrm{DFT}}N x((-k))_N
$$

$$
\sum_{n=0}^{N-1}|x(n)|^2
=\frac1N\sum_{k=0}^{N-1}|X(k)|^2
$$

### 圆周运算

$$
x_1(n)\circledast_Nx_2(n)
\xleftrightarrow{\mathrm{DFT}}X_1(k)X_2(k)
$$

$$
x_1(n)x_2(n)
\xleftrightarrow{\mathrm{DFT}}
\frac1N X_1(k)\circledast_NX_2(k)
$$

若两序列长度分别为 $N_1,N_2$：

$$
\boxed{N\ge N_1+N_2-1}
$$

补零到满足上式后，$N$ 点圆周卷积才等于线性卷积。

圆周移位：

$$
y(n)=x((n+m))_N
\quad\Longrightarrow\quad
Y(k)=X(k)W_N^{-km}
$$

### 频域采样与频谱分析

- 频域采样后 IDFT 得到时域周期延拓的叠加；原序列长度为 $M$ 时，$N\ge M$ 才无时域混叠。
- 参数关系：

$$
T_0=NT,\qquad F_0=\frac1{T_0}=\frac{f_s}{N},\qquad f_s=\frac1T
$$

| 现象 | 原因 | 改进 |
|---|---|---|
| 混叠 | $f_s$ 不足 | 提高 $f_s$，采样前低通 |
| 泄漏 | 有限截断或非整周期记录 | 相干采样、延长记录、加窗 |
| 栅栏效应 | 频谱只在离散频点观察 | 增加有效记录长度 |

> 补零只让频谱曲线更密，不提高真实频率分辨率；真实分辨率由 $T_0$ 决定。

## 4 快速傅里叶变换 FFT

设 $N=2^L$，共有 $L=\log_2N$ 级蝶形。

### DIT：按时间抽取

$$
X(k)=X_1(k)+W_N^kX_2(k)
$$

$$
X\left(k+\frac N2\right)=X_1(k)-W_N^kX_2(k)
$$

- 输入按偶、奇下标分组。
- 常见原位流图：输入倒位序，输出自然序。

### DIF：按频率抽取

$$
x_1(n)=x(n)+x\left(n+\frac N2\right)
$$

$$
x_2(n)=\left[x(n)-x\left(n+\frac N2\right)\right]W_N^n
$$

- 先做前后半段加减，再分偶、奇频点。
- 常见原位流图：输入自然序，输出倒位序。

### 运算量与应用

| 方法 | 复乘 | 复加 |
|---|---:|---:|
| 直接 DFT | $N^2$ | $N(N-1)$ |
| 基 2 FFT | $\dfrac N2\log_2N$ | $N\log_2N$ |

$$
\operatorname{IDFT}\{X(k)\}
=\frac1N\left[\operatorname{DFT}\{X^*(k)\}\right]^*
$$

FFT 求线性卷积：两序列补零到 $N\ge N_1+N_2-1$ → 分别 FFT → 频域相乘 → IFFT。

## 5 抽取、插值与采样率转换

### $D$ 倍抽取

$$
x_d(n)=x(Dn),\qquad f_s'=\frac{f_s}{D}
$$

$$
X_d(e^{j\omega})
=\frac1D\sum_{k=0}^{D-1}
X\left(e^{j(\omega+2\pi k)/D}\right)
$$

- 归一化频谱扩展 $D$ 倍并叠加，可能混叠。
- 抽取前先低通，使原信号限制在 $|\omega|\le\pi/D$。

### $I$ 倍插值

$$
x_e(n)=
\begin{cases}
x(n/I),&n=mI\\
0,&\text{其他}
\end{cases}
,\qquad f_s'=If_s
$$

$$
X_e(e^{j\omega})=X(e^{jI\omega})
$$

- 零值插入使频谱压缩为 $1/I$，并产生 $I$ 个镜像。
- 插值后接截止频率 $\pi/I$、通带增益 $I$ 的低通滤波器。

### 有理数倍转换

$$
f_s'=\frac IDf_s
$$

$$
x(n)\rightarrow\uparrow I\rightarrow H(e^{j\omega})
\rightarrow\downarrow D\rightarrow y(n)
$$

$$
\omega_c\le\min\left(\frac\pi I,\frac\pi D\right)
$$

必须先插值、后抽取；中间一个低通同时抗镜像和抗混叠。

## 6 数字滤波器结构

由差分方程

$$
y(n)+\sum_{k=1}^{N}a_ky(n-k)
=\sum_{r=0}^{M}b_rx(n-r)
$$

可得

$$
H(z)=\frac{\sum_{r=0}^{M}b_rz^{-r}}
{1+\sum_{k=1}^{N}a_kz^{-k}}
$$

| 类型 | 关键特征 |
|---|---|
| IIR | 冲激响应无限长，通常有反馈；阶数较低，但必须检查稳定性 |
| FIR | 冲激响应有限长，可无反馈；一定可稳定，容易实现严格线性相位 |

### 看系统函数画结构

- IIR 直接 II 型：分子、分母共用延时链，延时器最少。
- 级联型：把 $H(z)$ 因式分解成一、二阶节相乘；对系数量化较不敏感。
- 并联型：对 $H(z)$ 作部分分式展开，各支路相加。
- FIR 直接型：抽头延时线；线性相位型利用系数对称性合并乘法。

> 易错：直接 I 型有两条延时链；直接 II 型共用一条。结构等价不等于有限精度下误差完全相同。

## 7 IIR 低通滤波器设计

### 最小相位与全通

- 因果稳定最小相位系统：极点、零点都在单位圆内，其稳定逆系统也因果稳定。
- 全通系统：$|H_{ap}(e^{j\omega})|=1$；零点与极点关于单位圆成共轭倒数，只改相位、不改幅度。

### 模拟低通原型

#### 巴特沃斯

- 幅度平方单调，无波纹；$\Omega=\Omega_c$ 时衰减 $3\ \mathrm{dB}$。

$$
|H_a(j\Omega)|^2
=\frac1{1+(\Omega/\Omega_c)^{2N}}
$$

若通、阻带衰减指标为 $\delta_p,\delta_s$（dB）：

$$
N\ge
\frac{\lg\left(\dfrac{10^{0.1\delta_s}-1}
{10^{0.1\delta_p}-1}\right)}
{2\lg(\Omega_s/\Omega_p)}
$$

$N$ 向上取整，再由任一边界求 $\Omega_c$：

$$
\Omega_c=
\frac{\Omega_p}{(10^{0.1\delta_p}-1)^{1/(2N)}}
$$

或

$$
\Omega_c=
\frac{\Omega_s}{(10^{0.1\delta_s}-1)^{1/(2N)}}
$$

#### 切比雪夫 I 型

- 通带等波纹，阻带单调；同样指标下通常比巴特沃斯阶数低。

$$
\varepsilon=\sqrt{10^{0.1\delta_p}-1}
$$

考试若给归一化表：先算 $\varepsilon$ 和阶数 → 查表得到归一化原型 → 按截止频率去归一化。

### 模拟到数字

| 方法 | 映射 | 关键点 |
|---|---|---|
| 冲激响应不变法 | $h(n)=T h_a(nT)$ | $\omega\approx\Omega T$；模拟频谱周期叠加，可能混叠 |
| 双线性变换法 | $s=\dfrac2T\dfrac{1-z^{-1}}{1+z^{-1}}$ | 无混叠，但频率非线性，必须预畸变 |

若

$$
H_a(s)=\sum_k\frac{A_k}{s-s_k}
$$

则冲激响应不变法给出

$$
H(z)=\sum_k\frac{TA_k}{1-e^{s_kT}z^{-1}}
$$

双线性变换的预畸变：

$$
\boxed{\Omega_p=\frac2T\tan\frac{\omega_p}{2},\qquad
\Omega_s=\frac2T\tan\frac{\omega_s}{2}}
$$

### 数字低通设计题固定流程

1. 读出数字指标 $\omega_p,\omega_s,\delta_p,\delta_s$，统一单位。
2. 若用双线性变换，分别预畸变为 $\Omega_p,\Omega_s$；不可只变一个边界。
3. 选巴特沃斯或切比雪夫 I 型，算阶数并向上取整。
4. 查归一化模拟低通原型，按 $\Omega_c$ 去归一化，得到 $H_a(s)$。
5. 用题目指定的方法得到 $H(z)$。
6. 检查极点是否在单位圆内，并把边界代回验证指标。

> 易错：脉冲响应不变法的极点映射为 $z_k=e^{s_kT}$；双线性变换中的同一个 $T$ 必须贯穿预畸变和代换。频率若写成 $0.4\pi$，它已经是 rad，不要再乘 $\pi$。

## 8 FIR 低通滤波器设计

### 线性相位

长度为 $N$ 的实系数 FIR 具有严格线性相位，当且仅当

$$
h(n)=\pm h(N-1-n)
$$

$$
\tau=\frac{N-1}{2}
$$

低通要求 $H(e^{j0})\ne0$，因此采用偶对称：

| 类型 | 对称性 | 长度 | 对低通的意义 |
|---|---|---:|---|
| I 型 | 偶对称 | 奇数 | 可设计低通 |
| II 型 | 偶对称 | 偶数 | $H(e^{j\pi})=0$，也可设计低通 |
| III 型 | 奇对称 | 奇数 | $H(e^{j0})=0$，不能设计普通低通 |
| IV 型 | 奇对称 | 偶数 | $H(e^{j0})=0$，不能设计普通低通 |

实系数线性相位 FIR 的普通复零点通常四个一组：

$$
z_0,\quad z_0^*,\quad \frac1{z_0},\quad \frac1{z_0^*}
$$

### 窗函数法

先取

$$
\omega_c=\frac{\omega_p+\omega_s}{2},\qquad
\alpha=\frac{N-1}{2}
$$

理想低通冲激响应：

$$
h_d(n)=
\begin{cases}
\dfrac{\sin[\omega_c(n-\alpha)]}{\pi(n-\alpha)},&n\ne\alpha\\[6pt]
\dfrac{\omega_c}{\pi},&n=\alpha
\end{cases}
$$

加窗得到可实现 FIR：

$$
h(n)=h_d(n)w(n),\qquad 0\le n\le N-1
$$

常用工程近似：

| 窗 | 阻带最小衰减 | 过渡带宽 $\Delta\omega$ |
|---|---:|---:|
| 矩形窗 | $21\ \mathrm{dB}$ | $1.8\pi/N$ |
| 三角窗 | $25\ \mathrm{dB}$ | $6.1\pi/N$ |
| 汉宁窗 | $44\ \mathrm{dB}$ | $6.2\pi/N$ |
| 海明窗 | $53\ \mathrm{dB}$ | $6.6\pi/N$ |
| 布莱克曼窗 | $74\ \mathrm{dB}$ | $11\pi/N$ |

### 低通窗函数法固定流程

1. 算过渡带宽 $\Delta\omega=\omega_s-\omega_p$。
2. 按阻带最小衰减选择窗函数。
3. 用表中 $\Delta\omega\approx C\pi/N$ 估算 $N$，向上取整，并按需要调整长度奇偶。
4. 取 $\omega_c=(\omega_p+\omega_s)/2$、$\alpha=(N-1)/2$。
5. 算 $h_d(n)$，再算 $h(n)=h_d(n)w(n)$。
6. 利用 $h(n)=h(N-1-n)$ 自检，并验证频响指标。

> 易错：窗越平滑，旁瓣越低、阻带衰减越大，但主瓣更宽、过渡带更宽。增大 $N$ 主要缩窄过渡带，不能消除矩形窗的相对肩峰；换窗才能改变旁瓣水平。

## 一眼回忆：最容易直接写错的公式

$$
\omega=\Omega T,\qquad
X(e^{j\omega})=X(z)|_{z=e^{j\omega}}
$$

$$
N_{\text{卷积}}\ge N_1+N_2-1,\qquad
F_0=\frac{f_s}{N}=\frac1{T_0}
$$

$$
\operatorname{IDFT}\{X\}
=\frac1N[\operatorname{DFT}\{X^*\}]^*
$$

$$
\Omega=\frac2T\tan\frac\omega2,\qquad
s=\frac2T\frac{1-z^{-1}}{1+z^{-1}}
$$
