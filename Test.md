# I
## P 1

- 主流框架有 **PyTorch**、**TensorFlow**、**JAX** 和 **Keras** 等
- 能解决计算机视觉、自然语言处理、科学发现、推荐系统等
- 因为如果没有框架，开发者需要从底层的数学公式开始，手动编写成千上万行代码来实现一个简单的神经网络，框架的出现解决了以下核心痛点：
	- **自动求导（Autograd）：** 深度学习的核心是反向传播算法。框架能自动计算复杂的数学梯度，无需人工推导繁琐的导数公式。
	- **硬件加速：** 框架能自动将计算任务分配给 GPU 或 TPU，计算速度比普通 CPU 快几十甚至上百倍。
	- **组件化与标准化：** 提供现成的“积木”（如卷积层、池化层、损失函数），让开发者只需关注架构设计，而非底层实现。
	- **生态与模型库：** 拥有海量的预训练模型（如 GPT、ResNet），开发者可以直接“站在巨人的肩膀上”进行二次开发。
- 特点：
	- PyTorch：动态计算图、Pythonic（像写原生 Python 一样自然）、易于调试，
	- TensorFlow：静态计算图、生态极其完整（TFX, TFLite）、工业级部署非常成熟
	- JAX：极致的高性能计算，支持函数式编程，专门针对 TPU 优化
	- Keras：极简 API，高度封装，可以在 TensorFlow 或 PyTorch 之上运行

## P 2

- 在 VSCode 中的项目文件夹中的终端执行如下命令：

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

# 安装PyTorch
pip install torch torchvision torchaudio

# 选择解释器 -> .venv

# 验证安装
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"

# 若输出版本号则安装成功,如
2.11.0+cpu
False
```

## P 3

- 验证程序

```python
import torch

print("Hello, PyTorch!")
```


# II

## P 1 Pytorch 和 Numpy 的区别

- 核心关联：一脉相承
	- **数据结构相似：** NumPy 的核心是 `ndarray`，而 PyTorch 的核心是 `Tensor`（张量）。它们在处理多维数组的语法上几乎一模一样
	- **无缝转换：** 它们之间可以轻松地相互转换。你可以用 `torch.from_numpy()` 将 NumPy 数组转为张量，或者用 `.numpy()` 转回来
	- **共享内存：** 在 CPU 上进行转换时，PyTorch 张量和 NumPy 数组通常会**共享底层的内存地址**。这意味着修改其中一个，另一个也会随之改变，这种设计极大地节省了内存开销
- 核心区别：
	- 硬件加速 
		- **NumPy：** 主要运行在 **CPU** 上，不支持并行计算加速（如 CUDA）。
		- **PyTorch：** 原生支持 **GPU 和 TPU** 加速。对于大规模的矩阵运算，GPU 的处理速度通常是 CPU 的数十倍甚至上百倍。
	- 自动求导
		- **NumPy：** 只是一个数学库。如果你要计算一个函数的导数（梯度），你需要自己推导数学公式并手动编写代码
		- **PyTorch：** 拥有**自动求导机制**。它会记录你对张量的所有操作，只要调用 `.backward()`，它就能自动计算出复杂的梯度。这对于神经网络的训练是不可或缺的
	- 计算图：
		- **NumPy：** 立即执行计算，计算完后不保留操作之间的逻辑关系
		- **PyTorch：** 会动态构建一张“计算图”。这张图记录了数据是如何从输入流动到输出的，从而方便进行反向传播和模型优化

|**特性**|**NumPy**|**PyTorch**|
|---|---|---|
|**核心对象**| `np.ndarray` | `torch.Tensor` |
|**计算设备**|仅 CPU|CPU, GPU, TPU|
|**自动求导**|❌ 不支持|✅ 支持 (Autograd)|
|**适用领域**|通用科学计算、数据分析|深度学习、神经网络研究|
|**执行模式**|立即执行|动态图 (Eager Mode)|

- PyTorch 就是一个“拥有 GPU 加速和自动求导功能的 NumPy”

## P 2 Pytorch 的优点

- 动态计算图：
	- **直观理解：** 在 PyTorch 中，计算图是在运行时构建的。这意味着你可以像写普通的 Python 代码一样，使用 `if`、`for` 循环来改变神经网络的结构。
	- **优势：** 极易调试（Debug）。你可以直接在代码中插入 `print()` 或使用标准调试器查看任何中间变量的值，而不需要像静态图框架那样先定义好复杂的逻辑再通过“会话”运行。
- 卓越的 Python 体验：
	- **丝滑融合：** 它不强迫你学习一套复杂的 DSL（领域特定语言）。它与 Python 的生态系统（如 NumPy、SciPy、Matplotlib）结合得天衣无缝。
	- **学习曲线平缓：** 对于熟悉 Python 的开发者来说，写 PyTorch 代码就像在写带加速功能的数学表达式，没有任何割裂感。
- 强大的 TorchScript 与部署进化：
	- **模型转换：** 它可以将动态的 Python 代码转换为一种中间表示（IR），脱离 Python 解释器运行。
	- **全平台覆盖：** 支持通过 C++ 部署到服务器，或者通过 PyTorch Mobile 部署到手机端。
- 统治级的学术生态与模型库：
	- **论文复现：** 绝大多数最新的 AI 论文（如 Transformer 变体、扩散模型 Stable Diffusion）都会优先发布 PyTorch 源码。
	- **Hugging Face 集成：** 全球最大的 AI 模型社区 Hugging Face 深度适配 PyTorch。如果你想调用最新的大语言模型（LLM），PyTorch 通常是第一选择。
	- **TorchVision/TorchAudio/TorchText：** 针对视觉、语音、文本提供了极其丰富的工具包，极大地减少了“造轮子”的时间

## P 3 Tensor 是什么

- 是一个“超级数字容器”，在 Pytorch 中，无论是一张图片、还是一段话，都可以被表示为一个 Tensor，如 0 维 Tensor 是一个常量，1 维是一个向量，2 维是一个矩阵，3 维通常表示时间序列数据或彩色图像等
- 虽然我们看到的 Tensor 是“方方正正”的矩阵，但在电脑内存里，它们其实是**一长串连续排布的数字**，其由两部分组成：
	- **Storage (存储)：** 真正存放数字的地方，是一块连续的内存区域
	- **View (视图)：** 记录了如何解读这块内存（比如告诉程序：每数 3 个数就换一行）
- **核心优势：** 这种设计让 PyTorch 的 **`view()` 或 `reshape()`** 等操作极快。当你改变一个 Tensor 的形状时，PyTorch 并没有搬运数字，只是换了一种“眼光”去看待那块内存
- 还有其他附加属性：
	- **`dtype` (数据类型)：** 比如 `float32`。在 AI 里，精度越高（如 float64）计算越准但越慢，精度低一点（如 float16）可以大幅提升训练速度。
	- **`device` (设备)：** 标记这个 Tensor 住在 **CPU** 还是 **CUDA (GPU)** 上。不同设备上的 Tensor 不能直接相加，必须先把它们搬到同一个“房间”里。
	- **`requires_grad` (是否求导)：** 这是一个开关。如果设为 `True`，PyTorch 就会开启监控录像，记录这个 Tensor 参与的所有运算，以便稍后自动计算梯度。
- **Tensor 不仅仅是数据的载体，它还是一个“自带导航和计算逻辑”的智能数据结构。** 它是深度学习引擎中的齿轮，所有的数学变换和智能进化，都是通过 Tensor 之间的相互碰撞和反馈实现的

## P 4 实践

```python
import torch
  
# 1) Scalar (0D)
scalar = torch.tensor(3.14)
  
# 2) Vector (1D)
vector = torch.tensor([1, 2, 3, 4])
  
# 3) Matrix (2D)
matrix = torch.tensor([[1, 2, 3],

                       [4, 5, 6]])
  
# 4) 3D Tensor
tensor3d = torch.tensor([
    [[1, 2], [3, 4], [5, 6]],
    [[7, 8], [9, 10], [11, 12]]
])
  
def show_info(name, t):
    print(f"\n===== {name} =====")
    print(t)
    print("ndim:", t.ndim)
    print("shape:", t.shape)
    print("dtype:", t.dtype)
    print("device:", t.device)
    print("numel:", t.numel())
  
show_info("Scalar", scalar)
show_info("Vector", vector)
show_info("Matrix", matrix)
show_info("Tensor3D", tensor3d)
```

# III

## P 1 梯度

- **梯度（Gradient）** 的本质就是“函数增长最快的方向”
- 如果把 Tensor 比作砖块，那么梯度就是“指路明灯”，它告诉 AI 应该如何调整这些砖块来达到目标
- 想象你被困在一座大雾弥漫的山上，你的目标是找到**山谷的最低点**（在 AI 中，这代表误差最小的状态）：
	- **你在哪：** 代表模型当前的参数（Weights）。
	- **雾有多大：** 代表你看不见全局，只能通过脚下的坡度来判断方向。
	- **梯度是什么：** 梯度就是你脚下**最陡峭的上坡方向**。
	- **你怎么走：** 既然梯度是指向“最陡的上坡”，那么为了下山，你就要朝着**梯度的反方向**走一步。这一步的长度，就是我们常说的“学习率”。
- 数学本质：多维的导数
	- 在 $y = f(x)$ 中，导数 $f'(x)$ 告诉你在某个点上，当 $x$ 变化一点点时，$y$ 会变化多少
	- 梯度就是导数在多维空间的升级版
	- 对于一个复杂的神经网络模型，它的损失函数 $L$ 依赖于成千上万个参数 $(w_1, w_2, \dots, w_n)$
	- 这个向量（即梯度）包含了每一个参数对最终结果的影响力大小和方向
$$ \nabla L = \left( \frac{\partial L}{\partial w_1}, \frac{\partial L}{\partial w_2}, \dots, \frac{\partial L}{\partial w_n} \right) $$
- 神经网络的学习过程其实就是一个“不断碰壁并修正”的过程：
	- **前向传播：** AI 猜了一个答案，结果发现误差（Loss）很大。
	- **反向传播：** PyTorch 自动计算出 **Loss 对每个参数的梯度**。
	     - 如果某个权重的梯度是**正数**，说明增大它会让误差更大，所以我们要减小它。
	     - 如果梯度是**负数**，说明增大它会让误差减小，所以我们要增大它。
	- **更新参数：** 根据梯度微调所有参数，模型就变得“聪明”了一点点。

## P 2 Pytorch 中的梯度