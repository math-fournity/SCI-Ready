# Sci-Hub 人机检测实测报告 —— MinerU Skill 文献获取 SOP 依据

> **报告性质**：真实浏览器实测记录，所有结论均有一手证据支撑（截图、HTTP 响应、PDF 元数据）。
> **核心结论**：`sci-hub.jp` 已死亡（广告停放页）；可用镜像是 `sci-hub.ru`（推荐，AI 自动化最友好）和 `sci-hub.st`。人机检测共发现 3 层机制，全部可由 AI 自动通过，无需人类协助。

---

## 1. 测试时间与环境

| 项目 | 值 |
|------|-----|
| 测试时间 | **2026-10-18 10:43 – 11:00 UTC**（本地 06:43–07:00，America/New_York） |
| 浏览器 | BrowserOS neo v0.0.72（Chromium 内核，真实浏览器指纹） |
| MCP 端点 | `http://127.0.0.1:9210/mcp`（streamable HTTP） |
| MCP 工具链 | `tabs` / `navigate` / `snapshot` / `act` / `evaluate` / `grep` / `read` / `screenshot` / `download` / `wait` |
| 命令行工具 | curl（macOS 自带）、`file`、`pdfinfo`（poppler）、`mdls` |
| 网络环境 | 美国东部云网络（出口 IP 由 ddg9 cookie 泄露，此处从略） |
| 工具链备注 | CodeArts 内置 MCP 客户端会话句柄过期（"Session not found"），本次实测通过**自建 Python MCP 客户端**（重新 initialize 握手维护会话 ID）驱动同一 BrowserOS 实例完成。脚本见附录 D |

**⚠️ 时效性声明**：sci-hub 各域名可用性变化极快（本报告实测 `.se` 已 DNS 死亡、`.jp` 已沦为广告页）。本报告结论仅保证在上述测试时间点真实，Skill 每次执行时应按 §5 流程卡片的"存活探测"步骤重新确认。

---

## 2. 四个域名的存活状态总览

| 域名 | 状态 | 服务器/CDN | 人机检测 | 结论 |
|------|------|-----------|---------|------|
| `sci-hub.jp` | ❌ **死亡** | ddos-guard | 无（不值得检测） | 域名已沦为**广告停放页**：标题 "Science Hub"，正文只有 a-ads.com 加密货币广告 iframe，无任何 sci-hub 功能 |
| `sci-hub.se` | ❌ **死亡** | — | — | **DNS NXDOMAIN**（域名已从 DNS 消失，`nslookup` 确认） |
| `sci-hub.st` | ✅ 可用 | DDoS-Guard | 三层（见 §3） | 功能完整，但网络层 DDoS-Guard 会拦截一切非浏览器请求（含 PDF 直链 curl） |
| `sci-hub.ru` | ✅ **可用（推荐）** | 自建（无明显 CDN challenge） | 应用层 ALTCHA（见 §3） | 功能完整，**PDF 直链无需 cookie 即可 curl 直接下载**，AI 自动化最友好 |

**镜像关系**：`.st` 与 `.ru` 共享同一论文数据库与存储路径结构（同一 DOI 的 storage 路径完全一致：`/storage/zero/6657/ae3953e2190143a462dcebd18f7c4495/silver2016.pdf`），只是域名和防护层不同。**一个镜像查不到的论文，另一个也查不到**（数据库相同）。

---

## 3. 人机检测类型与通过方法总结（核心发现）

实测共遇到 **3 种不同层级的检测机制**：

### 3.1 DDoS-Guard 网络层 JS Challenge（仅 sci-hub.st）

- **特征**：页面标题 `DDoS-Guard`，正文 `Checking your browser before accessing sci-hub.st`，带 loading 图标和一个 "Show IP address" 按钮。curl 直接请求返回 **HTTP 403** + 902 字节 challenge 页。
- **实测通过方式**：**真实浏览器自动通过，无需任何操作**。导航后 10–29 秒内（本测一次轮询间隔内）自动跳转到目标页。
- **AI 操作要点**：导航后等待 + 轮询页面标题变化即可；**绝不要**在检测页上乱点（"Show IP address" 无用）。
- **影响范围**：DDoS-Guard 拦截**所有**非浏览器流量——包括 PDF storage 直链的 curl 下载（实测 403）。要下载 `.st` 的 PDF 必须在浏览器内完成，或复用浏览器会话的 DDoS-Guard cookie（`__ddg1_` ~ `__ddg10_`）。

### 3.2 Sci-Hub 应用层 "Are you a robot?"（sci-hub.st 与 sci-hub.ru 都有）

- **特征**：页面标题 `Sci-Hub: are you are robot?`（`.ru` 俄语版为 `Sci-Hub: проверка на робота`），正文极简：`Are you a robot?` + 一个 **"No" 链接**。触发时机：**提交 DOI 搜索时**（不是进主页时）。
- **实测通过方式**：**点击 "No" 链接** → 约 6–8 秒后自动跳转到论文页或结果页。零失败。
- **注意**：这个检测页**不会自动通过**（`.ru` 上实测等待 21 秒仍停留在检测页），必须主动点击。页面上唯一的可交互元素就是 "No"（快照中是 `generic [ref=e1] [cursor=pointer]`）。
- **这是给 AI 设计的检测**：故意做得比 Cloudflare 简单——只要客户端能正确渲染 DOM 并点击，就放行。真实浏览器 + MCP `act(click)` 完全能自动化。

### 3.3 ALTCHA 工作量证明（sci-hub.ru 的检测实现）

- `.ru` 的检测页加载 `/scripts/altcha.min.js`（[ALTCHA](https://altcha.org/)，开源 proof-of-work 验证方案，非传统验证码）。点击 "No" 后浏览器本地计算工作量证明并随请求提交，服务端校验。
- **实测表现**：点击 "No" → ~6 秒通过。**无需人类参与，无图片识别，无滑块**。

### 3.4 验证 cookie 的有效期行为

通过一次应用层检测后，服务端下发验证 cookie（`.ru` 的 `session` cookie 有效期 90 天，`.st` 类似）。**有效期内后续导航（包括直接访问论文 URL）不再触发检测**——实测通过一次后，同一浏览器会话内第二次、第三次访问论文页直接进入。这意味着：**一次点击验证，整个文献批量获取会话免检**。

---

## 4. 逐步操作记录（动作 → 观察 → 判断）

时间均为 UTC。每步附证据。

### 阶段 A：sci-hub.jp 实测（预期主目标，实际已死亡）

| # | 时间 | 动作 | 观察 | 判断 |
|---|------|------|------|------|
| A1 | 10:43:57 | MCP `tabs new` 打开 `https://sci-hub.jp/` | 页面打开，快照只有 1 个 iframe | 异常：正常 sci-hub 应有搜索框 |
| A2 | 10:44:12 | `screenshot` | 截图存档 `evidence/01_initial.jpg` | — |
| A3 | 10:44:36 | `snapshot` + `grep`（checking/captcha/cloudflare 等关键词） | **零匹配**——没有人机检测；iframe 内是 "How to build products with AI in 2026 Listen now youtu.be" | 不对劲：内容像广告 |
| A4 | 10:45:03 | `evaluate` 读 DOM | `title="Science Hub"`，`<iframe data-aa='2425588' src='//acceptable.a-ads.com/2425588/...'>`，**无 input 无 form** | **实锤：广告停放页**（a-ads.com 是加密货币广告网络） |
| A5 | 10:46:16 | `curl -I` 主页 | `HTTP 200`，`Server: ddos-guard`，正文 610B 空 HTML | ddos-guard 都懒得 challenge 这个空壳站 |
| A6 | 10:46:47 | 浏览器 + curl 双测 DOI 路径 `sci-hub.jp/10.1007/BF01449995` | 两侧均返回**同一个广告页**（广告轮换成 "Advertise in this ad space... aads.com"） | **sci-hub.jp 全站死亡，DOI 路径也无功能** |

### 阶段 B：镜像存活探测（curl）

| # | 时间 | 动作 | 观察 | 判断 |
|---|------|------|------|------|
| B1 | ~10:47 | `curl https://sci-hub.se/` | HTTP 000，`Could not resolve host`；`nslookup` → **NXDOMAIN** | 域名已消亡 |
| B2 | ~10:47 | `curl https://sci-hub.st/` | **HTTP 403**，902B，标题 `DDoS-Guard`，正文 "Checking your browser" | 活着，网络层 challenge |
| B3 | ~10:47 | `curl https://sci-hub.ru/` | **HTTP 200**，179KB，标题 `Sci-Hub`（耗时 15s，响应慢但成功） | 活着，curl 直接可达 |

### 阶段 C：sci-hub.st 浏览器全流程

| # | 时间 | 动作 | 观察 | 判断 |
|---|------|------|------|------|
| C1 | 10:48:04 | `navigate` → `https://sci-hub.st/` | 快照：`heading "Checking your browser before accessing sci-hub.st"` + loading 图标 + "Show IP address" 按钮 | **DDoS-Guard JS challenge 出现** |
| C2 | 10:48:33 | 等 10s 后检查（含工具间隔共 29s） | `title="Sci-Hub"`，正文是真实主页（捐赠地址、最近下载列表） | **challenge 已自动通过**，无需点击 |
| C3 | 10:48:58 | `snapshot mode=interactive` | 找到 `textbox "enter URL DOI" [ref=e1]` + `button "open" [ref=e2]` | 搜索框就位 |
| C4 | 10:49:11 | `act fill e1="10.1007/BF01449995"` + `act click e2` | diff 确认输入成功；点击后页面大变 | — |
| C5 | 10:49:26 | `evaluate` 读状态 | `title="Sci-Hub: are you are robot?"`，URL 未变 | **应用层机器人检测触发** |
| C6 | 10:49:45 | `snapshot` + `screenshot` | 页面仅一个可点元素（"No"）；`evidence/03_robot_check_st.jpg` | 检测页极简 |
| C7 | 10:50:21 | `act click e1`（No） | diff：检测元素移除，出现 loading image | 已提交验证 |
| C8 | 10:50:48 | 等 8s 后检查 | URL 跳到 `/10.1007/BF01449995`，`title="Sci-Hub: no articles found for your request"`，正文 "I do not have any papers matching your request :(" | **验证通过，但 Zermelo 1908 论文不在数据库**（见 §7） |

### 阶段 D：sci-hub.ru 浏览器全流程 + PDF 下载

| # | 时间 | 动作 | 观察 | 判断 |
|---|------|------|------|------|
| D1 | 10:51:08 | `curl sci-hub.ru/10.1007/BF01449995` | HTTP 200，7.3KB，标题 `Sci-Hub: проверка на робота`，加载 `altcha.min.js` | 应用层检测，ALTCHA 方案，俄语界面 |
| D2 | 10:51:45 | `navigate` → `.ru` DOI 页 | 检测页（同 C5 结构） | — |
| D3 | 10:52:14–28 | 轮询 3 次×7s（共 21s） | 始终停在 "Are you a robot?" | **不会自动通过，必须点击** |
| D4 | 10:53:14 | `act click`（No） | — | — |
| D5 | 10:53:20 | 6s 后检查 | 跳转到结果页：`no articles found` | ALTCHA 通过（~6s）；`.ru` 同样没有 Zermelo 论文 |
| D6 | 10:54:13 | `navigate` → `sci-hub.ru/10.1038/nature16961`（AlphaGo 论文，改测确定收录的 DOI） | **未再触发检测**（cookie 有效），直接论文页，快照有 `PluginObject`（PDF 内嵌预览） | 验证 cookie 复用生效 |
| D7 | 10:54:33 | `evaluate` 读论文页 | `title="Sci-Hub. Mastering the game of Go with deep neural networks and tree search / Nature, 2016"`；`embed src="https://sci-hub.ru/storage/zero/6657/ae3953e2190143a462dcebd18f7c4495/silver2016.pdf"` | **论文页正常，PDF 直链到手**；`evidence/04_paper_page_ru.jpg` |
| D8 | 10:55:44 | MCP `download` 工具点击 PDF 链接（ref e6） | **失败：`Download timed out after 60000ms. If the browser is set to ask where to save each file, it is waiting on that dialog.`** | 浏览器配置了"每次询问保存位置"，AI 无法点系统对话框——**重要失败模式** |
| D9 | 10:55:xx | `curl` 直链（无 cookie、无 referer） | **HTTP 200，2,682,222B，Content-Type: application/pdf** | **`.ru` 直链完全开放，curl 直接下载成功** ✅ |
| D10 | 10:56:xx | `file` + `pdfinfo` 验证 | 见 §8 | PDF 有效且元数据匹配 |

### 阶段 E：sci-hub.st 复验 + 直链对照

| # | 时间 | 动作 | 观察 | 判断 |
|---|------|------|------|------|
| E1 | 10:57:32 | `navigate` → `sci-hub.st/10.1038/nature16961` | 未触发检测，直接论文页，embed 直链同路径 | `.st` cookie 同样复用；两镜像共享存储路径 |
| E2 | 10:58:xx | `curl` `.st` PDF 直链 | **HTTP 403**，902B DDoS-Guard challenge HTML（不是 PDF） | **`.st` 直链被 DDoS-Guard 拦截**，与 `.ru` 形成关键差异 |

---

## 5. AI 操作流程卡片（Skill 可直接复用）

> 以下流程按"未来 AI 代理 + BrowserOS MCP 工具链"编写。MCP 内置客户端会话失效时，用附录 D 的直连脚本兜底。

### 5.0 前置：镜像存活探测（每次会话开始必做）

```
对每个候选域名（顺序：sci-hub.ru → sci-hub.st）:
  curl -s -o /dev/null -w "%{http_code}" --max-time 20 "https://<域名>/"
  - 200 → 该镜像活着（.ru 直达；.st 可能 403 但仍活着，进浏览器流程）
  - 000 + DNS 解析失败 → 域名死亡，跳过
  - 403/503 + "DDoS-Guard"/"Cloudflare" 字样 → 活着但有网络层检测，进浏览器流程
注意：sci-hub.jp / sci-hub.se 截至 2026-10-18 已死亡，不要再尝试。
```

### 5.1 标准获取流程（以 sci-hub.ru 为例，推荐）

```
步骤 1  浏览器导航到 https://sci-hub.ru/<DOI>
        （DOI 形如 10.1038/nature16961；也可先进主页用搜索框：
         snapshot → 找 textbox "enter URL DOI" → act fill → act click "open" 按钮）

步骤 2  判断页面状态（读 document.title）:
        a. "Sci-Hub: are you are robot?" / "проверка на робота"
           → 应用层检测：snapshot 找到唯一的可点元素（"No"）→ act click
           → 等待 5-15s → 重新读 title，应变为论文页或结果页
           → 若 30s 后仍是检测页，重试点击一次；仍失败 → 请求人类协助
        b. "Checking your browser" / "DDoS-Guard" / "Just a moment"（.st 才会有）
           → 网络层检测：什么都不点，轮询等待 10-30s，自动通过
        c. "Sci-Hub: no articles found for your request"
           → 该论文不在 sci-hub 数据库，换渠道（见 §6），不要换镜像重试
              （镜像数据库相同，换站无意义）
        d. "Sci-Hub. <论文标题> / <期刊>, <年份>"
           → 成功，进步骤 3

步骤 3  提取 PDF 直链（evaluate）:
        const e = document.querySelector("embed, object");
        return e ? (e.src || e.data) : null;
        → 得到 https://sci-hub.ru/storage/<...>/<文件名>.pdf

步骤 4  下载 PDF（按镜像选择方式）:
        - sci-hub.ru → curl 直链即可（无需 cookie，实测 200）:
            curl -s -o paper.pdf "<直链URL>" -A "<浏览器UA>"
        - sci-hub.st → 直链 curl 会被 DDoS-Guard 挡（403），必须:
            方案 a: 浏览器内 download 工具点击 PDF 链接
                   （前提：浏览器未开"每次询问保存位置"，否则超时失败）
            方案 b: 从浏览器导出 __ddg1_~__ddg10_ cookie 后带 cookie curl

步骤 5  验证 PDF:
        file paper.pdf          → 应为 "PDF document, version X"
        pdfinfo paper.pdf       → 页数、标题、Subject 里的 DOI 应与目标一致
        下载失败/HTML 假 PDF → 检查文件头是否 <!doctype html>（challenge 页伪装）
```

### 5.2 关键判断规则（防呆）

1. **"no articles found" ≠ 流程失败**，是数据库不收录。老论文（约 1970 年前）收录率低，直接换合法渠道。
2. **检测页不要乱点**：只点 "No"，不要点 "Show IP address" 或其它元素。
3. **验证一次管整个会话**：通过一次 "Are you a robot?" 后，同会话后续论文页直接进，无需重复验证。批量下载时先验证一次再循环。
4. **`.ru` 与 `.st` 结果一致**：一个说没有就是都没有，不要浪费时间换站重查同一 DOI。

---

## 6. 失败模式与应对

| 失败模式 | 识别特征 | 应对策略 |
|---------|---------|---------|
| **域名死亡（停放/广告）** | HTTP 200 但页面只有广告 iframe；无搜索框；a-ads.com / 域名停放商标 | 换镜像；把该域名从 Skill 候选列表移除并标注日期 |
| **DNS 消亡** | curl "Could not resolve host"，nslookup NXDOMAIN | 同上 |
| **DDoS-Guard 网络层拦截** | curl 403 + "DDoS-Guard" 标题；浏览器显示 "Checking your browser" | 浏览器自动过（等 10–30s）；curl 场景必须带浏览器 cookie |
| **应用层 "Are you a robot?" 不自动通过** | 标题含 "are you are robot?"，等待 21s 仍停留 | 点击 "No"（唯一可点元素），6–8s 后跳转 |
| **浏览器原生下载卡死** | MCP download 工具报 "Download timed out... waiting on that dialog" | 浏览器开了"每次询问保存位置"。改用 curl 直链（.ru）或带 cookie curl（.st）；或提示用户关闭该浏览器设置 |
| **数据库不收录** | "no articles found for your request" | **不要换镜像重试**（数据库相同）。换渠道：① arXiv/出版社开放版 ② 图书馆/馆际互借 ③ 邮件向通讯作者索取 |
| **假 PDF（challenge HTML 伪装）** | `file` 显示 HTML 而非 PDF；文件头 `<!doctype html>` | 下载被拦截了，回到 §5.1 步骤 2 重新过检测 |
| **强人机检测（本次未遇到但需预案）** | Cloudflare Turnstile 可见复选框/hCaptcha 图片识别 | **AI 应停下使用 `request_human_help` 请求人类协助，不要硬闯**。本次实测未遇到此类强检测，但 sci-hub 防护策略可能变化 |
| **MCP 客户端会话失效** | "Session not found" 错误 | 服务本身可能仍存活。用附录 D 直连脚本重新 initialize 握手；或 curl 探测端点确认 |

---

## 7. 关于测试 DOI 的说明（重要）

任务指定的测试 DOI `10.1007/BF01449995`（Zermelo 1908, *Untersuchungen über die Grundlagen der Mengenlehre. I*, Mathematische Annalen 65）在 **两个可用镜像（.st 与 .ru）均返回 "no articles found"**。

**判断**：这是 sci-hub 数据库覆盖问题（其库存约 8800 万篇，2021 年前存档为主，1908 年老期刊论文收录不全），**不是流程或检测失败**。为完成下载环节实测，改用确定收录的 `10.1038/nature16961`（AlphaGo 论文，Nature 2016，真实收费墙论文）走通了全流程。

**对 SOP 的启示**：用 sci-hub 获取**1900–1970 年代老论文命中率低**，Skill 应在 SOP 中提示用户：老论文优先走出版社开放档案（如 Springer Link 的免费旧卷）、Internet Archive、或图书馆扫描件。

---

## 8. 下载验证结果（PDF 元数据）

**文件**：`docs/research/evidence/silver2016_test.pdf`（curl 自 `https://sci-hub.ru/storage/zero/6657/ae3953e2190143a462dcebd18f7c4495/silver2016.pdf`，无 cookie）

```
$ file silver2016_test.pdf
PDF document, version 1.6

$ pdfinfo silver2016_test.pdf
Title:           Mastering the game of Go with deep neural networks and tree search
Subject:         Nature 529, 484 (2016). doi:10.1038/nature16961    ← DOI 匹配 ✔
Author:          David Silver
Creator:         Adobe InDesign CS6 (Windows)
Producer:        Adobe PDF Library 10.0.1
CreationDate:    Tue Jan 19 18:11:20 2016 EST                       ← 出版商原始文件 ✔
Pages:           20
File size:       2,682,222 bytes (2.68 MB)
Encrypted:       no
```

**结论**：文件为出版商原始 PDF（非扫描、非重构），DOI 与请求完全一致，20 页完整。下载链路验证通过。

**证据文件清单**（`docs/research/evidence/`）：

| 文件 | 内容 |
|------|------|
| `01_initial.jpg` | sci-hub.jp 初始状态（广告停放页） |
| `02_ddosguard_st_10s.jpg` | sci-hub.st DDoS-Guard 通过后主页 |
| `03_robot_check_st.jpg` | sci-hub.st "Are you a robot?" 检测页 |
| `04_paper_page_ru.jpg` | sci-hub.ru AlphaGo 论文页（PDF 内嵌预览） |
| `silver2016_test.pdf` | 成功下载的论文 PDF（2.68MB, 20 页） |

---

## 9. 法律与合规风险提示（Skill 必须随附）

> **⚠️ 此段必须原样保留在 MinerU Skill 的 SOP 中。**

Sci-Hub 分发受版权保护的学术论文，在**包括美国、欧盟、英国在内的多个司法辖区被法院认定侵犯版权**（Elsevier v. Sci-Hub 案，美国法院判赔 1.5 亿美元；域名多次被查封）。部分辖区（如俄罗斯）执行情况不同，这不妨碍其法律争议属性。

**使用边界**：
1. **仅限个人研究、学习、评论目的**，不得用于商业用途或再分发。
2. **永远优先合法渠道**：arXiv 预印本、出版社开放获取（OA）版本、Unpaywall/OpenAccess 按钮查询合法绿色版本、机构图书馆订阅、馆际互借、ResearchGate 向作者索取、Internet Archive。
3. sci-hub 只应作为**最后手段**，且用户应知悉所在辖区的法律风险。
4. Skill 的角色定位：如实记录技术流程（本报告）≠ 鼓励使用。MinerU Skill 应在文献获取 SOP 中把合法渠道排在前面，sci-hub 作为兜底选项并随附本风险提示。

---

## 附录 A：人机检测速查表

| 检测 | 看到什么 | AI 该做什么 | 耗时 |
|------|---------|------------|------|
| DDoS-Guard JS challenge | "Checking your browser" + loading | 什么都不做，轮询等待 | 10–30s 自动过 |
| Sci-Hub "Are you a robot?" | 大标题 + "No" 链接 | 点 "No"，等跳转 | 点击后 6–8s |
| ALTCHA（.ru 的实现） | 同上（俄语/英语） | 同上 | 同上 |
| Cloudflare Turnstile / hCaptcha | 复选框/图片 puzzle | **request_human_help 请求人类协助** | — |

## 附录 B：本次实测完整时间线

```
10:43:57  开始；打开 sci-hub.jp
10:44:12  .jp 截图（广告页）
10:45:03  .jp DOM 确认：无搜索框，仅 a-ads.com 广告 iframe → 死亡
10:46:16  .jp curl：200 + ddos-guard 空壳页
10:46:47  .jp DOI 路径 → 同样广告页 → 全站死亡实锤
10:47:xx  .se DNS NXDOMAIN → 死亡；.st 403 DDoS-Guard → 活；.ru 200 → 活
10:48:04  浏览器进 .st → DDoS-Guard 检测页
10:48:33  .st 检测自动通过（≤29s）
10:49:11  .st 搜索 10.1007/BF01449995 → 触发 "are you are robot?"
10:50:21  点 No
10:50:48  .st：no articles found（Zermelo 未收录）
10:51:08  curl .ru DOI 页 → ALTCHA 检测页（俄语）
10:52:14  .ru 轮询 21s 不自动过
10:53:14  .ru 点 No → 6s 过 → 同样 no articles found
10:54:13  .ru + 10.1038/nature16961 → 免检直进论文页（cookie 生效）
10:54:33  拿到 PDF 直链
10:55:44  浏览器 download 工具超时（询问保存位置对话框）→ 失败模式记录
10:55:xx  curl .ru 直链无 cookie 下载成功（2.68MB 有效 PDF）
10:57:32  .st 复验：免检直进论文页
10:58:xx  curl .st 直链 → 403 DDoS-Guard（与 .ru 关键差异）
```

## 附录 C：curl 探测命令模板

```bash
# 存活探测
curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" --max-time 20 "https://sci-hub.<域名>/"

# 直链下载（仅 .ru 有效）
curl -s -o paper.pdf --max-time 60 "https://sci-hub.ru/storage/<path>.pdf" \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# 验证
file paper.pdf && pdfinfo paper.pdf | head -12
```

## 附录 D：MCP 客户端会话失效的兜底方案

本次实测开始时，CodeArts 内置 MCP 客户端报 `Session not found`（会话句柄过期），但 BrowserOS MCP 服务本身存活（`curl http://127.0.0.1:9210/mcp` 可完成 initialize 握手）。

**解法**：自建轻量 MCP 客户端（Python，~150 行）：自行发送 `initialize` JSON-RPC → 保存响应头 `Mcp-Session-Id` → 后续 `tools/call` 均携带该头 → 遇 404 自动重新握手。脚本副本存于 `docs/research/evidence/mcp_browseros_fallback.py`（核心逻辑可内嵌进 MinerU Skill 作为浏览器工具链的容错层）。

**Skill 设计建议**：BrowserOS 工具链调用失败（Session not found）≠ 浏览器死了。Skill 应实现"端点探测 → 自行握手 → 重试"的三级容错，而非直接放弃浏览器流程。

---

*报告完。实测人：SciHub探路者（AgentTeam 任务 #1）。所有截图与 PDF 证据见 `docs/research/evidence/`。*
