# Lec08 Ax = b

解决了 $Ax = 0$ ，现在来解决 $Ax=b$ 看看

## Solvability conditions on b

举同样的矩阵

$$
A = \begin{bmatrix}1&2&2&2  \\ 2&4&6&8 \\ 3&6&8&10\end{bmatrix}
$$

可见这个矩阵第三行为第一行加第二行，那么右侧也必须满足 $b_{3}=b_{1}+b_{2}$

同样也可以说 $b$ 必须处于 $A$ 的列空间中，即 $C(A)$

## Complete solution

求解 $Ax=b$ ，我们一般是先找特解 （particular solution），然后再加上所有零空间中的向量得到通解，举如下例子

$$
\begin{bmatrix}1&2&2&2  \\ 2&4&6&8 \\ 3&6&8&10\end{bmatrix} \begin{bmatrix}x_{1} \\ x_{2} \\ x_{3} \\ x_{4}\end{bmatrix} = \begin{bmatrix}1 \\ 5 \\ 6\end{bmatrix}
$$

化简后得到

$$
\begin{bmatrix}1&2&2&2  \\  0&0&2&4 \\ 0&0&0&0 \end{bmatrix} \begin{bmatrix}x_{1} \\ x_{2} \\ x_{3} \\ x_{4}\end{bmatrix} = \begin{bmatrix}1 \\ 3 \\ 0\end{bmatrix}
$$

### A particular solution

那现在我们直接令所有自由元都为 $0$ ，那么可解出

$$
x_{p} = \begin{bmatrix}-2  \\ 0 \\  3/2 \\ 0\end{bmatrix}
$$

### Combined with the nullspace

然后全解为特解加上任意零空间中的向量

$$
x_{c}=x_{p}+x_{n}=  \begin{bmatrix}-2  \\ 0 \\  \dfrac{3}{2} \\ 0\end{bmatrix} + c_{1} \begin{bmatrix}-2 \\ 1 \\ 0 \\ 0\end{bmatrix}+c_{2}\begin{bmatrix}2 \\ 0 \\ -2 \\ 1\end{bmatrix}
$$

## Rank

上一讲已经讲过秩为矩阵中主元的个数，一定有 $r\le n$ 和 $r\le m$ ，对于 $m\times n$ 矩阵，我们分以下情况讨论解的数量

### Full column rank

若 $r=n$ ，说明每一列都有主元，那么自由元数量为 $0$ ，因此 $`N(A)=\{\mathbf{0}\}`$ ，此时方程要么只有一个解要么无解

### Full row rank

若 $r=m$ ，说明每一行都有主元，因此消元时不存在 $0=c$ 这种约束，因此对于任意 $b$ 都有解，若 $n>m$，则有无穷多解；若 $n=m$，则只有一个解

### Full row and column rank

若 $r=n=m$ ，即方阵且每一行每一列都有主元，此时 $R=I$ ，那么对于任意 $b$ 都有且只有一个解

