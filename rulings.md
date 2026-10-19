# Rulings

本文件保存用户原始意图与执行边界；当前需求与实现状态分别由 Feature、代码和验证证据承载。

## R-001 — 首次 GitHub 推送目标

- 日期：2026-10-18
- 状态：accepted
- 用户原意：计划推送到 `https://github.com/math-fournity/SCI-Ready`。
- 执行边界：记录目标不等于授权配置 remote、提交、推送或发布；这些动作仍需用户明确授权。
- 当前证据：GitHub 仓库公开，默认分支 `main`，当前只有 `LICENSE` 与 `Initial commit`。

## R-002 — 许可证需要选择

- 日期：2026-10-18
- 状态：open
- 用户原意：该仓库“有许可证选择”，需要处理，不能默认沿用未确认的选择。
- 当前证据：远端 `LICENSE` 为 MIT（Copyright 2026 Math Fournity）；本地尚无 `LICENSE`。
- 待确认：最终采用何种许可证，是否对代码、文档与第三方资料分层授权，以及是否保留远端 MIT。

## R-003 — 保留 Sci-Hub 与人机检测应对内容

- 日期：2026-10-18
- 状态：accepted
- 用户原意：不应删除 Sci-Hub 和人机检测绕行卖点。
- 执行边界：未经用户明确裁定，不得以平台合规风险为由从 README、spec 或相关对外材料删除这些内容；保留合法渠道优先与法律边界说明。
- 当前处理：恢复 README/spec/AGENTS 中被删除的相关表述；内部 `references/lit-acquisition.md` 未删除。

## R-004 — 许可证采用 MIT

- 日期：2026-10-18
- 状态：accepted
- 用户原意：许可证就是 MIT。
- 执行边界：仓库代码与原创文档按 MIT 发布；第三方材料不纳入 MIT 覆盖，需保留原始归属与许可说明。
- 当前处理：已新增 `LICENSE`，与远端 `math-fournity/SCI-Ready` 现有 MIT 文本一致。

## R-005 — 例程不使用版权文献

- 日期：2026-10-18
- 状态：accepted
- 用户原意：例子不要用版权文献。
- 执行边界：README、spec、Skill 及其 references 中的示例改用中性描述，不点名受版权保护的文献、书名或具体论文。
- 当前处理：README / spec / `SKILL.md` / `references/lit-acquisition.md` 中的版权文献名称已中性化；`docs/research/scihub-human-check-test.md` 属历史实测留档，未改写。
