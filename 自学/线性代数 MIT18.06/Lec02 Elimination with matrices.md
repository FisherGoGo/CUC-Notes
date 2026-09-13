这节课主要讲了矩阵的消元，还涉及了一点逆矩阵

# Method of Elimination

显示简单的消元过程，举了如下例子来教学

$$
\begin{bmatrix}
1&2&1 \\
3&8&1 \\
0&4&1
\end{bmatrix} \mathbf{x}= \begin{bmatrix}
2 \\
12 \\
2
\end{bmatrix}
$$

消元时我们先忽略右侧 $\mathbf{b}$ 矩阵，先只看左侧系数矩阵

位于 $(1,1)$ 的被称为 first-pivot ，即第一主元，我们用它来消除其他行的第一列，显而易见方法是对于第二行减去三倍的第一行，于是我们得到

$$
\begin{bmatrix}
1&2&1 \\
0&2&-2 \\
0&4&1
\end{bmatrix}
$$

然后位于 $(2,2)$ 就自然被称为 second-pivot ，如果遇到特殊情况使得此元素为 $0$ ，我们可以通过换行的方式来得到新的第二主元，当然若我们找不到新的主元，那么说明这个矩阵为非可逆的，且这个方程不存在唯一解，这个概念在后边的课程讲到，那我们继续消去第三行的第二列，显而易见就是第三行减去两倍第二行，得到

$$
U=\begin{bmatrix}
1&2&1 \\
0&2&-2 \\
0&0&5
\end{bmatrix}
$$

那么我们就得到我们想要的矩阵了，同时位于 $(3,3)$ 的被称为第三主元，然后进行回代即可

# Elimination Matrices

好了现在来用矩阵的视角构造消元矩阵，在 Lec01 里提到过当我们用一个矩阵左乘一个列向量，可以理解为这个矩阵的各列向量的线性组合，同样地，用一个行向量去左乘一个矩阵，可以理解为这个矩阵的各行向量的线性组合，如下

$$
\begin{bmatrix}
1&2&3
\end{bmatrix} \begin{bmatrix}
1&2&1 \\
3&8&1 \\
0&4&1
\end{bmatrix}=1 \begin{bmatrix}
1&2&1
\end{bmatrix}+2\begin{bmatrix}
3&8&1
\end{bmatrix}+3\begin{bmatrix}
0&4&1
\end{bmatrix}
$$

那么我们就运用到上述消元过程中，首先第一步可以写为：

$$
\begin{bmatrix}
1&0&0 \\
-3&1&0 \\
0&0&1
\end{bmatrix} \begin{bmatrix}
1&2&1 \\
3&8&1 \\
0&4&1
\end{bmatrix}= \begin{bmatrix}
1&2&1 \\
0&2&-2 \\
0&4&1
\end{bmatrix}
$$

这步也可以写成 $E_{21}A$ ，第二步 $E_{32}(E_{21}A)$ 如下：

$$
\begin{bmatrix}
1&0&0 \\
0&1&0 \\
0&-2&1
\end{bmatrix}(E_{21}A)
$$

最后整个过程可以写成：

$$
EA \mathbf{x}=E \mathbf{b}
$$

整个过程可逆，不影响求解，注意 $PA\ne AP$ 

# Inverses

这里引入一点逆矩阵的概念

想象当我们在做完第一步，即将第二行减去三倍第一行后，我们如何撤销这次操作，非常简单地就可以想到用第二行再加回三倍第一行即可，所以：

$$
(E_{21})^{-1}=\left(\begin{bmatrix}
1&0&0 \\
-3&1&0 \\
0&0&1
\end{bmatrix}\right)^{-1}=\begin{bmatrix}
1&0&0 \\
3&1&0 \\
0&0&1
\end{bmatrix}
$$

非常直觉地：

$$
(E_{21})^{-1}E_{21}=I
$$

因为撤销操作后相当于未操作，即乘单位矩阵