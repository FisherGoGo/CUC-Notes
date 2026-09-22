# Lec05 Transposes, Permutations, Vector Spaces

## Permutations

置换矩阵，在上一讲有提到过，我们会在消元遇到没有主元的情况下在当前列下方找到非零元素后进行行置换，这时候就会用到置换矩阵，即 $PA=LU$

对于大小为 $n$ 的方阵，存在 $n!$ 个置换矩阵

有一个特殊性质，置换矩阵的逆等于其转置 $P^{-1}=P^{T}$ ，且 $P^{T} P= I$

## Transposes

当我们转置一个矩阵时，它的行变成列、列变成行

$$
(A^{T})_{ij}=A_{ji}
$$

若 $A^{T}=A$ ，那我们称这个矩阵是对称的，还有 $A^{T}A$ 一定是对称的，如下

$$
(A^{T}A)^{T}=A^{T}A^{TT}=A^{T}A
$$

## Vector spaces

我们已经知道向量可以相加、也可以乘一个数，所以可以构造向量的线性组合，所有满足这些运算规则的一组向量，我们称之为 向量空间

经典的比如二维向量 $`\begin{bmatrix}a \\ b\end{bmatrix}`$ ，就是所有二维实数向量组成的集合，称为 $\mathbb{R}^{2}$ ，也就是我们熟悉的二维平面

然后进行推广，对于所有由 $n$ 个实数组成的列向量的集合

$$
\begin{bmatrix} x_{1}  \\  x_{2}  \\  \vdots \\ x_{n} \end{bmatrix}
$$

称为 $\mathbb{R}^{n}$

这个集合有一个关键性质，里边的向量进行线性组合后，依旧在这个集合里，称为封闭性

### Subspaces

对于一个大的向量空间里，本身还能独立构成一个向量空间的一个子集，称为子空间

比如说我们取一个非零向量 $`v=\begin{bmatrix}a \\ b\end{bmatrix}`$ ，然后考虑所有 $cv$ 其中 $c\in \mathbb{R}$ ，那么集合 $`\{cv: c\in \mathbb{R}\}`$ 也是一个向量空间，为一个经过原点的直线

$\mathbb{R}^{2}$ 的子空间有：$\mathbb{R}^{2}$ 、过原点的直线、$`\{0\}`$

$\mathbb{R}^{3}$ 的子空间有：$\mathbb{R}^{3}$ 、过原点的直线、过原点的平面、$`\{0\}`$

### Column space

假设有一个矩阵

$$
A = \begin{bmatrix}1&3 \\ 2 & 3 \\ 4 & 1 \end{bmatrix}
$$

其有两个列向量，都为三维向量，那么取它们的所有线性组合，称为矩阵 $A$ 的列空间，即

$$
C(A)=\{c_{1} \begin{bmatrix}1\\ 2 \\ 4\end{bmatrix}+c_{2} \begin{bmatrix}3 \\ 3\\ 1\end{bmatrix} : c_{1},c_{2}\in \mathbb{R} \} = \text{span} \{\begin{bmatrix}1 \\ 2 \\ 4\end{bmatrix} , \begin{bmatrix}3 \\ 3\\ 1\end{bmatrix} \}
$$
