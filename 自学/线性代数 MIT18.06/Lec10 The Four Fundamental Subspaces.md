# Lec10 The Four Fundamental Subspaces

对于 $m\times n$ 矩阵 $A$，这一讲主要讲四个基本子空间，分别是

- 列空间 $C(A)$ ，是一个在 $\mathbb{R}^{m}$ 的向量空间
- 零空间 $N(A)$ ，是一个在 $\mathbb{R}^{n}$ 的向量空间
- 行空间 $C(A^{T})$ ，是一个在 $\mathbb{R}^{n}$ 的向量空间
- 左零空间 $N(A^{T})$ ，是一个在 $\mathbb{R}^{m}$ 的向量空间

## Basis and Dimension

讨论它们的基与维度，对于秩为 $r$ 的 $m\times n$ 矩阵

### 列空间

$$
\dim C(A)=r
$$

### 零空间

$$
\dim N(A)=n-r
$$

### 行空间

之前我们讲过，先通过行变换化为 RREF；若主元列恰好在前 $r$ 列，就有如下形式，否则还需重排列与未知量

$$
R= \begin{bmatrix}I&F \\ 0&0\end{bmatrix}
$$

可见其维度也为秩

$$
\dim C(A^{T})=r
$$

### 左零空间

首先显而易见的结论为

$$
\dim N(A^{T})=m-r
$$

但是老师给了十分有意思的视角，类似 Lec03 里的方法，我们对一个矩阵作如下变换

$$
\begin{bmatrix}A_{m\times n}&I_{m\times m}\end{bmatrix} \rightarrow \begin{bmatrix}R_{m\times n}&E_{m\times m}\end{bmatrix}
$$

同样地，那么 $EA=R$ ，对于如下例子

$$
EA =
\begin{bmatrix}-1&2&0 \\ 1&-1&0 \\ -1&0&1\end{bmatrix}
\begin{bmatrix}1&2&3&1 \\ 1&1&2&1 \\ 1&2&3&1\end{bmatrix}
=
\begin{bmatrix}1&0&1&1 \\ 0&1&1&0 \\ 0&0&0&0\end{bmatrix}
=
R
$$

那么矩阵 $E$ 的最后一行转置后，即为左零空间的一组基中的唯一向量，因为这个正是使得行的线性组合为 $0$ 的向量

## New vector space

这里扩展了一下，之前我们一直都是在讨论列向量的向量空间，现在转换视角，来看看矩阵组成的 *向量空间*

比如我们令所有的 $3\times 3$ 矩阵组成一个向量空间，称为 $M$ ，我们任取其中的矩阵作线性组合，即做矩阵加法和标量乘法，得到的还是 $3\times 3$ 矩阵，所以这个集合是封闭的，检查向量空间不要求对矩阵乘法封闭；如下集合也都是它的子空间：

- 所有上三角矩阵
- 所有对称矩阵
- 所有对角矩阵

那我们考虑对于对角矩阵来说，这个向量空间的维数为 $3$ ，这个很容易理解，其他类似推广