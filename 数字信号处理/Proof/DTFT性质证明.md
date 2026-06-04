[[01_章节笔记/02 第二章 Z变换与DTFT变换#DTFT 的性质]]

# 时移
$$
\begin{aligned}DFTF[x(n-m)]&=\sum\limits_{n=-\infty}^{\infty} x(n-m)e^{-j\omega n}\end{aligned}
$$
- 我们令 $c=n-m$ ，则 $c=k+m$
- 原式转化为：
$$
DTFT[x(c)]=\sum\limits_{c=-\infty}^{\infty} x(c)e^{-j\omega(c+m)}=e^{-j\omega m}\sum\limits_{c=-\infty}^{\infty} x(c)e^{-j\omega c}=e^{-j\omega m}X(e^{j\omega})
$$
# 反转
$$
DFTF[x(-n)]=\sum\limits_{n=-\infty}^{\infty}x(-n)e^{-j\omega n}
$$
- 我们令 $n=-n$ ，那么原式转化为：
$$
\sum\limits_{n=-\infty}^{\infty} x(n)e^{-(j(-\omega) n)}=X(e^{-j\omega})
$$
# 共轭
$$
\begin{aligned}DTFT[x^{*}(n)]&=\sum\limits_{n=-\infty}^{\infty}x^{*}(n)e^{-j\omega n} \\ &=\sum\limits_{n=-\infty}^{\infty}\left(x(n)(e^{-j\omega})^{*} \right)^{*} \\ &=\sum\limits_{n=-\infty}^{\infty} \left(x(n)e^{j\omega}\right)^{*}=X^{*}(e^{-j\omega})\end{aligned}

$$
