# 第八章 线性相位 FIR 滤波器

本章主线：实系数 FIR 要获得严格线性相位，单位冲激响应必须关于中心偶对称或奇对称；对称性与长度奇偶共同决定四类 FIR 的必然零点和适用范围，窗函数法再用有限长序列逼近理想频率响应。

## 定义与特点

- FIR 滤波器的单位冲激响应 $h(n)$ 为有限长序列，差分方程可以写成 $y(n)=\sum\limits_{k=0}^{N-1}h(k)x(n-k)$
- 其系统函数一般写为 $H(z)=\sum\limits_{n=0}^{N-1}h(n)z^{-n}$
- 一般有 $N-1$ 个零点；若把 $H(z)$ 写成 $z$ 的有理式，则在 $z=0$ 处有 $N-1$ 阶极点
- 本章讨论实系数 FIR。其频率响应为：
$$
H(e^{j\omega})=\sum\limits_{n=0}^{N-1}h(n)e^{-j\omega n}=H(\omega)e^{j\theta(\omega)}
$$
---
- 由线性相位的定义可得 $\theta(\omega)$ 为 $\omega$ 的线性函数
- 线性相位分为两种：
	- 第一类：$\theta(\omega)=-\tau \omega$
	- 第二类：$\theta(\omega)=\beta-\tau\omega$
- 两者群延时 $-\dfrac{d\theta(\omega)}{d\omega}=\tau$ 为常数
- 对实系数 FIR，严格线性相位的充要条件是 $h(n)=h(N-1-n)$ 或 $h(n)=-h(N-1-n)$
## 幅度函数 $H(\omega)$

- 这里的幅度函数 $H(\omega)$ 是**实函数**，也叫振幅函数，不一定非负；之前常说的 $|H(e^{j\omega})|$ 是幅频响应，永远非负。若 $H(\omega)<0$，这个负号等价于额外引入一个 $\pi$ 的相位跳变。
- 由于线性相位滤波器满足对称性，所以有：
$$
\begin{aligned}H(z)&=\sum\limits_{n=0}^{N-1}h(n)z^{-n}=\sum\limits_{n=0}^{N-1}[\pm h(N-1-n)]z^{-n}\\&=\sum\limits_{m=0}^{N-1}[\pm h(m)]z^{-(N-1-m)}=\pm z^{-(N-1)}\sum\limits_{m=0}^{N-1}h(m)z^{m}\end{aligned}
$$
- 即：
$$
H(z)=\pm z^{-(N-1)}H(z^{-1})
$$
- 因为 $\sum\limits_{m=0}^{N-1}h(m)z^{m}=\sum\limits_{m=0}^{N-1}h(m)(z^{-1})^{-m}=H(z^{-1})$，所以对称性会把 $H(z)$ 和 $H(z^{-1})$ 联系起来。
---
- 当 $h(n)$ 为偶对称时：
$$
H(e^{j\omega})=H(z)|_{z=e^{j\omega}}=e^{-j\left( \frac{N-1}{2} \right)\omega}\sum\limits_{n=0}^{N-1}h(n)\cos\left[ \left(\left( \frac{N-1}{2} \right)-n\right)\omega \right]=H(\omega)e^{j\theta(\omega)}
$$
- 推导思路：先提出公共线性相位项 $e^{-j\frac{N-1}{2}\omega}$，令 $M=\dfrac{N-1}{2}$，则
$$
H(e^{j\omega})=e^{-jM\omega}\sum\limits_{n=0}^{N-1}h(n)e^{j(M-n)\omega}
$$
偶对称时 $h(n)=h(N-1-n)$，成对项中的虚部相互抵消，只剩余 $\cos[(M-n)\omega]$ 项。
- 幅度函数：$H(\omega)=\sum\limits_{n=0}^{N-1}h(n)\cos\left[ \left(\left( \frac{N-1}{2} \right)-n\right)\omega \right]$
- 相位特性：$\theta(\omega)=-\left( \dfrac{N-1}{2} \right)\omega$
- 群延时：$- \dfrac{d\theta(\omega)}{d\omega}=\tau= \dfrac{N-1}{2}$
- 当 $N$ 为奇数时：
	- $H(\omega)=\sum\limits_{n=0}^{\frac{N-1}{2}}a(n)\cos(\omega n)$ ，$a(0)=h\left( \frac{N-1}{2} \right)$ ，$a(n)=2h\left( \frac{N-1}{2}-n \right)$
- 当 $N$ 为偶数时：
	- $H(\omega)=\sum\limits_{n=1}^{\frac{N}{2}}b(n)\cos\left( \omega \left( n- \frac{1}{2} \right) \right)$ ，$b(n)=2h\left( \frac{N}{2}-n \right)$
- 上面两个式子分别对应线性相位 FIR 的 I 型和 II 型：
	- $N$ 为奇数、偶对称：I 型，$H(\omega)$ 是 $\omega$ 的偶函数，$\omega=0,\pi$ 处不被强制为 $0$。
	- $N$ 为偶数、偶对称：II 型，$H(\omega)$ 仍为偶函数，但由于含有 $\cos[\omega(n-\frac{1}{2})]$，必有 $H(\pi)=0$，所以不适合直接设计高通或带阻滤波器。
- 整理方法：把关于中心 $M=\dfrac{N-1}{2}$ 对称的两项相加，利用 $e^{jx}+e^{-jx}=2\cos x$；中心点若存在，单独作为 $a(0)$。
---
- 反之为奇对称：
$$
H(e^{j\omega})=H(z)|_{z=e^{j\omega}}=j\cdot e^{-j\left( \frac{N-1}{2} \right)\omega}\sum\limits_{n=0}^{N-1}h(n)\sin\left[ \left(\left( \frac{N-1}{2} \right)-n\right)\omega \right]=H(\omega)e^{j\theta(\omega)}
$$
- 推导思路同上，仍先提出公共线性相位项 $e^{-j\frac{N-1}{2}\omega}$。奇对称时 $h(n)=-h(N-1-n)$，成对项中的实部相互抵消，只剩余 $j\sin[(M-n)\omega]$ 项，因此相位中多出 $\dfrac{\pi}{2}$。
- 幅度函数：$H(\omega)=\sum\limits_{n=0}^{N-1}h(n)\sin\left[ \left(\left( \frac{N-1}{2} \right)-n\right)\omega \right]$
- 相位特性：$\theta(\omega)=\dfrac{\pi}{2}-\left( \dfrac{N-1}{2} \right)\omega$
- 群延时：$- \dfrac{d\theta(\omega)}{d\omega}=\tau= \dfrac{N-1}{2}$
- 当 $N$ 为奇数时：
	- $H(\omega)=\sum\limits_{n=1}^{\frac{N-1}{2}}c(n)\sin(\omega n)$ ，$c(n)=2h\left( \frac{N-1}{2}-n \right)$
- 当 $N$ 为偶数时：
	- $H(\omega)=\sum\limits_{n=1}^{\frac{N}{2}}d(n)\sin\left( \omega \left( n- \frac{1}{2} \right) \right)$ ，$d(n)=2h\left( \frac{N}{2}-n \right)$
- 上面两个式子分别对应线性相位 FIR 的 III 型和 IV 型：
	- $N$ 为奇数、奇对称：III 型，$H(\omega)$ 是 $\omega$ 的奇函数，必有 $H(0)=0$、$H(\pi)=0$，适合 Hilbert 变换器一类问题，不适合普通低通/高通。
	- $N$ 为偶数、奇对称：IV 型，$H(\omega)$ 是奇函数，必有 $H(0)=0$，但 $H(\pi)$ 不一定为 $0$，可用于微分器、Hilbert 变换器等。
- 整理方法：把关于中心 $M=\dfrac{N-1}{2}$ 对称的两项相减，利用 $e^{jx}-e^{-jx}=2j\sin x$；奇对称且 $N$ 为奇数时中心点必须为 $0$。

### 四类线性相位 FIR 速查

| 类型 | 对称性 | 长度 $N$ | 必然零点 / 端点限制 | 常见用途限制 |
|---|---|---:|---|---|
| I 型 | 偶对称 | 奇数 | 无固定的 $z=\pm1$ 零点 | 四类选频滤波器都可设计 |
| II 型 | 偶对称 | 偶数 | $H(e^{j\pi})=0$，$z=-1$ 为零点 | 不能直接设计高通、带阻 |
| III 型 | 奇对称 | 奇数 | $H(e^{j0})=H(e^{j\pi})=0$ | 不适合普通低通、高通；常用于 Hilbert 变换器 |
| IV 型 | 奇对称 | 偶数 | $H(e^{j0})=0$，$z=1$ 为零点 | 常用于微分器、Hilbert 变换器 |

> 易错点：分类看的是单位冲激响应长度 $N$ 的奇偶，不是滤波器阶数 $N-1$ 的奇偶。

## 零点

- 根据 FIR 系统函数有 $H(z)=\pm z^{-(N-1)}H(z^{-1})$ ，那么若存在零点 $z=z_{1}=re^{j\theta}$ ，那么就有 $z= \dfrac{1}{z_{1}}=\dfrac{1}{r}e^{-j\theta}$
- 又因为 $h(n)$ 为实数序列，$H(z)$ 对应的多项式系数为实数；实系数多项式若有复根 $z_1$，则其共轭 $z_1^*$ 也必为根。因此还存在 $z=z_{1}^{*}=re^{-j\theta}$ 和 $z=\dfrac{1}{z^{*}_{1}}=\dfrac{1}{r}e^{j\theta}$
- 所以零点一般以四点一组形式存在
## 窗函数设计法
### 原理

- 对于理想滤波器，其频率响应应该是在边界频率处有突变，其单位冲激响应 $h_{d}(n)$ 是无限长的非因果序列：频域矩形突变对应时域 sinc 型序列，左右无限延伸，并且为了线性相位通常以 $\alpha$ 为中心对称。实际系统无法直接实现，所以用有限长的 $h(n)$ 去逼近
- 最直接的方法是直接截取 $h_{d}(n)$ 的一部分作为 $h(n)$ ，那么可以写成：
$$
h(n)=h_{d}(n)\cdot w(n) \quad 0\le n\le N-1
$$
---
- 设计思路：
$$
H_{d}(e^{j\omega})\rightarrow h_{d}(n) \rightarrow h_{d}\cdot w(n) \rightarrow h(n) \rightarrow H(e^{j\omega})
$$
- 有理想低通滤波器：
$$
H_{d}(e^{j\omega})= \begin{cases}1\cdot e^{-j\alpha\omega}\quad |\omega|\le \omega_{c}\\\\ 0\quad\quad \omega_{c}<|\omega|\le \pi\end{cases}
$$
- 那么：
$$
h_{d}(n)=IDTFT[H_{d}(e^{j\omega})]=\frac{\sin[\omega_{c}(n-\alpha)]}{\pi(n-\alpha)}
$$
- 可见 $h_{d}(n)$ 为无限长以 $\alpha$ 为中心的偶对称序列
- 若我们取窗函数为最简单的矩形窗函数 $w(n)=R_{N}(n)$ ，其幅度函数为 $W_{R}(\omega)= \dfrac{\sin\left( \frac{\omega N}{2} \right)}{\sin\left( \frac{\omega}{2} \right)}$ 。因为时域相乘对应频域周期卷积，严格写为 $H(e^{j\omega})=\dfrac{1}{2\pi}H_{d}(e^{j\omega})*W_{R}(e^{j\omega})$，所以实际幅度无法完美逼近理想矩形，会出现频谱泄露
- 影响：
	- 改变边沿特性，形成了过渡带，宽度等于窗函数的主瓣宽度 $\Delta \omega = \frac{4\pi}{N}$
	- 过渡带两侧产生肩峰和余振，取决于窗函数的旁瓣。主瓣是 $W(\omega)$ 中以 $\omega=0$ 为中心的最大瓣，主要决定过渡带宽度；旁瓣是主瓣两侧较小的波瓣，主要决定通带/阻带纹波和阻带衰减。旁瓣越多则振荡越多，旁瓣相对值越大则肩峰越强，肩峰相对值与 $N$ 基本无关
	- 改变 $N$ ，只能改变窗函数主瓣宽度，不能改变肩峰相对值，最大肩峰总为 $8.95\%$ ，称为吉布斯现象
	- 选择不同的窗函数，得到不同性能的滤波器
---
- 我们选择窗函数时尽量满足以下要求：
	- 主瓣尽量窄，以获得较陡的过渡带
	- 相对于主瓣幅度，旁瓣要尽可能小，使能量集中于主瓣，从而减小肩峰和余振，以提高阻带的衰减和通带的平稳
- 实际上两者不可兼得，一般总是通过增加主瓣宽度来抑制旁瓣
### 常用窗函数

- 性能指标：
	- 阻带最小衰减：阻带被压低的程度，数值越大，阻带抑制越强
	- 过渡带宽：阻带截止频率和通带截止频率的差值，低通时 $\Delta \omega=\omega_{st}-\omega_{p}$

#### 矩形窗
$$
w(n)=R_{N}(n)
$$
- 最简单，从阻带衰减看，性能最差
- 幅度函数：
$$W_{R}(\omega)= \dfrac{\sin\left( \frac{\omega N}{2} \right)}{\sin\left( \frac{\omega}{2} \right)}$$
- 主瓣宽度：$\Delta \omega = \frac{4\pi}{N}$
- 过渡带宽： $\Delta \omega= \frac{1.8\pi}{N}$
- 阻带最小衰减：$21dB$

#### 三角窗（巴特列特窗）
$$
w(n)=\begin{cases} \dfrac{2n}{N-1}&0\le n\le \dfrac{N-1}{2}\\\\ 2- \dfrac{2n}{N-1}& \dfrac{N-1}{2}<n\le N-1\end{cases}
$$
- 幅度函数：
$$
W(\omega)\approx \frac{2}{N}\left[\frac{\sin\left( \frac{\omega N}{4} \right)}{\sin\left( \frac{\omega}{2} \right)}\right]^2
$$
- 主瓣宽度：$\Delta \omega = \frac{8\pi}{N}$
- 过渡带宽 $\Delta \omega \approx\frac{6.1\pi}{N}$
- 阻带最小衰减：$25dB$

#### 汉宁窗
$$
w(n)=\frac{1}{2}\left[ 1-\cos\left( \frac{2\pi n}{N-1} \right) \right]R_{N}(n)
$$
- 主瓣宽度：$\Delta \omega = \frac{8\pi}{N}$
- 过渡带宽 $\Delta \omega \approx\frac{6.2\pi}{N}$
- 阻带最小衰减：$44dB$

#### 海明窗
$$
w(n)=\left[0.54-0.46\cos\left( \frac{2\pi n}{N-1} \right)\right]R_N(n)
$$
- 主瓣宽度：$\Delta \omega=\dfrac{8\pi}{N}$
- 过渡带宽 $\Delta \omega\approx\dfrac{6.6\pi}{N}$
- 阻带最小衰减：$53dB$

#### 布莱克曼窗
$$
w(n)=\left[0.42-0.5\cos\left( \frac{2\pi n}{N-1} \right)+0.08\cos\left( \frac{4\pi n}{N-1} \right)\right]R_N(n)
$$
- 主瓣宽度：$\Delta \omega=\dfrac{12\pi}{N}$
- 过渡带宽 $\Delta \omega\approx\dfrac{11\pi}{N}$
- 阻带最小衰减：$74dB$

- 常用窗函数性能表：

| 窗函数 | 旁瓣峰值 / dB | 主瓣宽度 | 过渡带宽度 | 阻带最小衰减 |
|---|---:|---:|---:|---:|
| 矩形窗 | $-13$ | $\dfrac{4\pi}{N}$ | $\dfrac{1.8\pi}{N}$ | $21\text{ dB}$ |
| 三角窗 / 巴特列特窗 | $-25$ | $\dfrac{8\pi}{N}$ | $\dfrac{6.1\pi}{N}$ | $25\text{ dB}$ |
| 汉宁窗 | $-31$ | $\dfrac{8\pi}{N}$ | $\dfrac{6.2\pi}{N}$ | $44\text{ dB}$ |
| 海明窗 | $-41$ | $\dfrac{8\pi}{N}$ | $\dfrac{6.6\pi}{N}$ | $53\text{ dB}$ |
| 布莱克曼窗 | $-57$ | $\dfrac{12\pi}{N}$ | $\dfrac{11\pi}{N}$ | $74\text{ dB}$ |

> [!NOTE]
> 表中数值是工程设计常用近似值，不同教材可能因 $N$ 与 $N-1$ 的记号差异略有出入。做题时通常先用阻带衰减选窗，再用过渡带宽估算 $N$。

### 窗函数设计步骤

1. 给定要求的理想频率 $H_{d}(e^{j\omega})$ 和技术指标
2. 计算得到的理想频率响应对应的单位冲激响应 $h_{d}(n)$
3. 根据**阻带衰减**选的窗函数，根据**过渡带宽度** $\Delta\omega$ 选的 $N$ 值
4. 计算所需 FIR 滤波器的单位冲激响应 $h(n)=h_{d}(n)\cdot w(n)$
5. 计算所需滤波器频率响应，验证是否满足需求 $H(e^{j\omega})=DTFT[h(n)]$

> [!TIP]
> 低通窗函数法做题时，通常先取 $\omega_c=\dfrac{\omega_p+\omega_{st}}{2}$，再由表中 $\Delta\omega$ 估算 $N$，最后令 $\alpha=\dfrac{N-1}{2}$。若 $n=\alpha$，则 $h_d(n)=\dfrac{\omega_c}{\pi}$；否则 $h_d(n)=\dfrac{\sin[\omega_c(n-\alpha)]}{\pi(n-\alpha)}$。

#### 设计线性相位 FIR 滤波器

- 大体步骤不变，在设计高通、带通、带阻滤波器时，要利用低通滤波器
- 考试主要注重低通滤波器

## 本章自查问题

1. 实系数 FIR 具有严格线性相位的充要条件是什么？
2. 振幅函数 $H(\omega)$ 与非负的幅频响应 $|H(e^{j\omega})|$ 有什么区别？
3. 四类线性相位 FIR 分别由哪种对称性和哪种长度奇偶性构成？
4. II 型为什么不能直接设计高通或带阻滤波器？
5. III 型为什么在 $\omega=0$、$\pi$ 都必为零？
6. 实系数线性相位 FIR 的普通复零点为什么通常四个一组？
7. 窗函数的主瓣宽度和旁瓣高度分别影响滤波器的什么指标？
8. 窗函数法为什么先按阻带衰减选窗，再按过渡带宽确定 $N$？
