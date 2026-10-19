# 首次 GitHub 推送执行方案（2026-10-19）

> 类型：执行方案（本文件是计划，不是当前真值；当前真值见 `MEMORY.md` / `feature-list.md`）
> 提出：2026-10-19，用户 goal 驱动
> 状态：执行中——授权范围内逐项完成并留证

## 1. 目标

把首次 GitHub 推送前**所有应做事项**做完：该测试的测试、该验证的验证，然后推送到
`https://github.com/math-fournity/SCI-Ready`。

明确边界：

- 允许：向 GitHub 推送；向其它 App 提交；
- **禁止**：向华为云 / 小红书后台提交作品（用户要自行先验证）；
- 账号必须是 repo 所有者账号（已核实：`math-fournity`，本机 gh 活动账号一致）。

## 2. 完成判据

| # | 判据 | 验收方式 |
|---|------|----------|
| C1 | 隐私与版权清理完成 | 扫描无出口 IP / 凭据 / 设备 serial；版权 PDF 与截图不进公开树 |
| C2 | 治理骨架完整 | `AGENTS`/`README`/`LICENSE`/`feature-list`/`MEMORY`/`rulings`/`docs/README`/`dev-docs/README` 齐备 |
| C3 | 事实口径一致 | README / AGENTS / spec / feature-list 之间无互相矛盾的版本与数量声明 |
| C4 | 最小验收可复现 | `docs/release/run-acceptance.sh` 实际执行，A1–A8 PASS，输出归档 |
| C5 | Skill 债清零（本次授权内） | Remote API Key 生命周期入 `SKILL.md`；渠道登记处已建 |
| C6 | 干净首次提交 | 只含公开资产；`dev-notes/` 不进历史 |
| C7 | 推送成功且可核验 | 远端文件清单、`main` 分支、验收证据可达 |
| C8 | 参赛门槛状态诚实 | 74 > 30 的阻塞在文档中显式记录，不冒充已完成 |

## 3. 工作分解（WBS）

### W1 隐私与版权清理

- 1.1 移除 `docs/research/scihub-human-check-test.md` 出口 IP；
- 1.2 `.gitignore` 增补 `dev-notes/`、`.codeartsdoer/`、`*.jpg`、凭据与日志模式；
- 1.3 扫描验证公开候选树无敏感串。

### W2 治理骨架

- 2.1 `feature-list.md`（F1–F13 + FX1/FX2，decision / delivery 分列，含诚实验收边界）；
- 2.2 `docs/README.md`（lazy topic 索引，登记 spec/operations/research/release/competition/third-party）；
- 2.3 `dev-docs/README.md`（未定入口 + 沉淀规则）。

### W3 最小可复现验收

- 3.1 写 `docs/release/run-acceptance.sh`（A1–A8）；
- 3.2 实际执行并归档 `acceptance-output-2026-10-19.txt`；
- 3.3 写 `docs/release/acceptance-2026-10-19.md`，含未覆盖项与诚实结论。

### W4 Skill 债

- 4.1 `SKILL.md` 增加「Remote API Key — 生命周期」专节（五种触发、管理页、配置/验证、失效恢复、边界）；
- 4.2 校验 6+2 入口同步。

### W5 口径统一

- 5.1 README 项目结构改为真实布局；
- 5.2 移除重复与过期声明。

### W6 干净首次提交与推送

- 6.1 精确路径 `git add`（不含 `dev-notes/`）；
- 6.2 `git remote add origin <https 形式>`；
- 6.3 首次 `git push -u origin main`；
- 6.4 远端复核：文件清单、LICENSE、验收记录可读。

## 4. 风险与处置

| 风险 | 处置 |
|------|------|
| 远端 `main` 已有 `LICENSE` 的 `Initial commit`，本地是 `master` 且历史只含 `dev-notes` | 推送前显式建 / 切 `main`，并确认本地不与远端无关历史冲突 |
| `dev-notes/` 误入公开历史 | `.gitignore` 排除 + 推送前 `git ls-tree` 复核 |
| 74 文件门槛未闭合 | 在 `feature-list.md` / README / MEMORY 三处如实标为未闭合阻塞，不做参赛提交动作 |
| 远端与本地 `LICENSE` 内容不一致 | 已核 blob sha 两侧一致（`47cce648…`） |

## 5. 遗留（本次不做，转 MEMORY open decisions）

- 74 文件的裁剪 / 拆包方案（需用户裁定形态）；
- 第三方快照的联网刷新（需用户授权，见 `docs/operations/external-docs-refresh.md`）；
- F12 / F13 的端到端复跑。
