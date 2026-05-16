---
name: mvp-list
description: 处理 /mvp-list add <url> 或 /mvp-list add <image>，将餐厅或景点输入解析为 Place，寻找一个规范外部引用 ID，并生成可写入 gbrain 的 Markdown 索引资料。
---

# MVP List

这个 skill 负责 MVP List 的 Curate 与 Index 阶段：把用户从社交媒体、搜索、地图、截图或照片里发现的地点，整理成可被 gbrain 搜索、排序和比较的 Markdown Place 资料。

当前版本只处理单个地点的新增索引，不负责每周三触发、行程排序、agenda 输出或图片生成。

## 触发方式

当用户输入以下任一形式时使用本 skill：

- `/mvp-list add <url>`
- `/mvp-list add <image>`
- 用户要求“把这个餐厅/景点加入 mvp-list、索引、整理进 gbrain”

输入通常是一个 Place，类型只在以下两类中选择：

- `restaurant`
- `point_of_attraction`

## 执行原则

- 先确认地点身份，再补信息。不要在地点仍有歧义时写入 gbrain。
- 规范引用只需要一个高质量 ID，不要为了凑数同时追 Google Maps、Yelp、Apple Maps。
- 必须从当前公开来源核验动态信息，例如营业时间、评分、价格和地址；不要只凭模型记忆。
- 字段可以为空，但不能编造。无法确认时写 `null`，并在 `confidence_notes` 说明原因。
- 所有抓取到的事实都要保留来源 URL 和抓取日期，便于后续重索引。
- 最终产物是 gbrain 可输入的 Markdown，不是 JSON。结构化字段放在 YAML frontmatter，正文用短小标题保存可读摘要、访问信息、来源和置信度说明。
- 如果用户给的是图片，先从图片中识别店名、招牌、地址、菜单、地标或页面文字，再按文本地点继续处理。

## 工作流

1. 解析输入
   - URL：打开页面，提取地点名、城市、地址线索、地图链接、页面标题和页面正文。
   - Google Maps URL：先做结构化解析，再用公开来源核验动态字段。
     - 从 `/place/<name>` 提取地点名候选，URL decode 后把 `+` 视为空格。
     - 从 `!3d<lat>!4d<lon>` 提取地点坐标；缺失时可退回 `@<lat>,<lon>` 作为低置信坐标线索。
     - 从 `!1s<google_feature_id>` 或 `!16s<google_place_token>` 提取 Google Maps 引用；如果无法得到正式 Place ID，保留原始 Google Maps URL 作为高置信规范引用。
     - 不要把 Google Maps URL 里的 `entry`、`g_ep` 等分享参数当成地点身份。
   - 图片：使用视觉/OCR 识别可见文字、招牌、地址、菜名、地标和上下文。如果图像只能说明类别但不能定位具体地点，向用户要一个城市或更多线索。

2. 消歧与规范引用
   - 用地点名、城市、地址、坐标、官方站点或地图页面交叉验证具体 Place。
   - 优先选择以下任一规范引用，找到一个即可：
     - Google Maps place id 或可稳定解析的 Google Maps place URL
     - Yelp business id 或 alias
     - Apple Maps place id 或可稳定解析的 Apple Maps URL
     - 官方网站 URL，仅在地图或点评站点 ID 不可得时作为备用
   - 如果候选地点重名或跨城市重复，列出候选并请用户选择，不要猜测写入。

3. 分类
   - 餐饮服务为主：`restaurant`
   - 游玩、参观、自然景观、博物馆、公园、展览或亲子活动地：`point_of_attraction`
   - 同时具备两者时选择用户意图更强的一类，并在 `tags` 里记录另一面，例如 `restaurant_with_view`。

4. Markdown 索引资料生成
   - 按 `references/place-markdown-template.md` 生成 gbrain-ready Markdown。
   - `references/place.schema.json` 和 `references/place-template.json` 只作为字段完整性参考；不要把 JSON 当成最终输出，除非用户明确要求。
   - YAML frontmatter 是结构化搜索的主数据面，必须按 `references/place.schema.json` 的字段结构生成；除非同步更新 schema，否则不要添加 schema 外字段。
   - YAML frontmatter 至少包含 `schema_version`、`name`、`place_type`、`status`、`site_ids`、`location`、`open_hours`、`family_context`、`tags`、`sources`、`confidence_notes`。
   - 如果 `place_type` 是 `restaurant`，frontmatter 必须包含 schema 化的 `restaurant` 对象；如果是 `point_of_attraction`，frontmatter 必须包含 schema 化的 `point_of_attraction` 对象。
   - 生成 Markdown 后，尽量把 frontmatter 解析成对象并用 `references/place.schema.json` 校验；校验失败时不要写入，改为 `needs_review` 并说明失败字段。
   - Markdown 正文至少包含 `Summary`、`Visit Facts`、`Sources`、`Confidence Notes` 小节。
   - 通用字段优先级：规范 ID、名称、地址、坐标、营业时间、地点类型。
   - 餐厅字段优先级：菜系、评分、价格、招牌菜、氛围。
   - 景点字段优先级：主要看点数组、适合宝宝/家庭的说明、预计停留时间。

5. gbrain Markdown 写入
   - 如果 `$GBRAIN_REPO` 已设置，先读取该仓库的 README、AGENTS、CLAUDE、Codex 或索引脚本，找到现有写入入口。
   - 如果用户在当前请求里说明了 gbrain 路径，例如 `./.tmp/gbrain`，优先把它按当前 workspace 的相对路径解析，并把它当作本次 `$GBRAIN_REPO` 候选。
   - 如果 `$GBRAIN_REPO` 未设置且用户没有说明路径，先按顺序探测当前 workspace 的 `./.tmp/gbrain`、`./gbrain`，再从用户说明中定位其他 gbrain 仓库。
   - 对每个候选 gbrain 仓库，先确认目录存在且可读，再读取 README、AGENTS、CLAUDE、Codex、package.json、pyproject.toml、scripts、bin、import、imports、content 或 data 目录，寻找 Markdown 写入或导入入口。
   - 如果用户明确说“写入这个目录”且目录不存在，可以创建该目录作为本地 Markdown drop folder；但除非存在 gbrain CLI、查询工具或仓库文档确认该目录会被索引，否则只能报告“已写入 Markdown，未验证 gbrain 查询索引”。
   - 如果找不到 gbrain 仓库、gbrain CLI、gbrain 服务或可用 Markdown 写入入口，暂停流程并提示用户安装或配置 gbrain；此时只输出待写入 Markdown 草稿，不声称已索引。
   - 优先使用 gbrain 已有 CLI、脚本、API、Markdown import 目录或内容目录；不要为本 skill 发明新的持久化格式，除非用户明确要求。
   - 写入后，如果工具支持查询，做一次独立读取，确认新 Place 已进入索引。

6. 返回结果
   - 用中文简短说明：识别出的地点、选择的规范引用、补全程度、未确认字段、是否已写入 gbrain。
   - 如果没有写入，给出可直接用于后续写入的 Markdown 草稿。

## 实际写入约定

当目标是目录型 gbrain 输入，例如用户说 `gbrain folder is ./.tmp/gbrain`：

1. 解析目标目录
   - 相对路径按当前 workspace 解析。
   - 如果用户明确要求写入且目录不存在，创建目录。
   - 如果只是探测默认路径且目录不存在，不要创建；返回 Markdown 草稿和缺失原因。

2. 生成文件名
   - 使用 `<place-name>-<city>.md` 的小写 slug，例如 `the-mandarin-menlo-park.md`。
   - slug 只用 ASCII 小写字母、数字和连字符；去掉标点，连续空白压成一个连字符。

3. 生成 Markdown
   - 文件必须以 YAML frontmatter 开头，frontmatter 就是 `references/place.schema.json` 对应的结构化 Place 对象。
   - 正文只放人类可读的 `Summary`、`Visit Facts`、`Restaurant Notes` 或 `Point Of Attraction Notes`、`Sources`、`Confidence Notes`。
   - 结构化搜索所需字段必须在 frontmatter 中，不要只写在正文里。

4. 校验再写入
   - 写入前或写入后，解析 `---` 之间的 YAML frontmatter。
   - 用 `references/place.schema.json` 校验 frontmatter 对象。
   - 校验失败时，修正 frontmatter 后再写；不要把不符合 schema 的 Markdown 当作已索引结果。

5. 验证状态
   - 至少确认目标 Markdown 文件存在，并报告文件路径。
   - 如果没有 gbrain 查询工具，只能报告“已写入 Markdown，未验证 gbrain 查询索引”。
   - 如果有 gbrain 查询工具或仓库提供查询脚本，写入后必须独立查询一次确认可检索。

## 输出格式

已写入并验证时：

```markdown
已加入 MVP List：

- 地点：<name>
- 类型：<restaurant | point_of_attraction>
- 规范引用：<site>: <id_or_url>
- gbrain 状态：已写入并验证
- 主要缺口：<none 或字段列表>
```

已生成草稿但没有写入时：

```markdown
已生成 MVP List 待写入草稿：

- 地点：<name>
- 类型：<restaurant | point_of_attraction>
- 规范引用：<site>: <id_or_url>
- gbrain 状态：未写入，原因：<missing_gbrain | missing_write_entrypoint | needs_user_disambiguation | other>
- 下一步：请安装/配置 gbrain，或提供现有写入入口
- Markdown 草稿：紧随其后输出完整 gbrain-ready Markdown，格式见 `references/place-markdown-template.md`
```

需要用户消歧时：

```markdown
我找到了多个可能的地点，先不要写入。请选择一个：

1. <name> - <address> - <canonical_hint>
2. <name> - <address> - <canonical_hint>
```

## 质量门槛

- `name`、`place_type`、`site_ids` 至少一个条目、`sources` 至少一个条目是最小可索引集合。
- 写入前必须有足够证据说明这是同一个地点，而不是同名地点。
- 坐标、营业时间、评分、价格等动态或平台字段必须带来源。
- 任何不确定字段都放入 `confidence_notes`，不要混进确定事实。
- 生成的 Place Markdown 必须包含能通过 `references/place.schema.json` 校验的 YAML frontmatter 和来源小节；如果不能满足最小可索引集合，状态设为 `needs_review` 并说明缺口。

## 参考资料

- Markdown 模板：`references/place-markdown-template.md`
- JSON Schema 字段参考：`references/place.schema.json`
- JSON 空值字段参考：`references/place-template.json`
