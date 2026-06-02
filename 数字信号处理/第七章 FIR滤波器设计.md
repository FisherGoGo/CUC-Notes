# FIR 数字滤波器设计

## FIR 的特点

FIR 滤波器的系统函数为：

$$
H(z)=\sum\limits_{n=0}^{N-1}h(n)z^{-n}
$$

其中 $h(n)$ 长度为 $N$。

FIR 相比 IIR 的主要特点：

- 很容易实现严格线性相位
- 极点只在原点，因果 FIR 总是稳定
- 非因果有限长序列总可以通过延时变成因果序列
- 可用 FFT 实现快速卷积
- 同样设计指标下，阶数通常比 IIR 高

---

# 线性相位 FIR

频率响应：

$$
H(e^{j\omega})=\sum\limits_{n=0}^{N-1}h(n)e^{-j\omega n}
=H(\omega)e^{j\theta(\omega)}
$$

线性相位要求：

$$
\theta(\omega)=-\tau\omega
$$

或：

$$
\theta(\omega)=\beta-\tau\omega
$$

两者群延时都为常数：

$$
\tau_g(\omega)=-\frac{d\theta(\omega)}{d\omega}=\tau
$$

## 线性相位条件

若 $h(n)$ 是实序列，则 FIR 具有严格线性相位的充要条件为：

偶对称：

$$
h(n)=h(N-1-n)
$$

或奇对称：

$$
h(n)=-h(N-1-n)
$$

群延时：

$$
\tau=\frac{N-1}{2}
$$

## 频率响应形式

偶对称时：

$$
H(e^{j\omega})=H(\omega)e^{-j\omega\frac{N-1}{2}}
$$

$$
H(\omega)=\sum\limits_{n=0}^{N-1}h(n)
\cos\left[\left(\frac{N-1}{2}-n\right)\omega\right]
$$

奇对称时：

$$
H(e^{j\omega})=H(\omega)e^{j\frac{\pi}{2}}e^{-j\omega\frac{N-1}{2}}
$$

$$
H(\omega)=\sum\limits_{n=0}^{N-1}h(n)
\sin\left[\left(\frac{N-1}{2}-n\right)\omega\right]
$$

---

# 四类线性相位 FIR

| 类型 | 长度 $N$ | 对称性 | 必然零点 | 适用情况 |
|------|----------|--------|----------|----------|
| I 型 | 奇数 | 偶对称 | 无强制零点 | 低通、高通、带通、带阻均可 |
| II 型 | 偶数 | 偶对称 | $\omega=\pi$ 处 $H(\pi)=0$ | 不能设计高通、带阻 |
| III 型 | 奇数 | 奇对称 | $\omega=0,\pi$ 处为 0 | 微分器、希尔伯特变换器 |
| IV 型 | 偶数 | 奇对称 | $\omega=0$ 处 $H(0)=0$ | 微分器、希尔伯特变换器 |

> [!IMPORTANT] 记忆
> 偶对称做常规选频滤波器；奇对称常用于微分器和希尔伯特变换器。
>
> II 型在 $\pi$ 处必为 0，所以不能做高通、带阻。
>
> III / IV 型在 0 处必为 0，所以不能做低通。

## 线性相位 FIR 的零点性质

线性相位 FIR 满足：

$$
H(z)=\pm z^{-(N-1)}H(z^{-1})
$$

若 $H(z)$ 存在零点：

$$
z_0=re^{j\theta}
$$

则也存在倒易零点：

$$
\frac{1}{z_0}=\frac{1}{r}e^{-j\theta}
$$

由于 $h(n)$ 为实序列，零点还会以共轭形式出现。因此一般零点成组出现：

$$
z_0,\quad z_0^*,\quad \frac{1}{z_0},\quad \frac{1}{z_0^*}
$$

---

# 窗函数设计法

FIR 设计目标是用有限长 $h(n)$ 逼近理想频率响应 $H_d(e^{j\omega})$。

窗函数法思路：

$$
H_d(e^{j\omega})
\xrightarrow{IDTFT}
h_d(n)
\xrightarrow{\text{加窗}}
h(n)=h_d(n)w(n)
$$

理想滤波器通常有突变边界，所以 $h_d(n)$ 无限长、非因果。加窗相当于截取并平滑 $h_d(n)$。

## 理想低通

线性相位理想低通：

$$
H_d(e^{j\omega})=
\begin{cases}
e^{-j\alpha\omega}, & |\omega|\le \omega_c\\
0, & \omega_c<|\omega|\le \pi
\end{cases}
$$

理想单位冲激响应：

$$
h_d(n)=
\frac{\sin[\omega_c(n-\alpha)]}{\pi(n-\alpha)}
$$

当 $n=\alpha$ 时：

$$
h_d(\alpha)=\frac{\omega_c}{\pi}
$$

为得到 I 型线性相位 FIR，一般取：

$$
\alpha=\frac{N-1}{2}
$$

## 加窗影响

加窗后：

$$
h(n)=h_d(n)w(n)
$$

频域上等价于理想频响与窗函数频响卷积。

主要影响：

- 过渡带宽度由窗函数主瓣宽度决定
- 通带和阻带波动由旁瓣决定
- 增大 $N$ 可减小过渡带宽度
- 仅增大 $N$ 不能改变最大旁瓣相对高度
- 截断造成的固定旁瓣波动称为吉布斯效应

---

# 常用窗函数

## 矩形窗

$$
w(n)=R_N(n)
$$

特点：

- 主瓣最窄
- 旁瓣最大
- 阻带衰减最差

主瓣宽度近似：

$$
\Delta\omega\approx \frac{4\pi}{N}
$$

## 巴特列特窗（三角窗）

$$
w(n)=
\begin{cases}
\dfrac{2n}{N-1}, & 0\le n\le \dfrac{N-1}{2}\\[6pt]
2-\dfrac{2n}{N-1}, & \dfrac{N-1}{2}<n\le N-1
\end{cases}
$$

## 汉宁窗

$$
w(n)=\frac{1}{2}\left[1-\cos\left(\frac{2\pi n}{N-1}\right)\right]R_N(n)
$$

主瓣宽度近似：

$$
\Delta\omega\approx \frac{8\pi}{N}
$$

## 海明窗

$$
w(n)=\left[0.54-0.46\cos\left(\frac{2\pi n}{N-1}\right)\right]R_N(n)
$$

主瓣宽度近似：

$$
\Delta\omega\approx \frac{8\pi}{N}
$$

## 布莱克曼窗

$$
w(n)=
\left[
0.42-0.5\cos\left(\frac{2\pi n}{N-1}\right)
+0.08\cos\left(\frac{4\pi n}{N-1}\right)
\right]R_N(n)
$$

主瓣宽度近似：

$$
\Delta\omega\approx \frac{12\pi}{N}
$$

## 凯泽窗

$$
w(n)=
\frac{
I_0\left(\beta\sqrt{1-\left(1-\frac{2n}{N-1}\right)^2}\right)
}
{I_0(\beta)}R_N(n)
$$

$\beta$ 控制主瓣宽度和旁瓣幅度：

- $\beta=0$：矩形窗
- $\beta\approx 5.44$：接近海明窗
- $\beta\approx 8.5$：接近布莱克曼窗

## 窗函数性能对比

| 窗函数 | 旁瓣峰值 | 阻带最小衰减 | 过渡带特点 |
|--------|----------|--------------|------------|
| 矩形窗 | 约 $-13\text{dB}$ | 约 $-21\text{dB}$ | 最窄 |
| 巴特列特窗 | 约 $-25\text{dB}$ | 约 $-25\text{dB}$ | 较宽 |
| 汉宁窗 | 约 $-31\text{dB}$ | 约 $-44\text{dB}$ | 较宽 |
| 海明窗 | 约 $-41\text{dB}$ | 约 $-53\text{dB}$ | 较宽 |
| 布莱克曼窗 | 约 $-57\text{dB}$ | 约 $-74\text{dB}$ | 最宽 |

> [!NOTE] 权衡
> 主瓣窄意味着过渡带窄；旁瓣低意味着阻带衰减好。二者通常不能同时最优。

---

# 窗函数法设计步骤

1. 给定理想频率响应 $H_d(e^{j\omega})$ 和设计指标
2. 由 IDTFT 求 $h_d(n)$
3. 根据阻带衰减选择窗函数
4. 根据过渡带宽度 $\Delta\omega$ 确定 $N$
5. 计算 $h(n)=h_d(n)w(n)$
6. 求 $H(e^{j\omega})$ 并检查指标

## 常见理想冲激响应

低通：

$$
h_d(n)=\frac{\sin[\omega_c(n-\tau)]}{\pi(n-\tau)}
$$

高通：

$$
h_d(n)=
\frac{\sin[\pi(n-\tau)]}{\pi(n-\tau)}
-
\frac{\sin[\omega_c(n-\tau)]}{\pi(n-\tau)}
$$

带通：

$$
h_d(n)=
\frac{\sin[\omega_{c2}(n-\tau)]}{\pi(n-\tau)}
-
\frac{\sin[\omega_{c1}(n-\tau)]}{\pi(n-\tau)}
$$

带阻：

$$
h_d(n)=
\frac{\sin[\pi(n-\tau)]}{\pi(n-\tau)}
-
\frac{\sin[\omega_{c2}(n-\tau)]}{\pi(n-\tau)}
+
\frac{\sin[\omega_{c1}(n-\tau)]}{\pi(n-\tau)}
$$

其中：

$$
\tau=\frac{N-1}{2}
$$

当 $n=\tau$ 时，用极限值代入。例如低通：

$$
h_d(\tau)=\frac{\omega_c}{\pi}
$$

> [!TIP] 考试抓手
> 窗函数法题目一般按“求 $\omega_c$、求 $\Delta\omega$、选窗、定 $N$、写 $h_d(n)$、乘 $w(n)$”六步走。
