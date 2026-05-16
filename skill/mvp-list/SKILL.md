---
name: mvp-list
description: 处理 /mvp-list add <url> 或 /mvp-list add <image>，将餐厅或景点输入解析为 Place，寻找一个规范外部引用 ID，并补全地点索引资料后写入或准备写入 gbrain。
---

# MVP List

这个 skill 负责 MVP List 的 Curate 与 Index 阶段：把用户从社交媒体、搜索、地图、截图或照片里发现的地点，整理成可被 gbrain 搜索、排序和比较的结构化 Place 资料。

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
- 如果用户给的是图片，先从图片中识别店名、招牌、地址、菜单、地标或页面文字，再按文本地点继续处理。

## 工作流

1. 解析输入
   - URL：打开页面，提取地点名、城市、地址线索、地图链接、页面标题和页面正文。
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

4. 索引字段补全
   - 按 `references/place.schema.json` 生成符合 JSON Schema 的 Place JSON。
   - 需要空值模板时读取 `references/place-template.json`。
   - 通用字段优先级：规范 ID、名称、地址、坐标、营业时间、地点类型。
   - 餐厅字段优先级：菜系、评分、价格、招牌菜、氛围。
   - 景点字段优先级：主要看点数组、适合宝宝/家庭的说明、预计停留时间。

5. gbrain 写入
   - 如果 `$GBRAIN_REPO` 已设置，先读取该仓库的 README、AGENTS、CLAUDE、Codex 或索引脚本，找到现有写入入口。
   - 如果 `$GBRAIN_REPO` 未设置，先在当前 workspace 或用户说明中定位 gbrain 仓库。
   - 如果找不到 gbrain 仓库、gbrain CLI、gbrain 服务或可用写入入口，暂停流程并提示用户安装或配置 gbrain；此时只输出待写入 JSON 草稿，不声称已索引。
   - 优先使用 gbrain 已有 CLI、脚本、API 或 import 目录；不要为本 skill 发明新的持久化格式，除非用户明确要求。
   - 写入后，如果工具支持查询，做一次独立读取，确认新 Place 已进入索引。

6. 返回结果
   - 用中文简短说明：识别出的地点、选择的规范引用、补全程度、未确认字段、是否已写入 gbrain。
   - 如果没有写入，给出可直接用于后续写入的 JSON 草稿。

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
- 生成的 Place JSON 必须符合 `references/place.schema.json`；如果不能满足 schema，状态设为 `needs_review` 并说明缺口。

## 参考资料

- JSON Schema：`references/place.schema.json`
- 空值模板：`references/place-template.json`
