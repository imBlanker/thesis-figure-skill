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

## 视觉法则（贯穿全 skill，所有规则之上）

**46 项 checklist 是机械验证，但人画图不是机械的。在所有具体规则之前，先内化 3 条 meta 视觉法则——它们是规则的"为什么"，而不是另外的规则。**

### 法则 1：**0.1 秒直觉法则**

人看图先用直觉，再用理性。视觉流向 ≠ 逻辑流向 = 必错。
- 一条箭头从 `.east` 出发指向上方目标 → 读者直觉是"先往右走"，与"向上流"语义矛盾 → 即使最终连到正确目标，**已错**
- spine 黑 + stub 紫 在折角处 → 直觉看到"两条断线"，不是"一条 routing"
- 0.02cm 间距的 label 与 line → 直觉看到"label 在线上"
- **每写一条 \draw / 放一个 node，问自己**：第一眼看到这个，读者的直觉对吗？

### 法则 2：**读者眼睛轨迹**（沿主线走一遍）

每张图都有一条"读者视线的主线"。**审查时把自己当读者，沿主线从起点走到终点**——任何地方"卡住"（绕弯/混乱/不知道指哪）= blocker。
- 卡点案例：① fig97 Pedersen 框里出来个箭头 ② fig118 head spine 上 tip 撞坐标 ③ fig120 孤立彩点漂浮
- 反过来：如果整条主线**一气呵成读完**，即使有些小细节不完美，图整体可用
- **46 项 Y/N 是"细节体检"，眼睛走一遍是"整体心电图"——缺一不可**

### 法则 3：**删除测试 + 干净 > 塞满**

不必要的装饰 = 噪音。审查时反问：
- 删掉这个元素，读者还能理解吗？能 → 元素冗余，删
- 这条 leader 真的需要吗？还是位置对齐已经隐式关联？
- 迭代时：修一个 bug **不能引入另一个审美问题**（对称性丢/平行线断/间距不均）

---

**这 3 条法则在 ④.5 强制流程 Step 0 显式应用**。

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
- Python 工具（小依赖，缺失自动 `pip3 install`）：`pdfplumber`、`pymupdf`、`pathfinding`、`opencv-python`、`scikit-image`
  （`pymupdf` 不装 → `line-through-node` + `node-overlap` 两类几何检测会 ERROR 退出，不静默跳过——别忽略）

### ① 画图指令（强制显式输出，不可跳过）

**加载 `references/step1-instructions.md`**——里面有完整的 10 项要素清单、参考图测量规则、ASCII 草图法、嵌入可视化决策表、**密度参考表（按论文复杂度选档位）**、节点形状/连线速查、Pre-flight P1-P7。**禁止"心里想好直接写代码"**——跳过这步返工率 100%。

**关键认识**：步骤① 的输出不是"最大复杂度版本"。先判断论文实际复杂度（极简/中等/复杂/超复杂），再选画图档位。**从复杂版起步然后修瑕疵**比**从合适档位起步**累计 token 高一个数量级——MMAlign 11 轮迭代就是反面教材。

**🔴 强制物质化要求**（fig126 Tacotron2 教训：sub-agent 加载 step1 但跳过实际输出，产生大块空白）：

步骤 ① 必须**以文字形式实际输出**（不是"想了就过"），且**第一段写进 figure.tex 头部注释块**作为证据。**形式两选一**，按图复杂度选：

**🔵 form A/B 选择前的先决条件**（消除"节点数悖论"——判档依赖草图、草图依赖判档的循环）：

```
1. 先粗估档位（无需精确节点数，先看明显信号）：
   ① 含 hero 子结构 / 嵌入热力图 / 多 panel / ≥3 列 → 复杂档 → form B
   ② 含 fan-out / 时序生命线 / 12+ 模块 → 中等档 → form A 或 form B
   ③ 纯几何/单链/对比图（明显 < 15 节点）→ 极简档 → form A
2. 按粗判选 form 写注释块（form A 画 ASCII OR form B 写 narrative）
3. 注释块写完后**数节点 → ①.5 精确确认档位**
4. 若精确档位 ≠ 粗判档位 → 调整 form（极简误判为复杂 = 简化为 A；
   复杂误判为极简 = ASCII 画不下 → 改写 B）
```

**铁律**：先粗判 → 写注释块 → ①.5 精确确认 → 必要时调整。**禁止凭直觉直接选 form 又凭直觉判档**。

### 形式 A — ASCII 草图（适合：极简档 + 中等档无嵌入 viz / 无 hero 子结构）

```latex
% =====================================================================
% Step ① 设计文档（强制 — 不可跳过）
% =====================================================================
% 1. 领域：[XXX]            2. 格式：TikZ         8. 密度档：[极简/中等]
% 3. 布局策略：整图 W×H = _×_ cm, 信息流 [左→右], [M 行 N 列]
% 4. 模块列表：[N 个]，核心 = [X]
% 5. 连线逻辑：主流（实线）/ 反馈（虚线）
% 6. 空间规划：rail x = [...], 标签放线 [上/下/左/右]
% 7. 视觉强调：核心 vs 辅助
% 9. ASCII 草图：
%    +-----------+      +-----------+      +-----------+
%    | Encoder   |----->| Attention |----->| Decoder   |
%    +-----------+      +-----------+      +-----------+
% 10. 预防 issues：[2-3 个坑]
% =====================================================================
```

### 形式 B — Narrative 设计文字（适合：复杂档 / 含 hero 子结构 / 嵌入 viz / 多 panel）

复杂图 ASCII 表达不全（嵌入热力图/曲线/矩阵 ASCII 画不出来），用**叙述性空间描述**——设计师真实的思考方式：

```latex
% =====================================================================
% Step ① 设计文档（强制 — Narrative 形式，复杂档）
% =====================================================================
% 1. 领域：Audio (TTS)      2. 格式：TikZ        8. 密度档：复杂
% 3. 布局策略：整图 28cm × 18cm，三列水平布局 + 底部独立行
%
% 4. 模块布局（narrative — 每列一段，含子结构 + 视觉定位）：
%    
%    【左列 Encoder（x=0-6cm, y=0 至 -8cm）】
%       Characters → Char Embed → 3×1D Conv → Highway Net (4 layers) → BiLSTM
%       6 个小框竖排，每个 1.5×0.7cm，间距 1cm
%
%    【中列 Attention zone（x=8-14cm, y=0 至 -10cm）】
%       hero box 6×8cm，紫色 zone 包围
%       内部：Query/Memory/Location Features 三小框横排（顶部）
%             ↓
%             Attention Weights (softmax) 一框（中部）
%             ↓
%             嵌入 6×6 attention heatmap (s_i vs t_j) ← 占 hero 高度 40%
%             ↓
%             Context Vector 一框（底部）
%
%    【右列 Decoder（x=16-22cm, y=0 至 -10cm）】
%       Pre-net → LSTM Decoder → Linear Projection → Stop Token / Mel Frame
%       → Post-Net → Mel Spectrogram
%       Mel Spec 在 y=-10 处结束
%       右侧 Previous Mel Frame 在 (x=24, y=0)，dashed feedback 弧形回 LSTM Decoder
%
%    【底部独立行 WaveNet Vocoder（注意）】
%       y=-12cm，**只跨 x=8 至 x=22（attn+decoder 列下方）**，**不延伸到 x=0**
%       因为 Encoder 列 y=-8 就结束，y=-8 至 -12 留 4cm 空白会很丑 → 
%       方案：(a) WaveNet 不跨 Encoder 列下方；OR
%             (b) WaveNet 跨整宽但加补充元素填左下 4×4cm 空白（如 character demo）
%       → 选 (a)
%
% 5. 连线逻辑：encoder→attn (实线粗) / attn→decoder (实线粗) / decoder→wavenet (实线粗)
%             previous mel→pre-net (dashed 反馈)
%
% 6. 空间规划：autoregressive feedback rail 在 x=23-24（decoder 右侧）
%
% 7. 视觉强调：Attention hero 最大（紫色+heatmap），WaveNet 其次（青色宽框）
%
% 10. 预防 issues：
%    - WaveNet 不跨整宽 → 防左下空白
%    - heatmap 嵌入 hero 高度 40% 不要太大
%    - feedback 虚线 rail 远离 decoder 主流 ≥ 1cm
% =====================================================================
```

**Narrative 要求**：每列/每 zone 写一段，明确：(a) x/y 范围 (b) 内部子结构 (c) 与相邻列的关系 (d) 留白处理。**特别要预想"哪里可能出现大块空白"并写出应对**（fig126 的根本教训）。

**自验证**：sub-agent 在 ④.5 Step 0 时**必读 figure.tex 头部** 确认这段注释存在（form A 或 form B）；若不存在 → 直接 blocker，回 ①重做。

### ①.5 图档判断（创造性免责 + N/A 豁免）

**先判图档**，再走④.5 自评 — 避免极简几何图被规则"过度设计"（Batch 12 fig114 Newton 3 轮答 138 项大半 N/A 的反面教材）。

**判档方法**：步骤①注释块写完后，**数注释里出现的节点总数** + 看明显结构信号（hero / fan-out / 嵌入 viz / 时序），对照下表：

| 档位 | 判断（注释块数节点 + 结构信号）| ④.5 自评策略 |
|---|---|---|
| **极简档** | ≤15 节点 AND 无 hero AND 无 fan-out AND 无时序生命线 AND 无嵌入 viz | **明确走 18 项**：S1-S7（不跑 S8/S9/S10）+ T1-T6（不跑 T7）+ M1-M7（不跑 M8/M9/M10）+ E3/E9/E13（13 ⭐ 中与极简图有关的 E 类）+ A1-A4（不跑 A5）；**其余 28 项明确标 "N/A, 一句过"** |
| **中等档** | 15-30 节点 OR 有 hero OR 有 fan-out | 走全 46 项；E3/M6/S10 等若 0 候选写 "0 处, N/A" 一句即过 |
| **复杂档** | ≥30 节点 OR 嵌入 viz OR 多 hero | 走全 46 项，每项详细证据 |

**典型极简档**：几何示意（Newton/几何/向量）/纯曲线公式图（Bayesian/概率密度）/单链信号流（ConvNeXt block 主链）

**Step 0 与极简档的关系**（避免"是否豁免"歧义）：
- Step 0 全 5 段（A/B/C/D/E）**对所有档位强制**，不论极简/中等/复杂
- 极简档的 E 段只需验证 form A（ASCII 注释块）存在 + 可辨认；form B 不适用极简档
- 极简档豁免的是 46 项 checklist 中的 28 项，**不是 Step 0**

**豁免铁律**：N/A 是"已知该项对本图不适用"，不是"懒得查"。写一句话说明（如"无 fan-out 结构, E3 N/A"），把节省的注意力集中在真正适用的项。

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
`tikz-template.tex` 中 6 个预定义 styles 是经过 PGF 官方文档 + PlotNeuralNet 业界实践 + arrows.meta + bending library 综合调研的最佳实践：

| style | 用途 | 何时用（铁律） | 关键差异 |
|---|---|---|---|
| `arrow` / `arrow thick` / `arrow thin` | 长连线 | **⚠️ 仅 ≥ 1.5cm — 短于此必须改用 `arrow short`** | tip 6.5pt, `shorten >=2pt, shorten <=1pt` |
| **`arrow short`** | 短箭头（相邻 box 间） | **⚠️ < 1.5cm 必用此 style** | tip 3pt, `shorten >=1pt, shorten <=0pt` — 防止 tip 吃光 stem |
| `residual` | dashed skip / 反馈 | residual / feedback | 紫色虚线 + rounded corners |
| `leader` | annotation 引线 | 引线 / 标注 leader | 灰色 dotted |
| **`fan_stub`** / `fan_stub thin` / `fan_stub thick` | fan-out 树状分叉的 stub（spine → target） | **fan-out / fan-in 的 stub 段必用此** | **`shorten <=0pt`**——起点紧贴 spine 无 gap |

**禁止**自己手写 `-{Stealth[scale=X]}`——4 轮 Batch 教训证明手调 scale 治标不治本。只调 `line width`（0.6/1.0/1.6pt 三档），tip 通过 `length=⟨dim⟩ ⟨line_width_factor⟩` 语法自动跟随。`\usetikzlibrary{bending}` **必加载**，否则弯折路径上 tip 必然 mis-align。

**短箭头铁律**（Batch 10 用户反馈：fig91-95 大量"只有头的箭头"）：**任何 < 1.5cm 的连接箭头必须用 `arrow short`**，不要默认 `arrow` 或 `arrow thick`。原因：默认 `arrow` 的 tip = 5pt + 1.5×line_width = 6.5pt，加上 `shorten` 3pt，一条 15pt（0.5cm）的短箭头剩下 stem 只 5.5pt——视觉上"只剩个头"。`arrow short` 用 3pt tip + 1pt shorten，stem 保留充足。

**fan-out 树状分叉**（1 source → N targets）：spine 用普通 `\draw[line width=1.0pt]`（无 shorten），**stub 用 `fan_stub` 不用 `arrow`**——后者的 `shorten <=1pt` 会在 stub 起点和 spine 间留 1pt 视觉 gap（fig86 Batch 9 教训：MPD/MSD spine 全断裂）。

**`rounded corners` 使用规则**（Batch 10 用户反馈：fig92 出现"莫名其妙曲线"，[PGF 官方手册原话](https://tikz.dev/tikz-paths)："very short line segments → rounding causes inadvertent effects"）：

```
✅ 只在显式 ≥2 段折线用 rounded corners：
   \draw[arrow, rounded corners=5pt] (A) -- (corner) -- (B);
   \draw[arrow, rounded corners=5pt] (A) |- (B);             % | 和 - 是隐式 corner

❌ 直线禁加 rounded corners：
   \draw[arrow, rounded corners=5pt] (A) -- (B);   ❌ TikZ 在端点附近产生鬼影弧
```

**`|-` / `-|` L-bend 安全条款**（Batch 10 用户反馈：fig97 Pedersen Commitment hero 出现"箭头穿过框体"——`(msg.south) |- (ped_hero.west)` 中 msg.x 落在 hero 的 x 范围内，TikZ 把横线**画在 hero 内部**）：

```
✅ (A.south) |- (B.west) 仅当 A 不在 B 的水平投影内（A.x < B.x0 OR A.x > B.x1）：
   A
   |
   +----→ B          ← A 在 B 左上方，横线在 B 外部 OK

❌ (A.south) |- (B.west) 当 A.x ∈ [B.x0, B.x1]：
   A
   |
   |  ↓
   +→ B         ← 横线穿过 B 的内部 = pierce bug

✅ 修复 1：用 named coordinate 显式 waypoint 绕开 B：
   \coordinate (wp) at (B.x0 - 0.5cm, B.center.y);
   \draw[arrow] (A.south) |- (wp) -- (B.west);

✅ 修复 2：换 anchor 让箭头从 B 的上方接入：
   \draw[arrow] (A.south) -- (B.north);   % 直线，A 在 B 上方
```

PGF 不做 obstacle-aware routing（[官方手册确认](https://tikz.dev/base-nodes)），所以必须自己保证 `|-` / `-|` 的中段不撞 obstacle。`pdf-overlap-checker.py --json` 的 line-through-node 检测会抓到这种 bug。

**编译前两个 checker（pre-flight，所有路径通用）**：
- `python3 references/tikz-validator.py <file.tex>` — 几何/语法 gate：微斜线 / 溢出 / 碰撞 / 方向反转。**ERROR 必修**
- `python3 references/tikz-design-linter.py <file.tex> [--type rich|sequence|simple]` — **advisory** 设计指标。**默认 WARN 不阻挡**——简单论文图可以简单，linter 只汇报指标供 Claude+用户判断是否匹配论文复杂度。仅当 ≥8 节点且尺寸比 < 1.5（严重视觉层次缺失）才 ERROR。

### ④ 编译验证
```bash
# 字体探测：若 PingFang SC 不存在，自己改 .tex 里的 \setCJKmainfont 为本机可用字体
fc-list | grep -qi "PingFang SC" || echo "WARN: PingFang SC 缺失，请改 \setCJKmainfont"
xelatex -interaction=nonstopmode file.tex
grep "Missing character" file.log     # 静默失败检查，关键
pdftoppm -png -r 300 file.pdf out     # 产出 out-1.png
# overlap.json 落在 .tex 同目录（sub-agent ④.5 步用 Read 读这个绝对路径）
python3 references/pdf-overlap-checker.py file.pdf --json > "$(dirname file.pdf)/overlap.json"
# 跑完检查 overlap.json — 7 类检测：
#   基础 5 类（直接 fix）: text-overlap / text-overflow / off-center / text-line / line-crossing
#   candidate 2 类（需 triage）: line-through-node / node-overlap
# ERROR 类大概率是真 bug 直接修；candidate 类是几何线索（heatmap 矩阵 / fan-in 收敛
# / panel 边界等常误报），sub-agent 在 ④.5 自评时按坐标对照 PNG 决定 fix 还是 ignore。
```
draw.io：`xmllint --noout file.drawio && drawio -x -f pdf -o out.pdf file.drawio && pdftoppm -png -r 300 out.pdf out`。

### ④.5 **视觉反馈强制闭环（架构核心，不可跳过）**

**你的代码生成是"盲写"——写到第 800 行 TikZ 时你不知道渲染出来什么样**。所有标签碰撞、轴标题压字、生命线超界、子模块挤压、数学符号渲染怪——这类问题闸门 1+2 都检测不到，只有看到 PNG 才能发现。

**目标重述**：用户要的不是"一次性生成"，是"最终交到他手上的图必须完美"。**中间迭代多少轮无关紧要，只要图最后是完美的就行**。

**强制流程**：

```
0. Read 渲染出的 out-1.png + 视觉直觉先行（应用 3 大法则，见下）
1. Read overlap.json（路径 = .tex 同目录的 overlap.json，步骤 ④ 跑出来的结构化几何检测）
2. 加载 references/visual-review-checklist.md（46 项强制审查清单）
3. 逐项回答 46 个 Y/N：S1-S10（空间）/ T1-T7（文字）/ M1-M10（语义）/ E1-E14（连线精度）/ A1-A5（美学）
   每项必须有一句证据（"我在 PNG 中看到…" 或 "overlap.json 中 N 处 line-through-node 我标为 …"），不允许凭印象
4. 任一项 N → 列入 blocker → 输出 patch → Edit → 回 ④ 重编译 → 回 0
5. Step 0 + 全部 46 项 Y → **把图给用户看**（用户终审，AI 视觉有盲区）
6. 用户也通过 → 交付
```

**Step 0：视觉直觉先行（在 46 项 Y/N 之前必走）**

把自己当成第一次看这张图的读者，**用 3 大法则扫描整图**，输出 **5** 段证据：

| Step 0 检查 | 输出要求 | 法则 |
|---|---|---|
| **A. 3 秒第一印象** | 写出"3 秒内看到的 3 件事"（如 "蓝色主流左→右 / 中间有 hero / 右侧 3 个 head"）| 法则 1 |
| **B. 主线眼睛轨迹** | 找出图中**最重要的那条数据流**，用眼睛沿它从起点走到终点。任何"卡住"位置 = blocker（如 fig97 Pedersen 框里跑出箭头 / fig118 tip 撞坐标 / fig120 孤立彩点） | 法则 2 |
| **C. 删除测试** | 列出**疑似可删的元素**（孤立装饰 / 多余 leader / 重复 label）。空则一句 "无可删元素" | 法则 3 |
| **D. 审美退步测试**（round ≥ 2 时） | 对比上轮 PNG，本轮修了 X bug 但有没有引入新审美问题（对称丢 / 平行断 / 间距不均）？ | 法则 3 |
| **E. 大块空白扫描 + 步骤①注释核验**（2026-05-21 fig126 教训）| (1) **图整体扫描有无 > 3cm × 2cm 大块空白**（阈值与 S6 对齐，避免阈值分叉）（fig126 Encoder 列下方 + WaveNet 横跨全宽 → 左下 5×6cm 空白）；(2) **打开 figure.tex 头部确认有"Step ① 设计文档"注释块**——形式 **A (ASCII 草图) 或 B (Narrative 描述)** 二选一（复杂图用 B）；(3) **内容最低要求**——form A 含可辨认 ASCII 草图（不只是模板边框）；form B 含至少一处 x/y 范围描述（如 "Encoder x=0-6cm"）。若 (1) fail OR (2) 两种都没有 OR (3) 注释块为空洞模板 → critical blocker，回 ① 重做不是直接修 .tex | 法则 3 + 流程纪律 |

**Step 0 任一项 fail = blocker**，列入 patch 列表。**Step 0 通过才开始 Step 3 的 46 项**。

**为什么 Step 0 在 46 项之前**：46 项是机械验证（细节体检），容易陷入"逐项 Y / 整体烂"。Step 0 是视觉直觉（整体心电图），强迫 sub-agent **以读者视角看图**而不是 generator 视角。两者缺一不可。

**overlap.json 处理**（S8 + E12 配套）：
- `errors[]` 中的 text-overlap / text-overflow / off-center / text-line **大概率是真 bug**——按坐标定位 PNG，修
- `errors[]` 中的 line-through-node **是候选**（E12）——逐条 triage：
  - 矩阵 cell / 热力图 / 神经网络收敛节点的 hit → ignore（semantic 故意，已知误报）
  - 路径绕路穿过无关元素（如 dashed leader 穿过 box / 长曲线压在 node 上） → fix，重新 routing 或换 z-order
- `errors[]` 中的 node-overlap **是候选**（S8）——逐条 triage：
  - drop-shadow / parent-child 都已被 filter，命中的几乎都是真问题
  - panel-overflow 边界节点（如 PGM 节点底部超 panel 1-3pt） → 调坐标
  - 两个 sibling node 真重叠 → 分开
- 把 triage 决定写进 ④.5 自评的 S8 / E12 证据里（"node-overlap N 处：X 处 fix（panel 边界），Y 处 ignore"；"line-through-node N 处：M 处 fix（路径绕路），K 处 ignore（矩阵 cell）"）

**优化规则**（Batch 9 实测：fig89 耗 32min / fig86 耗 55min，多数时间在重复 Read 和 triage）：

1. **Reference 文档只首轮加载** — `SKILL.md` / `lessons.md` / `visual-patterns.md` / `step1-instructions.md` / `visual-review-checklist.md` 在 round 1 Read 一次后，**后续 round 不要重复 Read**（context 里已有）。只 Read 变化的：PNG + overlap.json + 你刚 Edit 的 figure.tex 片段
2. **空检测跳过 triage** — `overlap.json` 中 `line-through-node` 数组为空 → E12 直接答 Y："overlap.json 中 0 处 candidate"。`node-overlap` 同理 → S8 直接 Y。**不要为空数组写 reasoning**
3. **Triage 增量化** — round N 时只对 round N-1 之后**新出现**的 candidate 写 reasoning；之前 triage 过的复用结论（"同 round 1 第 3 处，仍 ignore"）
4. **ERROR 优先于 candidate** — 先把 `text-overlap` / `text-overflow` / `text-line` / `off-center` 这 4 类 ERROR 修完（这些大概率是真 bug），再回头 triage candidate。避免一边修 ERROR 一边重新 triage 同一批 candidate

**效率规则（避免 2-3x 时间膨胀）**：

1. **Reference docs 只在 round 1 Read 一次** —— `SKILL.md` / `lessons.md` / `visual-patterns.md` / `step1-instructions.md` / `visual-review-checklist.md` 在 round 1 加载到 context 后，后续 round **不要再 Read**——已经在 context 里。**仅 PNG / overlap.json / figure.tex 每轮 Read（这些会变）**。
2. **Empty candidate 跳过 triage** —— 如 overlap.json 的 `line-through-node` 数组为空，S8 / E12 直接答 "Y, 0 候选无需 triage" 即过；非空才逐条分析。
3. **Triage 缓存** —— round N 的 overlap.json triage 结论保留到 round N+1；只对**新出现**的 candidate（坐标或类型变了）写新 reasoning，已 triage 过的同坐标 candidate 直接复用 "round N 已判 ignore"。
4. **Triage 延后** —— 优先修 text-overlap / text-overflow / off-center / text-line 这 4 类 ERROR（**真 bug**），全清后再开始 triage line-through-node / node-overlap candidates。避免每轮都重新分析 candidate。

这 4 条联合预计节省 30-50% 时间，质量不损失。

**高漏检盲区**：checklist 里带 ⭐ 标记的 **13 项**是 R3-100 实测高漏检 — 审查时优先盯，写最详细的证据。详细分组见 `visual-review-checklist.md` 顶部说明。

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
| 步骤④.5 视觉反馈每一轮 | `references/visual-review-checklist.md`（46 项强制清单） |
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
| `pdf-overlap-checker.py <file.pdf> [--json]` | PDF 坐标级重叠 + 线穿节点 + 节点重叠几何检测（**7 类**：text-overlap / text-overflow / off-center / text-line / line-crossing / line-through-node / node-overlap） | 编译后必跑 |
| `figure-diff.py <ref.png> <out.png>` | SSIM + 3×3 区域差异 | 复刻任务必跑 |
| `tikz-path-router.py <spec.json>` | A* 自动避障路径 | 连线 ≥8 条可选 |

这些脚本**作为黑盒调用**——不要把源码读进上下文，跑 `--help` 看参数即可。

## 领域自适应

收到输入后**先识别论文领域**（计算机/密码学/生物/物理/化学/AI/网络/系统/区块链等），以该领域专家身份选术语和布局风格。
