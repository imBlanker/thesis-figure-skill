---
name: thesis-figure-skill
description: |
  生成学术论文配图：LaTeX/TikZ 代码（结构化图表，直接嵌入论文）或 draw.io XML
  （技术路线图、汇报配图）。自动按论文领域风格设计，编译验证后交付。
  Use when the user asks for: 论文配图、画架构图、画流程图、TikZ 图、draw.io 学术图、复刻论文图、tikz/latex diagram。
---

# Academic Diagram Skill (TikZ + draw.io)

把论文中的系统架构/协议流程/技术方案转化为高质量配图。**目标：高信息密度 + 设计感 + 一次过编译**。失败模式：平庸、对齐松散、坐标凭感觉。

## 工具选择

| 维度 | TikZ | draw.io |
|------|------|---------|
| **适合** | 嵌入 LaTeX 论文、数学公式、结构化图表 | 技术路线图、汇报展示、装饰性强（渐变/3D） |
| **精度** | 像素级 | 拖拽，坐标不如 TikZ 精确 |
| **中文** | 需 ctex/fontspec，`rotate=90` 中文会崩溃 | 原生支持 |
| **数学** | 原生 LaTeX 完美 | MathJax 一般 |
| **编译** | xelatex + pdftoppm | drawio CLI → PDF → PNG |
| **可编辑** | 代码即源 | `.drawio` 可在 app.diagrams.net 编辑 |

**默认 TikZ**。draw.io 用于：用户要求 / 参考图为 draw.io 风格 / 需要渐变-3D-空心字 / 内容简单且装饰 > 精确。
**输出格式仅这两种**——HTML/CSS/SVG 不可嵌入论文也无法在 draw.io 编辑。

## 硬约束（违反必失败）

⚠️ **xelatex + `rotate=90` 中文** — 渲染为不可读色块，所有中文标注必须水平
⚠️ **`\texttt` 包裹中文** — 报错，纯英文代码才用 `\texttt` / `code_block`
⚠️ **ctex 不可用** — 编译前 `kpsewhich ctex.sty`，否则切方案 B（fontspec）
⚠️ **`ucharclasses`** — tikz 节点内中英混排频繁 Missing character，禁用
⚠️ **xelatex 对缺失字体静默失败** — 编译后必须 `grep "Missing character" *.log`
⚠️ **单条 `\draw` + `rounded corners` 画长距离 U 型回路** — 路径异常，拆 3 段独立 `\draw`
⚠️ **SVG `clip-path` + `preserveAspectRatio="none"` 模拟梯形** — 高度不可控，禁用
⚠️ **空心描边字 stroke-width ≥ 1.2** — 笔画间隙被填满变模糊，控制 0.6-0.8

## 工作流（⓪→⑦）

```
⓪ 依赖检测 → ① 画图指令 → ② 加载规则 → ③ 生成代码 → ④ 编译验证 → ⑤ 评分 → ⑥ 迭代 → ⑦ 沉淀
```

### ⓪ 依赖检测（首次自动执行一次）
- TeX / pdftoppm 缺失：**只提示用户安装**，不自动装。
  `which xelatex || echo "请装 mactex-no-gui (macOS) / texlive-xetex (Linux)"`
  `which pdftoppm || echo "请装 poppler"`
- Python 工具（小依赖，缺失自动 `pip3 install`）：`pdfplumber`、`pathfinding`、`opencv-python`、`scikit-image`

### ① 画图指令（强制显式输出，不可跳过）
**加载 `references/step1-instructions.md`**——里面有完整的 10 项要素清单、参考图测量规则、ASCII 草图法、嵌入可视化决策表、**密度参考表（按论文复杂度选档位）**、节点形状/连线速查、Pre-flight P1-P7。**禁止"心里想好直接写代码"**——跳过这步返工率 100%。

**关键认识**：步骤① 的输出不是"最大复杂度版本"。先判断论文实际复杂度（极简/中等/复杂/超复杂），再选画图档位。**从复杂版起步然后修瑕疵**比**从合适档位起步**累计 token 高一个数量级——MMAlign 11 轮迭代就是反面教材。

### ② 加载专项规则
确定图表类型后，**按需**加载对应文件（见下方"按需加载索引"）。同时加载 `references/lessons.md` 获取该类型已验证的基线参数和踩坑经验。
基线参数已经是 25 批次 157 张图的结晶——**直接用，不要从零试错**。要偏离基线必须有具体理由。

### ③ 生成代码（**两层决策门，按顺序匹配**）

按以下顺序回答"用哪条路径生成"，**第一个 Yes 就走那条**：

**问 1：这张图是纯结构图吗？**（框 + 线 + 分组，**无**嵌入热力图/曲线/柱状/矩阵，**无** hero 内部多子节点）
→ Yes：**B 路（auto-layout）**
  1. 加载 `references/figure-spec.schema.md` 看 schema
  2. 输出 `figure-spec.json`（节点、边、zones、layout 引擎）
  3. 跑 `python3 references/dot-to-tikz.py figure-spec.json` → 产出 `figure.tex`
  4. 走 ④ 编译 + ④.5 视觉反馈
  - **适用**：架构图 / 流水线 / DAG / 协议时序 / 三栏映射 / 技术路线图 / 多实例汇聚
  - **优势**：0 个 Claude 选的坐标，0 类微斜线/穿框/拥挤 bug

**问 2：富视觉图（嵌入可视化 / 复杂 hero 子结构 / 不规则布局）**
→ **从零路**
  1. 起点：`references/tikz-template.tex`（含 preamble / 字体 / 配色 / **canonical 箭头 styles** / 防御写法）
  2. 加载 `references/visual-patterns.md`（9 个模式：hero 子结构、热力图、折线图、柱状图等）
  3. 复杂连线（≥8 条交叉风险）：可选 `python3 references/tikz-path-router.py spec.json` A* 避障
  4. 走 ④ 编译 + ④.5 视觉反馈

**🎯 箭头/连线必用 canonical pattern**（深度调研 2026-05-18，5 batches 教训）：
`tikz-template.tex` 中 `arrow/.style` / `arrow thick` / `arrow thin` / `residual` / `leader` 5 个预定义 styles 是经过 PGF 官方文档 + PlotNeuralNet 业界实践 + arrows.meta + bending library 综合调研的最佳实践。**禁止**自己手写 `-{Stealth[scale=X]}`——4 轮 Batch 教训证明手调 scale 治标不治本。只调 `line width`（0.6/1.0/1.6pt 三档），tip 通过 `length=⟨dim⟩ ⟨line_width_factor⟩` 语法自动跟随。`\usetikzlibrary{bending}` **必加载**，否则弯折路径上 tip 必然 mis-align。

**编译前两个 checker（pre-flight，所有路径通用）**：
- `python3 references/tikz-validator.py <file.tex>` — 几何/语法 gate：微斜线 / 溢出 / 碰撞 / 方向反转。**ERROR 必修**
- `python3 references/tikz-design-linter.py <file.tex> [--type rich|sequence|simple]` — **advisory** 设计指标。**默认 WARN 不阻挡**——简单论文图可以简单，linter 只汇报指标供 Claude+用户判断是否匹配论文复杂度。仅当 ≥8 节点且尺寸比 < 1.5（严重视觉层次缺失）才 ERROR。

### ④ 编译验证
```bash
fc-list | grep "PingFang SC" || (替换为本机可用字体)
xelatex -interaction=nonstopmode file.tex
grep "Missing character" file.log     # 静默失败检查，关键
pdftoppm -png -r 300 file.pdf out     # 产出 out-1.png
python3 references/pdf-overlap-checker.py file.pdf  # PDF 文字坐标级精度
```
draw.io：`xmllint --noout file.drawio && drawio -x -f pdf -o out.pdf file.drawio && pdftoppm -png -r 300 out.pdf out`。

### ④.5 **视觉反馈强制闭环（架构核心，不可跳过）**

**你的代码生成是"盲写"——写到第 800 行 TikZ 时你不知道渲染出来什么样**。所有标签碰撞、轴标题压字、生命线超界、子模块挤压、数学符号渲染怪——这类问题闸门 1+2 都检测不到，只有看到 PNG 才能发现。

**目标重述**：用户要的不是"一次性生成"，是"最终交到他手上的图必须完美"。**中间迭代多少轮无关紧要，只要图最后是完美的就行**。

**强制流程**：

```
1. Read 渲染出的 out-1.png（图像作为视觉输入进入上下文）
2. 加载 references/visual-review-checklist.md（39 项强制审查清单）
3. 逐项回答 39 个 Y/N：S1-S7（空间）/ T1-T6（文字）/ M1-M10（语义）/ E1-E11（连线精度）/ A1-A5（美学）
   每项必须有一句证据（"我在 PNG 中看到…"），不允许凭印象
4. 任一项 N → 列入 blocker → 输出 patch → Edit → 回 ④ 重编译 → 回 1
5. 全部 39 项 Y → **把图给用户看**（用户终审，AI 视觉有盲区）
6. 用户也通过 → 交付
```

**高漏检盲区**：checklist 里带 ⭐ 标记的 6 项是 R3-100 实测高漏检 — 审查时优先盯，写最详细的证据。

**没有轮数上限**。这是和之前最大的区别——之前 max 2 轮意味着"凑合交付"，现在是**只要还有 1 个 blocker 就不能交付**。3 轮、5 轮、8 轮都可以，只要最终的图是完美的。

**心理对抗**：你会在 2-3 轮后产生强烈的"差不多就过了"冲动——这是认知疲劳，不是图变完美了。**冲动出现 = blocker 还在**。强迫自己回答每项，写出证据。**用户看 1 眼能发现你 2 轮后漏掉的问题——说明单视角自评不可靠，必须靠清单穷举**。

**升级机制**：
- 第 3 轮还有 ≥5 blocker → 局部修补无救，回步骤① 重新设计画图指令
- 同一 blocker 连续 2 轮没修好 → 你修的方向错了，换思路
- 复杂图（≥40 元素）可并行 spawn 4 个子 agent 各盯一个维度，统一收集 blocker
- **自评 + 对抗 agent 全部说 0 blocker 后，仍然把图先给用户看**——人眼能发现 sub-agent + 自评全漏掉的问题（实测案例：用户在 Round 10 一眼指出 CMAM 标题切断边框、箭头刺入框内、junction dot 被 tip 戳——这 3 个我和 2 个对抗 agent 全没发现）。**用户的视觉是最后闸门，不是绕过点**。

**强制约束**：交付前必须能说出 PNG 里**具体的视觉细节**（哪些颜色在哪、哪个 zone 在哪一侧、热力图对角线特征等），证明你视觉输入过。

**单点最小修改原则**：每轮 patch 只改一类问题（如"全部标签重叠"或"全部轴标题没下移"），不要一轮里大改——大改会引入新 bug。一轮一类 blocker。优先用 `yshift/xshift` 微调位置，避免改坐标主框架。

### ⑤ 用户终审 + 交付
1. **把 PNG 给用户看**（不是询问"我做完了吗"，是直接展示结果）
2. 有参考图时同时跑 `python3 references/figure-diff.py <ref.png> <out.png>` 得 SSIM；< 0.85 的 3×3 区域和用户一起重点看
3. 用户指出问题 → 回 ④.5，把问题作为新一轮 blocker；用户没问题 → 交付

**步骤⑤ 不再独立做"自审三遍法"**——所有自审已经在 ④.5 的 30 项穷举里做过。把同一组审查做两次只是认知疲劳的来源，不是质量提升。

### ⑥ 迭代到完美（无上限）

**没有轮数表，没有"3 轮够了"**。规则极简：
- **还有 blocker → 继续修**（不管这是第 2 轮还是第 8 轮）
- **同一 blocker 连续 2 轮没修好 → 修复方向错了，换思路**
- **第 3 轮还有 ≥5 blocker → 局部修补救不了，回步骤① 重新设计画图指令**

用户的目标重述："中间迭代多少轮无关紧要，只要图最后是完美的就行"。**绝不允许"凑合交付"**——"改了 3 轮差不多了吧"是认知疲劳的产物，不是质量信号。

### ⑦ 经验沉淀
- 2 次以上才解决的问题 → 追加到 `references/lessons.md` 的 Part 2
- 发现更优参数 → 更新 `lessons.md` 的 Part 1 基线表（**只升不降**）
- 已被全局规则/Python checker 覆盖的内容**不要重复写入**

## 设计原则（对抗模型惯性）

容易陷入的刻板印象（必须警惕）：
- "心里有数，直接写代码" → **禁止跳过步骤①**，"想了"≠"想清楚了"
- "我能估比例" → **不行**。复刻必须像素级测量，凭感觉偏差 15-20%
- "框的大小差不多就行" → 不行。参考图通常扁宽 2:1~3:1，**默认不要正方形**
- "改了 3 轮差不多了吧" → 标准不会因为努力降低。还有 blocker 就继续修
- "这个小重叠用户看不出来" → 看得出来。300dpi 下清清楚楚
- "坐标差 0.2cm 没关系" → 0.2cm 在渲染图上是 24 像素
- "信息密度不够就硬塞东西" → **反例**。简单论文图就该简单——贝叶斯网络/几何/对比图天然元素少，强加 hero 和嵌入可视化是污染。`tikz-design-linter` 现在是 advisory，按论文实际复杂度决定密度

**信息密度匹配论文复杂度**：复杂模型架构图允许 30+ 元素 + hero 子结构 + 嵌入可视化；简单流程图 5-10 元素 + 清晰布局就够了。**不要把所有图都画到最大复杂度**。详见 `step1-instructions.md` 的"信息密度判断"。

## 常见图表类型

| 类型 | 布局 | 场景 |
|------|------|------|
| 系统架构图 | 自下而上分层 | 端→云→链、硬件→中间件→应用 |
| 协议/流程图 | 左→右或上→下 | 时序步骤、信号处理 |
| 数据流水线 | 左→右水平串联 | 输入→处理→输出，每步不同形状 |
| 电路/约束原理 | 左→右 | ZK 电路、信号管线、编译器 |
| 数据映射/转换 | 左-中-右三栏 | 格式转换、API 适配 |
| 时序交互 | 多列生命线+水平消息 | 多方协议 |
| 对比方案 | 左右并列 | 方案 A vs B，中间 ≥3cm |
| 几何/数学 | 坐标系+几何元素 | 算法原理、向量关系 |
| 技术路线图 | 三层分区（draw.io 模式 A） | 科研展示 |
| 同心嵌套 | 多层嵌套椭圆（draw.io 模式 B） | 宏观→微观 |
| 流水线链条 | 圆形节点+加号（draw.io 模式 C） | 技术叠加 |
| 侧栏+中心 | 左右侧栏+中心嵌套（draw.io 模式 D） | 技术突破+路径 |
| 总论-展开-归纳 | 顶部→三栏→底部（draw.io 模式 E） | 创新+应用+方案 |
| 分层技术路线图 | 背景→问题→框架→路线→结论（draw.io 模式 F） | 毕业论文路线图 |
| 多实例汇聚 | 横排三列→汇聚 | 联邦学习、分布式 |
| 数据可视化混合 | 框图内嵌波形/柱状/热力图 | 信号处理、深度学习注意力 |

## 按需加载索引

确定图表类型/工作流阶段后**才**加载对应文件：

| 触发条件 | 文件 |
|---------|------|
| 进入步骤① | `references/step1-instructions.md` |
| 步骤②（任何 TikZ 图，**必加载**） | `references/lessons.md` + `references/visual-patterns.md` |
| 步骤③ 决策门 | `references/figure-spec.schema.md`（B 路 spec） |
| 步骤③ 走 B 路 → 跑 `dot-to-tikz.py` | （脚本，不需 Read） |
| 步骤③ 走模板/从零 → 用 TikZ | `references/tikz-global-rules.md` + `references/tikz-template.tex` |
| 步骤④.5 视觉反馈每一轮 | `references/visual-review-checklist.md`（30 项强制清单） |
| 配色需求 | `references/tikz-colors.md` |
| 分层架构图 | `references/layered-architecture.md` |
| 时序交互图 | `references/sequence-diagram.md` |
| 数据流水线图 | `references/data-pipeline.md` |
| 三栏映射图 | `references/three-column-mapping.md` |
| 几何/数学示意图 | `references/geometry-math.md` |
| 含数据可视化的图 | `references/data-visualization.md` |
| draw.io 科研展示图 | `references/drawio-modes.md` |
| 步骤⑤ 有参考图 | `references/figure-diff.py`（脚本） |

**未列出的文件不要加载**——节省 token。

## Python 助手脚本（执行即可，不要 Read）

| 脚本 | 用途 | 何时跑 |
|------|------|--------|
| `dot-to-tikz.py <spec.json>` | B 路：spec → graphviz 自动布局 → TikZ | 结构化图 step ③ |
| `tikz-validator.py <file.tex>` | 微斜线/溢出/碰撞/方向反转（几何/语法 gate） | 编译前必跑 |
| `tikz-design-linter.py <file.tex> [--type ...]` | 元素数/尺寸比/线型/hero/嵌入viz（设计野心 gate） | 编译前必跑 |
| `pdf-overlap-checker.py <file.pdf>` | PDF 内部坐标级重叠检测 | 编译后必跑 |
| `figure-diff.py <ref.png> <out.png>` | SSIM + 3×3 区域差异 | 复刻任务必跑 |
| `tikz-path-router.py <spec.json>` | A* 自动避障路径 | 连线 ≥8 条可选 |

这些脚本**作为黑盒调用**——不要把源码读进上下文，跑 `--help` 看参数即可。

## 领域自适应

收到输入后**先识别论文领域**（计算机/密码学/生物/物理/化学/AI/网络/系统/区块链等），以该领域专家身份选术语和布局风格。
