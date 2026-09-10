第一讲的内容比较简单，算是一个入门

老师上来先举了一个线性方程组

$$\begin{aligned}2x-y &= 0 \\ -x+2y &= 3\end{aligned}$$
然后引入两个看这个方程组的方向

### Row Picture

顾名思义以 **行** 来看，拆分成两个独立的方程，那么求解实际上就是在求这两个直线的交点坐标
### Column Picture

这个视角更有意思一点，以一列一列地看，那么方程就变成如何配比两个向量，使其加在一起变成右侧向量，即

$$x\begin{bmatrix}2\\-1\end{bmatrix}+y \begin{bmatrix}-1\\ 2\end{bmatrix}= \begin{bmatrix}0\\ 3\end{bmatrix}  $$
# Matrix Picture

这个应该是线性代数的视角了，矩阵的视角，上述方程式可以写为

$$\begin{bmatrix}2&-1\\-1&2\end{bmatrix} \begin{bmatrix}x\\y\end{bmatrix}=\begin{bmatrix}0\\3\end{bmatrix}$$

左侧矩阵 $A=\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$ 称为系数矩阵， $\mathbf{x}=\begin{bmatrix}x\\y\end{bmatrix}$ 称为未知数向量，方程右边的数组成了向量 $\mathbf{b}=\begin{bmatrix}0\\ 3\end{bmatrix}$ 

三维下情况与二维十分类似，知识系数矩阵变大了

# Matrix Multiplication

现在来看我们怎么做矩阵乘以一个向量（这里建议先忘记在大学课堂上学习的那种矩阵乘法），比如对于如下：

$$\begin{bmatrix}2&5\\1&3\end{bmatrix}\begin{bmatrix}1\\2\end{bmatrix}= \mathbf{?}$$

我们有两种方法，一种方法是将 $\mathbf{x}$ 里的各分量看成矩阵各列向量做线性组合时的系数

$$\begin{bmatrix}2&5\\1&3\end{bmatrix}\begin{bmatrix}1\\2\end{bmatrix}= 1\begin{bmatrix}2\\1\end{bmatrix}+2\begin{bmatrix}5\\3\end{bmatrix}=\begin{bmatrix}12\\7\end{bmatrix}$$

这种方法说明 $A \mathbf{x}$ 是 $A$ 各列的一个线性组合

还有一种方法是让 $A$ 的每一行分别和向量 $\mathbf{x}$ 做点积来计算

$$\begin{bmatrix}2&5\\1&3\end{bmatrix}\begin{bmatrix}1\\2\end{bmatrix}= \begin{bmatrix}2\cdot 1+5\cdot 2\\1\cdot 1+3\cdot 2\end{bmatrix}=\begin{bmatrix}12\\7\end{bmatrix}$$
# Linear Independence

这个词的意思是**线性无关**，我们想一个问题，在如下方程，是不是对于所有的 $\mathbf{b}$ 都能求解

$$A \mathbf{x}= \mathbf{b}$$

这个问题等价于：$A$ 的线性组合是否能够填充满所有的 $xy-plane$  

当上述问题答案为 **不** 时，我们成矩阵 $A$ 为奇异矩阵，此时列向量为线性相关，这些列向量的所有线性组合，在二维情况下只会落在某一点或者某一直线上。即不能生成整个空间