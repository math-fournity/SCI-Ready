# AGENTS.md — CodeArts-WorkSpace

## 项目目标

参加 **华为开发者大赛 2026 — 小红书 Skill 创新赛道**，打造可复用的 Skill 组合参赛。

- 比赛页面：https://developer.huaweicloud.com/competition/information/1300000350/introduction
- 报名截止：2026-11-13
- 奖金总额：¥500,000
- 核心交付物：**MinerU 全链路文献处理 Skill**（文献获取 → 解析 → 视觉审计，v1.1 已完成，持续打磨中）

### 参赛硬性门槛

1. 必须至少使用华为云码道 CodeArts 或果办 OfficeAce 其中之一
2. 作品须提交到华为云 Skill 市场和小红书 Skill 市场
3. 单次提交 Skill 文件总大小 ≤40MB，文件数 ≤30 个
4. 作品须为原创、面向真实场景、可运行、可复用

### 评审五维标准

场景真实性 · 作品可用性 · Skill 复用率 · 技术完成度 · 内容传播力

## 目录结构

```
CodeArts-WorkSpace/
├── README.md                          ← 项目介绍（面向 GitHub）
├── AGENTS.md                          ← 本文件（项目工作指南）
├── .codeartsdoer/
│   └── mcp/mcp_settings.json          ← MCP 配置（含 browseros-neo）
├── docs/
│   ├── spec/
│   │   └── mineru-skill-spec.md       ← MinerU Skill 功能规格说明（v1.1，含 F11/F12/F13）
│   ├── research/
│   │   ├── scihub-human-check-test.md ← Sci-Hub 人机检测实测报告（2026-10-18）
│   │   └── evidence/                  ← 实测证据（截图/MCP 兜底脚本；PDF 已 gitignore）
│   ├── browseros-mcp/                 ← BrowserOS + CodeArts MCP 集成文档（16篇）
│   └── competition/
│       └── xiaohongshu-skill-competition.md  ← 比赛完整信息
└── .arts/                             ← CodeArts 内部目录（已 gitignore）
```

## 已有 Skill（用户级，位于 ~/.codeartsdoer/skills/）

| Skill | 路径 | 状态 | 说明 |
|-------|------|------|------|
| **mineru** | 真源 `~/.agents/skills/mineru/`；CodeArts 入口 `~/.codeartsdoer/skills/mineru/` | v1.1 全链路 | MinerU 4.x CLI 文献处理 Skill — **获取**（arXiv→DOI→Unpaywall→图书馆→GDZ 多渠道，合法渠道优先）、**解析**（PDF/Word/PPT/Excel 转 Markdown，OCR，大 PDF 分块 >200页）、**审计**（视觉逐页验证，单代理或 AgentTeam 并发舰队）。六个客户端入口共享同一真源：Codex、Claude Code、ZCode、Devin、OpenCode、CodeArts；CodeArts evolve 另有文件级硬链接。参考文献含 6 份：`references/文献渠道.md` 是文献渠道活登记处（找文献前先查它）。 |
| **codearts-config-guide** | `~/.codeartsdoer/skills/codearts-config-guide/` | 已完成 | CodeArts Agent 配置指南索引 Skill — 15 大类别，65 篇本地落盘文档，每篇含在线权威地址 |

### MinerU Skill 关键技术细节

- 可执行文件：`/Volumes/D/toolchain-cache/mineru-venv/bin/mineru`（不在 PATH 上）
- 云端端点：`https://mineru.net/api`（与桌面 App 相同）
- 默认路径：`--remote` 云端解析（standard tier，LaTeX 公式），与 App 质量一致
- 大 PDF 处理：`scripts/parse_large.py` 自动分块（>200页），已实测 289 页文档端到端（不指定具体文献名称）
- 本地服务器：`~/.mineru/doclib.sock`（launchd keepalive 自动启动）
- API Key：已配置在 `~/.mineru/doclib.db`（registered 级别，但不解除 200 页/文件上限）
- 参考文档（5 个 references）：`references/official-manual.md`（925行官方手册）、`references/output-schema.md`（输出目录契约）、`references/lit-acquisition.md`（F11 文献获取 SOP，基于 2026-10-18 sci-hub 实测 + 2026-10-17 GDZ 实测）、`references/visual-audit.md`（F12 视觉审计 SOP，二值化管线实测参数）、`references/audit-fleet.md`（F13 并发舰队 SOP）
- 本机权威配置：`~/README.md` 的 `0066` 条目；详细 owner 文档为 `~/Documents/readme-local/1066-mineru/mineru-pdf-conversion-setup.md`

## 开发环境

| 项目 | 值 |
|------|-----|
| 平台 | macOS (Apple Silicon) |
| Node | 26.7.0 |
| Python | 3.13.11 |
| Go | 1.26.0 |
| Maven | 3.9.13 |
| BrowserOS neo | MCP 端口 9210，CDP 端口 9115 |

## MCP 配置

`browseros-neo` MCP 服务已配置在 `.codeartsdoer/mcp/mcp_settings.json`，指向 `http://127.0.0.1:9210/mcp`（streamableHttp 类型）。使用前需确保 CodeArts IDE 已重启以建立 MCP 连接。

## 工作原则

- 用简体中文回复
- 通俗易懂地解释，直接判断对错
- 先说明计划再开始工作，不确定时停下来问
- 偏好 AgentTeam 多智能体协作方式完成复杂任务
- 长任务用 goal-x 打包
- **首次接触本仓库或帮用户安装 Skill 时，必须先读 [`docs/operations/external-docs-refresh.md`](docs/operations/external-docs-refresh.md) 并按 §2 提醒用户外部资料可能过期，在用户同意前不得联网更新。**

## 首次接触必做

1. 读 [`docs/operations/external-docs-refresh.md`](docs/operations/external-docs-refresh.md)，向用户报告外部资料快照时间，并询问是否联网更新。
2. 读 [`MEMORY.md`](MEMORY.md) 获取当前状态与待决事项。
3. 读 [`rulings.md`](rulings.md) 了解已生效的用户裁定。
4. 需要找文献、论文或公版材料时，先查 Skill 的 `references/文献渠道.md`（渠道活登记处），命中即用，未命中再公开检索；发现新渠道须回填登记。
