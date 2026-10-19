# BrowserOS MCP + CodeArts Agent 配置文档

## 概述

本目录包含 BrowserOS neo MCP 服务器与华为云码道（CodeArts Agent）集成的完整文档。

- **CodeArts Agent**：华为云的 AI 编码智能体，支持 MCP 协议扩展工具能力
- **BrowserOS neo**：专为 AI Agent 设计的浏览器，通过 MCP 协议让 AI 操控真实浏览器（含登录状态）

## 当前配置

### MCP 配置文件路径

```
/Users/aurolafly/CodeArts-WorkSpace/.codeartsdoer/mcp/mcp_settings.json
```

### 配置内容

```json
{
  "mcpServers": {
    "browseros-neo": {
      "url": "http://127.0.0.1:9210/mcp",
      "type": "streamableHttp"
    }
  }
}
```

### 关键端口信息

BrowserOS neo 在本机监听的端口（来自 `~/Library/Application Support/BrowserClaw/.browseros/config.json`）：

| 端口 | 用途 |
|------|------|
| 9210 | MCP Server（AI Agent 连接端点） |
| 9115 | CDP（Chrome DevTools Protocol） |
| 9010 | Proxy |

> **注意**：官方文档默认端口为 9200，但实际安装后端口可能不同。请以 `config.json` 中的 `ports.server` 值为准。

## 配置步骤

### 1. 安装 BrowserOS neo

```bash
brew tap browseros-ai/tap
brew install --cask browseros-neo
```

或直接下载：https://cdn.browseros.com/download/BrowserOS_neo.dmg

### 2. 启动 BrowserOS neo

打开 BrowserOS neo 应用，它会自动启动 MCP Server。

### 3. 确认 MCP 端点

查看配置文件获取实际端口：

```bash
cat ~/Library/Application\ Support/BrowserClaw/.browseros/config.json
```

找到 `ports.server` 字段，MCP 端点为 `http://127.0.0.1:<port>/mcp`。

### 4. 配置 CodeArts Agent

在 CodeArts IDE 中：

1. 点击右上角设置图标 → 进入全局设置
2. 左侧导航选择 **MCP 工具**
3. 点击 **配置 MCP** → 打开 `mcp_settings.json`
4. 添加 BrowserOS MCP 配置（见上方"配置内容"）
5. 保存（Cmd+S），等待工具启动完成

### 5. 使用

在 CodeArts 智能体模式下输入指令，例如：

```
打开 https://codearts.huaweicloud.com，提取产品的核心功能描述文本
```

## BrowserOS neo 提供的 MCP 工具

| 工具 | 功能 |
|------|------|
| `run` | 异步 JavaScript 脚本执行（首选，可组合完整操作流程） |
| `tabs` | 标签页管理（新建、列表、切换） |
| `navigate` | 页面导航 |
| `snapshot` | 页面无障碍树快照（含交互元素 ref 句柄） |
| `act` | 执行页面操作（点击、填写、按键、悬停等） |
| `evaluate` | 页面上下文 JavaScript 执行 |
| `read` | 页面内容提取为 Markdown |
| `grep` | 页面内容搜索 |
| `screenshot` | 页面截图 |
| `pdf` | 页面存为 PDF |
| `download` | 下载文件 |
| `upload` | 上传文件 |
| `wait` | 等待条件满足 |
| `windows` | 窗口管理 |
| `diff` | 页面变化对比 |
| `history` | 历史记录 |
| `name_session` | 命名会话 |
| `tab_groups` | 标签页分组 |
| `request_human_help` | 请求人工协助（登录、验证码等） |
| `await_human_help` | 等待人工协助完成 |
| `save_skill` | 保存可重复任务 |
| `mark_skill_run` | 标记技能运行 |

## 核心使用模式

### 基本循环：snapshot → act → verify

1. `snapshot`：渲染页面为无障碍树，交互元素带 `[ref=eN]` 句柄
2. `act`：通过 ref 驱动元素（点击、填写、按键等）
3. `act` 返回变化 diff — 信任它，不要盲目重新 snapshot

### 首选 `run`，粒度工具作为后备

`run` 是异步 JavaScript 脚本，可以组合完整操作循环（观察、操作、导航、读取、等待、批量提取）。只有在单步操作或调试时才使用粒度工具。

## 注意事项

- BrowserOS neo 必须在运行状态，MCP 连接才能生效
- BrowserOS neo 可以导入 Chrome 登录状态，AI 可使用已登录账号操作网页
- 所有数据存储在本地 `~/.browserclaw/`，不上传云端
- 建议同时启用的 MCP 不超过 8 个，3 个可获得最优体验
- 服务器名称不能超过 64 个字符

## 文档索引

| 文件 | 说明 |
|------|------|
| `codearts-mcp-ide-guide.md` | CodeArts Agent IDE MCP 配置指南（Markdown） |
| `codearts-mcp-ide-guide.html` | CodeArts Agent IDE MCP 配置指南（HTML） |
| `codearts-mcp-cli-guide.md` | CodeArts Agent CLI MCP 配置指南（Markdown） |
| `codearts-mcp-cli-guide.html` | CodeArts Agent CLI MCP 配置指南（HTML） |
| `codearts-mcp-cli-commands.html` | CodeArts Agent CLI MCP 命令参考（HTML） |
| `browseros-readme.md` | BrowserOS GitHub README |
| `browseros-mcp-connect.html` | BrowserOS MCP 连接指南 |
| `browseros-manual-url-setup.html` | BrowserOS 手动 URL 设置 |
| `browseros-claude-desktop.html` | BrowserOS Claude Desktop 扩展 |
| `browseros-install.html` | BrowserOS 安装指南 |
| `browseros-how-it-works.html` | BrowserOS 工作原理 |
| `browseros-dashboard.html` | BrowserOS 仪表盘 |
| `browseros-audit-replay.html` | BrowserOS 审计与回放 |
| `browseros-privacy.html` | BrowserOS 隐私与数据 |
| `browseros-llms-index.txt` | BrowserOS 文档索引（llms.txt） |

## 参考链接

- CodeArts MCP 官方文档：https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0010.html
- BrowserOS 官网：https://www.browseros.com
- BrowserOS 文档：https://docs.browseros.com
- BrowserOS GitHub：https://github.com/browseros-ai/BrowserOS
- MCP 官方协议：https://modelcontextprotocol.io