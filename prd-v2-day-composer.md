# Day Composer — PRD v2

> v1（`prd.md`）把这事看成 "place list + 周三触发 + itinerary 生成"。
> v2 重新定位：**不是旅行规划，是为一天 compose 一种感觉。**
> v2 是 **on-demand**：用户什么时候想规划就什么时候来，不做定时触发。

## TL;DR

把用户已经攒的小红书截图 / Maps 收藏当成 **taste samples**（不是候选地点），
匹配到我们已 index 好的湾区地点库，
结合今天的 mood + constraints，
输出一份带 **emotional arc + transitions + adaptive branches** 的"一天提案"。

杀手 moment：**"我没告诉你我要去哪里，我只给你看了我喜欢的感觉，你就找到了现实世界里可以去的版本。"**

---

## 北极星

**AI-composed real-world experiences** —
不是 travel planning，不是 recommendation，是 **composing how a day feels**。

类比：Spotify playlist editor，不是 Google Maps。

---

## 三个核心 Insight（这是 v2 vs v1 的全部差异）

### Insight 1：用户上传的不是候选地点，是 taste samples
用户存的东京茶馆、京都小巷、海边咖啡，**不是想去那里**，而是在表达 vibe。
系统抽 vibe signature → 在湾区库里找 **现实世界等价物**。

### Insight 2：输出不是 itinerary，是 Day Composition
真正 ship 的 value 是 **transition quality + emotional pacing**：
> 历史感 → 自然恢复 → 烟火气晚餐 → 轻松收尾 = "recovering but alive"
>
> 一种 day rhythm，不是 4 个独立的 POI。

Index 的不只是 place vibe，还包括 **place combination compatibility**（A+B = calm reflective；B+C = appetite reopening）。

### Insight 3：Intake 靠结构化框架 + 动态追问，不靠自由聊天
参考 SymptomAI 的医疗信息采集思路：
LLM 负责 orchestration / language / prioritization，
**reasoning structure 本身是 6 维 ontology**，不是 LLM 自由发挥。

---

## 🔭 Vision（Post-POC，不是 hackathon 范围）

> 以下「双边市场结构 / Creator 端 UX / 3 层架构 / 4 个 contract」是产品 vision。
> POC 阶段不做。
> POC 范围见本文最后「POC Spec」章节。

## 双边市场结构（Vision）

> 灵感来源：**世界邦**（达人定制旅行平台）的 AI-native 升级版。
> Powered by **小龙虾**（OpenClaw, agent runtime）+ **gbrain**（personal/place index）。

### 两边

- **Creator 端**：达人（Bay Area 本地玩家、生活方式编辑、家庭出游博主）
  → 创作 Day Composition 模板，授权给平台流通
- **Consumer 端**：周四晚要规划周六的家庭 / couple
  → 选模板 or 发起定制

### 两条产品线（对应世界邦的两条线）

| 路径 | 对应世界邦 | 形态 | 个性化深度 | TTL |
|---|---|---|---|---|
| **Fast Path** | 超级自由行（SKU 化） | 浏览达人已 publish 的 Day Composition → AI 帮 adapt 到你今天的 mood / constraints | 中（达人骨架 + AI 微调） | 2 分钟 |
| **Deep Path** | 定制自由行（1-on-1） | AI 顾问深度 intake → 匹配达人 → 达人 + AI co-compose | 高 | 48 小时 |

### 核心 product decision：角色纯粹性（直接 borrow 世界邦最聪明的一点）

| 角色 | 只做 | 不碰 | 为什么 |
|---|---|---|---|
| **达人** | 创作 Day Composition、写 narrative、推荐菜品 | ❌ 不做预定、不卖货 | 保持"懂行的朋友"信任感，不变成"旅行社" |
| **Platform（gbrain）** | place index、SKU 流通、预定链接、履约 | ❌ 不创作内容 | 供应链角色 |
| **AI Agent（小龙虾）** | intake 顾问、匹配、refine（不做行中） | ❌ 不替代达人的 narrative authorship；❌ 行中 adapt 交给通用 AI | 顾问 + orchestrator |
| **Consumer** | 表达 taste、选 plan、refine | — | — |

→ 这个分工是世界邦最值钱的洞察：**信任来自角色不混合**。
和你在 NoteGen 里"AI 出草稿 / 医生做最终判断"是同一个 pattern。

---

## AI-Native 重做世界邦（差异表）

| 环节 | 世界邦原版（2014） | Day Composer（2026） |
|---|---|---|
| **2 分钟 intake** | 表单 chatbot | LLM 动态 intake（6 维 Ontology + 截图 taste 抽取） |
| **2 小时人工顾问电话** | 真人销售澄清需求 | AI 顾问 agent 自动澄清、补 slot |
| **48 小时达人定制** | 纯人工创作 | AI 抽 vibe + 检索素材 + 达人 craft narrative & 微调 |
| **大数据匹配** | 后台静态 SKU 推荐 | gbrain semantic match（vibe + pacing + compatibility） |
| **行中服务** | 行程大师 App + 24h 人工客服 | 不做。出门后用通用 AI（ChatGPT / Claude / Siri）就够了，不是我们的差异化 |
| **个性化 ↔ 规模化张力** | 张力存在：达人贵且慢 vs 模板组合稀释承诺 | **AI 把 intake / matching / refine 全部规模化，达人只 focus 在最稀缺的"内容创作"环节** |

### 这个产品真正的护城河
**不是 AI**，是 **达人 SKU 库 + AI agent intake 能力**两件事的 compound。
LLM 能压缩 2 分钟和 2 小时那两段；
48 小时那段（达人对一种生活感的 authorship）才是 LLM 难替代的——而平台规模化了这种创作的分发。

---

## 用户旅程（5 步闭环）

| 步骤 | 谁做 | 产出 |
|---|---|---|
| 1. **Import** | 用户 | 10 张截图 / Maps links / 收藏链接 |
| 2. **Understand** | Agent | "你最近喜欢的 vibe summary" |
| 3. **Ask** | Agent | 3–5 个轻量 mood/constraint 问题（动态，不是表单） |
| 4. **Compose** | Agent | 2–3 条带 emotional arc 的路线 |
| 5. **Refine** | 用户 ↔ Agent | "太赶 / 更安静 / 加一个酒吧" → 调整（**hard cap：全流程 ≤ 10 轮**） |

### 两条 intake / refine 原则（这是 agent 质量的真正北极星）

**1. Sufficient-information 原则**
用户一句"轻松一点，带宝宝"就 infer 出 4 个 slot，**不要再问 20 个问题**。

**2. Maximum-information-gain follow-up 原则**
每个 follow-up question 必须按 **"问完这一句，agent 对最终 plan 的不确定性能降低多少"** 来排序。

| 反例（低 info gain） | 正例（高 info gain） |
|---|---|
| "你想几点出发？" | "你今天更想要 restore 还是 explore？"（一个问题决定整个 emotional arc） |
| "想吃什么菜系？" | "晚上想要安静收尾还是热闹烟火气？"（决定整条曲线的尾段） |
| "预算多少？" | "今天最不能接受的是什么？"（avoidance 比 preference 信息量大得多） |

用户没时间陪聊一百轮 — **全流程 hard cap 10 轮**，agent 自己负责把每一轮花在刀刃上。

---

## Interaction Layer 架构

> 灵感：Google **SymptomAI**（arXiv 2605.04012）+ **Adaptive Question Selection**（arXiv 2604.22067）。
> 我们把医疗信息采集的 "soft state machine + dynamic routing + slot filling" 模式搬到旅行 intake 上。
> Runtime 锁死 **小龙虾（OpenClaw）** —— 它的 multi-agent 能力是这个架构的依赖；不引入 LangGraph，只借设计模式。

### 1. Warm Surface / Hard Core 原则

**Surface（LLM 驱动）**：对话语气、reflective listening（MI / OARS 风格的"复述 + 提问"）、永远不向用户暴露 slot 名字或 confidence 数字——用户看到的是一个懂行的朋友，不是表单。
**Core（确定性代码）**：typed `IntakeState` + 每个 slot 的 confidence + Router 决定 "下一步问什么 / 该停了 / 该 compose 了"。
**关键禁令**：LLM **不能** 决定 "下一句问什么"——那是 Router 的职责。LLM 只负责"在 Router 指定的维度上，把问题问得像人话"。
（出处：SymptomAI, arXiv 2605.04012 —— "language is the interface, structure is the brain"。）

### 2. 四节点循环（cyclical graph）

```
       ┌─────────────────────────────────────────┐
       ▼                                         │
[Extractor] ─► [Router] ──不够──► [Q-Generator]──┘
   ▲              │
   │              └──够了──► [Composer] ──► TripPlan
[User turn]
```

| Node | Job | Model | Determinism |
|---|---|---|---|
| **Extractor** | parse 用户的自由文本 → slot updates + 每个 slot 的 confidence | Haiku 4.5 | LLM |
| **Router** | check stopping rule、决定下一条路径（继续问 / 去 compose） | 无（纯 Python） | **Deterministic** |
| **Q-Generator** | 给 lowest-confidence 的 slot 挑一个 highest-info-gain 的问题 | Sonnet 4.6 | LLM（constrained） |
| **Composer** | 生成 TripPlan（emotional arc + transition_reason + 菜品 + adaptive branch） | Sonnet 4.6 + vision | LLM |

> 实现层：4 个小模块跑在 **小龙虾** 上 —— 不依赖 LangGraph，cyclical graph 是用 4 个 Python 函数 + 一个 while loop 拼出来的。

### 3. Stopping Rule（formalized）

把原来含糊的"≤10 轮"替换为一条具体公式：

```
STOP if any of:
  1. turn_count >= 10                                          (hard cap)
  2. avg(confidence_i for i in 6 dims) >= 0.8
       AND min(confidence_i) >= 0.5                            (sufficient info)
  3. user 明确说 "好了 / 直接给我看 plan / done"               (escape hatch)
```

阈值 0.8 / 0.5 来自 SymptomAI 的 "sufficient information" 判据的 travel-domain 调参——`avg` 保证整体覆盖，`min` 保证不让某一维"漏底"导致 Composer 瞎 compose。算法 pattern 出处：arXiv 2604.22067（Adaptive Question Selection for Clinical Symptom Inquiry）。

### 4. Q-Generator 算法 sketch

每次被 Router 调用时，Q-Generator 跑下面 5 步：

1. **Identify lowest-confidence dimension** —— Router 已经传进来了，Q-Generator 不重判
2. **Enumerate 5–8 candidate questions** 针对该维度（LLM，prompt constrained 到 "must target slot=X"）
3. **Score each candidate by predicted info-gain** —— 让 LLM 自己估 "如果用户回答了这个，该 slot 的 confidence 预期能涨多少"（0-1 数值）
4. **Pick top-1**，用 MI / OARS 风格把它包装成"先复述用户已说的 + 再问"的句式（surface 层的温度由 prompt 保证）
5. **Feed back expected confidence delta to Router** —— 如果 best candidate 的 predicted delta < 0.1（再问也没用），Router 直接跳到 Composer，不强行凑满 10 轮

→ 这是 "Maximum Information Gain follow-up" 原则的具体化：之前在用户旅程那一节是 principle，这里是 algorithm。

---

## Experience Intake Ontology（6 维）

6 维 ontology 不是"我们要问用户哪 6 类问题"——它是 **`IntakeState` 类型本身**，是 agent 内存里那个每轮 mutate 的结构化对象。结构化 > 自由聊天，因为结构化才能让 Router 算 confidence、让 Q-Generator 选维度、让 Composer 知道哪些 slot 真的填好了。

下面是这个类型的正式定义。controlled vocabularies（`VibeTag` / `EmotionalRole` / `SocialFit` 等）的来源是 `mvp-list/backend-data-schema-v2.md` §2.0，因为 `IntakeState` 最终要序列化成 `ExperienceRequest` 发给 backend——两边必须用同一套 enum。

### A) IntakeState（typed schema）

```typescript
// enums imported from backend-data-schema-v2.md §2.0 controlled vocab
import type {
  VibeTag, MoodTag, PacingRole, EmotionalRole,
  SocialFit, EnergyLevel, ChaosTolerance, AvoidanceTag,
} from './backend-data-schema-v2';
import type { TasteSignature } from './backend-data-schema-v2'; // §2.5

type Provenance =
  | 'inferred_from_screenshots'
  | 'user_stated'
  | 'user_implied'
  | 'default';

type Slot<T> = {
  values: T[];
  confidence: number;            // 0–1, Extractor maintained
  provenance: Provenance;
  last_updated_turn: number;
};

type Turn = {
  role: 'user' | 'agent';
  text: string;
  turn_index: number;
};

type IntakeState = {
  // 0. Taste — derived from screenshots, not from chat
  taste_signature: {
    value: TasteSignature;       // full backend type from §2.5
    confidence: number;          // = TasteSignature.confidence (vision LLM)
    provenance: 'inferred_from_screenshots';
  };

  // 1. Emotional Intent          —— maps → ExperienceRequest.experience_intent.primary_mood
  emotional_intent:  Slot<EmotionalRole>;

  // 2. Social Configuration      —— maps → trip_context.companions
  social_config:     Slot<SocialFit>;

  // 3. Energy Profile            —— maps → constraints.energy_level + constraints.chaos_tolerance
  energy_profile: {
    energy_level:     { value: EnergyLevel;     confidence: number; provenance: Provenance };
    chaos_tolerance:  { value: ChaosTolerance;  confidence: number; provenance: Provenance };
    last_updated_turn: number;
  };

  // 4. Practical Constraints     —— maps → trip_context + constraints
  practical_constraints: {
    date:                 { value: string | null; confidence: number; provenance: Provenance };  // ISO date
    time_window:          { value: string | null; confidence: number; provenance: Provenance };  // "14:00-22:00"
    start_location:       { value: string | null; confidence: number; provenance: Provenance };
    transport:            { value: 'car'|'rideshare'|'transit'|'walk_bike'|'mixed'|null; confidence: number; provenance: Provenance };
    max_drive_minutes:    { value: number | null; confidence: number; provenance: Provenance };
    budget:               { value: 'tight'|'moderate'|'flexible'|'splurge'|null; confidence: number; provenance: Provenance };
    kid_friendly:         { value: boolean | null; confidence: number; provenance: Provenance };
    needs_parking:        { value: boolean | null; confidence: number; provenance: Provenance };
    last_updated_turn: number;
  };

  // 5. Taste Anchors (explicit)  —— maps → experience_intent.desired_vibe + taste_context.food_preferences
  taste_anchors: {
    desired_vibe:       Slot<VibeTag>;            // from chat + screenshot reinforcement
    food_preferences:   Slot<string>;             // free-form strings ("natural wine", "fusion")
    last_updated_turn: number;
  };

  // 6. Avoidance                 —— maps → experience_intent.avoid
  avoidance:         Slot<AvoidanceTag>;

  // bookkeeping
  turn_count: number;
  transcript: Turn[];
  stopped_reason?: 'hard_cap' | 'sufficient_info' | 'user_escape' | null;
};
```

每轮循环：Extractor 读 `transcript[-1]` → 产出一个 partial `IntakeState` diff → merge 到当前 state（confidence 取 max，provenance 升级，turn_index 更新）→ Router 算 `avg(confidence_i)` 和 `min(confidence_i)` 决定下一步。

### B) IntakeState → ExperienceRequest 映射表

序列化时把 `IntakeState` 摊平成 backend §2.6 的 `ExperienceRequest`。逐字段对照：

| IntakeState 字段 | ExperienceRequest 字段（§2.6） | 备注 |
|---|---|---|
| `practical_constraints.date.value` | `trip_context.date` | ISO date string |
| `practical_constraints.time_window.value` | `trip_context.time_window` | `"HH:MM-HH:MM"` |
| `practical_constraints.start_location.value` | `trip_context.start_location` | free-form string |
| `social_config.values` | `trip_context.companions` | `SocialFit[]` |
| `practical_constraints.transport.value` | `trip_context.transport` | enum |
| `emotional_intent.values` | `experience_intent.primary_mood` | `EmotionalRole[]` |
| `taste_anchors.desired_vibe.values` | `experience_intent.desired_vibe` | `VibeTag[]` |
| `avoidance.values` | `experience_intent.avoid` | `AvoidanceTag[]` |
| `practical_constraints.max_drive_minutes.value` | `constraints.max_drive_minutes` | int |
| `practical_constraints.kid_friendly.value` | `constraints.kid_friendly` | bool |
| `practical_constraints.needs_parking.value` | `constraints.needs_parking` | bool |
| `practical_constraints.budget.value` | `constraints.budget` | enum |
| `energy_profile.energy_level.value` | `constraints.energy_level` | `EnergyLevel` |
| `energy_profile.chaos_tolerance.value` | `constraints.chaos_tolerance` | `ChaosTolerance` |
| `taste_signature.value` | `taste_context.taste_signature` | full `TasteSignature` object |
| `taste_anchors.food_preferences.values` | `taste_context.food_preferences` | `string[]` |
| `(not in IntakeState)` | `constraints.stop_count_target` | default 4 — set at serialize time |
| `(not in IntakeState)` | `constraints.max_drive_minutes_per_leg` | optional — derive from `max_drive_minutes / stop_count` if absent |
| `(not in IntakeState)` | `taste_context.novelty_level` | **alignment bug — see below** |

**Alignment bugs 待修（这次不动 backend schema，但 friend 需要确认）**：

1. **`novelty_level` 类型冲突**：backend §2.6 把 `taste_context.novelty_level` 定成 `EnergyLevel`（low/medium/high），但 "novelty" 跟 energy 是两回事——一个高 energy 的人也可以偏好 familiar 而非 novel。`IntakeState` 里我目前没建模 `novelty`；建议 backend 新增 `NoveltyLevel` enum（`familiar | balanced | novelty_seeking`），或者从 ontology 删掉这个字段，让 `desired_vibe` 里的 `novelty` / `familiar` VibeTag 承担。
2. **`primary_mood` 的语义二义性**：`EmotionalRole`（restore/explore/...）出现在两个地方——`Place.composition.emotional_roles`（这个地方"服务"什么 mood）和 `ExperienceRequest.experience_intent.primary_mood`（用户今天想要什么 mood）。复用 enum 是好的，但 `IntakeState.emotional_intent` 命名上跟 `primary_mood` 不对齐，serialize 时容易混淆。建议把字段统一为 `primary_mood` 或 `emotional_intent`，二选一。
3. **`MoodTag` vs `EmotionalRole`**：backend 同时有 `MoodTag`（reflective/restorative/...）和 `EmotionalRole`（restore/explore/...）。`IntakeState` 只采集 `EmotionalRole`，但输出的 `TripPlan.mood_tags` 用的是 `MoodTag`。Composer 需要做一次 enum 映射（restore → reflective+restorative 之类），这个映射规则要么固化到 Composer prompt，要么 backend 提供一张映射表。

### C) Sufficient-information 原则（保留）

6 维 schema 看起来很多，但 agent 的工作 **不是** 把每个 slot 都填满——是 **填到够用为止**。一句 "轻松一点带宝宝" 就能 infer 出 `emotional_intent=[restore, slow_down]` + `social_config=[family_with_baby]` + `avoidance=[rushed]` + `chaos_tolerance=low` 四个 slot，剩下的能 default 就 default、不要再追问 20 个问题。

Router 的 stopping rule（见上面"Interaction Layer 架构 §3"）就是这条原则的代码化：**confidence 够了就走，没必要凑满**。

---

## One-Page Output 结构

> 参考：Spotify playlist + Aman/Black Tomato cinematic deck + Apple editorial cards。
> **不是** Google Maps、不是表格。

```
顶部
├── Day Theme        「旧湾区与恢复感的一天」（narrative anchor）
├── Mood Tags        reflective · warm · lightly exploratory · not rushed
└── Emotional Arc    slow opening → breathing → lively dinner → light closing
                     （时间线 + vibe 曲线可视化）

中间（4–6 张 Experience Cards）
每张：
├── 大图（vibe image / screenshot）
├── 一句话标题       "A quiet historical opening"
├── Why fits today   "今天想轻探索但不疲惫，这里比大型 museum 轻盈"
├── Logistics        🚗 8min  🅿️ easy  👶 baby-friendly
├── Transition       "indoor narrative → outdoor breathing"（连到下一张）
└── Optional tip     "建议 sunset 前到湖边"

如果是餐厅，加 Dish-Level Recommendation
├── 招牌菜列表 + 点单逻辑
└── "前半天偏安静，晚上可以加一点烟火气热炒收尾"

底部
└── Adaptive Branches
    ├── 如果宝宝状态不好 → skip comedy，去 nearby dessert
    └── 如果 energy 更高 → 加 downtown wine bar
```

---

## Creator 端 UX（达人侧）

> 达人最大的痛点不是"想不出去哪"，是 **"我脑子里有一天的感觉，但写出来太累"**。
> 平台 = 用 AI 把达人的隐性 expertise 显性化、SKU 化。

### 达人发布一个 Day Composition 的流程

1. **Capture（最低门槛）**：达人扔进去自己的真实出行素材——照片、Maps timeline、消费记录、随手 voice memo
2. **AI 起 draft**：小龙虾 agent 自动 propose：day_theme、emotional_arc、each stop 的 why_fits、transition、菜品推荐
3. **达人精修**：在 AI draft 上改 narrative、加私货 tip、删 over-touristy 的部分
4. **AI 自动打 schema 标签**：vibe_tags、pacing_role、social_fit、energy_cost、avoidance_tags（达人不用懂 ontology）
5. **Publish to gbrain**：成为一个可被 consumer 端 fast-path 检索的 SKU

### 达人 dashboard 关心的指标
- SKU 被 consumer 浏览 / lock-in / refine 的次数
- "我的模板被 AI 改写到什么程度"（衡量原创性 vs 适配性）
- 哪些 vibe / season / social_config 缺供给（平台给达人的"约稿提示"）

### 关键：达人 SKU 不是死的 itinerary
而是 **template + flex slots**：
- 固定的：day_theme、emotional_arc、核心 1-2 个 anchor 地点
- 可被 AI 替换的：餐厅（按 consumer 饮食偏好）、收尾活动（按 social_config）、transitions（按出发地）

→ 这解决了世界邦那个"模块化复制稀释个性化"的根本张力：**模板携带 narrative & arc，AI 只 swap 兼容元素**。

---

## 架构（3 层，不是 5 个 agent）

> 早期就拆 5 agent 是过度设计。MVP 阶段：1 Orchestrator + 2 tools。
> Marketplace 把架构从 2 层扩成 3 层：Creator / Platform / Consumer。

```
┌─────────────────────────────────────────────────────────┐
│  CREATOR LAYER                                          │
│  - 达人 capture（素材 → AI draft）                       │
│  - 达人 craft narrative & 精修                           │
│  - SKU publish (DayCompositionTemplate)                 │
└────────────┬────────────────────────────────────────────┘
             │  DayCompositionTemplate
             ▼
┌─────────────────────────────────────────────────────────┐
│  PLATFORM LAYER (gbrain + 小龙虾)                        │
│  ├─ Place Intelligence (你朋友负责)                      │
│  │   - Bay Area place index                             │
│  │   - vibe / pacing / compatibility schema             │
│  │   - reservation links / logistics                    │
│  └─ SKU Index                                           │
│      - 达人 templates 检索                               │
│      - flex-slot 替换引擎                                │
└────────────┬────────────────────────────────────────────┘
             │  PlaceCandidate[] + SKUCandidate[]
             ▼
┌─────────────────────────────────────────────────────────┐
│  CONSUMER INTERACTION LAYER (你负责)                     │
│  - Intake conversation (6 维 Ontology)                   │
│  - Information-sufficiency judgment                     │
│  - Fast path: SKU 浏览 + AI adapt                       │
│  - Deep path: compose from scratch + refine             │
└─────────────────────────────────────────────────────────┘
```

---

## 三个 Contract（团队分工 contract）

### 1. `ExperienceRequest`（交互层 → 信息层）

```json
{
  "trip_context": {
    "date": "2026-01-10",
    "time_window": "14:00-22:00",
    "start_location": "Sunnyvale",
    "companions": ["partner", "baby"],
    "transport": "car"
  },
  "experience_intent": {
    "primary_mood": ["restore", "light_exploration"],
    "desired_vibe": ["quiet", "cultural", "not_too_tiring"],
    "avoid": ["touristy", "overcrowded", "too_rushed"]
  },
  "constraints": {
    "max_drive_minutes": 45,
    "kid_friendly": true,
    "needs_parking": true,
    "budget": "flexible"
  },
  "taste_context": {
    "liked_examples": ["Tokyo jazz bar screenshot", "quiet tea house"],
    "food_preferences": ["fusion", "natural wine"],
    "novelty_level": "medium"
  }
}
```

### 2. `PlaceCandidate`（信息层 → 交互层）

```json
{
  "candidates": [
    {
      "id": "place_123",
      "name": "Alviso Adobe",
      "type": "historic_site",
      "location": "Milpitas",
      "hours": "14:30 tour, 2nd Sat of month",
      "vibe_tags": ["quiet", "historic", "low_stimulation"],
      "pacing_role": "opening",
      "fit_score": 0.87,
      "fit_reason": "matches cultural + light exploration intent",
      "logistics": {
        "parking": "easy",
        "kid_friendly": true,
        "estimated_duration_minutes": 45
      },
      "story_context": "19th-century adobe site with local Bay Area history",
      "booking_url": "..."
    }
  ],
  "possible_transitions": [
    {
      "from": "place_123",
      "to": "place_456",
      "drive_minutes": 8,
      "transition_reason": "indoor history → outdoor nature reset"
    }
  ]
}
```

### 3. `DayCompositionTemplate`（Creator 端 → Platform，SKU 化）

```json
{
  "template_id": "sku_quiet_bay_recovery_001",
  "author": { "creator_id": "mia", "display_name": "Mia" },
  "day_theme": "旧湾区与恢复感的一天",
  "mood_tags": ["reflective", "warm", "lightly exploratory"],
  "emotional_arc": ["slow opening", "breathing", "lively dinner", "light closing"],
  "social_fit": ["family-with-baby", "couple"],
  "season_fit": ["fall", "winter"],
  "anchor_stops": [
    { "place_id": "alviso_adobe", "pacing_role": "opening", "fixed": true }
  ],
  "flex_slots": [
    { "slot": "dinner", "role": "lively", "tag_constraints": ["烟火气", "non-touristy"] },
    { "slot": "closing", "role": "light_social", "alternatives": ["comedy", "dessert", "wine_bar"] }
  ],
  "private_tips": ["sunset 前到湖边", "dong que 走 walk-in 不接受预定"],
  "narrative": "今天会从安静的历史空间开始..."
}
```

### 4. `PlanCandidate`（交互层 compose 产物）

```json
{
  "day_theme": "旧湾区与恢复感的一天",
  "mood_tags": ["reflective", "warm", "lightly exploratory"],
  "emotional_arc": ["slow opening", "breathing", "lively dinner", "light closing"],
  "stops": [
    { "place_id": "...", "time": "14:30", "why_fits_today": "...", "transition_to_next": "..." }
  ],
  "dish_recommendations": { "place_id": "...", "dishes": [...], "ordering_logic": "..." },
  "adaptive_branches": [
    { "condition": "baby is fussy", "alternative": "skip comedy, go to nearby dessert" }
  ]
}
```

---

## Schema 演进（现有 `place.schema.json` 需要补什么）

现有 schema 是 **place-centric**（name, address, hours, dishes）；
v2 是 **composition-centric**，需要新增字段：

- `vibe_tags`: enum 列表（quiet / cinematic / lively / cultural / outdoor / warm / fast / slow / ...）
- `emotional_role`: enum（restore / explore / celebrate / reconnect / ...）
- `pacing_role`: enum（opening / breathing / peak / recovery / closing）
- `chaos_tolerance_required`: low / medium / high
- `compatibility_hints`: { good_before: [...], good_after: [...] }
- `energy_cost`: low / medium / high
- `social_fit`: solo / couple / family-with-baby / friends / ...

→ 这是给信息层（朋友）的 schema spec。

---

## 🎯 POC Spec（Hackathon，1–2 天，1 人）

### 北极星问题
**能不能在 90 秒内让 demo 观众脱口而出"卧槽"？**

那个"卧槽"来自杀手 moment：
> "我只给你看了我喜欢的感觉，你就给了我现实世界里可以去的版本。"

倒推 POC 必须证明的**唯一一件事**：
**LLM 能从 5 张截图 + 3 个问题，produce 一份让人想去过的一天（带 emotional arc 和 why_fits_today）。**

其他全砍。

### Demo Flow（90 秒）

```
[0-15s]  用户拖 5 张截图（小红书 / Maps / 相册）到一个网页
[15-30s] Agent: "我看到你喜欢 X 这种 vibe。问 3 个问题——"
         Q1: 周六想 restore 还是 explore?
         Q2: 带宝宝 / 只你们俩?
         Q3: 不想要哪种感觉?
[30-60s] 生成 one-page："旧湾区与恢复感的一天"
         - Day Theme + Mood + Emotional Arc 可视化曲线
         - 4 张 Experience Card（图 + why_fits_today + 8min 🚗 transition）
         - 1 个 Adaptive Branch（"宝宝累了 → skip comedy，去 nearby dessert"）
[60-90s] 用户说"更安静一点" → 重新 compose，证明可 refine
```

### 必须真实的（决定 wow）

| 模块 | 必须做到 |
|---|---|
| **Vision intake** | LLM 看图能抽 vibe signature（"安静 / 自然光 / 低噪音 / 慢"），不是 OCR |
| **动态 intake** | 3 个问题感觉像聪明朋友，不是表单 |
| **why_fits_today** | 每个 stop 的推荐理由真的引用了 taste + mood，不能是通用文案 |
| **Emotional arc** | one-page 有视觉化曲线 / 渐变 / 时间线，不是 bullet list |
| **One-page 美学** | 像 Aman deck / Spotify share card，不是 Notion 表格 |

### 可以全砍 / 用 stub 的

| 模块 | POC 怎么做 | Why 可以砍 |
|---|---|---|
| **gbrain place index** | 手工 curate 30–50 个湾区地点 JSON + hand-tag vibe | demo 不 query 全库；30 个够 cover 8 种 mood combo |
| **Creator / 达人 SKU** | 不做 | Marketplace 是 Vision |
| **Reservation / booking** | 静态链接 | 不影响 wow |
| **真实 Maps API** | hand-coded transitions 表 | 不影响 wow |
| **多 adaptive branches** | 1 个 hard-coded fork | demo 只演 1 个 |
| **Refine 深度** | 支持 1 轮 refine | 证明可调即可 |
| **多日 / 全天** | 只做半日 4 stops | sample 已经证明半日有 wow |
| **历史 / 账户** | localStorage / in-memory | hackathon 不需要 |

### 技术栈建议
- 前端：Next.js + Tailwind + framer-motion（arc 曲线动画）
- LLM：Claude Sonnet 4.6（vision intake）+ prompt scaffold
- 后端：单文件 Node / Python，读手工 JSON
- 部署：Vercel，分享 URL 直接 demo

### POC 边界图

```
INPUT                       POC SCOPE                    OUTPUT
─────                       ─────────                    ──────
5 张截图   ──vision──►   ┌────────────────┐  ──HTML──►  One-page:
3 个回答   ──intake──►   │  LLM agent     │             · Day Theme
                         │   +            │             · Emotional Arc
                         │  hand-curated  │             · 4 Cards
                         │  30-place JSON │             · 1 Branch
                         └────────────────┘             · 1 refine 轮
                         ❌ no marketplace
                         ❌ no real index
                         ❌ no booking
                         ❌ no creator side
```

### Demo 当天怎么 pitch
- **Hook（10s）**："你存了 1000 张小红书截图，周六还是不知道去哪。"
- **Wow（60s）**：演 demo flow。
- **Vision（20s）**："这只是 single-user POC。下一步：达人发布 SKU、AI 顾问规模化定制——AI-native 版世界邦。"

---

## Out of Scope (明确不做，哪怕 long term 也不做)
- ❌ **定时自动触发**（不做每周三 / 周四晚自动推送，永远是 on-demand）
- ❌ **行中实时 adapt / reroute**（出门后用通用 AI 就够了，不是我们的差异化）
- ❌ 通用旅行规划（不去抢 Google Trips / TripAdvisor）
- ❌ B2B / 商家入驻

---

## 成功标准

**定性（dogfood）**
- 用户读完 one-page 的第一反应是：**"我真的想去过这一天"**，不是 "信息完整"
- 用户能在 ≤ 2 次 refine 内 lock in 一个 plan

**定量（eval）**
- Intake sufficiency rate：是否在 ≤ 5 个问题内 cover 6 个维度
- Composition coherence：emotional_arc 在 LLM-as-judge 下的连贯性评分
- Transition quality：每个 transition 是否有可解释的理由

---

## v1 → v2 关键差异 cheat sheet

| 维度 | v1 (`prd.md`) | v2 (this doc) |
|---|---|---|
| 用户输入意义 | 候选地点收藏 | **Taste samples** |
| 触发方式 | 每周三自动 | **完全 on-demand**（用户主动来） |
| 核心交互 | 上传 → 自动出方案 | **Intake 对话 → compose → refine** |
| 输出 | Agenda + overview 图 | **Day Composition**（theme + arc + cards + branches） |
| Index 对象 | Place metadata | Place + **vibe + pacing role + compatibility** |
| 架构 | 单 pipeline | **2-layer + 3 contracts** |
| 灵魂 | 工具 | **"一天的感觉"** |
