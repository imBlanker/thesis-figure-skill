# TikZ Snippets Library

> **何时加载**：步骤 ③ 生成代码时，如果是复杂档（含嵌入 viz / 信息 panel / 公式嵌入），**优先用 snippet 拼装**而不是从零写。
> **核心理念**：snippets 是手工精雕的乐高积木——sub-agent 拼装 N×M 组合，保证基线质量同时不千图一面。

## 为什么有这个目录

Batch 13-17 演化教训：纯文本 Philosophy + 18 项 checklist 让 sub-agent 知道"要嵌入 viz / panel / 公式"，但**写出来的视觉重量、留白、配色协调仍然失败**——因为这些是 visual perception 而不是 textual 任务。

**Snippet Library 解决方案**：给 sub-agent 一套**手工精雕的 TikZ 片段**（每个 30-60 行），sub-agent **复制粘贴 + 替换参数** 即可达到 examples 06-10 水平。

## Snippet 清单

| 文件 | 用途 | 适用图档 |
|---|---|---|
| `attention-heatmap.tex` | N×N attention/correlation 热力图 + colorbar | 复杂档 Transformer / GAT / ViT |
| `bar-chart.tex` | Benchmark 柱状图 + 数字标注 + grid | 复杂档含 metrics |
| `hyperparams-table.tex` | Multi-row parameter table | 复杂档含 model spec |
| `multi-zone-palette.tex` | 6 色 zone tone + accent palette 模板 | 复杂档总配色策略 |
| `pipeline-stages.tex` | N-stage 水平管线 + zone tint | 复杂档主流结构 |
| `formula-box.tex` | 公式 box（标题 + 数学 + 注释） | 任意档位嵌入公式 |

## 使用规则

1. **复制粘贴，替换参数** — 每个 snippet 顶部有 `% USAGE` 注释说明参数位置
2. **不要修改 snippet 核心结构** — 只改 placeholder（如 `{{N}}` / `{{cell_size}}` / `{{label_prefix}}`）
3. **多个 snippet 拼装时** 用 `multi-zone-palette.tex` 的颜色 token 保持统一
4. **不能简化代码** — 比如 attention-heatmap 的 colorbar 必须保留（这是高质量的标志）

## 不要做的事

- ❌ 看 examples 06-10 PNG 然后照抄主题——这些 snippet 已经抽象了"设计语法"
- ❌ 自创"简化版" snippet——简化 = 信息稀疏 = 平庸
- ❌ 用 snippets 但**只用一个**——复杂档应该拼 ≥ 3 个 snippet（如 pipeline + heatmap + bar chart）

## 编译验证

每个 snippet 文件本身是 **standalone 可编译的 .tex**——可以直接：
```bash
xelatex attention-heatmap.tex
```
看 demo 效果。然后把核心代码段（`\begin{tikzpicture}` 到 `\end{tikzpicture}`）复制到你的 `figure.tex`。
