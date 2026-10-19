# 首次推送验收记录（2026-10-19）

> 类型：发布证据（release evidence）
> 覆盖范围：本仓库对外声明的核心能力与提交门槛，不覆盖 `~/.agents/skills/mineru/` 的全部 SOP 行为。
> 执行环境：macOS (Apple Silicon)，MinerU CLI 4.0.8 / Python 3.11.15，远端 `standard` tier。

## 1. 执行方式

```bash
bash docs/release/run-acceptance.sh 2>&1 | tee docs/release/acceptance-output-2026-10-19.txt
```

脚本逐项执行并输出 `PASS`/`FAIL`；任一项失败即整体失败，不放宽判据。

## 2. 检查项与结果

| # | 检查项 | 判据 | 结果 |
|---|--------|------|------|
| A1 | `mineru` CLI 可执行 | 版本输出含 `4.0.` | 见输出文件 |
| A2 | 本地 doclib server 运行中 | `running: true` | 见输出文件 |
| A3 | 远端 parse service 健康 | `parse_server.remote.healthy: true` | 见输出文件 |
| A4 | Remote 访问级别 | `access_level` 为 `registered` 或 `anonymous`，且 `guidance` 可判读 | 见输出文件 |
| A5 | 小文档云端解析 | 1 页 PDF `--remote --json` 返回 `content` 且无 `error` | 见输出文件 |
| A6 | 页块级定位读取 | `read` 返回非空 content | 见输出文件 |
| A7 | 分块参数正确传递 | `parse_large.py` 含 `--pages` 与大 `--limit` | 见输出文件 |
| A8 | JSON 控制流契约 | `--json` 输出可解析，含 `parse`/`content` 或 `error` 字段 | 见输出文件 |
| A9 | 参赛文件数门槛 | Skill 文件数 ≤30 或明确记录为未闭合阻塞 | ❌ 未闭合（74 > 30），见 `feature-list.md` |
| A10 | 提交体积门槛 | 单次提交 ≤40MB | ✅ `mineru` 121,927 B + `guide` 832,030 B ≈ 0.91 MB |

## 3. 未覆盖项（诚实边界）

- 视觉审计（F12）与并发舰队（F13）未在本文件中端到端复跑，其状态在 `feature-list.md` 中标为
  `implemented` 而非 `verified`；
- Linux / Windows 平台的 server 自动启动未验证；
- `docs/browseros-mcp/` 等第三方快照的时效性未在本文件中更新（按
  `docs/operations/external-docs-refresh.md` 由用户授权后刷新）。

## 4. 结论

A1–A8、A10 由本次实际执行证明；A9 为已知未闭合阻塞，不在本次推送范围内以“已完成”表述。
