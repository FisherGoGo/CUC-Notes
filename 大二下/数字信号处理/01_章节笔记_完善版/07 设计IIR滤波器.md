# 第七章 设计 IIR 数字滤波器

本章主线：先理解最小相位和全通系统，再设计模拟低通原型 $H_a(s)$，通过冲激响应不变法或双线性变换得到数字低通，最后转换成所需的选频滤波器。

## 最小相位系统

对因果稳定有理系统，全部极点位于单位圆内。若全部零点也位于单位圆内，则称为最小相位系统。

最小相位系统的常用性质：

- 系统及其逆系统都因果稳定；
- 在幅频响应相同的因果稳定系统中，相位延迟和群延迟最小；
- 单位冲激响应能量更集中在 $n=0$ 附近。

若因果稳定系统含有单位圆外零点，可以把这些零点通过全通因子反射到单位圆内：

$$
H(z)=H_{\min}(z)H_{ap}(z)
$$

其中 $H_{\min}(z)$ 为最小相位部分，$H_{ap}(z)$ 为全通部分。两者相乘保持原系统的幅频响应不变。

## 全通系统

归一化全通系统满足：

$$
|H_{ap}(e^{j\omega})|=1
$$

实系数 $N$ 阶全通系统可写为：

$$
H_{ap}(z)=\pm
\frac{z^{-N}+a_1z^{-N+1}+a_2z^{-N+2}+\cdots+a_N}
{1+a_1z^{-1}+a_2z^{-2}+\cdots+a_Nz^{-N}}
$$

若 $p$ 是单位圆内极点，则对应零点为：

$$
z_0=\frac{1}{p^*}
$$

即零点和极点关于单位圆成共轭倒数关系。全通系统只改变相位，不改变幅度，常用于相位均衡和最小相位分解。

> 易错点：若极点 $p=re^{j\theta}$，对应零点是 $1/p^*=(1/r)e^{j\theta}$，不是简单写成 $1/p$。

## 设计 IIR 数字滤波器步骤

1. 根据要求（低通、高通、带通、带阻）整理数字滤波器设计指标
2. 由低通数字滤波器的设计指标得出模拟低通滤波器的设计指标
3. 设计模拟低通滤波器（巴特沃斯、切比雪夫 I 型）
4. 将模拟低通滤波器转化为数字低通滤波器（冲激响应不变法，双线性变换法）
5. 将数字低通滤波器转化为要求的数字选频滤波器（数字域频带转化）

## 根据幅度平方函数设计系统函数

- 幅度平方函数：
$$
|H_{a}(j\Omega)|^{2}=H_{a}(j\Omega)H_{a}(-j\Omega)=H_{a}(s)H_a(-s)|_{s=j\Omega}
$$
- $H_{a}(s)$ 为模拟滤波器的系统函数，$H_{a}(j\Omega)$ 为模拟滤波器的频率响应
- 对于实系数滤波器，零极点以共轭复数对出现；$H_a(s)H_a(-s)$ 的根关于虚轴成镜像分布，不能把这个结论直接说成 $H_a(s)$ 自身的极点关于虚轴对称
---
- 有 $z=e^{sT}=e^{(\sigma+j\Omega)T}=e^{\sigma T}\cdot e^{j\Omega T}$
- 可见 $e^{j\Omega T}$ 只表示相角，而在 $s$ 平面左半部分，$\sigma<0$ ，那么 $|e^{\sigma T}|<1$ ，即单位圆内
- 为了使 $H_{a}(s)$ 是因果稳定系统，需要将 $H_{a}(s)H_{a}(-s)$ 的所有左半平面极点归于 $H_{a}(s)$ ；但对于零点没有因果稳定性的限制，只需要对半分配，且满足零点以共轭对形式出现。如果要求最小相位系统，则需要将所有左半平面的零点分给 $H_{a}(s)$
- 有 $H_{a}(s)|_{s=0}=H_{a}(j\Omega)|_{\Omega=0}$

## 巴特沃斯滤波器

- 巴特沃斯滤波器的幅度平方函数为
$$
|H(j\Omega)|^{2}= \frac{1}{1+\left( \frac{\Omega}{\Omega_{c}} \right)^{2N}}
$$
- 其中 $N$ 为阶数，$\Omega_{c}$ 为滤波器截止频率
- 当 $\Omega=\Omega_{c}$ 时，$|H(j\Omega_{c})|= \frac{1}{\sqrt{2}}$ ，相当于 3dB 衰减，又称为 3dB 带宽
- 通带有最大平坦振幅特性，阶数越高，曲线越陡，越接近理想形态

### 设计指标

- $N$ 滤波器阶数
- $\Omega_{p}$ 通带截止频率
- $\Omega_{st}$ 阻带截止频率
- $\delta_{p}$ 通带最大衰减（dB），$\delta_{p}=20\lg \dfrac{|H(j0)|}{|H(j\Omega_{p})|}$
- $\delta_{s}$ 阻带最小衰减（dB），$\delta_{s}=20\lg \dfrac{|H(j0)|}{|H(j\Omega_{st})|}$

### 设计流程

1. 根据指标要求确定**阶数**与**截止频率**：

当滤波器对通带要求更高时要求：
$$
\delta_{p}=10\lg\left[1+\left(\frac{\Omega_{p}}{\Omega_{c}}\right)^{2N}\right]
$$

当滤波器对阻带要求更高时要求：
$$
\delta_{s}=10\lg\left[1+\left(\frac{\Omega_{st}}{\Omega_{c}}\right)^{2N}\right]
$$
两式联立，可得，注意向上取整：
$$
N\ge \frac{\lg[(10^{0.1\delta_{s}}-1) / (10^{0.1\delta_{p}}-1)]}{2\lg(\Omega_{st} / \Omega_{p})}
$$
由通带、阻带指标分别得到截止频率边界：
$$
\Omega_{c,p}=\frac{\Omega_{p}}{\sqrt[2N]{10^{0.1\delta_{p}}-1}},\qquad
\Omega_{c,s}=\frac{\Omega_{st}}{\sqrt[2N]{10^{0.1\delta_{s}}-1}}
$$
为同时满足两项指标，应选择：

$$
\Omega_{c,p}\le\Omega_c\le\Omega_{c,s}
$$

阶数 $N$ 向上取整后，这个区间通常不为空。取下界会恰好满足通带指标，取上界会恰好满足阻带指标。

2. 根据阶数**查表**

直接查表得到归一化系统函数的分母多项式 $s^{N}+a_{N-1}s^{N-1}+\ldots+a_{1}s+a_{0}$。归一化巴特沃斯多项式通常首项和常数项都为 $1$。

3. 去归一化

将归一化的系统函数中的 $s$ 替换为 $\dfrac{s}{\Omega_{c}}$ ，即 $H_{a}(s)=H_{a_{N}}\left( \dfrac{s}{\Omega_{c}} \right)$

## 切比雪夫 I 型滤波器

- 振幅特性：在通带内等波纹，在阻带内单调下降
- 平方函数：
$$
|H_{a}(j\Omega)|^{2}= \frac{1}{1+\varepsilon^{2}C_{N}^{2}\left( \frac{\Omega}{\Omega_{c}} \right)}
$$
- 其中 $N$ 为阶次，$\Omega_c$ 为截止频率， $\varepsilon$ 为波动程度，对应通带波纹 $\delta_{p}$ ，$C_{N}(x)$ 为 $N$ 阶切比雪夫多项式
- 当 $N$ 为偶数时，$H_{a}(j0)=\dfrac{1}{\sqrt{1+\varepsilon^{2}}}$ ，$N$ 为奇数时，$H_{a}(j0)=1$
- $H_{a}(j\Omega_{c})= \dfrac{1}{\sqrt{1+\varepsilon^{2}}}$

### 设计指标

- $N$ 滤波器阶数
- $\Omega_{c}$ 通带截止频率
- $\varepsilon$ 与通带波纹 $\delta_{p}$ 有关的参数，满足:
$$
\delta_{p}=20\lg \frac{|H(j\Omega)|_{max}}{|H(j\Omega)|_{min}}=10\lg \frac{|H(j\Omega)|_{max}^{2}}{|H(j\Omega)|_{min}^{2}}=10\lg(1+\varepsilon^{2}) \Rightarrow \varepsilon^{2}=10^{0.1\delta_{p}}-1
$$

### 设计流程

1. 根据指标确定**阶数**

阶数 $N$ 可以由通带、阻带衰减确定，若阻带起始频率为 $\Omega_{st}$ ，则阻带幅度平方函数满足 $|H_{a}(j\Omega)|^{2}\le \frac{1}{A^{2}}$ ，那么由 $\delta_{s}=20\lg \frac{1}{1 / A}=20\lg A$ ，又因为 $\varepsilon^{2}=10^{0.1\delta_{p}}-1$ ，所以有
$$
N\ge \frac{arcch[\sqrt{A^{2}-1} / \varepsilon]}{arcch(\Omega_{st}  /\Omega_{c} ) }=\frac{arcch[\sqrt{10^{0.1\delta_{s}}-1} / \varepsilon]}{arcch(\Omega_{st} / \Omega_{c})} = \frac{ arcch\left[ \sqrt{\frac{10^{0.1\delta_{s}}-1}{10^{0.1\delta_{p}}-1}} \right] }{arcch(\Omega_{st} / \Omega_c)}
$$
其中 $arcch(x)=\ln(x+\sqrt{x^{2}-1})$，也可写作 $\operatorname{arccosh}(x)$。

2. 根据**阶数**和**通带波纹**查表

带归一化函数 $H_{a_{N}}(s)= \dfrac{d_{0}}{s^{N}+a_{N-1}s^{N-1}+\ldots+a_{1}s+a_{0}}$ ，对于 $d_{0}$ 我们用 $H_{a}(j0)=H_{a_{N}}(s)|_{s=0}$ 来计算，根据阶数奇偶性来确定值

3. 去归一化

将 $s$ 替换为 $\dfrac{s}{\Omega_c}$ ，即 $H_{a}(s)=H_{a_{N}}\left( \dfrac{s}{\Omega_{c}} \right)$
有时用 $\Omega_{p}$ 代替 $\Omega_c$

## 模拟低通滤波器转化为数字低通滤波器

### 映射方法

- 将已知的模拟滤波器 $H_{a}(s)$ 映射为数字滤波器 $H(z)$ ，即 $s$ 平面到 $z$ 平面的映射变化
- 映射变化必须满足：
	- $H(z)$ 的频率响应要能模仿 $H_{a}(s)$ 的频率响应，$s$ 平面的虚轴 $s=j\Omega$ 要映射为 $z$ 平面的单位圆 $e^{j\omega}$
	- 因果稳定的 $H_{a}(s)$ 要映射为因果稳定的 $H(z)$ ，即 $s$ 左半平面 $Re[s]<0$ 要映射为 $z$ 平面单位圆内部 $|z|<1$

### 冲激响应不变法

- 使数字滤波器的 $h(n)$ 能模仿模拟滤波器的 $h_{a}(t)$
- 可以通过对 $h_{a}(t)$ 进行等间隔采样来得到数字滤波器的单位冲激响应。若先不考虑幅度修正，有：
$$
h(n)=h_{a}(t)|_{t=nT}
$$
- 那么就有如下流程：
$$
H_{a}(s) \rightarrow h_{a}(t) \rightarrow h(n) \rightarrow H(z)
$$
- 同时这个过程也是时域采样、频率周期延拓的过程，我们有：
$$
H(z)|_{z=e^{sT}}= \frac{1}{T}\sum\limits_{k=-\infty}^{\infty}H_{a}\left( s-j \frac{2\pi}{T}k \right)
$$
> [!NOTE]- 上式推导：时域采样会导致频域周期延拓
> 设采样后的冲激响应为
> $$
> h(n)=h_{a}(nT)
> $$
> 它的 DTFT 为
> $$
> H(e^{j\omega})=\sum\limits_{n=-\infty}^{\infty}h_{a}(nT)e^{-j\omega n}
> $$
> 根据时域采样定理：连续时间信号以间隔 $T$ 采样后，频域会以采样角频率 $\Omega_{s}=\dfrac{2\pi}{T}$ 为周期延拓，因此
> $$
> H(e^{j\omega})=\frac{1}{T}\sum\limits_{k=-\infty}^{\infty}H_{a}\left(j\frac{\omega-2\pi k}{T}\right)
> $$
> 又因为在 $z=e^{sT}$ 上取值时，数字频率对应关系可以写成
> $$
> z=e^{sT}=e^{j\omega}\Rightarrow s=j\frac{\omega}{T}
> $$
> 所以可推广写成
> $$
> H(z)|_{z=e^{sT}}=\frac{1}{T}\sum\limits_{k=-\infty}^{\infty}H_{a}\left(s-j\frac{2\pi}{T}k\right)
> $$
> 这个式子说明：冲激响应不变法本质上保留了时域冲激响应采样点，但频域会发生周期延拓；如果延拓后的频谱互相重叠，就会产生混叠失真。

- 可以看出只有模拟滤波器是严格限带，且频带严格限于折叠频率之内，才不会产生**混叠失真**，但大部分模拟滤波器不是理想的

> [!IMPORTANT] 适用范围
> 冲激响应不变法适合设计低通、带通一类频谱主要集中在低频或有限频带内的滤波器；不适合直接设计高通、带阻滤波器，因为高频部分周期延拓后更容易混叠。

#### 数字化

- 我们设模拟滤波器的系统函数只有一阶极点，且系统函数为真分式：
$$
H_{a}(s)=\sum\limits_{k=1}^{N} \frac{A_{k}}{s-s_{k}}
$$
- 那么有：
$$
h_{a}(t)=L^{-1}[H_{a}(s)]=\sum\limits_{k=1}^{N}A_{k}e^{s_{k}t}u(t)
$$
- 我们进行采样：
$$
h(n)=h_{a}(t)|_{t=nT}=\sum\limits_{k=1}^{N}A_{k}e^{s_{k}nT}u(nT)
$$
- 再求 $z$ 变换：
$$
\begin{aligned}H(z)&=\sum\limits_{n=-\infty}^{\infty}h(n)z^{-n}=\sum\limits_{n=-\infty}^{\infty}\sum\limits _{k=1}^{N}A_{k}e^{s_{k}nT}u(nT)z^{-n}\\&=\sum\limits_{n=0}^{\infty}\sum\limits_{k=1}^{N}A_{k}e^{s_{k}nT}z^{-n}=\sum\limits_{k=1}^{N}\sum\limits_{n=0}^{\infty}A_{k}(e^{s_{k}T}z^{-1})^{n}\\&=\sum\limits_{k=1}^{N} \frac{A_{k}}{1-e^{s_{k}T}z^{-1}}\end{aligned}
$$
- 可以发现 $s$ 平面的极点 $s_{k}$ 变换到 $z$ 平面的极点 $z=e^{s_{k}T}$
- 又因为 $H(z)|_{z=e^{sT}}= \frac{1}{T}\sum\limits_{k=-\infty}^{\infty}H_{a}\left( s-j \frac{2\pi}{T}k \right)$ ，采样后的频率响应幅度会带有 $\dfrac{1}{T}$ 的比例因子，所以我们加以修正：
$$
h(n)=Th_{a}(t)|_{t=nT}
$$
- 所以我们得到最终系统函数：
$$
H(z)=\sum\limits_{k=1}^{N} \frac{TA_{k}}{1-e^{s_{k}T}z^{-1}}
$$
- 这个方法的极点映射关系很重要：
$$
z_{k}=e^{s_{k}T}
$$
- 因此只要模拟滤波器稳定，即 $Re[s_{k}]<0$，就有 $|z_{k}|<1$，数字滤波器也稳定。

#### 用冲激响应不变法设计数字低通滤波器步骤

1. 给定指标：$\omega_{p}\quad \omega_{st}\quad \delta_{p}\quad \delta_{s}$
2. 选择合适 $T$ 值，求解模拟指标 $\Omega_{p}=\dfrac{\omega_{p}}{T}\quad \Omega_{st}=\dfrac{\omega_{st}}{T}$
3. 根据模拟指标设计模拟滤波器 $H_{a}(s)$
4. 将 $H_{a}(s)$ 展开为 $\sum\limits_{k=1}^{N} \dfrac{A_{k}}{s-s_{k}}$ 的形式
5. 最后根据冲激响应不变法得到数字滤波器系统函数 $H(z)$

### 双线性变换法

- 双线性变换法先用非线性频率压缩，把模拟频率轴 $(-\infty,\infty)$ 压缩到有限区间，再通过 $z=e^{s_{1}T}$ 映射到 $z$ 平面，从而消除频谱混叠
- 首先第一步，从 $s \rightarrow s_{1}$ ，我们通过正切变换 $\Omega = c\tan\left( \frac{\Omega_{1}T}{2} \right)$ 实现，可以得到：
$$
s= c\cdot \frac{1-e^{-s_{1}T}}{1+e^{-s_{1}T}}
$$
- 然后第二步，从 $s_{1} \rightarrow z$ ，通过 $z=e^{s_{1}T}$ ，得到：
$$
s=c\cdot \frac{1-z^{-1}}{1+z^{-1}}
$$
- 为了使模拟滤波器与数字滤波器在低频处有较为确切的对应关系，即低频特性类似，需满足：
$$
\Omega=c\tan\left( \frac{\Omega_{1}T}{2} \right)\approx c
 \frac{\Omega_{1}T}{2}\approx \Omega_{1}
$$
- 我们得到常数 $c= \dfrac{2}{T}$ ，所以：
$$
s=\frac{2}{T}\cdot \frac{1-z^{-1}}{1+z^{-1}}
$$
- 双线性变换中，模拟频率 $\Omega$ 与数字频率 $\omega$ 的关系为：
$$
\Omega=\frac{2}{T}\tan\left( \frac{\omega}{2} \right)
$$
- 由于 $\tan(\cdot)$ 是非线性的，数字频率轴 $0\sim\pi$ 会被非线性地映射到模拟频率轴 $0\sim\infty$，这称为**频率畸变**或**频率翘曲**。
- 为了让设计出来的数字滤波器在给定截止频率处准确满足指标，不能直接把数字频率 $\omega_{p},\omega_{st}$ 当成模拟频率使用，而要先把它们变成模拟频率：
$$
\Omega_{p}=\frac{2}{T}\tan\left( \frac{\omega_{p}}{2} \right),\quad
\Omega_{st}=\frac{2}{T}\tan\left( \frac{\omega_{st}}{2} \right)
$$
- 这个“先把数字频率按反映射换成模拟频率”的过程，就叫**预畸变**。

> [!NOTE]- 预畸变的记忆方式
> 双线性变换本身会把模拟频率压缩成数字频率，如果不提前修正，截止频率位置会偏。预畸变就是在设计模拟滤波器之前，先故意把模拟指标“扭一下”，使它经过双线性变换后刚好落在原来要求的数字频率上。
>
> 考试做题时常用步骤是：
> 1. 给定数字指标 $\omega_{p},\omega_{st},\delta_{p},\delta_{s}$
> 2. 预畸变：
> $$
> \Omega=\frac{2}{T}\tan\left( \frac{\omega}{2} \right)
> $$
> 3. 用 $\Omega_{p},\Omega_{st}$ 设计模拟低通滤波器
> 4. 再代入
> $$
> s=\frac{2}{T}\frac{1-z^{-1}}{1+z^{-1}}
> $$
> 得到数字滤波器 $H(z)$
>
> 注意：预畸变只改变频率指标，不改变通带衰减 $\delta_{p}$ 和阻带衰减 $\delta_{s}$。

#### 用双线性变换法设计数字低通滤波器步骤

1. 给定指标：$\omega_{p}\quad \omega_{st}\quad \delta_{p}\quad \delta_{s}$
2. 通过预畸变，确定模拟指标 $\Omega= \dfrac{2}{T}\cdot \tan\left( \frac{\omega}{2} \right)$。若题目把 $T$ 归一化，应始终使用题目给定或课程约定的同一个 $T$
3. 根据模拟指标设计模拟滤波器 $H_{a}(s)$
4. 得到系统函数 $H(z)=H_{a}(s)|_{s=\frac{2}{T}\cdot \frac{1-z^{-1}}{1+z^{-1}}}$

> [!TIP] 两种方法对比
> - 冲激响应不变法：频率关系近似线性，缺点是会频谱混叠。
> - 双线性变换法：不会频谱混叠，缺点是频率非线性，需要预畸变。

## 数字选频滤波器

### 选频滤波器

- 数字滤波器按照频率响应的通带特性可以分为低通、高通、带通和带阻几种
- 数字滤波器的频率响应是以 $2\pi$ 为周期的函数，所以通常只需讨论主值区间 $0\le\omega\le\pi$，即折叠频率以内的频率特性。

#### 分类

- 低通滤波器：
	- $\omega_{p}$ 通带截止频率
	- $\omega_{st}$ 阻带截止频率，且 $\omega_{p}<\omega_{st}$
	- $\delta_{p}$ 通带波纹
	- $\delta_s$ 阻带最小衰减
- 高通滤波器：
	- $\omega_{p}$ 通带截止频率
	- $\omega_{st}$ 阻带截止频率，且 $\omega_{st}<\omega_{p}$
	- $\delta_{p}$ 通带波纹
	- $\delta_s$ 阻带最小衰减
- 带通滤波器：
	- $\omega_{p_{1}},\omega_{p_{2}}$ 通带截止频率
	- $\omega_{st_{1}},\omega_{st_{2}}$ 阻带截止频率，且 $\omega_{st_{1}}<\omega_{p_{1}}<\omega_{p_{2}}<\omega_{st_{2}}$
	- $\delta_{p}$ 通带波纹
	- $\delta_s$ 阻带最小衰减
- 带阻滤波器：
	- $\omega_{p_{1}},\omega_{p_{2}}$ 通带截止频率
	- $\omega_{st_{1}},\omega_{st_{2}}$ 阻带截止频率，且 $\omega_{p_{1}}<\omega_{st_{1}}<\omega_{st_{2}}<\omega_{p_{2}}$
	- $\delta_{p}$ 通带波纹
	- $\delta_s$ 阻带最小衰减

### 数字频率转换

- 给定一个数字低通滤波器 $H_{L}(z)$ ，希望得到数字选频滤波器 $H_{d}(z)$
- 假设我们定义一个映射关系 $z^{-1}=G(Z^{-1})$ ，那么有 $H_{d}(Z)=H_{L}(z)|_{z^{-1}=G(Z^{-1})}$
- 我们希望因果稳定的 $H_{L}(z)$ 变换后仍是因果稳定的，因此映射关系需要满足：
	- $z$ 平面的单位圆映射为 $Z$ 平面的单位圆
	- $z$ 平面单位圆内部映射为 $Z$ 平面单位圆内部
	- $G(Z^{-1})$ 是 $Z^{-1}$ 的有理函数
---
- 我们用 $\theta$ 表示 $z$ 平面的数字频率，$\omega$ 表示 $Z$ 平面的数字频率
- 有 $e^{-j\theta}=G(e^{-j\omega})=|G(e^{-j\omega})|e^{j\arg[G(e^{-j\omega})]}$ ，所以有 $|G(e^{-j\omega})|=1$ ，即 $G(Z^{-1})$ 为全通函数，所以可以写为:
$$
z^{-1}=G(Z^{-1})=\prod_{i=1}^{N} \frac{Z^{-1}-a_{i}^{*}}{1-a_{i}Z^{-1}}
$$

> [!TIP] 数字频率转换做题顺序
> 1. 明确已有低通滤波器的截止频率 $\theta_{c}$
> 2. 明确目标滤波器的截止频率 $\omega_{c}$ 或 $\omega_{1},\omega_{2}$
> 3. 根据目标类型选择低通、高通、带通或带阻的 $G(Z^{-1})$
> 4. 将原低通系统函数中的 $z^{-1}$ 替换为 $G(Z^{-1})$
> 5. 检查映射后是否仍满足因果稳定和单位圆到单位圆的条件

### 转换

#### 数字低通——数字低通

- 给定 $\theta_{c}$ 为给定数字低通滤波器的截止频率，$\omega_{c}$ 为目标滤波器的截止频率，那么映射关系为：
$$
z^{-1}=G(Z^{-1})=\frac{Z^{-1}-\alpha}{1-\alpha Z^{-1}}
$$
- 我们有：
$$
e^{-j\theta_{c}}= \frac{e^{-j\omega_c}-\alpha}{1-\alpha e^{-j\omega_c}}
$$
- 得到：
$$
\alpha= \frac{\sin\left(\frac{\theta_{c}-\omega_{c}}{2}\right)}{\sin\left(\frac{\theta_{c}+\omega_{c}}{2}\right)}
$$

#### 数字低通——数字高通

- 给定 $\theta_{c}$ 为给定数字低通滤波器的截止频率，$\omega_{c}$ 为目标滤波器的截止频率，那么映射关系为：
$$
z^{-1}=G(Z^{-1})=-\frac{Z^{-1}+\alpha}{1+\alpha Z^{-1}}
$$

- 我们有：
$$
\begin{aligned}\theta_{c}&\leftrightarrow -\omega_{c}\\-\theta_{c}& \leftrightarrow \omega_{c}\\0& \leftrightarrow \pi\end{aligned}
$$
- 同上我们得到：
$$
\alpha= -\frac{\cos\left(\frac{\theta_{c}+\omega_{c}}{2}\right)}{\cos\left(\frac{\theta_{c}-\omega_{c}}{2}\right)}
$$
- 若给定高通指标 $\omega_{p}$ 和 $\omega_{st}$ ，我们求低通指标 $\theta_{p}$ 和 $\theta_{st}$
- 若专门取 $\theta_{c}=\pi-\omega_{c}$，则 $\alpha=0$，映射才会简化为 $z^{-1}=-Z^{-1}$。这只是截止频率互补时的特殊情况，不是所有低通到高通转换都能这样简化
- 又因为 $\theta_{st} \leftrightarrow -\omega_{st}$ ，此时 $z^{-1}=e^{-j\theta_{st}}$ 和 $Z^{-1}=e^{-[j(-\omega_{st})]}=e^{j\omega_{st}}$ ，再代入映射关系，有 $e^{-j\theta_{st}}=e^{j\omega_{st}}$ ，所以 $\theta_{st}=\pi-\omega_{st}$ ，所以映射关系简化为：
$$
z^{-1}=G(Z^{-1})=-Z^{-1}
$$

#### 数字低通——数字带通

- 给定 $\theta_{c}$ 为给定数字低通滤波器的截止频率，$\omega_{1},\omega_{2}$ 为目标滤波器的下、上截止频率，那么映射关系为：
$$
z^{-1}=G(Z^{-1})= - \frac{Z^{-2}+\alpha_{1}Z^{-1}+\alpha_{2}}{\alpha_{2}Z^{-2}+\alpha_{1}Z^{-1}+1}
$$
- 我们有：
$$
\begin{aligned}\theta_{c}&\leftrightarrow -\omega_{1},\omega_{2}\\-\theta_{c}& \leftrightarrow \omega_{1},-\omega_{2}\\0& \leftrightarrow \pm\omega_{0}\\\pi& \leftrightarrow 0\end{aligned}
$$
- 得到：
$$
\alpha_{1}= \frac{-2\beta k}{k+1}\quad \alpha_{2}=- \frac{k-1}{k+1}
$$
- 其中：
$$
\beta=\frac{\cos\left(\frac{\omega_{2}+\omega_{1}}{2}\right)}{\cos\left(\frac{\omega_{2}-\omega_{1}}{2}\right)}  \quad   k=\cot\left( \frac{\omega_{2}-\omega_{1}}{2} \right)\tan \frac{\theta_{c}}{2}
$$

#### 数字低通——数字带阻

- 给定 $\theta_{c}$ 为给定数字低通滤波器的截止频率，$\omega_{1},\omega_{2}$ 为目标滤波器的下、上截止频率，那么映射关系为：
$$
z^{-1}=G(Z^{-1})= \frac{Z^{-2}+\alpha_{1}Z^{-1}+\alpha_{2}}{\alpha_{2}Z^{-2}+\alpha_{1}Z^{-1}+1}
$$
- 我们有：
$$
\begin{aligned}\theta_{c}&\leftrightarrow \omega_{1},-\omega_{2}\\-\theta_{c}& \leftrightarrow -\omega_{1},\omega_{2}\\0& \leftrightarrow 0,\pi\\\pi& \leftrightarrow \pm \omega_{0}\end{aligned}
$$
- 得到：
$$
\alpha_{1}= \frac{-2\beta }{k+1}\quad \alpha_{2}=\frac{1-k}{1+k}
$$
- 其中：
$$
\beta=\frac{\cos\left(\frac{\omega_{2}+\omega_{1}}{2}\right)}{\cos\left(\frac{\omega_{2}-\omega_{1}}{2}\right)}  \quad   k=\tan\left( \frac{\omega_{2}-\omega_{1}}{2} \right)\tan \frac{\theta_{c}}{2}
$$

> 注意：数字频率转换公式对“原型频率记为 $\theta$、目标频率记为 $\omega$”这一约定很敏感。若题目采用相反记号，应先重画频率对应关系，不能只替换字母。

## 本章自查问题

1. 最小相位系统的零点、极点分别位于哪里？为什么逆系统也稳定？
2. 全通系统的零点和极点为什么是共轭倒数关系？
3. 巴特沃斯与切比雪夫 I 型的幅频特点有何不同？
4. 巴特沃斯阶数计算后为什么要向上取整？$\Omega_c$ 应落在哪个允许范围内？
5. 冲激响应不变法为什么会产生频率混叠？
6. 双线性变换为什么没有混叠，却需要预畸变？
7. 两种模拟到数字映射如何保证稳定系统仍然稳定？
8. 完整 IIR 选频滤波器设计流程分为哪五步？
9. 数字低通到高通的映射在什么特殊条件下可以简化为 $z^{-1}=-Z^{-1}$？
