# MinerU Skill — 功能规格说明 (Spec)

> 版本：v1.1-draft | 日期：2026-10-18
> 定位：让 AI 代理具备"获取、读取和理解文献"能力的 Skill 插件
> v1.1 变更：新增 F11 文献获取（BrowserOS 多渠道）、F12 转换后视觉审计、F13 并发舰队验证——Skill 从"文档解析"升级为"文献获取→解析→审计"全链路

## 1. 产品定位

MinerU Skill 是一个 **面向 AI 代理的文献读取能力插件**。它让 Codex、Claude Code、ZCode、CodeArts 等代理具备**获取文献**（BrowserOS 多渠道下载）、**解析文档**（PDF/Word/PPT/Excel → Markdown）、**验证质量**（二值化视觉审计 + 并发舰队）的全链路能力，输出结构化 Markdown 和精确引用定位。

**不是什么**：不是 RAG 框架，不是 chat-with-doc 应用，不是给人类直接使用的 GUI 工具。
**是什么**：是 AI 代理的"眼睛+手"——让代理能找到文献、读懂内容、引用段落、处理大篇幅文件，并自我验证解析质量。

## 2. 核心功能 (Features)

### F1. 多格式文档解析

| 功能 | 说明 | 状态 |
|------|------|------|
| PDF → Markdown | 支持文字版和扫描版 PDF | ✅ 已有 |
| Word → Markdown | .docx/.doc 格式 | ✅ 已有 |
| PPT → Markdown | .pptx/.ppt 格式 | ✅ 已有 |
| Excel → Markdown | .xlsx/.xls 格式 | ✅ 已有 |
| EPUB → Markdown | 电子书格式 | ✅ 已有 |
| HTML/MHTML → Markdown | 网页格式 | ✅ 已有 |
| CSV → Markdown | 表格数据 | ✅ 已有 |
| OFD → Markdown | 开放版式文档 | ✅ 已有 |

**输出质量**：默认使用云端 `standard` tier（与 MinerU 桌面 App 同一引擎和端点），支持 LaTeX 公式提取。

### F2. OCR 与版面识别

| 功能 | 说明 | 状态 |
|------|------|------|
| 扫描件 OCR | 识别扫描版 PDF 和图片中的文字 | ✅ 已有 |
| LaTeX 公式提取 | 数学公式转为 LaTeX 语法 | ✅ 已有 |
| 表格结构识别 | 保持表格结构输出 | ✅ 已有（依赖引擎） |
| 图片提取 | 提取文档中的图片资源 | ✅ 已有 |
| 版面布局还原 | 保持原文档的版面结构 | ✅ 已有（依赖引擎） |

### F3. 精确引用定位

| 功能 | 说明 | 状态 |
|------|------|------|
| 页/块级定位 | `doc:{id}/tier:{tier}/page:{page}/block:{block}` 格式 | ✅ 已有 |
| 定位读取 | 通过 locator 读取特定页/块内容 | ✅ 已有 |
| 上下文扩展 | `--context N` 参数读取周围 N 个块 | ✅ 已有 |
| 图片导出 | `--format image` 导出页/块为图片 | ✅ 已有 |
| 连续阅读 | `next_request` 标记自动续读 | ✅ 已有 |

### F4. 大文档分块处理

| 功能 | 说明 | 状态 |
|------|------|------|
| 自动分块 | >200 页文档自动按 chunk 分块解析 | ✅ 已有 |
| 分块合并 | 各 chunk 的 Markdown 自动合并，页码连续 | ✅ 已有 |
| 大 limit 支持 | `--limit 100000000` 避免默认截断 | ✅ 已有 |
| 长等待支持 | `--wait 600` 适应大块解析耗时 | ✅ 已有 |
| 瞬态错误重试 | 自动重试 3 次瞬态错误 | ✅ 已有 |
| 智能分块策略 | 按章节/段落边界分块而非固定页数 | 🔲 待实现 |
| 进度反馈 | 长时间解析任务的进度报告 | 🔲 待实现 |

### F5. 搜索与发现

| 功能 | 说明 | 状态 |
|------|------|------|
| 内容搜索 | `search` 在已索引文档中搜索关键词 | ✅ 已有 |
| 文件查找 | `find` 按文件名/扩展名查找 | ✅ 已有 |
| 文档列表 | `list docs` 列出所有已索引文档 | ✅ 已有 |
| 文档详情 | `show file` 查看文档元信息 | ✅ 已有 |

### F6. 导出与批量

| 功能 | 说明 | 状态 |
|------|------|------|
| 单文件导出 | `--output` 导出为 Markdown 文件 | ✅ 已有 |
| ZIP 包导出 | `mineru-kit` 导出完整产物（md + images + JSON） | ✅ 已有 |
| 批量处理 | `mineru-kit` 支持批量操作 | ✅ 已有 |

### F7. 跨代理复用

| 功能 | 说明 | 状态 |
|------|------|------|
| 共享机制 | 同一份 Skill 供多个代理使用（symlink 或直接加载） | ✅ 已有 |
| 统一命令接口 | 所有代理使用相同的 CLI 命令 | ✅ 已有 |
| JSON 输出 | `--json` 参数输出结构化 JSON | ✅ 已有 |
| 错误码体系 | `error.code` / `retryable` / `user_action` | ✅ 已有 |
| 渐进式披露 | cheatsheet → references → 完整手册 | ✅ 已有 |

### F8. 隐私与安全

| 功能 | 说明 | 状态 |
|------|------|------|
| 云端/本地选择 | `--remote` 云端 vs `--local` 本地 | ✅ 已有 |
| 敏感文档确认 | 敏感文档需用户确认后才上传 | ✅ 已有 |
| API Key 安全 | 本地安全存储，禁止打印/提交/日志 | ✅ 已有 |
| 禁止泄露 Key | SKILL.md 明确禁止打印/提交 Key | ✅ 已有 |

### F9. 健壮性与运维

| 功能 | 说明 | 状态 |
|------|------|------|
| 服务器自动启动 | 平台原生机制自动启动本地服务器 | ✅ 已有（macOS） |
| 瞬态错误恢复 | `internal_error`/`remote_unreachable` 自动重试 | ✅ 已有 |
| 错误恢复指南 | SKILL.md 内置错误码→动作映射表 | ✅ 已有 |
| 跨平台适配 | Linux/Windows 的服务器管理和自动启动 | 🔲 待实现 |

### F10. 文档结构大纲（待实现）

| 功能 | 说明 | 状态 |
|------|------|------|
| 自动生成大纲 | 解析后自动生成文档目录/大纲 | 🔲 待实现 |
| 大纲导航 | 通过大纲快速定位到特定章节 | 🔲 待实现 |

### F11. 文献获取（BrowserOS 多渠道）

通过 BrowserOS MCP 操作浏览器，按渠道优先级获取文献全文，给定文献 ID（DOI/arXiv ID/PPN）即可落地 PDF：

| 功能 | 说明 | 状态 |
|------|------|------|
| arXiv 优先 | 免费 channel 优先：arXiv ID / 出版社开放获取版本 | ✅ 已有 |
| DOI → SciHub 渠道 | 遇收费墙先拿 DOI，再经 sci-hub.jp 获取；含人机检测应对方法 | 🔲 编写中（实测中） |
| GDZ 哥廷根渠道 | 历史文献扫描件：IIIF 图像 API（`manifests.sub.uni-goettingen.de/iiif/image/gdz:{PPN}:{序号}/full/2000,/0/default.jpg`） | ✅ 已有（实测） |
| 渠道降级策略 | 免费渠道 → DOI 解析 → 镜像站轮询 → 请求人类协助 | 🔲 编写中 |
| 下载验证 | `file`/`pdfinfo` 验证 PDF 有效性、页数、大小 | ✅ 已有 |
| 人机检测应对 | 记录检测类型→等待/点击/换镜像/请求人类协助的决策树 | 🔲 编写中（实测中） |
| 获取台账 | 每次获取记录：文献 ID、渠道、时间、结果、SHA-256 | 🔲 编写中 |

**法律边界**：sci-hub 在部分司法辖区有版权争议，Skill 文档须明示"仅限个人研究用途、优先合法渠道（arXiv/出版社开放获取/机构仓储/GDZ 公共领域）"。

### F12. 转换后视觉审计（PDF→Markdown 质量验证）

把 PDF 每页渲染为二值化 PNG，用视觉模型逐页比对 MinerU 输出与页面原文：

| 功能 | 说明 | 状态 |
|------|------|------|
| 二值化管线 A（高质量） | `pdftoppm -png -gray -r 300` → `magick -threshold 50% -strip -define png:bit-depth=1 -compress zip`；实测 751KB/页，阈值 40/50/60% 校准数据完整 | ✅ 已有（实测） |
| 二值化管线 B（快速） | `gs -sDEVICE=pngmono -r150` 单命令直出 | ✅ 已有（实测） |
| 逐页审计循环 | 渲染→读图→定位 md 段→五点比对→落签→分级→下一页 | ✅ 已有 |
| 三级分级 | PASS（吻合）/ PASS±（瑕疵不误导）/ FAIL（内容错误/丢段） | ✅ 已有 |
| 高 DPI 局部放大 | `pdftoppm -r 600 -x -y -W -H` 局部重渲染（非放大已有图），公式/脚注精查 | ✅ 已有 |
| 局部 MinerU 技巧 | 无视觉模型时：高 DPI 局部图交给 MinerU OCR，结果仅作比对参考（定位器不对应原页，须标注"局部交叉印证"） | ✅ 已有 |
| 工具边界适配 | analyzeImage 对整页大图返回空、对裁剪局部图正常——审计优先读条带裁剪图 | ✅ 已有（实测） |
| 审计范围裁剪 | 全审→关键词抽样±2页→定向证据句核查的三级成本决策 | ✅ 已有 |
| 修复闭环 | FAIL 必修 md + 独立提交 + 修复登记（可追溯链） | ✅ 已有 |

### F13. 并发舰队验证（AgentTeam 模式）

CodeArts AgentTeam 假设：大文档逐页视觉验证必须由多子代理舰队并发完成：

| 功能 | 说明 | 状态 |
|------|------|------|
| 文件分片互斥 | 一页一文件 `pages/<pdf>/p-NNN.md` 天然无冲突；总账本由 Team Leader 独占（单一 CANONICAL_INTEGRATOR） | 🔲 编写中 |
| 页区间分配模式 | 单份大 PDF 按 `p1-50/p51-100/...` 切区间，每区间一个子代理 | 🔲 编写中 |
| 文档分配模式 | 多份 PDF 时每份一个子代理（单篇单 Peer） | 🔲 编写中 |
| 分账本合并 | 子代理各写分账本，Team Leader 定期合并，避免并发 append 损坏 | 🔲 编写中 |
| 修复串行化 | 审计子代理只报告不修复；md 修复由 Team Leader 串行执行 | 🔲 编写中 |
| 断点恢复协议 | append-only 分账本，接力者读末尾行即知"哪份/哪页/最后等级" | 🔲 编写中 |
| 子代理续命 | 失败子代理用 session_id 恢复上下文，不新起代理重做 | 🔲 编写中 |
| 并发度控制 | 3-5 个子代理（实测经验值），页数÷区间估算数量 | 🔲 编写中 |

## 3. API 设计原则

### 命令接口

所有功能通过 CLI 命令暴露，遵循统一模式：

```bash
# 解析
mineru parse <file> [--remote] [--pages A-B] [--limit N] [--json] [--output <path>]

# 读取
mineru read <locator> [--limit N] [--context N] [--format text|image] [--json]

# 搜索
mineru search <query> [--min-tier <tier>] [--json]
mineru find <pattern> [--ext <ext>]

# 管理
mineru list docs [--json]
mineru show file <file> [--json]
mineru usage [--json]
mineru server status|start [--json]
```

> **注意**：`mineru` 可执行文件的路径因安装方式和平台而异。如果不在 PATH 上，需使用完整路径调用。

### 输出契约

- **JSON 模式**（`--json`）：所有命令支持 JSON 输出，包含 `data`、`error`、`next_request` 字段
- **错误处理**：分支依据 `error.code` / `retryable` / `user_action`，不依据自然语言描述
- **续读标记**：`next_request` / `<!-- Next: ... -->` 标记下一步操作，代理跟随即可
- **定位器格式**：`doc:{short_id}/tier:{tier}/page:{page}/block:{block}`

### 渐进式信息披露

```
SKILL.md (cheatsheet)
  → references/official-manual.md (完整手册)
    → references/output-schema.md (输出目录契约)
  → references/lit-acquisition.md (文献获取 SOP：渠道优先级/人机检测/台账)
  → references/visual-audit.md (视觉审计 SOP：二值化管线/高DPI局部/局部MinerU技巧)
  → references/audit-fleet.md (并发舰队 SOP：分片互斥/调度循环/断点恢复)
```

代理先读 cheatsheet 即可完成大部分工作；需要深入细节时再读 references。

## 4. 跨平台兼容性

| 平台 | 本地服务器通信 | 自动启动机制 | 状态 |
|------|--------------|------------|------|
| macOS | Unix domain socket | launchd keepalive | ✅ 已验证 |
| Linux | Unix domain socket | systemd service | 🔲 待适配 |
| Windows | Named pipe / TCP loopback | Windows Service / 启动项 | 🔲 待适配 |

跨平台适配是后续工作的一部分。核心 CLI 命令和云端解析功能在所有平台上均可使用，差异仅在于本地服务器的通信方式和自动启动机制。

## 5. Skill 组合架构

参赛提交形态为 **Skill 组合**：

| Skill | 角色 | 说明 |
|-------|------|------|
| **mineru** | 核心 | 文档解析与读取能力 |
| **codearts-config-guide** | 辅助 | CodeArts Agent 配置指南索引（15 类 65 篇） |

组合的价值：mineru 让代理能读懂文档，codearts-config-guide 让代理能正确配置 CodeArts 环境，两者配合形成"文档理解 + 环境配置"的完整能力闭环。

## 6. 提交约束

| 约束 | 限制 | 当前 mineru Skill 状态 |
|------|------|----------------------|
| 文件总大小 | ≤40MB | 需评估（预计 <5MB，均为文本/脚本） |
| 文件数量 | ≤30 个 | ❌ 当前 `mineru` 8 + `codearts-config-guide` 66 = 74 个；提交前必须裁剪或拆包 |
| 原创性 | 必须原创 | ✅ |
| 可运行 | 必须可运行 | ✅（需 MinerU CLI 安装） |
| 可复用 | 必须可复用 | ✅（跨代理共享） |

## 7. 待实现功能优先级

| 优先级 | 功能 | 理由 |
|--------|------|------|
| P0 | 文献获取渠道整合（F11） | 全链路入口：给定 ID 即得 PDF |
| P0 | 并发舰队验证（F13） | AgentTeam 假设下的审计效率基础 |
| P1 | 文档结构大纲 | 自动生成目录，便于代理导航大文档 |
| P1 | 进度反馈 | 长时间解析任务的进度报告 |
| P1 | 跨平台适配 | Linux/Windows 的服务器管理和自动启动 |
| P2 | 增量解析 | 只解析新增/变更页面 |
| P2 | 批量处理增强 | 更完善的批量操作接口 |

## 8. 评审标准对标

| 评审维度 | 对标措施 |
|----------|---------|
| 场景真实性 | 真实文档处理工作流（获取→解析→审计），已实测 289 页文档端到端 + 692 页二值化审计参数标定 |
| 作品可用性 | 一行命令解析文档，清晰的错误恢复指南，自动运维，人机检测决策树 |
| Skill 复用率 | 六个客户端入口共享同一真源，统一 JSON API，渐进式披露，审计/舰队 SOP 可移植到任何 PDF 项目 |
| 技术完成度 | SKILL.md + 官方手册 + 输出契约 + 分块脚本 + 3 份新增 references（文献获取/视觉审计/舰队） |
| 内容传播力 | README.md 混合型展示 + 真实使用场景演示 + 多代理舰队工作范式 |
