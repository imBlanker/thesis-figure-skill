# 视觉审查强制清单（39 项）

> **何时加载**：步骤 ④.5 视觉反馈循环中每一轮加载本文件。
> **加载后必须做的事**：Read PNG 后**逐项**回答 30 个 Y/N 检查项。**不允许凭印象跳过**——
> 必须每项给出明确 Y 或 N + 一句简短证据（"我在 PNG 中看到 X 在位置 Y"）。
> **任一项 N = blocker**，必须修复后重新审查全部 30 项。
>
> **本清单已合并旧 `review-checklist.md` 中仍有效的人审项**。步骤⑤ 不再加载独立的 review-checklist，
> 步骤④.5 视觉审查通过 = 步骤⑤ 评分通过。

## 强制流程

```
1. Read 渲染出的 PNG（图像输入进上下文）
2. 加载步骤① 的画图指令文本（用来对照）
3. 逐项回答下面 39 项，每项强制 Y/N 不允许 "差不多"
4. 任一 N → 列为 blocker → 输出修复 patch → recompile → 回 1
5. 全部 30 项 Y → 输出给用户看（用户是最后闸门，AI 视觉有盲区）
6. 用户也说 OK → 交付
7. **没有轮数上限**——只要还有 N 或用户有意见，就继续修。N 远比"3 轮够了"重要
```

**心理对抗**：你会有强烈的"差不多就过了"冲动（这是认知疲劳）。**这种冲动出现 = blocker 还在**。强迫自己回答每项，写出证据。

**⭐ 高漏检项**：带 ⭐ 标记的 6 项（E3 / E7 / E8 / **E9** / M8 / M9）是 R3-100 用户/主 agent 复审实测，sub-agent 自评 100% 漏过的盲区——**审查时优先盯这 6 项，每项的证据要写得最详细**。E9 是 Batch 3 用户复审新增（紧密布局 tip 精度，跨 5 张图都触发）。

## 维度 1：空间 / Spatial（7 项）

- [ ] **S1** 任意两个文字标签都不重叠（包括轻微 1-2px 触碰）？
- [ ] **S2** 任意标签都不被连线穿过——**包括 hero sub-panel 内小盒子（≤1.5cm 宽）内部连线穿过盒内文字**（fig11 教训：CSP Block 小盒子里 .east/.west 连线和盒内 label 同 y，渲染出来线在字上压过去，像 strikethrough）。**自评必看 hero sub-panel 内每个小盒**
- [ ] **S3** **强制重叠枚举**——不只检查"节点框 vs 节点框"，逐一扫描整图标出**任何视觉重叠**：(a) box vs box，(b) text vs line/arrow，(c) leader vs unrelated element，(d) annotation box vs background zone。**自评必须写出"X 处重叠：位置 / 类型"或"0 处重叠"**，禁止印象判断。fig55/58/60 教训：sub-agent 自评 S3=Y 但用户能看到 3 张图都有重叠
- [ ] **S4** 所有 zone 边框**完整包含**其声明的全部 members（无元素溢出 zone）？
- [ ] **S5** 同行/同列同类元素位置对齐（同 y 或同 x，差距 < 0.1cm）？
- [ ] **S6** 没有可避免的大块白色空带——**强制扫描整图，逐片量连续无内容区域的 width × height**。任何 > 3cm × 2cm 的空白 → 写 "在 X-Y 范围有 W × H 空白" 并标 N。**递归/折叠类协议（IPA、Merkle fold、聚合树）末尾轮天然短**，要注意 bottom info box 不要锁 zone 底导致中间出现衰减空白（fig22 教训）。修复：info box 紧贴最末轮内容 / 空白补充半技术内容 / info box 挪出 zone 外
- [ ] **S7** 容器（zone / hero）的标题**没有**用 fill 嵌在容器边框上切断边框？标题应在容器外白空间或容器内远离边框。

## 维度 2：文字 / Typographic（6 项）

- [ ] **T1** 所有数学公式字符（`\mathbf`, `\frac`, 下标、希腊字母）渲染正常（**无小点、无 sigil、无问号、无空白方块**）？
- [ ] **T2** 所有标签字号在 300dpi PNG 下可读（即 ≥ `\scriptsize`）？
- [ ] **T3** 编译日志无 `Missing character` 警告？
- [ ] **T4** 任一标签都不被截断——**对每个 text width < 3cm 的标签盒，显式量字符数 vs box width**（中文每字 ~0.4cm，英文每字 ~0.2cm）。fig15 教训："R groups alternate above/below sheet" 在 2.5cm 框里溢出右边界，自评 35/35 Y 漏检。**自评写 "label X (Ncm) in box (Mcm) → fit ✓/✗"**
- [ ] **T5** 同图内中/英文标签使用一致（不在某处出现孤立的英文标签或反之）？
- [ ] **T6** 字体全图统一（无 Computer Modern fallback 出现在中文环境的英文/公式上）？

## 维度 3：语义 / Semantic（10 项）

- [ ] **M1** 画图指令里列出的**每个模块**在 PNG 中都能找到？
- [ ] **M2** 画图指令里规定的**每条连线**都画出来了？
- [ ] **M3** 每条连线的源/目标方向和指令一致——**逐条线显式回答 "tip 在哪一端"**：tip 必须在 **destination** 端（信息流入处），不是 source 端。fig18 教训：MLP I/O 箭头两端 tip 都反了，自评 N/A 跳过；强制写"input→MLP: tip at MLP.west ✓"避免漏检
- [ ] **M4** 每条连线的样式（颜色/虚实/粗细）和指令规定一致？
- [ ] **M5** 双向/对称关系的箭头（contrastive、bidirectional flow）两端都有 tip（用 `{Stealth}-{Stealth}`）？
- [ ] **M6** 指令里规定的 **hero 模块**（如果有）视觉上比辅助模块大 ≥2 倍？*（简单图无需 hero，本项 N/A 视为 Y）*
- [ ] **M7** **没有指令外的多余元素**（"多即是少"——不在指令里的装饰应该删）？
- [ ] ⭐ **M8** **Hero substructure 真正"独一无二"**——如果展开的内容对所有 instance 都一样（Transformer Layer 1 = Layer 2 = ... = Layer N），**不要绑定具体 instance**。改标题为"通用展开 (Per-stage detail)"或选有独特性的 instance。
- [ ] ⭐ **M9** **多目标广播（1-to-N message）** 用 fork dot + N 条独立箭头或 N 条独立箭头，**不是**单条双箭头曲线？（`{Stealth}-{Stealth}` 双头**专属于 ↔ 双向**，不可挪用）
- [ ] **M10** 多步骤被压缩成单一视觉元素时**显式标注** (`{4,5}` / `(2 substeps)` / `∀t` / "(applied at every step)")？不标 = 视觉撒谎

## 维度 4：连线精度 / Edges（11 项）

- [ ] **E1** 箭头 tip 真正止于目标框**外侧**（不刺入框内）？默认 `shorten >=6pt`，必要时 `[xshift=-2pt]box.west`
- [ ] **E2** Junction / 汇合点节点（小 dot 或 coordinate）**不被箭头 tip 戳**——**包括 Y-fork / 单 source 多 target 起点的 dot**（fig28 Mask R-CNN box head 教训：FC→dot→{class,bbox} 的 FC 出来那段不能带 tip）？规则：dot 周围所有相邻线都无 tip，**tip 只画在最终到达 target box 的那段**。
- [ ] ⭐ **E3** Fan-out / Fan-in 强制清点——**逐一列出图中所有 3+ 条线从同一区域散出或汇入的位置**（不能跳过"没有"，必须显式写 "0 处" 或 "N 处: ..."）。每处必须是 tree pattern (trunk + spine + stubs)，不是"扫帚式"散射。
- [ ] **E4** 连线之间不交叉（除非真有 cross 语义）？
- [ ] **E5** "能直就直"——源/目标 x 或 y 对齐时用直线，不画 L 弯？
- [ ] **E6** **任何 90° 弯折都用 `rounded corners=5-8pt`** + **虚线 routing 强制 90° 直角，禁用 Bezier 曲线/对角线段**——sharp 90° 看起来粗糙廉价；非 90° 曲线/对角 routing 看起来乱。所有 dashed leader / residual skip / reference 引线**首选 90° L-bend with rounded corners**，不用 `to[bend left/right]` 或自由曲线。fig48 教训：sharp 90°；fig56 教训：dashed STE arc 曲线本可用 90°
- [ ] ⭐ **E7** **自由浮动的 annotation / callout / step number / 旁注文字都有 dotted/dashed leader line 引到具体元素**？（仅靠 y 对齐隐式关联**不算**——这是读者认知负担最大的失败模式之一）
- [ ] ⭐ **E8** **所有 leader / 虚线 / 引线必须有可见终点**（节点边、文字、箭头 tip 中至少一个）。没有终点的悬空虚线 = blocker
- [ ] ⭐ **E9** **箭头/连线必须用 canonical 模板**（深度调研 2026-05-18）——所有 `\draw[arrow]` / `\draw[arrow thick]` / `\draw[arrow thin]` / `\draw[residual]` 用 `tikz-template.tex` 预定义 styles，**禁止**手写 `-{Stealth[scale=X]}`。前 4 轮"按箭头长度选 scale"的方案被深度调研推翻 — TikZ 原生设计是 `length=⟨dim⟩ ⟨line_width_factor⟩` + `width'=⟨pt⟩ ⟨length_factor⟩` + `bending` library 让 tip **自动跟随 line width**。**自评 E9**：(1) `bending` library 是否加载？(2) 是否用 canonical `arrow/.style`？(3) line width 选档（0.6 / 1.0 / 1.6 pt）是否合理？三项都 Y 才过
- [ ] **E10** **长距离虚线/leader 路径不绕图大半圈**——同源同目标的虚线如果绕过 ≥3 个无关元素或转折 ≥3 次，读者难追踪。修复：(a) 缩短路径直连，(b) 与其它平行虚线归入同一"通道"（lane）相邻走，(c) 移动 source 或 target 减少绕路距离。fig36 教训：residual skip 紫虚线从 Linear Projection 绕半圈过 Stop Token + PostNet 上方再下到 ⊕ — 路径模糊读者迷路
- [ ] **E11** **路径视觉连续性**——所有 `\draw` 路径从起点到终点视觉上**无断点**。检查：(a) 多段 `\draw` 拼接段端点严格一致（用 named coordinate，不要手写浮点坐标），(b) 路径若被其它元素遮挡 → 用 pgfonlayer 把路径放上层 OR 移动遮挡元素，(c) 同一逻辑线**用单个 `\draw` 多段** `(A)--(mid)--(B)` 优于拆 2 个 `\draw`。fig57 教训：STARK 多段路径中间出现视觉断点

## 维度 5：美学 / Aesthetic（5 项）

- [ ] **A1** 整图视觉平衡（左右两半权重相当，不头重脚轻）？
- [ ] **A2** 配色和谐（同类元素同色，强调色用得克制）？
- [ ] **A3** 同行/同层并列元素**等宽等高**？
- [ ] **A4** Zone 标签位置在 zone 视觉中心正上方且与其他 zone 标签**同 y**？
- [ ] **A5** **多个 legend 框间距 ≥1cm**——并排的 legend 框如果间距 <1cm，视觉上像一个被分割的大框，读者不知道两个框是独立 legend 还是合并组。fig17 教训：legend 两框紧贴 → 应该合并成单框 OR 横向加 ≥1cm gap

## 审查输出格式

每轮审查结束后必须以以下格式输出：

```
=== Visual review round N ===
[S1] Y/N  — <一句证据>
[S2] Y/N  — <一句证据>
...
[A4] Y/N  — <一句证据>

Blockers (N items): [S2, T1, ...]
Warns (Y but borderline): [S6, ...]

Patch plan (single class per round, minimal change):
  - <具体 Edit 描述>
```

输出"Blockers: []"且**用户确认**后才能交付。

## 升级机制

- **第 3 轮还有 ≥5 blocker** → 局部修补救不了，回步骤① 重新设计画图指令
- **同一 blocker 连续 2 轮没修好** → 你修复方向错了，换思路
- **审查 5 轮后宣称 0 blocker 但你"心里觉得还有问题"** → 清单本身不够细，把怀疑写成新项追加本文件
- **自评 + 对抗 sub-agent 都 0 blocker 后**：**仍然把图给用户看**。实测案例：MMAlign Round 10 自评 + 2 个对抗 sub-agent 复查全部漏掉了"标题切断 hero 边框 / 箭头刺入 task head / junction 被 tip 戳"3 个真实 blocker，**用户一眼指出来了**。AI 视觉有结构性盲区，用户终审是设计的一部分，不是绕过点。

## 复杂图可选：4-agent 并行专项审查

对于 ≥40 元素的富视觉图，并行 spawn 4 个子 agent：

```
你是 <维度名> 专项审查者。Read PNG: <path>，对照画图指令: <plan>。
**只**审查 <维度> 的 N 项清单（见本文件）。每项 Y/N + 证据。
不审查其他维度——专注本维度。
```

每个 agent 用上面 5 个维度（Spatial / Typographic / Semantic / Edges / Aesthetic）之一。

## 历次用户终审发现的盲区（合入主清单）

| 发现日期 | 用户/sub-agent 看到的问题 | 编入清单的位置 |
|---|---|---|
| 2026-05-16 | hero 标题白底盖住橙色边框圆角 | S7 |
| 2026-05-16 | 箭头 tip 刺入 task head 框（shorten 2pt 不够） | E1 |
| 2026-05-16 | MLP→junction 段被箭头 tip 戳进 dot | E2 |
| 2026-05-16 | 3 条 fan-out 从同点散射，扫帚式 | E3 |
| 2026-05-16 | L_con 对比损失只有一端 tip，视觉显示单向 | M5 |
| 2026-05-17 | R3-100 fig01/fig07 Stage→FPN / Spectrogram→3 Conv1D 仍是 broom，sub-agent 自评 0 blocker — E3 需要"强制清点"语义而非被动检查 | E3（强化为 forced enumeration） |
| 2026-05-17 | R3-100 fig07 callout / fig08 右栏标注 / fig10 步骤编号全部自由浮动无 leader | E7（新增） |
| 2026-05-17 | R3-100 fig09 Score function 4 段虚线悬空，无终点 | E8（新增） |
| 2026-05-17 | R3-100 fig01/fig07 Hero substructure 选了通用结构展开，无 instance 独特性 | M8（新增） |
| 2026-05-17 | R3-100 fig03 PSI 消息 3 用单条双箭头曲线表达 1-to-N 广播 | M9（新增） |
| 2026-05-17 | R3-100 fig05 糖酵解 step 4-5 双酶压成一条箭头；fig06 ε̂ 只画到一个 reverse 步骤 | M10（新增） |
| 2026-05-18 | R3-100 Batch 3 fig23/26/27/28/29 5 张图都有 tip 戳进相邻 box / 文字（紧密布局下 shorten 6pt 不够） | E9（新增 ⭐） |
| 2026-05-18 | R3-100 Batch 3 fig28 Box head Y-fork: FC→dot→{class,bbox} 中 FC 出来段带 tip 戳进 dot | E2 强化（覆盖 Y-fork 起点） |
| 2026-05-18 | R3-100 Batch 3 fig22 Bulletproofs IPA: Round 4 与 bottom info box 之间 >3cm 空白（递归折叠协议末尾轮短，info 锁底导致中间空） | S6 强化（强制度量空白） |
| 2026-05-18 | R3-100 Batch 4 fig31/32/33/36/37/38 6 张图：E9 强制 scale ≥ 1.3 在短箭头上导致 tip 头大身子小（占长度 20-30%）| E9 修订（scale 按箭头长度调整：长 1.0-1.3 / 中 0.9-1.0 / 短 0.7-0.9） |
| 2026-05-18 | R3-100 Batch 4 fig36 residual skip 紫虚线绕图大半圈过 3 个无关元素 + 多次转折 | E10 新增（长虚线 routing 不绕路） |
| 2026-05-18 | R3-100 Batch 5 fig43/46/47 箭头 tip 形状奇怪 — Stealth 在 scale 0.75-0.9 下凹背变"细长针刺" | E9 强化第三项（短箭头换 Latex / Triangle 实心 tip） |
| 2026-05-18 | R3-100 Batch 5 fig48 sharp 90° 折线 + 多 `\draw` 段间不连续 | E6 强化（任何 90° 都用 rounded corners + 段间共享 named coordinate） |
| 2026-05-18 | R3-100 Batch 5 fig41 Hero panel "side-dependency"（CPB 偏置悬挂）造成拥挤 | 新 lesson（hero 拒绝 side-dependency） |
| 2026-05-18 | R3-100 Batch 5 fig46 文字超出 box（T4 recurrence，fig15 老问题再现） | T4 已存 — 重申 |
| 2026-05-18 | R3-100 Batch 6 fig55/58/60 重叠（box/text/leader）— S3 抽象自评滑过 | S3 强化（强制枚举每处重叠 + 类型） |
| 2026-05-18 | R3-100 Batch 6 fig57 多段 \draw 拼接端点不一致 → 视觉断点 | E11 新增（路径视觉连续性 + named coord） |
| 2026-05-18 | R3-100 Batch 6 fig56 虚线 STE arc 用曲线 routing 本可 90° 直角 | E6 进一步（虚线优先 90° 直角，禁 Bezier） |
| 2026-05-18 | R3-100 Batch 6 箭头末端 4 轮迭代仍有问题 — rules 可能不够，需 concrete TikZ template | 下一步：visual-patterns.md 加 canonical 模板 |
| 2026-05-18 | 深度调研（PGF/TikZ 官方 + PlotNeuralNet + arrows.meta + bending lib）：发现 5 个根因 — bending library 没加载 / scale 不该手调 / line width 才是核心 / width' sep 没用 / 业界用粗线默认 tip | tikz-template.tex `arrow/.style` canonical 模板 + E9 简化为"用 canonical 不要手写 Stealth" |

新的用户终审发现的问题，按此格式追加 + 编入主清单。
