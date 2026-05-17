# Day Composer — Frontend Spec v2

> 受众：Mia（设计 + 工程，单人 hackathon）
> 状态：**POC 实现蓝图**，可直接用于 1–2 天开发
> 参考文档：`prd-v2-day-composer.md`、`backend-data-schema-v2.md`
> 前端消费的数据：`TripPlan` JSON（backend schema §2.9）
> 美学基准：Aman Resorts editorial cinematic

---

## Section 1: The Final User-Facing Artifact

这是最重要的一节。读完应该能在脑子里"看到"产品。

### 1.1 总体结构概述

用户最终看到的是一个**单页、全屏、可垂直滚动的 Day Composition 展示页**。不是 dashboard，不是表格，不是 app shell——是一份**可以截图发给朋友的美丽文档**，同时是可以交互的 live URL。

类比：Black Tomato 的手工行程 PDF，但是活的、可 refine 的、带动画的。

四个主要区块，从上到下：

```
Hero Section          — 全屏沉浸，Day Theme + Mood，慢淡入
Emotional Arc         — 视觉化曲线，展示一天的能量走向
Experience Cards      — 每个 stop 一张大卡，全宽或双列，带过渡说明
Adaptive Branches     — 底部，条件分支，低调排版，不像流程图
```

底部固定：`RefineBar`（"更安静 / 加一个酒吧" 输入条）

---

### 1.2 桌面端 ASCII 线框（Desktop, ≥1280px）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ [HERO SECTION]  — 100vh, full-bleed                                     │
│                                                                         │
│                                                                         │
│    旧湾区与恢复感的一天                         ← day_theme (serif h1) │
│                                                                         │
│    reflective  ·  warm  ·  lightly exploratory  ·  not rushed          │
│                    ← mood_tags (small caps, tracked wide)              │
│                                                                         │
│    周六 14:30 → 22:00  ·  Sunnyvale 出发  ·  🚗 car + baby             │
│                    ← trip_context summary (mono caption)               │
│                                                                         │
│    [↓ scroll to compose]                  ← animated scroll cue       │
│                                                                         │
│  ░░░░░░░░░░░░░░░░░░░░░░░ (vibe image, full-bleed, darkened 40%) ░░░░  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ [EMOTIONAL ARC SECTION]  — ~60vh, cream background                     │
│                                                                         │
│  The shape of your day                     ← section label (sans, xs) │
│                                                                         │
│   low ╭────────╮         ╭──────────────╮  high                       │
│       │        ╰────────╯              ╰─────╮                        │
│  ─────┤                                      ╰────────  ─────         │
│  14:30 │  opening  │ breathing │  peak   │  closing                   │
│        ↑           ↑           ↑          ↑                           │
│    Alviso     Sandy Wool   Dong Que   Spaced Out                       │
│    Adobe      Lake         Restaurant  Comedy                          │
│                    ← emotional_arc[].label + vibe_curve_value SVG     │
│                                                                         │
│  Arc labels below curve, dot per stop, CatmullRom smooth              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ [EXPERIENCE CARDS — Stop 1]  — ~90vh, full-bleed image left            │
│                                                                         │
│  ┌─────────────────────────┐  ┌────────────────────────────────────┐  │
│  │                         │  │  14:30                              │  │
│  │                         │  │  A quiet historical opening    ← title │
│  │   [hero_image_url]      │  │                                    │  │
│  │                         │  │  今天想 restore，又不想完全静止；   │  │
│  │   60% width             │  │  adobe 比 museum 轻盈，宝宝好带。  │  │
│  │                         │  │  ← why_fits_today                  │  │
│  │                         │  │                                    │  │
│  │                         │  │  🚗 8min  🅿️ easy  👶 friendly      │  │
│  │                         │  │  ← logistics_inline                │  │
│  │                         │  │                                    │  │
│  │                         │  │  [Book tour →]  ← booking_url     │  │
│  │                         │  │                                    │  │
│  │                         │  │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │  │
│  │                         │  │  indoor narrative → outdoor        │  │
│  │                         │  │  breathing                         │  │
│  │                         │  │  ← transition_to_next (caption)    │  │
│  └─────────────────────────┘  └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ [EXPERIENCE CARDS — Stop 2]  — layout flips: image right               │
│  (alternating left/right image keeps eye engaged, Aman pattern)        │
│                                                                         │
│  ┌────────────────────────────────────┐  ┌─────────────────────────┐  │
│  │  15:00                              │  │                         │  │
│  │  Lakeside breathing            ← title  │   [hero_image_url]   │  │
│  │                                    │  │   Sandy Wool Lake       │  │
│  │  why_fits_today copy               │  │                         │  │
│  │                                    │  │                         │  │
│  │  🚗 already here  👶 stroller ok   │  │                         │  │
│  │                                    │  │                         │  │
│  │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │  │                         │  │
│  │  outdoor reset → appetite-opening  │  │                         │  │
│  └────────────────────────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ [EXPERIENCE CARD — Stop 3, Restaurant]  — full-bleed treatment         │
│                                                                         │
│  ░░░░░░░░░░░░░░░░ dark overlay on full-width image ░░░░░░░░░░░░░░░░░  │
│  ░░  18:30                                                         ░░  │
│  ░░  Lively neighborhood dinner           ← stop.title (white serif) ░░│
│  ░░  你说不想 touristy；walk-in only 本地客。  ← why_fits_today    ░░  │
│  ░░                                                                 ░░  │
│  ░░  ┌──────────────────────────────────┐                          ░░  │
│  ░░  │ Dish recommendations             │  ← collapsed by default  ░░  │
│  ░░  │  #15 香松腊肠锅巴饭  · 先点     │                          ░░  │
│  ░░  │  #88 烤生蚝         · 开胃      │                          ░░  │
│  ░░  │  #92 鱼籽扇贝       · 主菜      │                          ░░  │
│  ░░  │  #103 铁板螺丝      · 收尾      │                          ░░  │
│  ░░  │  ordering_logic copy             │                          ░░  │
│  ░░  └──────────────────────────────────┘                          ░░  │
│  ░░                                                                 ░░  │
│  ░░  warm fullness → social light closing  ← transition             ░░  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ [ADAPTIVE BRANCHES]  — ~40vh, warm off-white background                │
│                                                                         │
│  If things shift...              ← section label                       │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │  宝宝困了 / 状态不好                                           │    │
│  │  → skip comedy, 去附近 dessert                ← condition + alt│    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │  如果 energy 更高                                              │    │
│  │  → 加 downtown wine bar                                        │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ [REFINE BAR]  — sticky bottom, always visible                          │
│                                                                         │
│  [🎵 更安静一点 ·  加一个酒吧 ·  宝宝今天很累]  [→ Recompose]         │
│  ← chip suggestions + freetext input + submit button                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 1.3 移动端 ASCII 线框（Mobile, ≤430px）

```
┌───────────────────────────────────────┐
│ [HERO SECTION]  — 100svh              │
│                                       │
│                                       │
│  旧湾区与恢复感的一天                 │
│  ← serif h2, 2-line wrap ok          │
│                                       │
│  reflective · warm                    │
│  not rushed  ← 2 rows of mood_tags   │
│                                       │
│  周六 · Sunnyvale · 🚗 + 👶           │
│  ← condensed trip summary            │
│                                       │
│  [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   │
│  [░ full-bleed image behind text  ░]  │
│  [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   │
│                                       │
│        ↓                              │
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│ [EMOTIONAL ARC]  — ~50vh              │
│                                       │
│  The shape of your day                │
│                                       │
│  ╭───╮     ╭──────╮                  │
│  │   ╰─────╯      ╰──╮              │
│  ─                    ╰──            │
│  14:30     16:00  18:30  20:00       │
│                                       │
│  (dot labels: place names, small)     │
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│ [EXPERIENCE CARD — Stop 1]            │
│                                       │
│  ┌───────────────────────────────┐   │
│  │                               │   │
│  │   [hero_image_url]            │   │
│  │   100% width, 200px height    │   │
│  └───────────────────────────────┘   │
│                                       │
│  14:30                                │
│  A quiet historical opening           │
│                                       │
│  why_fits_today copy...               │
│                                       │
│  🚗 8min  🅿️ easy  👶 ok             │
│                                       │
│  [Book tour]                          │
│                                       │
│  ── indoor narrative →                │
│     outdoor breathing ──             │
│     ← transition note, centered      │
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│ [EXPERIENCE CARD — Stop 3, Restaurant]│
│                                       │
│  [full-bleed image 100% width]        │
│                                       │
│  18:30                                │
│  Lively neighborhood dinner           │
│  why_fits_today...                    │
│                                       │
│  [▸ What to order]  ← accordion      │
│  ┌───────────────────────────────┐   │
│  │ #15 · 香松腊肠锅巴饭 · 先点   │   │
│  │ #88 · 烤生蚝 · 开胃          │   │
│  │ ordering_logic                │   │
│  └───────────────────────────────┘   │
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│ [ADAPTIVE BRANCHES]                   │
│                                       │
│  If things shift...                   │
│                                       │
│  ┌───────────────────────────────┐   │
│  │ 宝宝困了                      │   │
│  │ → 去附近 dessert              │   │
│  └───────────────────────────────┘   │
│                                       │
│  ┌───────────────────────────────┐   │
│  │ Energy 更高                   │   │
│  │ → downtown wine bar           │   │
│  └───────────────────────────────┘   │
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│ [REFINE BAR]  — sticky bottom, 64px   │
│                                       │
│  [更安静] [加酒吧]  [输入...] [→]     │
└───────────────────────────────────────┘
```

---

### 1.4 逐区块详解

#### Hero Section

**目的**: 在用户看到任何具体 stop 之前，先让他们感受到"这一天的整体感"——主题 + 情绪基调 + 一张 vibe 图。

**内容字段**:

| 视觉元素 | JSON 字段 | 备注 |
|---|---|---|
| 主标题 | `TripPlan.day_theme` | 中文叙事锚，如"旧湾区与恢复感的一天" |
| Mood 标签行 | `TripPlan.mood_tags[]` | 枚举值：reflective · warm · lightly_exploratory · not_rushed；点号分隔，小型大写 |
| 行程摘要行 | `ExperienceRequest.trip_context` | 日期 + 出发地 + companions emoji 组合 |
| 背景图 | `TripPlan.stops[0].image_url` 或 `TasteSignature.liked_examples[0].image_url` | 取第一张 stop 的图；fallback 到 taste 样本图 |

**视觉处理**:

- 背景图：100vh，`object-fit: cover`，黑色渐变叠加（顶部 0% → 底部 55% opacity），让白色文字在任何图片上都可读
- `day_theme`：编辑体衬线字体，desktop h1 约 64–80px，mobile h2 约 40px，font-weight 300 或 400（light editorial，不是粗体）
- `mood_tags`：全大写，tracking 0.15em，12–13px，白色 70% opacity，点号分隔
- 行程摘要行：monospace 字体，11–12px，white 50% opacity

**动画**:

- 进入时：整个 hero 内容 `opacity: 0 → 1`，duration 1.2s，easing `cubic-bezier(0.16, 1, 0.3, 1)`（expo ease-out）
- `day_theme` 最先出现，delay 0.2s
- `mood_tags` 每个 tag 依次淡入，stagger 0.08s，delay 0.6s 后开始
- 背景图：平行的从 `scale(1.03) → scale(1)` Ken Burns 效果，duration 2.5s，让画面感觉"呼吸"

---

#### Emotional Arc Section

**目的**: 让用户在看具体地点之前，先理解"这一天的能量走向"——这是 Day Composer 区别于普通行程表的核心 UI。

**内容字段**:

| 视觉元素 | JSON 字段 |
|---|---|
| 曲线节点 | `TripPlan.emotional_arc[]`，每个 item 的 `vibe_curve_value`（0–1）作为 Y 轴 |
| 节点标签（上方） | `emotional_arc[i].label`：如"slow opening"、"lively dinner" |
| 节点标签（下方） | `stops[i].place_id` 对应的地点名 |
| X 轴时间标记 | `stops[i].time`（HH:MM） |

**视觉处理**:

- SVG 宽度：100%，高度约 120px（desktop）/ 80px（mobile）
- 曲线：`d3-shape` 的 `curveCatmullRom` alpha=0.5，平滑连接各节点
- 线条：2px，`#8B7355`（暖棕）或 `--color-accent`
- 节点：4px 实心圆，hover 放大到 6px
- 背景：`--color-cream`（#F7F3EC），无网格线，极简
- X 轴：无刻度线，只有时间文字，12px mono，`--color-stone`

**动画**:

- ScrollTrigger 触发（GSAP）：当 section 进入视口 30% 时触发
- framer-motion `pathLength` draw-in：曲线从左到右画出，duration 1.8s，easing `easeInOut`
- 节点：在曲线画到对应 X 位置时，`scale: 0 → 1` 弹出，每个 stagger 根据节点 X 位置自动计算

---

#### Experience Cards

**目的**: 每个 stop 一张卡，是整个页面花时间最多的部分。必须同时承载"美学感染力"和"实用信息"，二者不可互相伤害。

**内容字段（per stop）**:

| 视觉元素 | JSON 字段 |
|---|---|
| 大图 | `Stop.image_url`（fallback: `PlaceCandidate.hero_image_url`） |
| 时间戳 | `Stop.time` |
| 标题 | `Stop.title` |
| 推荐理由 | `Stop.why_fits_today`（正文，最重要的文字） |
| Logistics 图标行 | `Stop.logistics_inline.drive_minutes_from_prev` + `parking` + `kid_friendly` |
| 私货提示 | `Stop.optional_tip`（若存在则显示，斜体小字） |
| 过渡说明 | `Stop.transition_to_next`（连接下一张的过渡语） |
| 预订链接 | `PlaceCandidate.booking_url`（若有） |

**餐厅专属**（`place_type === 'restaurant'`）:

| 视觉元素 | JSON 字段 |
|---|---|
| 菜品列表 | `TripPlan.dish_recommendations[].dishes[]`（`name`、`menu_number`、`dish_role`、`note`） |
| 点单逻辑 | `dish_recommendations[].ordering_logic` |

**视觉处理**:

- Desktop：左右交替布局（奇数 stop 图片在左，偶数在右），60/40 分割，`min-height: 85vh`
- Mobile：图片在上（约 220px 高），文字在下，全宽
- 餐厅 stop：图片全宽 + 深色叠加，文字和菜单浮在图上（更戏剧性，匹配用餐仪式感）
- `why_fits_today`：这是核心文案，字号不能太小——desktop 18–20px，mobile 16px，`leading-relaxed`
- Logistics 行：小 badge/pill 样式，图标 + 文字，背景 `--color-cream`，圆角 4px，文字 12px
- `optional_tip`：斜体，`--color-stone`，12px，加一个竖线分隔或短横线前缀

**菜单区块设计**（重要）:

- 默认**展开**（PRD 的"killer moment"是细节）
- 列表行：`#15  香松腊肠锅巴饭  ·  先点`，menu_number 用 monospace，dish_role 用小 badge（"签到"、"开胃"、"主菜"、"收尾"）
- 末尾追加 `ordering_logic` 段落，稍大字号，做"点单白话文"的总结
- Mobile 上可以 accordion 折叠（`▸ What to order`），节省屏幕高度

**动画**:

- 每张卡用 Lenis 滚动 + GSAP ScrollTrigger：进入视口时，图片 `translateY(20px) → 0`，opacity `0 → 1`，duration 0.9s
- 文字侧用 framer-motion：`y: 30 → 0`，`opacity: 0 → 1`，stagger 0.1s（时间戳 → 标题 → 正文 → logistics → tip）
- 过渡说明（`transition_to_next`）：在两张卡之间渲染，居中，`opacity: 0 → 1`，ScrollTrigger 在上一张卡 80% 离屏时触发

---

#### Adaptive Branches Section

**目的**: 告诉用户"如果情况不对，这个计划怎么弯"。这是 Day Composer 最体现智能感的细节之一，但视觉上必须低调——Aman 绝不会在手册里画流程图。

**内容字段**:

| 视觉元素 | JSON 字段 |
|---|---|
| 触发条件 | `AdaptiveBranch.condition` |
| 替代方案 | `AdaptiveBranch.alternative` |
| 相关 stop | `AdaptiveBranch.branch_at_stop_index` → 对应 `stops[i].title` |

**视觉处理**:

- 区块标题："If things shift..." 或"如果这一天改变了方向"，小号 serif，居左
- 每个 branch：单行横向卡片，左侧条件（轻量 sans），右侧箭头 `→`，右侧替代方案
- 背景：微暖白（`#FAF8F5`），不加边框，只用左侧 2px 细线（`--color-accent`）作标注
- 不使用流程图、不使用节点、不使用连线——纯排版
- 多个 branch：垂直堆叠，间距 16px，不做 accordion

**动画**:

- ScrollTrigger：每个 branch card 依次淡入 + 向上 10px 平移，stagger 0.15s

---

#### Refine Bar（Sticky Bottom）

**目的**: 让用户在读完整个 plan 后，能立即"调音"，而不是回到另一个界面。

**内容**:

- 左侧：3–4 个快捷 chip（基于 `AdaptiveBranch.condition` + 常见修改语，如"更安静"、"加一个酒吧"、"宝宝状态不好"）
- 中间：自由文本输入框，placeholder "调整这一天..."
- 右侧：提交按钮"→ Recompose"

**视觉处理**:

- 高度 64px（desktop）/ 56px（mobile）
- 背景：`--color-charcoal`（深炭灰），白色文字，轻微 backdrop blur
- Chip：2px border，hover 时 fill，font-size 12px
- 键盘弹出时（mobile）：bar 随键盘上移（`env(safe-area-inset-bottom)` 处理）
- 不遮挡关键内容：最后一张卡有 `padding-bottom: 80px`

**交互**:

- 用户选 chip 或输入文字后，点 "→ Recompose"
- 提交后：整个页面内容区 fade out（opacity 0.3），显示 loading state
- Loading 完成：新 `TripPlan` JSON 注入，页面平滑 animate-in（不是整页刷新）

---

### 1.5 Loading State（这是 demo 的高光时刻）

90 秒 demo 里，5–15 秒的 LLM 等待必须感觉**有意义**，而不是"等 AI 慢"。

**Loading 设计**:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                                                         │
│     Composing your day                                  │
│     ← serif, 32px, slow fade pulse                      │
│                                                         │
│     Reading your taste...  ✓                           │
│     Finding the right opening...  ✓                    │
│     Tuning the evening arc...  ▋                       │
│     ← progressive checklist, each step fades in 1s apart│
│                                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

- 全页 cream 背景，无 spinner——spinner 感觉像工具，不像 Aman
- 文字描述 agent 在做什么的步骤（fake streaming 也行——从固定文案里依次显示）
- 步骤完成时打 ✓，下一步开始时有 ▋ cursor 闪烁
- 可以叠加极轻的 CSS gradient animation（暖光扫描）作为背景动效

**Refine loading**（重新 compose 时）:

- 不全页覆盖，而是 existing plan 内容 blur + 50% opacity
- "Recomposing..." 小字出现在 RefineBar 附近
- 新内容 ready 后：fade-in 替换

---

### 1.6 Empty State（截图上传前）

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   [上传区域，虚线边框，中心]                            │
│                                                         │
│   Drop your saved vibes here                           │
│   ← serif 24px                                         │
│                                                         │
│   Screenshots, photos, anything that shows             │
│   how a good day feels to you                          │
│   ← body 16px, stone color                             │
│                                                         │
│   [Choose files]  ← 唯一 CTA                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

上传后显示 thumbnail grid（3列），每张图下方显示 LLM 提取的 vibe tags（实时或 batch 完成后）。

---

### 1.7 Typography Spec

**字体对**：Fraunces (serif) + Inter (sans)

理由：Fraunces 是 Google Font，开源，variable font，有"光学调整"功能（字重低时 serif ball terminals 特别美），是 Tiempos Headline 最接近的开源平替，完全 free for commercial use。Inter 是最成熟的屏幕 sans，hackathon 阶段 Geist 也可以。

| 用途 | 字体 | 大小（desktop/mobile） | Weight | Letter-spacing |
|---|---|---|---|---|
| Hero 主标题（`day_theme`） | Fraunces | 72px / 40px | 300 | -0.02em |
| Section 标题（"The shape of your day"） | Fraunces | 32px / 24px | 400 | -0.01em |
| Card 标题（`stop.title`） | Fraunces | 28px / 22px | 400 | -0.01em |
| 正文（`why_fits_today`） | Inter | 18px / 16px | 400 | normal |
| Mood tags | Inter | 12px / 11px | 500 | 0.12em，uppercase |
| Caption（时间、logistics） | Inter Mono 或 JetBrains Mono | 12px / 11px | 400 | 0.05em |
| Dish 列表 | Inter | 14px / 14px | 400 | normal |
| Menu number | JetBrains Mono | 13px / 13px | 500 | 0.02em |

Line-height intent:
- 标题：`leading-tight`（1.1–1.2）
- 正文：`leading-relaxed`（1.6–1.7）
- Caption：`leading-none`（1.0）

---

### 1.8 Color Palette

基准：Aman 用暖象牙、深棕、肤色调 taupe，绝不用纯黑或纯白。参考 aman.com 截图的色调。

| 角色 | 色名 | Hex | 用途 + 氛围 |
|---|---|---|---|
| `--color-cream` | Parchment | `#F7F3EC` | 主背景。温暖书页感，不刺眼，与图片无缝衔接 |
| `--color-charcoal` | Deep Espresso | `#1C1814` | 深色文字 + RefineBar 背景。不是纯黑，带棕调 |
| `--color-stone` | Warm Stone | `#8B7D6B` | 次要文字（caption、mood tags）、分隔线 |
| `--color-accent` | Aged Copper | `#8B7355` | 曲线颜色、左侧 branch 细线、hover state |
| `--color-sand` | Desert Sand | `#D4C4A8` | Card logistics badge 背景、chip 边框 |
| `--color-white-warm` | Off White | `#FEFCF8` | 浮层、modal、dish 卡片背景 |

只用这 6 色。不引入蓝色、绿色或任何高饱和色——Day Composer 的美学是"褪色照片里的金色时刻"。

---

### 1.9 Animation Timing：Aman Slow 的具体数字

Aman 的感觉来自：**让内容晚 0.3–0.5 秒才开始动，然后用超过 0.8s 完成动画**。所有人类眼睛都会感到"这个人不着急"。

| 动画 | Duration | Easing | 备注 |
|---|---|---|---|
| Hero fade-in | 1.2s | `cubic-bezier(0.16, 1, 0.3, 1)` | expo ease-out，快进慢出 |
| Hero background Ken Burns | 2.5s | `linear` | 视差感 |
| Mood tags stagger | 0.08s per tag | 同上 | 从第 0.6s 开始 |
| Arc draw-in (pathLength) | 1.8s | `easeInOut` | framer-motion |
| Arc node pop-in | 0.3s per node | `spring(stiffness: 300, damping: 20)` | 弹性 |
| Card image slide-in | 0.9s | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | GSAP ScrollTrigger |
| Card text stagger | 0.1s per element | `cubic-bezier(0.16, 1, 0.3, 1)` | framer-motion |
| Branch card fade-in | 0.6s + 0.15s stagger | `easeOut` | |
| Page-level transitions | ≥ 0.8s | `easeInOut` | 不用 instant |

Lenis 参数建议：`lerp: 0.06`（默认 0.1 偏快，降低让滚动更粘稠），`smoothWheel: true`。

**ScrollTrigger 触发点**：`start: "top 75%"`（当元素顶部进入视口 75% 时触发），不用 `top bottom`（太早），不用 `top 30%`（太晚）。

---

### 1.10 Interaction Patterns（设计决策）

**Refine 方式**（见 Section 3 详细权衡，此处是结论）：

推荐：**Sticky Bottom Chip Bar + 自由输入**（见 1.4 RefineBar 设计）。芯片来自 `adaptive_branches[].condition` + 3 个预设（"更安静"、"加一个活动"、"时间太赶"）。用户点击 chip 后输入框自动 populate，可以追加文字，然后提交。不做 modal，不做 sidebar chat——这些都会打断沉浸感。

**Artifact 形态**：Live interactive URL（主要）+ 截图/分享（次要）。具体：每个 compose 产生的 plan 有一个 `?plan=<id>` URL，可以直接分享。不做 server-rendered PNG（hackathon 阶段工作量不合算）。

**分享**：`navigator.share()` API（mobile）+ 复制链接按钮（desktop）。Share card 用 `<meta og:image>` 指向 hero stop 的图片，`og:title` 用 `day_theme`，`og:description` 用 mood tags 拼接。

---

## Section 2: Component-Level Spec

### 2.1 Component Tree

```
<PlanPage>
├── <HeroSection>
├── <EmotionalArc>
├── <ExperienceCardList>
│   └── <ExperienceCard>  (×N stops)
│       ├── <StopImage>
│       ├── <StopContent>
│       │   ├── <StopMeta>     (time, logistics badges)
│       │   ├── <WhyFitsToday>
│       │   ├── <DishPanel>    (restaurants only)
│       │   └── <OptionalTip>
│       └── <TransitionNote>   (between cards)
├── <AdaptiveBranches>
│   └── <BranchCard>  (×N branches)
├── <RefineBar>      (sticky bottom)
└── <LoadingOverlay> (covers PlanPage during compose)

Parallel:
<IntakePage>         (before compose — separate route)
├── <VibeUploader>
├── <IntakeChat>
└── <ComposeCTA>
```

---

### 2.2 Props TypeScript Signatures

基于 `TripPlan` schema（`backend-data-schema-v2.md` §2.9）：

```typescript
// Vocabulary types (from §2.0)
type MoodTag = 'reflective' | 'restorative' | 'celebratory' | 'lightly_exploratory'
  | 'deeply_exploratory' | 'warm' | 'intimate' | 'social' | 'playful'
  | 'not_rushed' | 'energizing' | 'grounding'

type PacingRole = 'opening' | 'breathing' | 'peak' | 'recovery' | 'closing'

// Arc beat
interface ArcBeat {
  label: string           // e.g. "slow opening"
  pacing_role: PacingRole
  vibe_curve_value: number | null  // 0–1, Y-axis position
}

// Stop logistics inline
interface LogisticsInline {
  drive_minutes_from_prev: number | null
  parking: 'easy' | 'moderate' | 'hard' | 'none' | null
  kid_friendly: boolean | null
}

// Stop
interface Stop {
  place_id: string
  event_id: string | null
  time: string            // "HH:MM"
  duration_minutes: number | null
  title: string | null
  why_fits_today: string
  transition_to_next: string | null
  optional_tip: string | null
  image_url: string | null
  logistics_inline: LogisticsInline
}

// Dish
interface Dish {
  name: string
  menu_number: string | null
  dish_role: 'appetizer' | 'small_plate' | 'main' | 'side' | 'rice_noodle'
    | 'dessert' | 'drink' | 'signature' | null
  note: string | null
}

// Dish recommendation
interface DishRecommendation {
  place_id: string
  dishes: Dish[]
  ordering_logic: string
}

// Adaptive branch
interface AdaptiveBranch {
  branch_at_stop_index: number | null
  condition: string
  alternative: string
  alternative_place_id: string | null
  alternative_event_id: string | null
}

// Top-level TripPlan
interface TripPlan {
  composition_id: string | null
  day_theme: string
  mood_tags: MoodTag[]
  emotional_arc: ArcBeat[]
  stops: Stop[]
  transitions: Transition[]
  dish_recommendations: DishRecommendation[]
  adaptive_branches: AdaptiveBranch[]
  source_template_id: string | null
}

// Transition (inline in TripPlan)
interface Transition {
  from_place_id: string
  to_place_id: string
  drive_minutes: number
  walk_minutes: number | null
  transit_minutes: number | null
  transition_reason: string
  arc_shift: string | null    // "opening→breathing"
  energy_delta: 'down' | 'flat' | 'up' | null
}
```

**Component props**:

```typescript
// <PlanPage>
interface PlanPageProps {
  plan: TripPlan
  onRefine: (instruction: string) => Promise<TripPlan>
  isRefining: boolean
}

// <HeroSection>
interface HeroSectionProps {
  dayTheme: string                // plan.day_theme
  moodTags: MoodTag[]            // plan.mood_tags
  heroImageUrl: string | null    // plan.stops[0].image_url
  tripSummary: string            // formatted from ExperienceRequest context
}

// <EmotionalArc>
interface EmotionalArcProps {
  arc: ArcBeat[]                 // plan.emotional_arc
  stops: Pick<Stop, 'time' | 'title'>[]
}

// <ExperienceCard>
interface ExperienceCardProps {
  stop: Stop
  index: number                  // for alternating layout
  dishRec: DishRecommendation | null  // null if not restaurant
  transitionToNext: Transition | null
}

// <DishPanel>
interface DishPanelProps {
  dishes: Dish[]
  orderingLogic: string
  isMenuNumbered: boolean        // from Place.restaurant.menu_numbered
}

// <AdaptiveBranches>
interface AdaptiveBranchesProps {
  branches: AdaptiveBranch[]
  stops: Pick<Stop, 'title'>[]  // to look up branch_at_stop_index
}

// <BranchCard>
interface BranchCardProps {
  branch: AdaptiveBranch
  relatedStopTitle: string | null
}

// <RefineBar>
interface RefineBarProps {
  suggestedChips: string[]      // from adaptive_branches + presets
  onSubmit: (instruction: string) => void
  isLoading: boolean
}

// <LoadingOverlay>
interface LoadingOverlayProps {
  phase: 'initial' | 'refine'
  steps?: string[]
}
```

---

### 2.3 satus 上的文件结构

在 `darkroomengineering/satus` starter 基础上，**不修改 satus 自身结构**，只在约定路径下新增：

```
app/
  compose/
    page.tsx              ← IntakePage（上传 + 问答）
  plan/
    [id]/
      page.tsx            ← PlanPage（SSR，接收 plan JSON）
  api/
    compose/
      route.ts            ← POST，调用 OpenClaw，返回 TripPlan
    refine/
      route.ts            ← POST，接收 instruction + plan_id，返回新 TripPlan

components/
  plan/
    hero-section.tsx
    emotional-arc.tsx     ← SVG + framer-motion pathLength
    experience-card.tsx
    stop-image.tsx
    stop-content.tsx
    dish-panel.tsx
    transition-note.tsx
    adaptive-branches.tsx
    branch-card.tsx
    refine-bar.tsx
    loading-overlay.tsx
  intake/
    vibe-uploader.tsx
    intake-chat.tsx
    compose-cta.tsx

lib/
  types/
    trip-plan.ts          ← TypeScript interfaces（上方 §2.2）
    vocab.ts              ← Enum types
  hooks/
    use-plan-compose.ts   ← composing state + refine mutation
    use-lenis.ts          ← already in satus, extend if needed
  utils/
    arc-path.ts           ← d3-shape CatmullRom path generator
    format-logistics.ts   ← drive_minutes → "🚗 8min" etc.
    dish-role-label.ts    ← "rice_noodle" → "签到" etc.
  data/
    places.json           ← 手工 curate 的 30–50 个湾区地点（POC）

public/
  fonts/
    Fraunces/             ← variable font files
```

---

### 2.4 动画系统分工（Lenis vs GSAP vs framer-motion）

三个系统各司其职，不交叉：

| 系统 | 职责 | 具体用途 |
|---|---|---|
| **Lenis** | 平滑滚动容器 | 所有页面的 scroll 物理感。`lerp: 0.06`，不改其他，让 GSAP ScrollTrigger 监听 Lenis 的 scroll event |
| **GSAP + ScrollTrigger** | Scroll-linked 动画 | 图片进入视口触发的 slide-in（translateY + opacity）；emotional arc 画线触发 |
| **framer-motion** | 组件状态动画 | SVG `pathLength` draw-in；hero 文字淡入 stagger；page-level loading fade；branch card 逐个出现；任何"状态切换"动画（loading ↔ content） |

**规则**：凡是"跟着 scroll 走的动画"用 GSAP；凡是"组件 mount/unmount 或状态改变的动画"用 framer-motion；凡是"鼠标滚轮的手感"用 Lenis。三者不互相接管对方的职责。

Lenis + GSAP 连接方式（satus starter 已有，直接用）：
```
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))
```

---

## Section 3: Open Design Decisions

### 决策 1：Mobile-First vs Desktop-First（Hackathon demo 优先级）

**问题**: 90 秒 demo 是在笔记本上投影还是手机上分享给朋友看？

**选项 A（Desktop-first）**: 左右交替卡片布局，全屏 hero，emotional arc 横向展开。Demo 体验极佳，5 分钟能做出让人惊叹的视觉。Mobile 响应式留到 demo 后再做。

**选项 B（Mobile-first）**: 全部单列，竖向卡片，适合截图分享给朋友。Demo 在手机上展示更"真实用户场景"，但桌面投影时画面显窄，可能减弱冲击力。

**选项 C（两者）**: 做 responsive——当然最好，但 hackathon 1–2 天的真实工时有限。

**推荐：A（Desktop-first）。** 理由：hackathon demo 几乎一定是对着笔记本/屏幕展示，视觉冲击力在那个场景里决定胜负。Mobile responsive 可以在 demo 后 1 小时内用 Tailwind 断点补全——基础 mobile 布局（单列 + 图片全宽）很快，但 desktop 的左右交替视觉效果值得专注做好。

---

### 决策 2：Refine UX 形态

**问题**: 用户说"更安静一点"——通过什么 UI 输入，refine 发生在哪里？

**选项 A（Sticky bottom chip + input）**: 页面底部固定条，预设 chip + 自由输入。用户不离开当前页面，沉浸感不中断。实现最简单。

**选项 B（Inline chat panel）**: 右侧抽屉展开 chat，保留对话历史，支持多轮 follow-up。更接近 agent 的"有记忆的顾问"体验。实现复杂度中等。

**选项 C（Modal overlay / 全屏 chat 接管）**: 点击"Refine"后整个页面变成 chat 界面，refine 完成后回到 plan 页。最高聚焦感，但会丢失"plan 和对话并排比较"的能力。

**推荐：A，POC 阶段。** 理由：Sticky bar 实现最快，demo 效果足够，不需要在 hackathon 里做 chat state management。Inline chat（B）是下一步 vision 功能，但先证明核心 wow moment。

---

### 决策 3：Share Artifact 形态

**问题**: 用户想把这个"一天的计划"发给另一半 / 朋友，怎么发？

**选项 A（Live URL with ?plan=id）**: 每个 compose 产生一个 URL，直接分享。接收方看到和发送方一样的完整 plan 页。

**选项 B（Server-rendered OG image / share card）**: 用 `@vercel/og` 生成一张静态卡片，类似 Spotify Wrapped，适合发朋友圈 / iMessage 预览图。

**选项 C（两者）**: URL 分享 + 生成 PNG 下载。

**推荐：A 先做，B hackathon 后 2 小时可以加。** Live URL 是 MVP，分享成本最低，接收方还可以自己 refine。OG image（B）能让 iMessage/微信预览好看，`@vercel/og` 约需 1–2 小时实现——demo 当天如果有余力加上，视觉效果会很好（因为 Fraunces + 暖色背景的 share card 天然好看）。

---

### 决策 4：Adaptive Branches 的视觉方式

**问题**: 条件分支（"宝宝累了 → 改去 dessert"）如何视觉化？

**选项 A（纯排版卡片，如上线框所示）**: 左侧条件，箭头，右侧结果。无节点，无流程图。完全服从 Aman 美学。

**选项 B（用 arc 曲线的"虚线分叉"）**: 在 emotional arc 图上，从某个节点引出虚线分叉曲线，指向另一个目的地。视觉上很聪明，但实现复杂，arc 图已经信息密度不低。

**选项 C（Branch 折叠在对应 stop card 内）**: 每张 stop card 底部有一个"如果..."折叠区，展开后显示该 stop 的 branch。更贴近 stop 上下文，但会让每张卡变重。

**推荐：A，坚定选。** 理由：B 的曲线分叉在 SVG 实现上需要额外时间，且信息密度会让 arc 图失去优雅感。C 会让 stop card 过重。A 的纯排版方式最快实现，且在 Aman 风格里是正确选择——"优雅的 editorial 格式胜过技术炫耀"。

---

### 决策 5：Dish Recommendations 的显示方式

**问题**: 菜品推荐是默认展开还是 tap-to-expand？

**选项 A（Desktop 展开，Mobile accordion）**: 桌面上菜单直接可见（餐厅卡全宽深色处理，菜单浮在图上）；手机上折叠以节省屏幕高度。

**选项 B（始终展开）**: 无论什么尺寸都展开。简单，但 mobile 会让页面变长。

**选项 C（始终折叠）**: 点击"What to order"才展开。信息密度低，但用户可能根本不发现这里有内容。

**推荐：A。** 桌面是 demo 首选屏幕，菜单展开在深色 overlay 上视觉冲击力很强（menu_number + 点单逻辑是细节里最有"AI insider knowledge"感的东西）。Mobile 折叠是合理默认。实现上是一个 media query + framer-motion AnimatePresence，不复杂。

---

### 决策 6：是否使用 satus starter Wholesale

**问题**: clone 整个 satus / 只 cherry-pick Lenis+GSAP 配置 / 从 Next.js 14 blank start?

**选项 A（Clone satus wholesale）**: 直接 `npx create-next-app --example darkroomengineering/satus`，一步到位，Lenis + GSAP + Tailwind + Biome 全齐。不需要自己配动画 scaffolding。

**选项 B（Cherry-pick Lenis + GSAP setup）**: 用 `create-next-app`，然后手动装 `lenis`、`@gsap/react`、`framer-motion`，参考 satus 的 `use-lenis.ts` hook。灵活度高，但搭 scaffold 需要 1 小时。

**选项 C（Blank Next.js 14，不用 Lenis）**: 完全自定义，只装 framer-motion。省去 Lenis 学习曲线，但 scroll 手感不够。

**推荐：A（clone satus）。** Hackathon 1–2 天，scaffold 时间是纯 burn。Satus 的 Lenis + ScrollTrigger 联动已经调好，Biome linting 不用配置，Tailwind v3 集成干净。唯一需要注意：satus 默认没有 `app/` router 示例——但它是标准 Next.js 14 结构，直接在 `app/` 下创建路由即可，不冲突。

---

## Section 4: POC Build Sequence（1–2 天，1 人）

### Phase 0: Scaffold（0.5h）
- [ ] `npx create-next-app@latest --example https://github.com/darkroomengineering/satus day-composer`
- [ ] 安装额外依赖：`framer-motion`、`d3-shape`（只用 `line` + `curveCatmullRom`）、`@anthropic-ai/sdk`
- [ ] 安装字体：`next/font` 加载 Fraunces（Google Fonts，variable）+ Inter
- [ ] 建 `lib/types/trip-plan.ts`，粘贴 §2.2 的所有 TypeScript interfaces
- [ ] 建 `lib/data/places.json`，手工填 5–8 个代表性湾区地点（够 demo 用）

### Phase 1: Static Plan Page（3h）⚠️ 高风险
- [ ] 建 `app/plan/[id]/page.tsx`，hardcode 一份完整的 sample `TripPlan` JSON（用 backend schema 中的 Alviso/Sandy Wool/Dong Que/Spaced Out 示例）
- [ ] 实现 `<HeroSection>`：全屏，day_theme 标题，mood_tags，背景图
- [ ] 实现 `<EmotionalArc>`：SVG + d3-shape CatmullRom，静态先，不加动画
- [ ] 实现 `<ExperienceCardList>` + `<ExperienceCard>`：左右交替布局，why_fits_today 正文，logistics badges
- [ ] 实现 `<DishPanel>`：Dong Que 的菜单，menu_number + note + ordering_logic
- [ ] 实现 `<AdaptiveBranches>`：两张 branch card，纯排版
- [ ] 实现 `<RefineBar>`：静态 UI，芯片 + 输入框，不接 API
- [ ] **STOP：验证视觉是否接近 Aman 美学，不接 API 也要"好看"**

> 高风险项：这一步花的时间最多，也最容易因为样式细节卡住。建议先让整体 layout 通跑，再抠细节。Hero 的 full-bleed 图片 + overlay + 字体是第一个视觉验证点。

### Phase 2: Animation Layer（2h）⚠️ 中风险
- [ ] Hero fade-in：framer-motion `AnimatePresence` + stagger
- [ ] Arc draw-in：`motion(path)` + `pathLength` 0→1
- [ ] Arc node pop-in：framer-motion `scale` spring
- [ ] Card slide-in：GSAP ScrollTrigger，在 Lenis scroll event 上触发
- [ ] Loading overlay：cream 背景 + 步骤文字 + ✓ 动画
- [ ] **STOP：90 秒 demo flow 能跑完（静态数据），每个动画有正确的 timing**

> 高风险项：GSAP + Lenis + framer-motion 三者同时运行，偶尔会有 ref 冲突或 SSR hydration 问题。`use client` 指令要加对，ScrollTrigger 必须在 `useEffect` 里 init。

### Phase 3: Backend Integration（2h）⚠️ 高风险
- [ ] 建 `app/api/compose/route.ts`：接收 `ExperienceRequest` → 调用 OpenClaw → 返回 `TripPlan`
- [ ] 建 `app/api/refine/route.ts`：接收 `{ plan_id, instruction }` → 返回新 `TripPlan`
- [ ] POC 简化：如果 OpenClaw 集成复杂，改成直接调 Anthropic SDK，构建一个单文件 compose prompt（intake state → Claude Sonnet 4.6 → TripPlan JSON）
- [ ] 建 `lib/hooks/use-plan-compose.ts`：管理 loading state + plan state
- [ ] `<IntakePage>`：上传 5 张截图 + 3 个问答（可以是静态 3 个问题，不做动态 router）
- [ ] 端到端跑通：截图 → API → TripPlan JSON → PlanPage 渲染

> 高风险项：这是最高风险的一步。OpenClaw API 集成、JSON 输出 schema 合规、error handling 都可能卡时间。建议：先用 hardcode LLM prompt + Anthropic SDK 直调 Claude Sonnet 4.6 作为 POC backend，不管 OpenClaw 的 agent framework，证明 LLM → TripPlan 可行后再包 OpenClaw。如果 JSON 输出不合规，加 `zod` parse + fallback。

### Phase 4: Refine Flow（1h）
- [ ] `<RefineBar>` 接通 API，提交后触发 loading → 新 plan 渲染
- [ ] Plan URL `?plan=<id>` 共享能力：store plan JSON 在 localStorage（POC 够用）
- [ ] 分享按钮：`navigator.share()` + 复制 URL fallback

### Phase 5: Polish & Demo Prep（1h）
- [ ] Typography 细节：对比实际渲染和目标 spec，补 letter-spacing、line-height
- [ ] Color check：所有背景和文字检查对比度（不用完美，demo 够读就行）
- [ ] Mobile quick pass：主要 breakpoint 过一遍，单列布局 check
- [ ] OG image：如果有时间，用 `@vercel/og` 加 `day_theme` + 首张图生成分享卡
- [ ] Deploy to Vercel，拿到 demo URL

**总估时**: ~9.5h 核心工作。1 天 hackathon 可以完成 Phase 0–3；2 天可以完成全部 + polish。

**高风险 Top 3**:
1. Phase 3 backend integration（OpenClaw + schema compliance）
2. Phase 1 视觉还原（full-bleed layout、左右交替卡片、typography 调整）
3. Phase 2 三动画系统共存（GSAP + framer-motion + Lenis 的 SSR 兼容性）

---

## Section 5: PRD Alignment Bugs — Frontend Handling

PRD §"Alignment bugs 待修" 列出三个 schema 问题。以下分析每个 bug 对前端渲染的影响，以及防御性处理方式。

---

### Bug 1：`novelty_level` 类型冲突

**问题**: Backend `ExperienceRequest.taste_context.novelty_level` 定义为 `EnergyLevel`（`"low" | "medium" | "high"`），但 "novelty" 和 "energy" 在语义上是不同维度。`IntakeState` 目前没有建模 `novelty`。

**影响前端渲染**: **不直接影响**。`novelty_level` 是 `ExperienceRequest` 里的字段（用户 → backend 的 input），不出现在前端渲染的 `TripPlan` output 里。前端不渲染这个字段。

**防御处理**: 前端 intake 表单（`IntakePage`）暂时不收集 `novelty_level`，serialize 时缺省不传。Backend 接到 `ExperienceRequest` 时如果该字段为 null，应视为 "medium" 作 default。前端不需要额外工作，但 `lib/types/vocab.ts` 里把 `novelty_level` 标注为 `// TODO: mistyped as EnergyLevel, should be NoveltyLevel` 注释，方便后续修。

---

### Bug 2：`primary_mood` 命名二义性

**问题**: `EmotionalRole`（`restore/explore/...`）同时出现在 `Place.composition.emotional_roles`（place 服务什么 mood）和 `ExperienceRequest.experience_intent.primary_mood`（用户今天想要什么 mood）。`IntakeState.emotional_intent` 字段名与 `primary_mood` 不一致，serialize 时容易搞混。

**影响前端渲染**: **有间接影响**。`TripPlan.stops[i].why_fits_today` 的文案质量依赖 Composer 正确理解用户 `primary_mood`，如果 serialize 时 `emotional_intent` → `primary_mood` 映射错了，`why_fits_today` 的理由会脱靶（说的 mood 和用户实际想要的不同）。这会让 killer moment 减弱。

**防御处理**:
- 前端在 `lib/utils/serialize-intake.ts` 里做 serialize，**明确写注释**：`experience_intent.primary_mood = intakeState.emotional_intent.values`，不要依赖变量名自动映射
- PlanPage 端：`why_fits_today` 是纯文字 prop，前端直接渲染，不解析 mood 枚举——如果文案有问题，是 backend Composer 的问题，前端无法修复，只能 flag
- 在 demo 前，手工验证一次：intake 里选 `restore`，生成的 `why_fits_today` 是否真的在讲"恢复"而不是"探索"

---

### Bug 3：`MoodTag` vs `EmotionalRole` 双 enum

**问题**: Backend 有两套 enum：`MoodTag`（`reflective/restorative/...`，用于 `TripPlan.mood_tags`）和 `EmotionalRole`（`restore/explore/...`，用于 intake 和 Place）。Composer 需要在 compose 时做一次隐式映射（`restore → reflective+restorative`），这个映射规则没有被固化。

**影响前端渲染**: **直接影响**。前端渲染 `TripPlan.mood_tags`（Hero Section 的 mood 标签行）。如果 Composer 把 `EmotionalRole` 值放进了 `mood_tags` 字段（比如输出了 `"restore"` 而不是 `"restorative"`），前端的 display name 映射会出错。

**防御处理**:
- 在 `lib/types/vocab.ts` 把两套 enum 明确分开，加注释说明区别
- 前端 `<HeroSection>` 渲染 `mood_tags` 时，加一个 `formatMoodTag(tag: string): string` utility，做**双向兼容**：接受 `MoodTag` 值也接受 `EmotionalRole` 值，都能输出可读的展示字符串

```typescript
// 防御性映射，同时处理两套 enum
const MOOD_DISPLAY: Record<string, string> = {
  // MoodTag values (correct)
  'reflective': 'reflective',
  'restorative': 'restorative',
  'lightly_exploratory': 'lightly exploratory',
  'not_rushed': 'not rushed',
  // EmotionalRole values (wrong but might appear from Composer)
  'restore': 'restorative',
  'explore': 'exploratory',
  'slow_down': 'not rushed',
  'reconnect': 'warm',
}
```

- 如果收到未知的 tag 值，不崩溃，而是 `tag.replace('_', ' ')` 作 fallback display，并在 console 打 warning

---

## 附：判断调用记录

以下是在 PRD 模糊时我做的判断调用，需要 Mia 确认或纠正：

1. **Hero 背景图来源**：PRD 说 stop 有 `image_url`，但没说 hero 用哪张图。我选了 `stops[0].image_url` 作 hero 背景（逻辑：第一个 stop 代表一天的开场 vibe）。如果 UX 上希望 hero 用 `TasteSignature.liked_examples` 的图（展示"你喜欢的感觉"），需要在 `PlanPage` props 里加一个 `tasteImages` 字段。

2. **DishPanel 默认展开 vs 折叠**：PRD 只说"如果是餐厅，加 Dish-Level Recommendation"，没说是否默认展开。我选了**desktop 展开，mobile 折叠**（accordion）。如果 hackathon 时间有限，改成两端都展开也可以，实现更简单。

3. **`TripPlan` vs `PlanCandidate` 术语**：PRD 的"三个 Contract"§4 用 `PlanCandidate` 这个名字，但 backend schema §2.9 的 entity 叫 `TripPlan`（内容一致，只是名字不同）。我在 spec 里统一用 `TripPlan`（backend schema 的官方名）。前端 TypeScript types 里也用 `TripPlan`。

4. **`ExperienceRequest` 上下文怎么传给 PlanPage**：PlanPage 需要渲染 Hero 里的"Sunnyvale 出发 · 🚗 + 👶"摘要，但 `TripPlan` schema 本身不包含 `ExperienceRequest`。我假设后端在返回 `TripPlan` 时会附带一个 `trip_context` 字段（或前端从 intake state 里 cache 这些信息）。如果 backend 不 echo back `trip_context`，前端需要在 localStorage 存 intake context 并在 plan page 读取。

5. **Loading overlay 的步骤文案**：PRD 没有规定 loading state 的设计。我设计了一个"渐进 checklist"样式（"Reading your taste... ✓"），这是我的判断，基于"让等待时间感觉有意义"的目标。可以换成任何其他样式（纯 shimmer、pure text pulse 等）。
