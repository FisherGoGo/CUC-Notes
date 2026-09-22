# Lec03 Multiplication and Inverse Matrices

这节课主要介绍了矩阵乘法和逆

## Matrix Multiplication

课中用了五种方法来进行矩阵乘法 $AB=C$

首先若 $A$ 为 $n\times m$ 矩阵，而 $B$ 为 $m\times p$ 矩阵，那么 $C$ 为 $n\times p$ 矩阵，在下文会用以前的知识讲解为何

### Standard

最标准的方法，也是国内用的最多的方法：

$$
c_{ij}=\sum\limits_{k=1}^{m}a_{ik}b_{kj}
$$

这样子可以直接算出 $C$ 矩阵每个位置的具体值

### Columns and Rows

这个方法在前两节课经常提到过，一个矩阵左乘一个列向量，可以看成矩阵各列的线性组合，结果是一个新的列向量；一个行向量左乘一个矩阵，则得到矩阵各行的线性组合

那么 $AB$ 可以拆成矩阵 $A$ 左乘 $p$ 个列向量，得到 $p$ 个列向量，也可以拆成 $B$ 右乘 $n$ 个行向量，得到 $n$ 个行向量，所以最终矩阵为 $n\times p$

### Column times row

这个方法属实新颖，我们考虑用列向量左乘行向量会发生什么，比如

$$
\begin{bmatrix}
2 \\
3 \\
4
\end{bmatrix} \begin{bmatrix}
1& 6
\end{bmatrix}=\begin{bmatrix}
2&12 \\
3&18 \\
4&24
\end{bmatrix}
$$

可以发现对于答案矩阵，每一列都是其他列的倍数，每一行也是其他行的倍数，或者是每一行都是右侧行向量的倍数，每一列都是左侧列向量的倍数，那么对于普通的矩阵乘法就可以写成：

$$
AB=\sum\limits_{k=1}^{m} \begin{bmatrix}
a_{1k} \\
a_{2k} \\
\vdots \\
a_{nk}
\end{bmatrix} \begin{bmatrix}
b_{k1}&b_{k2}&\ldots&b_{kp}
\end{bmatrix}
$$

### Blocks

同样我们也可以对矩阵进行分块，如下矩阵

$$
\begin{bmatrix}
A_{1}&A_{2} \\
A_{3}&A_{4}
\end{bmatrix} \begin{bmatrix}
B_{1}&B_{2} \\
B_{3}&B_{4}
\end{bmatrix}= \begin{bmatrix}
C_{1}&C_{2} \\
C_{3}&C_{4}
\end{bmatrix}
$$

其中 $C_{1}=A_{1}B_{1}+A_{2}B_{3}$ ，其他同理

## Inverses

首先我们先来看那些不存在逆的矩阵，我们称为 singular ，即奇异矩阵，如下例子

$$
\begin{bmatrix}
1&3 \\
2&6
\end{bmatrix} \begin{bmatrix}
3 \\
-1
\end{bmatrix} =\begin{bmatrix}
0 \\
0
\end{bmatrix}
$$

可以写成 $AX= \mathbf{0}$ ，首先这里 $X\ne \mathbf{0}$ ，为什么这个矩阵不存在逆，逆矩阵的定义为 $A^{-1}A=I$ ，你会发现你无法找到一个矩阵使得满足条件，也可以从这个视角看，若存在逆矩阵 $A^{-1}$ ，那么有 $A^{-1}AX=A^{-1} \mathbf{0}$ ，即 $X= \mathbf{0}$ ，这与我们之前的条件矛盾，说明 $A$ 中存在一列无法做出任何贡献，其为其他列的线性组合

好的那我们现在来看那些非奇异矩阵，存在逆的矩阵，如

$$
\begin{bmatrix}
1&3 \\
2&7
\end{bmatrix}_{A} \begin{bmatrix}
a&b \\
c&d
\end{bmatrix}_{A^{-1}}=\begin{bmatrix}
1&0 \\
0&1
\end{bmatrix}_{I}
$$

我们的目的是解出 $A^{-1}$ ，可以看出解 $n$ 个线性方程组，即 $A$ 乘以 $A^{-1}$ 的第 $j$ 列得到 $I$ 的第 $j$ 列，这与 Lec02 里讲的相似，但是我们想要一下子解决 $n$ 个线性方程组，于是有了如下方法

### Gauss-Jordan Elimination

我们做如下矩阵：

$$
\begin{bmatrix}
A&I
\end{bmatrix}=\begin{bmatrix}
1&3&1&0 \\
2&7&0&1
\end{bmatrix}
$$

然后对这个矩阵进行变换，使得其变成

$$
\begin{bmatrix}
I&E
\end{bmatrix}
$$

那么 $A^{-1}=E$ ，为什么这样子可行

因为做变换相当于左乘变换矩阵，即

$$
E \begin{bmatrix}
A&I
\end{bmatrix}=\begin{bmatrix}
I&E
\end{bmatrix}
$$

那么 $EA=I$ ，根据定义 $E$ 为 $A$ 的逆矩阵

