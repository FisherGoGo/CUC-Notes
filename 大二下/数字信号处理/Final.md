# 周期计算

对于 $\sin(\omega_{0} n)$ 的正弦函数，若 $T=\frac{2\pi}{\omega_{0}}$ 为有理数则有周期，反之没有
# DTFT
$$
X(e^{j\omega})=DTFT[x(n)]=\sum\limits_{n=-\infty}^{\infty}x(n)e^{-j\omega n}
$$
$$
x(n)=IDTFT[X(e^{j\omega})]=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}d\omega
$$

| 性质 | 时域 | 频域 |
|---|---|---|
| 线性 | $ax(n)+by(n)$ | $aX(e^{j\omega})+bY(e^{j\omega})$ |
| 时移 | $x(n-m)$ | $e^{-j\omega m}X(e^{j\omega})$ |
| 频移 | $e^{j\omega_0n}x(n)$ | $X(e^{j(\omega-\omega_0)})$ |
| 反转 | $x(-n)$ | $X(e^{-j\omega})$ |
| 共轭 | $x^*(n)$ | $X^*(e^{-j\omega})$ |
