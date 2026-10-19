# External Docs Refresh — 外部资料联网更新规程

> 类型：当前有效运维规程（版本 v1，2026-10-18）
> 适用对象：本仓库 `docs/` 下所有来自第三方、可能随时间变化的外部资料
> 授权边界：本规程本身不授权任何网络行为；每次实际更新都必须取得用户明确同意

## 0. 为什么要这份规程

本仓库混有两类内容：

1. **原创资产**：Skill 源码、SOP、规格、评测；
2. **外部资料快照**：从第三方站点抓取的文档，会随上游改版、赛事规则变化、产品版本升级而过期。

外部资料一旦过期，读者会把旧规则当成当前事实。因此它们需要显式的抓取时间、来源 URL 与更新规程。

## 1. 受管清单（SNAPSHOT MANIFEST）

下表是外部资料的唯一登记处。新增外部资料必须在此登记，否则不得进入 `docs/`。

| 本地路径 | 来源 URL | 抓取时间 | 变化风险 | 更新方式 |
|---|---|---|---|---|
| `docs/competition/xiaohongshu-skill-competition.md` | https://developer.huaweicloud.com/competition/information/1300000350/introduction | 2026-10-18 | 中（赛程、奖项、报名状态） | 重新抓取正文并更新 `抓取时间` |
| `docs/browseros-mcp/*.html`、`*.md`（16 篇） | https://docs.browseros.com/ 、https://support.huaweicloud.com/ （CodeArts Agent 文档） | 2026-10-18 | 中高（产品迭代频繁） | 逐篇重新保存并更新抓取时间 |
| `~/.agents/skills/mineru/references/official-manual.md` | https://github.com/opendatalab/MinerU/blob/master/skills/mineru/SKILL.md | 2026-09-29 | 高（上游随版本演进） | 重新拉取 master 分支全文 |
| `~/.agents/skills/mineru/references/output-schema.md` | 本机 MinerU App 输出目录（`MINERU_HOME` 下的 history 目录）实际契约 | 2026-09-29 | 中（随 App 版本变化） | 重新只读核验目录与 schema |

更新后必须同步更新表中的 `抓取时间`，并在 commit message 写明更新了哪几项。

## 2. 首次接触 / 安装时的强制提醒（必须执行）

**触发时机**：AI 第一次接触本仓库，或用户要求安装/配置本仓库的 Skill 时。

AI 必须先向用户报告以下信息，然后**停下等待用户决定**：

1. 本仓库包含 N 项外部资料快照，最新抓取时间见 §1 表格；
2. 这些内容可能已经过期，影响判断与操作；
3. 询问用户是否同意联网更新，以及更新的范围（全部 / 仅指定项）。

模板措辞（可直接使用）：

```text
本仓库的 docs/ 下包含外部资料快照（BrowserOS 文档、华为云大赛页面、MinerU 上游手册等），
抓取时间为 2026-10-18，之后上游可能已变更。是否同意我现在联网重新获取并更新这些文件？
可选范围：
1) 全部更新    2) 只更新 MinerU 上游手册    3) 只更新比赛信息    4) 暂不更新
```

**边界（不可越过）**：

- 未取得用户明确同意前，不得发起任何网络请求；
- 用户拒绝时，保持现状并在交付物中标注“内容快照时间为 X，可能已过期”；
- 更新只覆盖登记在 §1 的路径，不得顺手抓取未登记来源。

## 3. 用户同意后的更新流程

```bash
# 步骤 1：确认来源可达（只读探测）
curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' -L --max-time 30 '<SOURCE_URL>'

# 步骤 2：抓取到临时文件，先核验再替换
curl -L --max-time 60 -o /tmp/refresh-candidate '<SOURCE_URL>'
file /tmp/refresh-candidate

# 步骤 3：人工/AI 比对差异，确认变化是否影响本仓库结论

# 步骤 4：替换目标文件，更新 §1 抓取时间
# 步骤 5：精确路径提交，commit message 记录更新项与来源 URL
```

每一步的验收：

1. 探测返回 200（HTML 文档允许 200 + 重定向后的规范 URL）；
2. 抓取内容的类型与登记一致（HTML/PDF/Markdown）；
3. 若内容实质变化，必须判断是否影响 Skill 行为、参赛资格或规格描述，并在 commit 中说明；
4. 替换后文档头部的来源/时间标注同步更新。

## 4. 失败模式

| 失败模式 | 识别 | 处理 |
|---|---|---|
| 来源 404 / 域名变更 | 探测非 200 | 保留旧文件，在 §1 标注 `DEAD(source moved)`，报告用户 |
| 抓回 challenge 页 | `file` 显示 HTML 但内容是验证页 | 丢弃，不改动原文件 |
| 内容大幅重写 | 与旧版差异超过可核对范围 | 只更新快照，不改 Skill 逻辑；逻辑变更另开任务 |
| 上游改许可 | 新内容许可与 MIT 冲突 | 停止覆盖，报告用户并重新评估 |

## 5. 与其它规程的关系

- 本规程只更新文档快照，不修改 `~/.agents/skills/mineru/` 中的 Skill 行为；
- Skill 行为变更走正常需求流程，不因文档更新而隐性发生；
- 涉及 MinerU 版本升级（如 4.0.8 → 4.0.12）属于独立决策，需单独授权，不并入文档刷新。
