# MEMORY

> 当前态与恢复入口。README 负责资产地图；需求、裁定与稳定设计分别由各自 owner 承载。

## Current execution queue

1. **首次 GitHub 发布准备**：目标远端已确定为 `https://github.com/math-fournity/SCI-Ready`。
2. **许可证已定为 MIT**（R-004）：本地已新增与远端一致的 `LICENSE`；第三方材料另行说明，不纳入 MIT 覆盖。
3. 首次 GitHub 推送（仓库 `math-fournity/SCI-Ready`，所有者账号 `math-fournity`，也是本机 gh 活动账号）。
4. 不得向华为云 / 小红书后台提交；那部分由用户自行验证后再操作。
5. **参赛文件数硬阻塞**：`mineru` 8 + `codearts-config-guide` 66 = 74，超过 ≤30 文件；必须先裁剪或拆包。

## Current state

- 本地 Git：`master`，无 remote；项目文件仍是未跟踪状态。
- 远端 Git：`math-fournity/SCI-Ready`，公开仓库，默认分支 `main`，HEAD `8c5f69127e789d0516c8b70939b2df8017b0123e`，仅有 `Initial commit` 和 `LICENSE`。
- 许可证：本地 `LICENSE` = 远端 MIT 文本（sha1 一致）。
- Skill 真源：`~/.agents/skills/mineru/`；六个客户端入口共享同一 `SKILL.md` 与 `references/lit-acquisition.md`；CodeArts evolve generated entry 是文件级硬链接。
- 对外口径：用户已明确否决删除 Sci-Hub 与人机检测应对内容；README/spec 已恢复，保留合法渠道优先与法律边界说明。
- 已脱敏：`docs/research/scihub-human-check-test.md` 出口 IP 已移除；`.gitignore` 已排除 `dev-notes/`、`.codeartsdoer/`、`*.jpg`、凭据与日志模式。
- 最小验收已跑通：`docs/release/acceptance-output-2026-10-19.txt`，A1–A8 全 PASS，exit 0。
- 示例素材已改用公共领域来源：GDZ IIIF 公版期刊实测可用（HTTP 200，2000×2699 JPEG，1908 年 *Mathematische Annalen*）。
- 外部资料联网更新规程：`docs/operations/external-docs-refresh.md`；`AGENTS.md` 已将“首次接触先提醒用户”列为必做项。

## Open decisions

- **74 文件如何裁剪或拆包**（只交 `mineru`、把配置指南合并成更少索引文件、还是拆成多个独立作品）——这是参赛提交的唯一阻塞，GitHub 推送不受其影响。
- GitHub 仓库与最终比赛提交包是否共用同一范围（当前计划：GitHub 存完整工作区，提交包另行裁剪）。

## Next action

已推送到 `math-fournity/SCI-Ready` 的 `main`：

- 远端 34 个 blob，`dev-notes/` 为 0，secret/PII 扫描为 NONE；
- 5 条提交的 author/committer 均已核验为 `math-fournity`（另有一条建仓时 GitHub web 自动生成的
  `Initial commit`，committer 为 `web-flow`）；
- 远端树与本地一致；验收证据（A1–A8，8/8 PASS，含非缓存复跑）在远端可读；
- 未向华为云 / 小红书后台提交（按用户要求）。

## History

- 2026-10-18：用户指定目标远端为 `https://github.com/math-fournity/SCI-Ready`，并明确许可证需要选择。
- 2026-10-18：核实六客户端共享真源；确认 74 文件超过比赛门槛；用户否决删除 Sci-Hub 与人机检测内容，相关对外说明已恢复。
- 2026-10-18：许可证定为 MIT 并落盘；例程改用中性描述，移除版权文献名称（R-004 / R-005）。
- 2026-10-18：示例切换为公版素材并实测验证；新增外部资料联网更新规程；README 补 BrowserOS 路由预设矫正说明。
- 2026-10-18：新增 `references/文献渠道.md` 文献渠道活登记处（Gutenberg 实测坑、GDZ 公版源、Fields-Medalists repo 登记）；Skill 改为「先查本地渠道登记处再联网」。
- 2026-10-19：按用户 goal 执行全量准备——脱敏出口 IP、补 `feature-list.md` / `docs/README.md` / `dev-docs/README.md` / 发布证据、跑通 A1–A8 验收（8/8 PASS）、Skill 补 Remote API Key 生命周期专节；README 更新为真实治理布局。
