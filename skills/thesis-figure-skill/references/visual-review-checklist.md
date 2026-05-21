# 视觉审查强制清单（47 项）

> **何时加载**：步骤 ④.5 视觉反馈循环中每一轮加载本文件。
> **加载后必须做的事**：Read PNG + Read overlap.json 后**逐项**回答 46 个 Y/N 检查项。
> **不允许凭印象跳过**——必须每项给出明确 Y 或 N + 一句简短证据
> （"我在 PNG 中看到 X 在位置 Y" 或 "overlap.json 中 N 处 line-through-node，triage 为…"）。
> **任一项 N = blocker**，必须修复后重新审查全部 46 项。
>
> **本清单已合并旧 `review-checklist.md` 中仍有效的人审项**。步骤⑤ 不再加载独立的 review-checklist，
> 步骤④.5 视觉审查通过 = 步骤⑤ 评分通过。

## 强制流程

```
0. Read PNG + 视觉直觉先行（3 大法则扫描，见 SKILL.md 顶部"视觉法则"段）
   → 输出 A/B/C/D/E **5 段证据**：
     A. 3 秒第一印象
     B. 主线眼睛轨迹
     C. 删除测试
     D. 审美退步测试（round ≥ 2）
     E. 大块空白扫描 + 步骤①注释核验（2026-05-21 fig126/fig137 教训）——
        (1) 扫描整图有无 > 3cm × 2cm 大块空白（阈值与 S6 对齐）；
        (1a) **客观度量铁律**：必须**写出怀疑区的 x/y 范围 + 宽×高**
             （例："Encoder.east x=7 至 Decoder.west x=18 = 11cm 宽 × 5cm 高"），
             **禁止抽象判断**"无空白"。fig137 教训：sub-agent 写"rail 填充"= 自欺。
        (1b) **填充判定**：一个区域算"已填充"当且仅当区域内有
             ≥1 个 box/text/嵌入 viz/标注块。**细线（rail/leader/dashed/arrow）不算**
             ——线占面积可忽略。只有线穿过 = 仍是空白。
        (2) 打开 figure.tex 头部确认有"Step ① 设计文档"注释块——
            form A (ASCII 草图) 或 form B (Narrative 描述) 二选一（复杂图用 B）；
            注释块**最低内容要求**：form A 含可辨认 ASCII；form B 含至少一处 x/y 范围描述。
            若两种都缺、或注释块为空洞模板（无实质内容）→ critical blocker，
            回 ① 重做（**不是改 .tex，而是回 ① 重新规划布局**：拉近两个 hero / 
            中间加内容 / 改为垂直布局）。
   → 任一 fail = blocker
1. Read overlap.json（步骤 ④ 跑出的 7 类几何检测结构化报告）
2. 加载步骤① 的画图指令文本（用来对照）
3. 逐项回答下面 46 项，每项强制 Y/N 不允许 "差不多"
4. 任一 N → 列为 blocker → 输出修复 patch → recompile → 回 0
5. Step 0 + 全部 46 项 Y → 输出给用户看（用户是最后闸门，AI 视觉有盲区）
6. 用户也说 OK → 交付
7. **没有轮数上限**——只要还有 N 或用户有意见，就继续修。N 远比"3 轮够了"重要
```

**极简档说明**：①.5 判出极简档时，Step 0 全 5 段**仍强制**，但 E 段只需验证 form A（ASCII 注释块）存在 + 可辨认即可；form B 不适用极简档。

**为什么先 Step 0 再 46 项**：46 项是**机械验证**（细节体检），单走容易"逐项 Y 但整体烂"。Step 0 是**视觉直觉**（整体心电图），强迫从读者视角看图。两者缺一不可。

**Step 0 的 3 大法则**（详细见 SKILL.md）：

- **法则 1：0.1 秒直觉法则** — 人先用直觉看图，视觉流向 ≠ 逻辑流向 = 必错
- **法则 2：读者眼睛轨迹** — 沿主线走一遍，任何"卡住"位置 = blocker
- **法则 3：删除测试 + 干净 > 塞满** — 不必要的装饰 = 噪音；迭代不能引入新审美问题

**心理对抗**：你会有强烈的"差不多就过了"冲动（这是认知疲劳）。**这种冲动出现 = blocker 还在**。强迫自己回答每项，写出证据。

**⭐ 高漏检项**：带 ⭐ 标记的 14 项（**S8 / S9 / S10 / T7 / M8 / M9 / E3 / E7 / E8 / E9 / E12 / E13 / E14 / E15**）是 R3-100 用户/主 agent 复审实测，sub-agent 自评 100% 漏过的盲区——**审查时优先盯这 14 项**。注意分组：
- **几何工具检测类**（必跑 `pdf-overlap-checker.py --json` 配套）：S8 / E12（node-overlap + line-through-node candidate triage）
- **间距测量类**（必报具体 cm 数值）：S9 / S10 / T7
- **fan/连线 canonical 类**（按模板规范）：E3 / E9 / E13 / E14 / E15
- **逻辑/语义类**（视觉对照画图指令）：M8 / M9 / E7 / E8

## 维度 1：空间 / Spatial（10 项）

- [ ] **S1** 任意两个文字标签都不重叠（包括轻微 1-2px 触碰）？
- [ ] **S2** 任意标签都不被连线穿过——**包括 hero sub-panel 内小盒子（≤1.5cm 宽）内部连线穿过盒内文字**（fig11 教训：CSP Block 小盒子里 .east/.west 连线和盒内 label 同 y，渲染出来线在字上压过去，像 strikethrough）。**自评必看 hero sub-panel 内每个小盒**
- [ ] **S3** **强制重叠枚举**（视觉层面）——逐一扫描整图标出**非几何检测器能抓的视觉重叠**：(a) text vs line/arrow（粗实线压字、leader 穿文字），(b) leader vs unrelated element，(c) annotation box vs background zone，(d) **微重叠 1-3px**（接近但未完全重叠，几何 IoU 阈值抓不到）。**注**：sibling node vs sibling node 的几何重叠已由 **S8** 用 `pdf-overlap-checker.py --json` 自动检测，S3 不必再重复。**自评必须写出"X 处重叠：位置 / 类型"或"0 处重叠"**，禁止印象判断。fig55/58/60 教训：sub-agent 自评 S3=Y 但用户能看到 3 张图都有重叠
- [ ] **S4** 所有 zone 边框**完整包含**其声明的全部 members（无元素溢出 zone）？
- [ ] **S5** 同行/同列同类元素位置对齐（同 y 或同 x，差距 < 0.1cm）？
- [ ] **S6** 没有可避免的大块白色空带——**强制扫描整图，逐片量连续无内容区域的 width × height**。任何 > 3cm × 2cm 的空白 → 写 "在 X-Y 范围有 W × H 空白" 并标 N。**递归/折叠类协议（IPA、Merkle fold、聚合树）末尾轮天然短**，要注意 bottom info box 不要锁 zone 底导致中间出现衰减空白（fig22 教训）。修复：info box 紧贴最末轮内容 / 空白补充半技术内容 / info box 挪出 zone 外
- [ ] **S7** 容器（zone / hero）的标题**没有**用 fill 嵌在容器边框上切断边框？标题应在容器外白空间或容器内远离边框。
- [ ] ⭐ **S8** **节点几何重叠检测**（2026-05-19 新加）——读 `pdf-overlap-checker.py --json` 的 `node-overlap` category。每条都是**两个 sibling node rect 的真实几何相交**（drop shadow / 包含关系已过滤）。逐条对照 PNG triage：① panel-overflow 边界节点（如 PGM 节点底边超出 panel 1-3pt）→ blocker 必须调位置；② 真节点重叠 → blocker 必须分开。自评 **S8**：(1) 跑了 `--json` 看 node-overlap？(2) 每条都 triage 了？(3) 标 fix 的全部已修？三项都 Y 才过
- [ ] ⭐ **S9** **最小邻接间距强制扫描**（2026-05-19 Batch 10 用户反馈：fig91-95 仍频繁出现重叠）——逐对相邻元素测量并写出距离：① 同行 sibling box ≥ 0.8cm；② 跨行 box ≥ 0.6cm；③ text 与所在 box 边距 ≥ 0.3cm（防 text 切边框）；④ 连线与无关 box 边距 ≥ 0.4cm（防擦框）。自评必写："X 处违反: A box 与 B box 仅 0.4cm / 0 处违反"，禁止印象判断
- [ ] ⭐ **S10** **时序图 annotation/compute box 距 lifeline ≥ 0.5cm** *（仅时序图适用，非时序图直接 "非时序图, N/A" 一句过）*——所有放在时序图里的 annotation box / compute box / formula box：(a) 测量 box 的最近边离最近 lifeline 的水平距离；(b) 必须 ≥ 0.5cm，否则与 lifeline 上的 activation bar (±0.225cm 半宽) 视觉重叠；(c) 一行多 box 时，box 的中心 x 应避开所有 lifeline x（不只与最近的）。自评 S10：写"N 个 annotation box: 最近距离 X cm ✓ / X 处违反: ..."（fig107 教训）

## 维度 2：文字 / Typographic（7 项）

- [ ] **T1** 所有数学公式字符（`\mathbf`, `\frac`, 下标、希腊字母）渲染正常（**无小点、无 sigil、无问号、无空白方块**）？
- [ ] **T2** 所有标签字号在 300dpi PNG 下可读（即 ≥ `\scriptsize`）？
- [ ] **T3** 编译日志无 `Missing character` 警告？
- [ ] **T4** 任一标签都不被截断——**对每个 text width < 3cm 的标签盒，显式量字符数 vs box width**（中文每字 ~0.4cm，英文每字 ~0.2cm）。fig15 教训："R groups alternate above/below sheet" 在 2.5cm 框里溢出右边界，自评 35/35 Y 漏检。**自评写 "label X (Ncm) in box (Mcm) → fit ✓/✗"**
- [ ] **T5** 同图内中/英文标签使用一致（不在某处出现孤立的英文标签或反之）？*（纯英文/纯中文图直接 Y）*
- [ ] **T6** 字体全图统一（无 Computer Modern fallback 出现在中文环境的英文/公式上）？*（T3 编译期 Missing character 检查已覆盖，本项作交叉验证）*
- [ ] ⭐ **T7** **标签放置规范 + 最小间距 + fill=white 安全用法**（2026-05-20 Batch 11/12 + 2026-05-21 fig137 v2 用户反馈）——
  - **方向**：水平箭头/线段上的标签必须用 `anchor=above`/`below`，**禁止** `anchor=left`/`right`（会落在线 y level 重叠）；垂直线同理用 `anchor=left`/`right`
  - **最小间距铁律**（fig116 + fig137 v2 教训）：label 边缘到 line 的距离**视觉默认 ≥ 0.5cm**；绝对最低 ≥ 0.3cm（compile fail 阈值，**边界值不安全**）；fig137 v2 "Multitask Output" 标题离 spine 仅 0.3cm = 视觉上太紧。正确写法：`anchor=south at (x, line_y+0.5)` 或 `anchor=south, yshift=14pt at (x, line_y)`
  - **`fill=white` + 单字符 label 警告**（fig137 v2 "Q" 紫色方块教训）：`\node[fill=white, inner sep=1pt, font=\scriptsize\bfseries, color=PURPLE] {Q}` 在白底 PDF 上，fill=white 不可见，紫色粗体单字符把 inner sep 区域填满 → 看起来像紫色方块漂浮（fig120 类教训变体）。**修复**：(a) 用 `fill=white, inner sep=3pt`（更大 padding） OR (b) 不用 `\bfseries`（normal weight 不会把 inner sep 填满）OR (c) 用更长 label（"Q (Query)" 而非 "Q"）
  - **典型 bug 模式**：①`\node[..., right] at (3.0, 0.5) {3'};` 同 y 压字（fig110）；②`\node[..., anchor=south] at (14.0, -1.98) {z_b};` 线在 y=-2.0，间距仅 0.02cm（fig116）；③ fig137 v2 单字符紫色 bfseries Q = "紫色方块"
  - 自评 T7：写"N 个 label：全 above/below ✓ / 每个 label 到对应 line 距离 ≥ 0.5cm ✓ / 0 处 fill=white 单字符 bfseries（或所有此类 label 已加 inner sep ≥ 3pt） ✓"，**禁止印象判断**——必须报具体数值

## 维度 3：语义 / Semantic（10 项）

- [ ] **M1** 画图指令里列出的**每个模块**在 PNG 中都能找到？
- [ ] **M2** 画图指令里规定的**每条连线**都画出来了？
- [ ] **M3** 每条连线的源/目标方向和指令一致——**逐条线显式回答 "tip 在哪一端"**：tip 必须在 **destination** 端（信息流入处），不是 source 端。fig18 教训：MLP I/O 箭头两端 tip 都反了，自评 N/A 跳过；强制写"input→MLP: tip at MLP.west ✓"避免漏检
- [ ] **M4** 每条连线的样式（颜色/虚实/粗细）和指令规定一致？
- [ ] **M5** 双向/对称关系的箭头（contrastive、bidirectional flow）两端都有 tip（用 `{Stealth}-{Stealth}`）？
- [ ] **M6** 指令里规定的 **hero 模块**（如果有）视觉上比辅助模块大 ≥2 倍？*（极简档/无 hero → "无 hero, N/A" 一句过）*
- [ ] **M7** **没有指令外的多余元素**（"多即是少"——不在指令里的装饰应该删）？
- [ ] ⭐ **M8** **Hero substructure 真正"独一无二"**——如果展开的内容对所有 instance 都一样（Transformer Layer 1 = Layer 2 = ... = Layer N），**不要绑定具体 instance**。改标题为"通用展开 (Per-stage detail)"或选有独特性的 instance。
- [ ] ⭐ **M9** **多目标广播（1-to-N message）** 用 fork dot + N 条独立箭头或 N 条独立箭头，**不是**单条双箭头曲线？（`{Stealth}-{Stealth}` 双头**专属于 ↔ 双向**，不可挪用）
- [ ] **M10** 多步骤被压缩成单一视觉元素时**显式标注** (`{4,5}` / `(2 substeps)` / `∀t` / "(applied at every step)")？不标 = 视觉撒谎

## 维度 4：连线精度 / Edges（15 项）

- [ ] **E1** 箭头 tip 真正止于目标框**外侧**（不刺入框内）？默认 `shorten >=6pt`，必要时 `[xshift=-2pt]box.west`
- [ ] **E2** **`\draw[arrow*]` 的 tip 终点必须是 node.anchor，禁止是裸坐标 / `\coordinate`**——tip 指向空气 = bug。三类违规：
  - (a) **Y-fork / fan-out 起点 dot 被 tip 戳**：fig28 Mask R-CNN box head 教训，FC→dot→{class,bbox} 的 FC 出来那段不能带 tip
  - (b) **Y-junction / fan-in 汇合点被 tip 戳**：fig120 sgRNA Assembly 教训，crRNA+tracrRNA→sgRNA 的两条 incoming 都用 `\draw[arrow]` 带 tip → "><" 视觉
  - (c) **spine 中间节点 / 共享 rail 上的 tip**（fig118 用户反馈新发现）：`\draw[arrow] (bu_p3.east) -- (14.5, 0.0);` tip 落在裸坐标 (14.5, 0.0) 而非任何 node → "撞墙"视觉
  
  **铁律**：(i) **incoming/spine 段全部用 `\draw[line width=...]` 或 `\draw[fan_stub]`（视 stub 起点）**，**禁用 `\draw[arrow]`**；(ii) tip 段终点必须是 `(target_box.anchor)` 形式，不是 `(x,y)` 坐标；(iii) 所有相关段同色
  
  **自评 E2 写**："N 条 `\draw[arrow]`：每条终点 = box.anchor ✓ / 0 条 tip 撞 coordinate ✓"
- [ ] ⭐ **E3** Fan-out / Fan-in 强制清点 + **stub-spine 视觉连续性 + 颜色一致性**——**逐一列出图中所有 3+ 条线从同一区域散出或 2+ 条线汇入同一目标的位置**（不能跳过"没有"，必须显式写 "0 处" 或 "N 处: ..."）。

  **🔴 反绕过铁律**（2026-05-21 fig137 v2 教训）：**只要有 ≥2 条 `\draw[arrow]` 从同一 source.anchor 出发到不同 targets**（即使写法是两条独立 `\draw`、不是 spine + stub），**仍算 fan-out**，必须重写为 canonical。fig137 v2 sub-agent 用 2 条独立 `\draw[arrow] (enc_an2.east) -- ... -- (ca_k.west)` / `(enc_an2.east) -- ... -- (ca_v.west)` 绕过 E3 自评 → corner 处的 `rounded corners + thick line` 产生可见 bulge 像 fork dot。**判定**：grep figure.tex，如果同一 `node.anchor` 出现 ≥2 次作为 `\draw[arrow]` 起点 → 必须重写。

  每处必须：

  **(a) Fan-out canonical（1 source → N targets）**：trunk + spine + N stubs（tree pattern，不是扫帚式）
  ```latex
  \draw[arrow, color=COLOR] (source) -- (spine_center);             % trunk WITH tip removed
  \draw[line width=1pt, color=COLOR] (spine_L) -- (spine_R);         % horizontal spine, NO tip
  \draw[fan_stub, color=COLOR] (spine_L) -- (target1.north);         % stub WITH tip
  \draw[fan_stub, color=COLOR] (spine_R) -- (target2.north);         % stub WITH tip
  ```

  **(b) Fan-in canonical（N sources → 1 target，fig120 用户反馈教训）**：N stubs + spine + 单条 outgoing
  ```latex
  \coordinate (Y) at (Y_spine);
  \draw[line width=1pt, color=COLOR, rounded corners=5pt]
    (source1.south) -- (source1.south |- Y);              % drop NO tip
  \draw[line width=1pt, color=COLOR, rounded corners=5pt]
    (source2.south) -- (source2.south |- Y);              % drop NO tip
  \draw[line width=1pt, color=COLOR]
    (source1.south |- Y) -- (source2.south |- Y);         % horizontal spine NO tip
  \draw[arrow, color=COLOR] (midpoint) -- (target.north); % 唯一带 tip + 同色
  ```

  **(c) 颜色铁律（fig120 spine 黑 + stub 紫/绿教训）**：**spine + 所有 stubs + 出口 trunk 全部 SAME COLOR**。分支识别**靠 target box 颜色**承担，不靠线的颜色。唯一例外：dashed residual / dashed feedback（dashed 已视觉区分，可独立着色）

  **(d) `fan_stub` style（shorten <=0pt）**不能用 `arrow`（`shorten <=1pt` 留 gap）

  **(e) spine 中点不放 `fill=white` 的 sum/junction 圆圈**——会截断 spine

  **(f) 折角必须 `rounded corners=5pt`**——sharp 90° L-bend 视觉粗糙（E6 已规定）

  **🔴 (g) 几何铁律**（2026-05-21 fig137 v3 教训：spine 飞角 + trunk 偏心 + box 不等宽）：
  - **g1. spine 范围 = stubs 精确范围**：`spine.x_left == leftmost stub.x` AND `spine.x_right == rightmost stub.x`，**禁止 spine 两端伸出 stubs 范围之外**（fig137 v3 spine 17.4-25.4 但 stubs 18.2-24.7 → 两端"飞角"0.7-0.8cm 悬空）
  - **g2. trunk.x = stubs 中心**：trunk 进入 spine 的 x 必须 = (leftmost stub.x + rightmost stub.x) / 2，**不能跟 source box 中心走**（fig137 v3 trunk x=22 跟 otok 中心走，但 stubs 中心 21.45 → 偏右 0.55cm）。若 source box 中心 ≠ stubs 中心，**移动 source box 到 stubs 中心**（fan-out 通常 source 比 targets 重要，targets 的对齐优先）
  - **g3. stubs 等距分布**：`stub[i+1].x - stub[i].x` 全相等（误差 < 0.1cm）。**禁止因 box 宽度不等被迫调整 stub 位置**
  - **g4. 所有 target box 等宽等高**（A3 强制）：取 `max(label_width) + 0.4cm padding` 设为统一 `minimum width`；标签长度差异大（如 `[lang]` vs `hello world ...`）时**缩短长 label**（如改 "hello world" → "text" 或 "[txt]"）OR 全部统一 box 宽度

  自评 E3 写："N 处 fan-out/fan-in: 第 X 处 = fan-{out|in} → spine+stubs+trunk 全色 = COLOR ✓ / incoming/outgoing 段数 = a→b ✓ / 仅最终段带 tip ✓ / rounded corners=5pt ✓ / **几何检查**：spine.x = [leftmost.x, rightmost.x] ✓ / trunk.x = stubs 中心 ✓ / stub 间距均等 ✓ / box 等宽 ✓"。*极简档/无 fan 结构 → "0 处 fan, N/A" 一句过*
- [ ] **E4** 连线之间不交叉（除非真有 cross 语义）？
- [ ] **E5** "能直就直"——源/目标 x 或 y 对齐时用直线，不画 L 弯？
- [ ] **E6** **任何 90° 弯折都用 `rounded corners=5-8pt`** + **虚线 routing 强制 90° 直角，禁用 Bezier 曲线/对角线段**——sharp 90° 看起来粗糙廉价；非 90° 曲线/对角 routing 看起来乱。所有 dashed leader / residual skip / reference 引线**首选 90° L-bend with rounded corners**，不用 `to[bend left/right]` 或自由曲线。fig48 教训：sharp 90°；fig56 教训：dashed STE arc 曲线本可用 90°
- [ ] ⭐ **E7** **自由浮动的 annotation / callout / step number / 旁注文字 / 装饰点 都有 dotted/dashed leader 或同行 label 配对**？(a) 仅靠 y 对齐隐式关联**不算**——读者认知负担最大；(b) **legend dot / 色标圆点必须紧贴 label**（< 0.3cm 间距），**禁止孤立彩色圆点漂浮**（fig120 教训：4 个彩色圆点散布图中没 label，看上去是装饰失误）；(c) 自评 E7 写："N 个 annotation：M 个有 leader / K 个有同行 label / 0 处孤立 ✓"
- [ ] ⭐ **E8** **所有 leader / 虚线 / 引线必须有可见终点**（节点边、文字、箭头 tip 中至少一个）。没有终点的悬空虚线 = blocker
- [ ] ⭐ **E9** **箭头/连线必须用 canonical 模板**（深度调研 2026-05-18）——所有 `\draw[arrow]` / `\draw[arrow thick]` / `\draw[arrow thin]` / `\draw[residual]` 用 `tikz-template.tex` 预定义 styles，**禁止**手写 `-{Stealth[scale=X]}`。前 4 轮"按箭头长度选 scale"的方案被深度调研推翻 — TikZ 原生设计是 `length=⟨dim⟩ ⟨line_width_factor⟩` + `width'=⟨pt⟩ ⟨length_factor⟩` + `bending` library 让 tip **自动跟随 line width**。**自评 E9**：(1) `bending` library 是否加载？(2) 是否用 canonical `arrow/.style`？(3) line width 选档（0.6 / 1.0 / 1.6 pt）是否合理？三项都 Y 才过
- [ ] **E10** **长距离虚线/leader 路径不绕图大半圈**——同源同目标的虚线如果绕过 ≥3 个无关元素或转折 ≥3 次，读者难追踪。修复：(a) 缩短路径直连，(b) 与其它平行虚线归入同一"通道"（lane）相邻走，(c) 移动 source 或 target 减少绕路距离。fig36 教训：residual skip 紫虚线从 Linear Projection 绕半圈过 Stop Token + PostNet 上方再下到 ⊕ — 路径模糊读者迷路
- [ ] **E11** **路径视觉连续性**——所有 `\draw` 路径从起点到终点视觉上**无断点**。检查：(a) 多段 `\draw` 拼接段端点严格一致（用 named coordinate，不要手写浮点坐标），(b) 路径若被其它元素遮挡 → 用 pgfonlayer 把路径放上层 OR 移动遮挡元素，(c) 同一逻辑线**用单个 `\draw` 多段** `(A)--(mid)--(B)` 优于拆 2 个 `\draw`。fig57 教训：STARK 多段路径中间出现视觉断点
- [ ] ⭐ **E12** **线穿过节点几何检测**（2026-05-19 新加）——编译完后**必读** `pdf-overlap-checker.py --json`。category=`line-through-node` 是**候选**（矩阵/热力图/收敛节点/生物结构常误报）。Triage 规则：① **batch ignore 模式**（推荐用于已知误报场景）：当 ≥ 5 处候选源于同类已知误报（如 heatmap cells、DNA strand、neuron 收敛），写**一句批量声明**："N 处 line-through-node 均为 X 已知误报，批量 ignore" 即可，**禁止逐条 reasoning**；② **fix 类**（路径绕路穿过无关元素，如 fig80 apoptosis 穿调控盒）→ blocker，**每处单独写位置 + 修复策略**。**自评 E12**：(1) 跑了 `--json`？(2) ignore 用批量声明 OR fix 逐条？(3) 标 fix 全修？三项都 Y 才过
- [ ] ⭐ **E13** **短箭头形状 + rounded corners 规范**（2026-05-19 Batch 10 用户反馈）——① **箭身 < 1.5cm 的箭头必须用 `arrow short`**（tip 3pt + shorten <=0pt），不用 `arrow` / `arrow thick`；② **直线 `(A) -- (B)` 禁加 `rounded corners`**，[PGF 官方手册](https://tikz.dev/tikz-paths)证实短段加 rounded 会产生鬼影弧。`rounded corners` 只在 ≥2 段折线 `(A)--(corner)--(B)` 或 `(A) |- (B)` 用。**自评 E13 简化**：若图无 < 1.5cm 短箭头 → 一句 "无短箭头, N/A" 即过；若有 → 一句"所有短箭头均用 `arrow short`，所有 rounded corners 都在多段折线"即过（**不必报具体条数**）
- [ ] ⭐ **E14** **`|-` / `-|` L-bend 不穿 obstacle + residual rail 间距**（2026-05-19 Batch 10 用户反馈 fig97 hit；2026-05-20 Batch 11 用户反馈 fig108 ViT residual U-bend）——
  - **L-bend pierce 检查**：逐条扫所有 `\draw[arrow*]` 含 `|-` 或 `-|`：① `(A) |- (B.west/east)`：要求 A.x **不在** B 的 x 范围内；② `(A) -| (B.north/south)`：要求 A.y 不在 B 的 y 范围内。**违反则横/竖线段会穿过 B 的 body**——TikZ 不做 obstacle-aware routing。修复：用 named coordinate waypoint 绕开
  - **Residual rail 间距**：所有 `\draw[residual]` 的 rail（中段平行 lane）**必须距最近的 hero/box 边界 ≥ 0.5cm**——否则 residual 经"右出 0.8cm 再回头"造成视觉 U 型回路（fig108 教训：rail x=17.4 离 addnorm1.east x≈17.0 只 0.4cm 太挤）。修复：把 rail 进一步外移
  - 自评 E14：写"N 条 |-/-| L-bend：M 条满足投影不重叠 ✓；K 条 residual：rail-box 间距均 ≥ 0.5cm ✓"
- [ ] ⭐ **E15** **同一 anchor 不能被多条 incoming arrow 同时 tip** *（2026-05-21 fig137 v2 教训）*——
  - **判定**：grep figure.tex，如果同一个 `node.anchor`（如 `dec_ca.west`）作为 ≥2 条不同 `\draw[arrow]` 的**终点**出现 → blocker
  - **典型违规**：`\draw[arrow, purple] (dec_ca.west) -- (ca_q.east)` 和 `\draw[arrow, orange] ... -- (dec_ca.west)` 两条 incoming tip 都在 `dec_ca.west` → 视觉撞车（不同颜色不同方向的箭头在同一像素点重叠）
  - **修复**：(a) **换 anchor**——一条用 `.west` 一条用 `.north`/`.south`，让 tip 分开；(b) **加 anchor offset**——`[xshift=-2pt]dec_ca.west` vs `[xshift=+2pt]dec_ca.west`；(c) **改 routing**——把其中一条拉远绕到另一边
  - 自评 E15 写："N 个 box 有多条 incoming：每个 box 的 anchor/offset 列表 = ... / 0 处同 anchor 撞车 ✓"

## 维度 5：美学 / Aesthetic（5 项）

- [ ] **A1** 整图视觉平衡（左右两半权重相当，不头重脚轻）？
- [ ] **A2** 配色和谐（同类元素同色，强调色用得克制）？
- [ ] **A3** 同行/同层并列元素**等宽等高**？
- [ ] **A4** Zone 标签位置在 zone 视觉中心正上方且与其他 zone 标签**同 y**？
- [ ] **A5** **多个 legend 框间距 ≥1cm** *（无 legend 或单 legend 框直接 Y）*——并排的 legend 框如果间距 <1cm，视觉上像一个被分割的大框，读者不知道两个框是独立 legend 还是合并组。fig17 教训：legend 两框紧贴 → 应该合并成单框 OR 横向加 ≥1cm gap

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
| 2026-05-19 | R3-100 Batch 8 用户复审：箭头大幅改善后，剩"重叠 + 线穿过路径" — 自评清单逐项 Y 仍漏（fig80 apoptosis 红虚线穿 3 调控盒等） | E12 新增 ⭐（几何级 `pdf-overlap-checker.py --json` line-through-node 检测 + 人工 triage） |
| 2026-05-19 | R3-100 Batch 9 用户复审：fig86 等 4-5 张图分叉 stub 和 spine 之间有 1pt 视觉断裂 — `\draw[arrow]` 的 `shorten <=1pt` 在 stub 起点制造 gap | E3 强化 + tikz-template.tex 新加 `fan_stub/.style`（`shorten <=0pt`）；spine 中点禁放 `fill=white` 圆圈 |
| 2026-05-21 | R3-100 Batch 14 fig137 v2 用户复审：(a) Encoder 出来 2 条独立 `\draw[arrow]` 到 K/V，corner 处 rounded bulge 像 fork dot；(b) "Q" label 用 `fill=white + bfseries + 单字` 渲染像紫色方块；(c) 紫色 Q 和橙色 Attn-out 两条 incoming 都 tip 到 `dec_ca.west` 同一 anchor 撞车；(d) "Multitask Output" 标题离 spine 仅 0.3cm 边界值视觉太紧 | (a) E3 加"反绕过铁律"：多 \draw 共起点仍算 fan-out；(b) T7 加 fill=white 单字符 bfseries 警告；(c) **E15 新增**：同 anchor 多 incoming 不可同点；(d) T7 视觉默认从 0.3cm → 0.5cm |

新的用户终审发现的问题，按此格式追加 + 编入主清单。
