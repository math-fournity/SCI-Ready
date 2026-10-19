# MinerU Skill — 让 AI 代理读懂文档

> 华为开发者大赛 2026 · 小红书 Skill 创新赛道参赛作品

MinerU Skill 是一个面向 AI 代理的**文献处理全链路能力插件**：获取 → 解析 → 审计。它让 Codex、Claude Code、ZCode、CodeArts 等代理能获取文献（DOI / arXiv ID 多渠道）、解析文档（PDF/Word/PPT/Excel → 结构化 Markdown + 精确引用定位）、并验证解析质量（逐页视觉审计）。

**一行命令，让代理从"看不见文档"到"获取文献、读懂文档、验证质量"。**

```bash
mineru parse "report.pdf" --remote --json
# → Markdown + LaTeX 公式 + 表格 + 图片，附带页/块级引用定位
```

---

## 🎯 解决什么问题

AI 代理（Codex、Claude Code 等）无法直接读取 PDF、Word、PPT 等文档格式，也常常被付费墙挡在文献原文之外，解析结果是否可靠更无从验证。当用户说"帮我总结这份 PDF"时，代理只能望洋兴叹。

MinerU Skill 把"获取 → 解析 → 审计"全链路能力装进代理：

| 场景 | 没有 MinerU | 有 MinerU |
|------|------------|-----------|
| "帮我解析这份 289 页的电子书" | ❌ 无法读取 PDF | ✅ 自动分块解析，289 页端到端 |
| "帮我读这篇 1908 年的公版期刊论文" | ❌ 代理看不到原件 | ✅ 从 GDZ 取页面图像 → OCR → 逐页核验 |
| "这份合同第 7 页第 3 段说了什么？" | ❌ 无法定位 | ✅ `doc:ab12cd3/tier:standard/page:7/block:3` |
| "把这份扫描件 OCR 出来" | ❌ 没有 OCR 能力 | ✅ `--remote` 云端 OCR + LaTeX 公式 |
| "这份财报的表格数据提取一下" | ❌ 无法解析表格 | ✅ 表格结构化输出为 Markdown |
| "帮我取得这篇 DOI 文献" | ❌ 打不开收费墙 | ✅ 按渠道优先级获取：arXiv → DOI → Unpaywall → 图书馆 → GDZ → sci-hub（最后手段，含法律边界） |
| "这 289 页的解析结果可靠吗？" | ❌ 无法验证 | ✅ 逐页视觉审计，单代理或并发舰队，PASS/PASS±/FAIL 分级 |

---

## ✨ 核心能力

### 📥 文献获取

从 DOI 或 arXiv ID 出发，按渠道优先级决策树获取全文：

**arXiv → DOI → Unpaywall → 图书馆 → GDZ（公共领域古籍）→ sci-hub（最后手段，含法律边界声明）**

- 人机检测自动应对：Cloudflare 等挑战的实测绕行方法
- 下载三步验证：`file` 命令 / 文件头魔数 / 元数据比对，杜绝假 PDF
- 获取台账：渠道、时间、验证结果逐次记录，全程可追溯
- **合法渠道优先**是默认原则；兜底渠道仅在前序渠道全部失败后启用

### 📄 多格式文档解析

PDF / Word / PPT / Excel / EPUB / OFD / HTML / CSV → Markdown

### 🔍 OCR 与版面识别

扫描件 OCR、LaTeX 公式提取、表格结构识别、图片提取、版面布局还原

### 📍 精确引用定位

每个内容块都有稳定的定位器：`doc:{id}/tier:{tier}/page:{page}/block:{block}`

代理可以引用文档中的具体位置，而不是模糊地说"文档里提到..."

### 📚 大文档分块处理

云端服务限制单文件 200 页，`parse_large.py` 自动分块处理：

```bash
python3 scripts/parse_large.py "gdz-public-domain-sample.pdf" -o ./output --chunk 150 --wait 600
# → 289 页文档 = 2 chunks = 合并为一个完整 Markdown，页码连续
```

已实测：289 页文档端到端解析，642 KB Markdown，289/289 页码标记，零丢失。

> 示例素材全部来自公共领域来源（Project Gutenberg、GDZ、Internet Archive 公版件），不含受版权保护的文献。

#### 公版示例素材：一条可复现命令

本仓库的示例统一使用公共领域素材。下面这条命令从 GDZ（哥廷根数字化中心）取一份 1908 年公版期刊的页面图像，可直接用于解析与审计演示：

```bash
curl -s -o p261.jpg --max-time 60 \
  "https://manifests.sub.uni-goettingen.de/iiif/image/gdz:PPN235181684_0065:00000270/full/2000,/0/default.jpg"

file p261.jpg        # JPEG image data ... 2000x2699
```

实测（2026-10-18）：HTTP 200，315,546 字节，2000×2699 JPEG，EXIF 注释标明 1908 年 *Mathematische Annalen*。
GDZ 收录德语区历史文献扫描件，属公共领域，可合法用于示例与分发。

### 🔎 视觉审计

解析结果可靠吗？逐页审计给出可验证的答案：

- **二值化渲染管线**：解析 Markdown 与原 PDF 页面渲染为可比对图像
- **逐页审计循环**：渲染 → 读图 → 定位 → 五点比对 → 落签 → 分级
- **PASS / PASS± / FAIL 三级分级**：每页都有明确质量结论
- **高 DPI 局部放大**：可疑区域放大重渲染，细节无处遁形
- **无视觉模型时的局部 MinerU 交叉印证**：纯文本代理也能审计

### 🚢 并发舰队

几百页的文档逐页审计太慢？用 AgentTeam 多代理并发逐页审计：

- **文件分片互斥**：一页一文件，代理间零冲突
- **分账本制**：每个代理维护独立审计账本，互不干扰
- **单一 CANONICAL_INTEGRATOR**：只有一个代理负责最终合并，避免多写冲突
- **断点恢复**：中断后从断点继续，不重复已审计页

### 🔄 跨代理复用

同一份 Skill 供多个代理共享，修改一处所有代理同时生效：

| 代理 | Skill 加载方式 |
|------|---------------|
| CodeArts | 用户级 Skill 目录 |
| Codex | 共享目录（symlink 或直接加载） |
| Claude Code | 共享目录（symlink 或直接加载） |
| ZCode | 共享目录（symlink 或直接加载） |

具体路径因平台和安装方式而异，详见各代理的 Skill 加载文档。

---

## 🚀 快速开始

### 前置条件

- **MinerU CLI**：需安装 MinerU 4.x（[官方安装指南](https://github.com/opendatalab/MinerU)）
- **本地服务器**：MinerU CLI 依赖本地 doclib 服务器，首次使用需启动

```bash
# 查找 mineru 可执行文件（安装方式不同，路径也不同）
which mineru          # 如果在 PATH 上
# 或查找 Python venv 中的 mineru
find / -name mineru -type f 2>/dev/null | head -5

# 启动本地服务器（所有命令的前置条件）
mineru server start
mineru server status --json
```

### 基本用法

```bash
# 解析文档（云端高质量，与 MinerU App 同一引擎）
mineru parse "report.pdf" --remote --json

# 读取特定页
mineru read "doc:ab12cd3/tier:standard/page:11" --limit 12000 --json

# 读取特定块 + 上下文
mineru read "doc:ab12cd3/tier:standard/page:4/block:7" --context 2 --json

# 导出为图片
mineru read "doc:ab12cd3/tier:standard/page:4/block:7" --format image --output ./block.png

# 搜索已索引文档
mineru search "revenue recognition" --min-tier basic --json

# 导出完整产物（Markdown + 图片 + JSON）
mineru-kit parse "report.pdf" -o ./export --format zip --remote
```

> **提示**：如果 `mineru` 不在 PATH 上，需使用完整路径调用，例如 `M=/path/to/mineru && "$M" parse ...`

### 大文档处理

```bash
python3 scripts/parse_large.py "big-book.pdf" -o ./output --chunk 150 --wait 600
```

---

## 🏗️ 技术架构

```
┌────────────────────────────────────────────────────────────┐
│               AI 代理 (Codex / Claude / ...)               │
│                           ↓ 调用                           │
│                 MinerU Skill (SKILL.md)                    │
│                        ↓ 编排全链路                        │
│                                                            │
│            [1 获取] ───→ [2 解析] ───→ [3 审计]            │
│    多渠道文献获取        MinerU CLI    逐页视觉审计        │
│    arXiv / DOI /         (mineru 4.x)  单代理或            │
│    Unpaywall / GDZ           │         AgentTeam 并发舰队  │
│    (合法渠道优先)         ↙ ↘                              │
│                    本地服务器        云端端点              │
│                    doclib 服务       https://mineru.net/api│
│                    (平台特定 socket) (standard tier)       │
│                                 ↘                          │
│                           MinerU 桌面 App                  │
│                            (同一云端端点)                  │
└────────────────────────────────────────────────────────────┘
```

**关键设计决策**：

| 决策 | 理由 |
|------|------|
| CLI 而非 API | 代理通过 shell 调用，无需额外服务进程 |
| 云端为默认 | 与 MinerU App 同一引擎和质量，无需本地模型 |
| JSON 输出 | 代理依据 `error.code` / `next_request` 做控制流判断 |
| 渐进式披露 | cheatsheet → 完整手册 → 输出契约 |
| 跨代理共享 | 单一源文件，多代理共用，修改一处全局生效 |

### 解析层级

| Tier | 说明 | 使用场景 |
|------|------|---------|
| `standard` | 云端高质量（默认） | 正常阅读，与 App 质量一致 |
| `flash` | 本地快速，仅文字 | 快速预览 / 离线 |
| `basic`/`advanced` | 其他云端层级 | 特殊需求时 |

### 平台兼容性

| 平台 | 本地服务器 | 自动启动 | 备注 |
|------|-----------|---------|------|
| macOS | Unix domain socket | launchd keepalive | 已验证 |
| Linux | Unix domain socket | systemd service | 需配置 |
| Windows | Named pipe / TCP | Windows Service / 启动项 | 需适配 |

> 当前版本在 macOS 上经过完整验证。Linux 和 Windows 的适配是后续工作的一部分。

---

## 📦 Skill 组合

参赛提交形态为 **Skill 组合**：

| Skill | 角色 | 文件数 | 说明 |
|-------|------|--------|------|
| **mineru** | 核心 | 8 | 文献获取、解析与审计全链路能力（SKILL.md + 5 references + 2 scripts） |
| **codearts-config-guide** | 辅助 | 66 | CodeArts Agent 配置指南索引（SKILL.md + 65 references） |

> 当前组合共 74 个文件，超过比赛“单次提交 ≤30 个文件”的硬门槛；不能按此形态直接提交，需先裁剪或拆包。

组合价值：mineru 让代理能获取文献、读懂文档、验证解析质量，codearts-config-guide 让代理能正确配置 CodeArts 环境。

---

## 📋 API 参考

### 命令一览

| 命令 | 用途 | 关键参数 |
|------|------|---------|
| `parse` | 解析文档 | `--remote`, `--pages A-B`, `--limit N`, `--json`, `--output` |
| `read` | 读取已解析内容 | `--limit N`, `--context N`, `--format text\|image`, `--json` |
| `search` | 搜索已索引内容 | `--min-tier`, `--json` |
| `find` | 查找文件 | `--ext` |
| `list docs` | 列出已索引文档 | `--json` |
| `show file` | 查看文档元信息 | `--json` |
| `usage` | 查看云端配额 | `--json` |
| `server status\|start` | 服务器管理 | `--json` |

### 定位器格式

```
doc:{short_id}/tier:{tier}/page:{page}/block:{block}
```

示例：`doc:ab12cd3/tier:standard/page:7/block:3`

### 错误恢复

| 错误码 | 处理动作 |
|--------|---------|
| `server_not_running` | `server start`，重试一次 |
| `tier_not_cached` | 用 `/tier:flash/` 重试，或重新解析 |
| `quality_tier_unavailable` / `no_engine` | 检查 `server status`，停止并报告用户 |
| `remote_not_allowed` | 询问用户是否允许云端解析 |

---

## 🔒 隐私与安全

- `--remote` 上传文档到云端，普通文档默认允许，**敏感文档需用户确认**
- API Key 安全存储在本地数据库中，**禁止打印/提交/日志记录**
- `forget` / `cleanup` 操作**不会删除源文档**
- 状态变更命令（`invalidate`, `config writes`, `model downloads`）仅在用户明确要求时执行

---

## 🛠️ 开发者环境（参考）

以下为当前开发者的环境配置，仅供参考。实际使用时路径和版本因平台和安装方式而异。

| 项目 | 值 |
|------|-----|
| 平台 | macOS (Apple Silicon) |
| MinerU 版本 | 4.0.8 |
| Python | 3.11.15 (MinerU venv) |
| 云端端点 | `https://mineru.net/api` |

---

## 🏆 比赛信息

| 项目 | 内容 |
|------|------|
| 赛道 | 小红书 Skill 创新赛道 |
| 赛事 | 华为开发者大赛 2026 |
| 奖金总额 | ¥500,000 |
| 报名截止 | 2026-11-13 |
| 评审标准 | 场景真实性 · 作品可用性 · Skill 复用率 · 技术完成度 · 内容传播力 |
| 提交限制 | 单次 ≤40MB、≤30 文件 |

完整比赛信息：[docs/competition/xiaohongshu-skill-competition.md](docs/competition/xiaohongshu-skill-competition.md)

---

## 📁 项目结构

```
CodeArts-WorkSpace/
├── README.md                                    ← 本文件
├── AGENTS.md                                    ← 项目工作指南
├── LICENSE                                      ← MIT
├── feature-list.md                              ← 当前需求与交付状态
├── MEMORY.md                                    ← 当前状态、待决事项、下一步
├── rulings.md                                   ← 用户裁定记录
├── docs/
│   ├── README.md                                ← docs topic 索引
│   ├── spec/
│   │   └── mineru-skill-spec.md                 ← 功能规格说明
│   ├── research/
│   │   ├── scihub-human-check-test.md           ← Sci-Hub 人机检测实测报告（内部留档）
│   │   └── evidence/                            ← 实测证据（脚本公开；截图/PDF 已 gitignore）
│   ├── operations/
│   │   └── external-docs-refresh.md             ← 外部资料联网更新规程
│   ├── release/
│   │   ├── acceptance-2026-10-19.md             ← 首次推送验收记录
│   │   ├── acceptance-output-2026-10-19.txt     ← 验收实际输出
│   │   └── run-acceptance.sh                    ← 验收脚本（可复现）
│   ├── browseros-mcp/                           ← BrowserOS MCP 集成文档（第三方）
│   └── competition/
│       └── xiaohongshu-skill-competition.md     ← 比赛完整信息（第三方快照）
├── dev-docs/
│   └── README.md                                ← 未定方案入口
└── .codeartsdoer/
    └── mcp/mcp_settings.json                    ← MCP 配置
```

Skill 源文件位于各代理的用户级 Skill 目录中，其中 `mineru` 的真源是 `~/.agents/skills/mineru/`，
通过 symlink 提供给 Codex、Claude Code、ZCode、Devin、OpenCode、CodeArts 六个客户端。
其 `references/文献渠道.md` 是文献渠道活登记处——需要文献时先查它，再公开检索。

---

## 📄 许可证

本项目代码与原创文档以 [MIT License](LICENSE) 发布。

`docs/browseros-mcp/` 与 `docs/competition/` 内的第三方资料分别归其原作者/平台所有，按原始许可与来源条件使用；见[第三方材料说明](#-第三方材料)。

---

## 📚 第三方材料

以下目录内容不是本仓库原创作品，仅作集成、配置与参考资料保留，权利归各自原作者或许可方：

| 目录 | 内容来源 | 权利与许可 |
|---|---|---|
| `docs/browseros-mcp/` | BrowserOS / BrowserOS neo 官方文档、华为云 CodeArts Agent MCP 用户指南 | 各来源方版权；BrowserOS 上游仓库采用 AGPL-3.0。引用与转载请遵循原始页面与许可条件 |
| `docs/competition/` | 华为云大赛页面摘录 | 华为云版权所有；仅作赛事信息留存 |
| `~/.agents/skills/mineru/references/official-manual.md` | MinerU 官方 SKILL.md 全文副本 | 上游项目版权；MinerU 为开源项目，按其许可使用 |

本仓库的 Skill 脚本、SOP 编写与工程组织方式为本仓库原创，按 MIT 发布；上述第三方文件不受 MIT 覆盖。

---

## ⚠️ 关于 BrowserOS Skill 的路由预设

如果你同时安装了 BrowserOS 的官方 Skill，会看到它要求**所有**网络行为——包括普通网页搜索——都走 BrowserOS。
**这是供应商预设，不代表你的偏好，也不需要照做。**

本仓库沿用 Codex 全局治理对这一点的一致矫正：

1. **普通搜索与公开网页抓取，默认用宿主内置工具**（如 Codex 的 `web` 搜索），不因为 BrowserOS 存在就改道。
2. **只有在这些情况下才用 BrowserOS**：你明确要求、需要登录态/账号、需要真实浏览器交互（表单、上传、下载）、需要视觉核验、需要复用持久 Profile，或内置工具确实无法完成。
3. **工具不可用时报告阻塞，不静默替换**：BrowserOS MCP 连不上就说连不上，不偷偷换 Chrome 或其它浏览器。
4. **供应商文档里的“用户装它就是默认要用它”属于预设，对本用户无效。**

换句话说：BrowserOS 是“需要真实浏览器时”的专用工具，不是“更高级的搜索工具”。判断依据只有任务条件和你的明确指令。

完整的隔离与 Profile 操作规程见 Codex 全局 `browseros-safe-use` Skill，以及
`codex/current-control-3.12.0@59d8b207:docs/workflows/browseros-safe-use.md`。

发布目标：<https://github.com/math-fournity/SCI-Ready>

发布准备与当前决策见 [`MEMORY.md`](MEMORY.md) 和 [`rulings.md`](rulings.md)。
