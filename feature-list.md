# feature-list

> 当前需求与交付状态。`decision` 与 `delivery` 分列：文档存在、已实现、已验证、运行观察是四个不同状态。
> Skill 行为真源在 `~/.agents/skills/mineru/`，本文件是仓库侧的需求投影。

## 交付形态与硬门槛

| 项 | 值 |
|----|----|
| 参赛形态 | Skill 组合（`mineru` 核心 + `codearts-config-guide` 辅助） |
| 硬门槛 | 单次提交 ≤40MB、≤30 个文件 |
| 当前规模 | `mineru` 8 文件 + `codearts-config-guide` 66 文件 = **74 文件，超限** |
| 状态 | ❌ 未闭合，必须裁剪或拆包后才能提交（见 MEMORY open decisions） |

## Feature 状态

| ID | Feature | decision | delivery | SRC | DES | IMP | VER |
|----|---------|----------|----------|-----|-----|-----|-----|
| F1 | 多格式文档解析（PDF/Office/EPUB/OFD/HTML/CSV） | accepted | implemented | `docs/spec/mineru-skill-spec.md` F1 | 同左 | `SKILL.md` cheatsheet + CLI | 依赖 MinerU 引擎；本机实测 289 页分块 |
| F2 | OCR / 公式 / 表格 / 版面识别 | accepted | implemented | spec F2 | 同左 | `--remote` standard tier | 本机实测 |
| F3 | 页/块级精确引用定位 | accepted | implemented | spec F3 | 同左 | `read` + locator | 本机实测 |
| F4 | 大文档分块（>200 页） | accepted | verified | spec F4 | 同左 | `scripts/parse_large.py` | 289 页端到端：2 chunks、289/289 页码标记、642 KB |
| F5 | 搜索与发现 | accepted | implemented | spec F5 | 同左 | `search`/`find`/`list`/`show` | 未单独立项验收 |
| F6 | 导出与批量 | accepted | implemented | spec F6 | 同左 | `mineru-kit` | 未单独立项验收 |
| F7 | 跨客户端复用 | accepted | implemented | spec F7 | 同左 | 六客户端入口共享真源 symlink | 已核实 6 入口哈希一致 |
| F8 | 隐私与安全（Key 处理、敏感文档确认） | accepted | implemented | spec F8 | 同左 | `SKILL.md` 隐私段落 | 未单独立项验收 |
| F9 | 健壮性与运维（错误码恢复、保活） | accepted | implemented | spec F9 | 同左 | `scripts/keepalive.sh` + 错误码表 | 未单独立项验收 |
| F10 | 文档结构大纲 | candidate | not-implemented | spec F10 | — | — | — |
| F11 | 文献获取（多渠道，含 sci-hub 最后手段） | accepted | **in-progress** | spec F11 | `references/lit-acquisition.md` | 同左 | sci-hub 三层检测实测 2026-10-18；GDZ 实测；渠道降级与台账仍编写中 |
| F12 | 转换后视觉审计 | accepted | implemented | spec F12 | `references/visual-audit.md` | 同左 | 二值化管线定参实测；未做本机端到端全篇复跑 |
| F13 | 并发舰队验证 | accepted | **in-progress** | spec F13 | `references/audit-fleet.md` | 同左 | SOP 已沉淀；三处并发原语尚未本机复跑 |
| FX1 | 文献渠道活登记处 | accepted | implemented | 2026-10-19 用户裁定 | — | `references/文献渠道.md` | Gutenberg/GDZ/Fields-Medalists repo 均已实测或核实 |
| FX2 | Remote API Key 生命周期 | accepted | **in-progress** | 2026-10-18 用户要求 | ADR-0026 | `SKILL.md` 待补 Key 专节 | 官方 guidance 契约已核实；Skill 文案尚未落盘 |

## 验收边界（诚实声明）

本仓库**没有可执行的自动化测试套件**；现有 `delivery: verified` / `implemented` 状态来自逐项人工实测与
源码/CLI 行为核对，不等于回归测试覆盖。首次推送的验收以
 `docs/release/acceptance-2026-10-19.md` 记录的命令与输出为准。
