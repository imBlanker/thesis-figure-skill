# thesis-figure-skill — Evolution Roadmap

> **终极目标**：从"高保真复印 skeleton"进化为 **`style × structure` 可自由组合的学术绘图工坊**，同时支持用户把自己画的好图沉淀入库（self-growing library）。

## 当前状态（2026-05-22）

| Phase | 描述 | 状态 |
|---|---|---|
| 1 | 入口模式分流 + 沉淀通道 | ✅ 已实装（A 默认 + C 现有路径 + D 沉淀） |
| 2 | 风格轴（style preset）| 🚧 待启动 |
| 3 | 沉淀通道（D 模式 Φ）| ✅ 已和 Phase 1 一起实装 |
| 4 | Remix 模式（B）| 📅 计划中 |
| 5 | 原创模式（C 全栈实装）| 📅 部分已实装（Module-First 子流程），后续扩 vision-audit 多轮 GAN |

---

## 五阶段路线图

### Phase 1 ✅ — 入口分流 + 沉淀通道

**目标**：把 skill 从"单一路径"变成 4 模式分流。

**已完成**：
- SKILL.md 新增 `⓪.5 入口模式分流` section（在依赖检测后、画图指令前）
- 4 种路径定义清楚：A skeleton / B remix / C 原创 / D 沉淀
- 触发关键词表 + 判断优先级规则
- SKILL.md 新增 `Φ 沉淀通道` section（在 ⑦ 经验沉淀之后）
- Φ.1-Φ.7 完整流程文档：编译验证 → vision-audit → 分析 layout → 命名 → 生成 USAGE header → 写入库 → 提醒补 CONSTRAINTS

**模式实装状态**：
- **A**：默认路径，使用现有 6 个 skeleton (B/C/D/E/F/G) + CONSTRAINTS section
- **B**：stub，触发后回退到 A 并提示
- **C**：现有 Module-First 子流程 ③.A→③.D（已在 SKILL.md 中存在，本期挂入分流入口）
- **D**：完整流程已写入 SKILL.md "Φ 沉淀通道"

---

### Phase 2 🚧 — 风格轴（style preset）

**目标**：让用户在 `structure × style` 两个维度独立选择。

**4 个 preset**（学术语境）：

| Preset | 视觉特征 | 适合场景 |
|---|---|---|
| 1. **Academic Professional**（默认）| 当前 acaXxxLine 配色 / 软填充 / drop shadow / sans 圆角 | 主流期刊、conference paper |
| 2. **Brutalism / High Contrast** | 纯黑白 / 粗边 / 无 shadow / sans bold / 直角 | 强调结构 / 反"AI 美学"/ 安全/系统类 |
| 3. **Editorial / Magazine** | 单一 accent 色 / 大留白 / 不对称 / 大标题 | 综述论文 / 海报 / 重点突出 |
| 4. **Light Luxury** | 浅奢淡彩 / 细 hairline / 优雅 typography | 文科 / 跨学科 / 论文海报 |

**工程要求**：
- **重构现有 skeleton 用 token 而非硬编码色**：
  - 现状：`\definecolor{acaBlueLine}{HTML}{3B82F6}` 直接嵌在每个 skeleton
  - 目标：`\definecolor{primary_line}{HTML}{...}` 由 preset 定义，skeleton 只引用 token
  - Token 集（约 10 个）：`primary_line/fill`, `secondary_line/fill`, `accent_line/fill`, `hero_bg`, `zone_bg_{1..5}`, `bar_chart_palette`, `text_main/sub`
- **每个 preset 是一个 .tex snippet**：`references/style-presets/preset-{academic,brutalism,editorial,luxury}.tex`
- **sub-agent 在 ③ 选择 `style × structure` 后**：`\input{preset-X.tex}` + 用 skeleton

**风险**：
- 现有 6 个 skeleton 都需重构 → **单向门**（做了回不去）
- 必须保证重构后版面与原版一致，否则之前调好的 CONSTRAINTS 失效
- vision-audit 需要在每个 `style × structure` 组合都跑一次回归

**估计**：2-3 个 session

---

### Phase 3 ✅ — 沉淀通道（D 模式）

**目标**：用户画好的 .tex 自动入库为新 skeleton。

**已完成**（Phase 1 一起）：见 SKILL.md "Φ 沉淀通道" section。

**关键设计决策**：
- **Φ.5 自动生成 USAGE 但 CONSTRAINTS 留空 + TODO**：自动提取版面约束需要分析"哪些坐标改了会出 bug"，这是反向工程，自动化太难。让用户手工补，反正用户最了解自己踩过的坑。
- **命名约定**：`example-skeleton-{H..Z}-<topic>.tex`（字母递增，主题 kebab-case）
- **Φ.2 简化版 audit**：D 通道入库的图已经被用户视觉确认过，没必要再走完整 18 项 checklist，只跑关键 6 项（S1/S5/T1/M3/E5/V1）防明显事故。

---

### Phase 4 📅 — Remix 模式（B）

**目标**：用户能跨 skeleton 选模块拼装。

**方案**：
- 把每个 skeleton **拆成命名模块**：
  - D 的雷达 (`module-radar-5axis.tex`) / D 的客户端层 / D 的双图表
  - E 的多模态融合 hero / E 的 SHAP panel
  - F 的 phase chip + zone / F 的 party box
  - G 的 chart panel / G 的中心 hero / G 的多 city 并行
  - 等等...
- 用户多选 3-5 个模块
- sub-agent 在 canvas 上自动放置 + 接线
- vision-audit 验证

**前置依赖**：Phase 2 完成
- 没有 token 化，模块拼接时配色会冲突（D 的 acaPurpleLine vs F 的 acaPurpleLine 是不同 HEX）
- token 化后，所有模块用 `primary_line` / `accent` 等抽象名，preset 决定具体颜色

**风险**：
- 拼装路径多 (`6 模块 choose 3` = 20+ 种组合)，layout 冲突难预测
- 模块之间留白、对齐策略要建模

**估计**：2-3 个 session

---

### Phase 5 📅 — 原创模式（C）全栈实装

**目标**：从用户的自然语言描述生成全新 layout。

**现状**：现有 Module-First 子流程（③.A→③.D）已是 C 模式的雏形，但只是 sub-agent 自己生成 + 一次 vision-audit，没有 GAN-style 多 agent 协作。

**Phase 5 扩展**：
- **architect agent**：先设计 zone 布局（输出 ASCII 草图 + 坐标网格）
- **implementer agent**：从 architect 的 spec 写 TikZ
- **vision-auditor agent**：渲染后看 PNG，输出 blocker 列表
- **iteration controller**：根据 blocker 决定回 architect 还是 implementer
- 多轮迭代到 vision-auditor 0 blocker

**前置依赖**：
- Phase 2 完成（C 也要支持 style × structure，否则原创设计只能用默认配色）
- Phase 4 完成（remix 的模块库 architect 可以引用作为零件目录）

**风险**：
- 原创路径错误最难调试（不像 skeleton 有 ground-truth 版面对比）
- vision-audit 工具的准确率必须先提到 90%+，否则 GAN 收敛慢
- token 成本最高（多轮迭代 × 多 agent）

**估计**：3-4 个 session

---

## 设计决策记录

### 为什么 mode-based 而非单一智能默认？

- 不同用户场景诉求差异巨大（赶时间 vs 求原创 vs 想沉淀）
- 单一默认必然失败：Batch 16 教训——Philosophy First 让 sub-agent 默认套 examples 06 复杂风格，用户实际想要中等清晰图时变乱
- 显式 mode 让用户和 skill 都清楚生成边界

### 为什么 D 和 Phase 1 一起做，而 B 后做？

- **D 独立性最强**：不依赖 Phase 2 的 token 化（沉淀路径只读 .tex 不改色）
- **D 杠杆比最高**：用户花 10 分钟入库一个 skeleton，未来 N 个 session 受益
- **D 实装成本低**：~80 行 SKILL.md 文档 + 一次 Phase 1 编辑搞定
- **B 依赖 Phase 2**：模块拼接时颜色冲突需要 token 化解决，否则做出来视觉灾难

### 为什么 C 现在已经"算实装"，但放 Phase 5？

- Module-First 子流程已存在并稳定运行
- 但它只是 sub-agent 自己一轮 audit，还不是真正的 GAN-style 多 agent 协作
- Phase 5 是把 C 扩到"成熟 GAN 工作流"层级

### Style preset 为什么只选 4 个？

- 学术语境下覆盖面足够：professional / 反 AI 美学 / 文艺综述 / 优雅
- 不做 dark theme（学术正文不匹配）
- 不做 retro-futurism / sketch / brutalism 扩展变体（非学术）
- 4 个足以验证 `style × structure` 笛卡尔积是否成立；如果用户跑下来发现需要更多，再扩

---

## 不做的事（明确反范围）

- ❌ dark theme 默认（学术正文不匹配）
- ❌ Python/matplotlib 替代 TikZ（用户已明确禁止）
- ❌ SVG / HTML / Canvas 输出（无法嵌入论文）
- ❌ Phase 1 同时做 token 化（避免一次改太多，留给 Phase 2）
- ❌ 自动提取 CONSTRAINTS 写入新 skeleton（Φ.5 留空 + 让用户手工补，自动反向工程太难）

---

## 未来可能方向（不在当前 5 阶段内）

- LaTeX 风格之外：Beamer / 学术海报
- 自动生成 ASCII art 版本（用于 README / markdown 文档）
- 多语言支持（日文 / 韩文 / 阿拉伯文）
- 集成 IDE 插件（VSCode / JetBrains）
- 多人协作沉淀（团队级 skeleton 库 + 标签 / 分类）

---

## 版本历史

| 日期 | 事件 |
|---|---|
| 2026-05-22 | Phase 1 实装完成（⓪.5 入口分流 + Φ 沉淀通道），ROADMAP.md 初版 |
| 2026-05-22 之前 | 6 个 skeleton (B-G) + 4 个 skeleton 的 CONSTRAINTS 文档（D/E/F/G）完成；batch47 验证 CONSTRAINTS 文档生效 |
