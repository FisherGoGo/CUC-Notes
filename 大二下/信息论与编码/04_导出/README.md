# 信息论与编码 PDF 导出流程

本目录保存 `01_笔记` 中已完成章节的 PDF 导出版。

## 当前导出范围

- `01 信源.md`
- `02 离散信道.md`
- `03 编码.md`
- `04 限失真.md`
- `05 有噪信道编码.md`

`06 纠错编码.md` 仍未完成，暂不导出。

## 使用工具

使用仓库脚本：

```powershell
python tools\md_to_xelatex_pdf.py <输入 Markdown> <输出 PDF>
```

该脚本会先把 Markdown 转成临时 LaTeX 文件，再调用本机 TeX Live 的 `xelatex` 生成 PDF。这样 `$...$` 和 `$$...$$` 中的公式会被真正渲染，而不是作为源码显示。

选择 XeLaTeX 的原因：

- 中文笔记需要 CJK 字体支持。
- 信息论笔记中有大量 LaTeX 公式。
- Pandoc 官方的 PDF 流程也是通过 LaTeX 引擎生成 PDF；本机当前没有 Pandoc，但已经有 TeX Live 和 `xelatex`。

## 批量导出命令

在仓库根目录执行：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$items = @(
  @('大二下\信息论与编码\01_笔记\01 信源.md','大二下\信息论与编码\04_导出\01 信源.pdf'),
  @('大二下\信息论与编码\01_笔记\02 离散信道.md','大二下\信息论与编码\04_导出\02 离散信道.pdf'),
  @('大二下\信息论与编码\01_笔记\03 编码.md','大二下\信息论与编码\04_导出\03 编码.pdf'),
  @('大二下\信息论与编码\01_笔记\04 限失真.md','大二下\信息论与编码\04_导出\04 限失真.pdf'),
  @('大二下\信息论与编码\01_笔记\05 有噪信道编码.md','大二下\信息论与编码\04_导出\05 有噪信道编码.pdf')
)

foreach ($i in $items) {
  python tools\md_to_xelatex_pdf.py $i[0] $i[1]
}
```

## 导出后检查

建议至少检查页数和首末页渲染：

```powershell
python -c "from pathlib import Path; from pypdf import PdfReader; base=Path('大二下/信息论与编码/04_导出'); [print(p.name, len(PdfReader(str(p)).pages), p.stat().st_size) for p in sorted(base.glob('0*.pdf'))]"
```

如果需要抽查页面：

```powershell
pdftoppm -f 1 -l 1 -png -r 110 '大二下\信息论与编码\04_导出\01 信源.pdf' tmp\pdf_check\01_first
```

## 注意事项

- 不要用旧的 `tools/md_to_print_pdf.py` 导出这门课的公式笔记；它会把 LaTeX 公式当源码排进 PDF。
- Obsidian callout 会被简化为普通加粗提示，不保留 Obsidian 的视觉样式。
- 脚本只做轻量 Markdown 转换，不应替代源笔记排版整理；如果 PDF 中出现层级混乱，优先回到 Markdown 源文件调整结构。
