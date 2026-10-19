# docs

> 稳定知识入口索引。采用 lazy 生成：下表登记每个 topic 的目录、入口、登记状态与激活条件；
> topic README 只在首次出现需记录的稳定事实时创建并登记。禁止为空壳目录凑齐结构。

## Topic 索引

| topic | 目录 | 入口 | 登记状态 | 激活条件 |
|-------|------|------|----------|----------|
| spec（产品规格） | `docs/spec/` | `docs/spec/mineru-skill-spec.md` | 已登记 | Skill 功能需求变化 |
| operations（运维规程） | `docs/operations/` | `docs/operations/external-docs-refresh.md` | 已登记 | 外部资料快照刷新、首次接触提醒 |
| research（研究留档） | `docs/research/` | `docs/research/scihub-human-check-test.md` | 已登记（**内部留档，不进入参赛提交包**） | 新增实测研究记录 |
| release（发布证据） | `docs/release/` | `docs/release/acceptance-2026-10-19.md` | 已登记 | 新的发布/验收轮次 |
| competition（赛事信息快照） | `docs/competition/` | `docs/competition/xiaohongshu-skill-competition.md` | 已登记 | 赛事规则变化时按 `docs/operations/external-docs-refresh.md` 刷新 |
| third-party（第三方资料） | `docs/browseros-mcp/` | `docs/browseros-mcp/README.md` | 已登记 | 上游文档变化时刷新；**权利归原作者，不受 MIT 覆盖** |

## 未登记但存在的目录

以下目录已存在但尚未产生需要登记的稳定事实，暂不创建 topic README，也不视为漂移：

| 目录 | 现状 | 激活条件 |
|------|------|----------|
| `docs/research/evidence/` | 仅存实测证据文件（脚本可公开，截图与 PDF 已 gitignore） | 有需要公开引用的证据时再登记 |

## 当前设计 / 需求 / 状态的真值位置

- 当前需求：`feature-list.md`（仓库根）
- 用户原始意图与裁定：`rulings.md`（仓库根）
- 当前状态、待决事项、下一步：`MEMORY.md`（仓库根）
- 资产地图与授权范围：`README.md`（仓库根）
- Skill 行为与 SOP：`~/.agents/skills/mineru/`（真源，非本仓库文件）

本目录只保存稳定知识，不复制上述 owner 的正文。
