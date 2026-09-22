# Lec11 Matrix Spaces; Rank 1; Small World Graphs

## New vector spaces

书接上文，我们来继续讨论由矩阵而非列向量组成的 *向量空间*

还是 $3\times 3$ 矩阵，它的维度是 $\dim =9$ ，那么它的一组基是什么，最容易想到的即为

$$
\begin{bmatrix}1&0&0 \\ 0&0&0 \\ 0&0&0\end{bmatrix} ,\begin{bmatrix}0&1&0 \\ 0&0&0 \\ 0&0&0\end{bmatrix},\begin{bmatrix}0&0&1 \\ 0&0&0 \\ 0&0&0\end{bmatrix},\ldots,\begin{bmatrix}0&0&0 \\ 0&0&0 \\ 0&0&1\end{bmatrix}
$$

那对称矩阵呢，它的维度是 $\dim = 6$ ，一组基如下

$$
\begin{bmatrix}1&0&0 \\ 0&0&0 \\ 0&0&0\end{bmatrix} ,\begin{bmatrix}0&1&0 \\ 1&0&0 \\ 0&0&0\end{bmatrix},\begin{bmatrix}0&0&0 \\ 0&1&0 \\ 0&0&0\end{bmatrix},\ldots,\begin{bmatrix}0&0&0 \\ 0&0&0 \\ 0&0&1\end{bmatrix}
$$

同样上三角矩阵的维度为 $\dim = 6$ ，这里不赘述

记对称矩阵空间为 $S$，上三角矩阵空间为 $U$，全体 $3\times 3$ 矩阵空间为 $M$。子空间 $D=S\cap U$ 为一个合法的向量空间，因为它们两个的交集为所有对角矩阵，那它们两个的并集是一个向量空间吗，显然不是，但是 $S+U=M$ ，这里的意思是任取一个矩阵来自对称矩阵，再任取一个矩阵来自上三角矩阵，将它们两个相加，可以生成所有 $3\times 3$ 矩阵，然后有一个有意思的式子

$$
\dim S +\dim U =\dim(S+U) +\dim(S\cap U)
$$

## Rank one matrices

我们称 $\operatorname{rank}(A)=1$ 的矩阵为秩一矩阵，如下边这个

$$
A=
\begin{bmatrix}1&4&5 \\ 2&8&10\end{bmatrix}
$$

所有秩一矩阵都可以变成 $A=UV^T$ 的形式，即一个非零列向量左乘一个行向量，如

$$
A = \begin{bmatrix}1 \\ 2\end{bmatrix} \begin{bmatrix}1&4&5\end{bmatrix}
$$

