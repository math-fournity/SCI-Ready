#!/usr/bin/env python3
"""直接通过 streamable HTTP 协议调用 BrowserOS neo MCP 的辅助脚本。

背景：CodeArts MCP 客户端会话句柄过期（Session not found），
但 MCP 服务本身存活（http://127.0.0.1:9210/mcp）。
本脚本自行完成 MCP initialize 握手并维护会话 ID，
从而继续驱动 BrowserOS 浏览器完成实测任务。

用法:
  mcp_browseros.py <tool_name> '<json_args>'
  mcp_browseros.py --list                      # 列出所有工具名
  mcp_browseros.py --screenshot <page> <path>  # 截图并保存到指定路径

image 类型的返回内容会自动保存为文件（--screenshot 模式下保存到指定路径）。
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
import uuid

MCP_URL = "http://127.0.0.1:9210/mcp"
SESSION_FILE = "/tmp/browseros_mcp_session.txt"
IMG_DIR = "/tmp/browseros_shots"


def http_post(body, session_id=None, timeout=180):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(
        MCP_URL, data=json.dumps(body).encode(), headers=headers, method="POST"
    )
    return urllib.request.urlopen(req, timeout=timeout)


def parse_sse(resp):
    """解析 SSE 流，返回 JSON-RPC 消息列表"""
    messages = []
    for raw in resp:
        line = raw.decode("utf-8", errors="replace").rstrip("\n\r")
        if line.startswith("data: "):
            data = line[6:]
            if data.strip():
                try:
                    messages.append(json.loads(data))
                except json.JSONDecodeError:
                    pass
    return messages


def initialize():
    """完成 MCP initialize 握手，返回会话 ID"""
    init_body = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "curl-helper", "version": "1.0"},
        },
    }
    resp = http_post(init_body)
    sid = resp.headers.get("Mcp-Session-Id")
    parse_sse(resp)  # 排空响应流
    if not sid:
        raise RuntimeError("initialize 未返回 Mcp-Session-Id 响应头")
    # 发送 initialized 通知（协议要求）
    http_post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid


def get_session(force_new=False):
    if not force_new:
        try:
            with open(SESSION_FILE) as f:
                sid = f.read().strip()
            if sid:
                return sid
        except FileNotFoundError:
            pass
    sid = initialize()
    with open(SESSION_FILE, "w") as f:
        f.write(sid)
    return sid


def rpc_call(method, params):
    """带会话自愈的 JSON-RPC 调用"""
    body = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": params,
    }
    sid = get_session()
    try:
        resp = http_post(body, sid)
        messages = parse_sse(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # 会话在服务端失效，重新握手一次
            sid = get_session(force_new=True)
            resp = http_post(body, sid)
            messages = parse_sse(resp)
        else:
            raise
    for m in messages:
        if "result" in m or "error" in m:
            return m
    return None


def handle_content(result, img_path=None):
    """打印 text 内容；image 内容存文件"""
    if result is None:
        print("!! 无 JSON-RPC 响应")
        sys.exit(2)
    if "error" in result:
        print("!! RPC 错误:", json.dumps(result["error"], ensure_ascii=False))
        sys.exit(3)
    rpc_result = result.get("result", {})
    if rpc_result.get("isError"):
        print("!! 工具执行错误")
    content = rpc_result.get("content", [])
    os.makedirs(IMG_DIR, exist_ok=True)
    saved = []
    for i, c in enumerate(content):
        if c.get("type") == "text":
            print(c.get("text", ""))
        elif c.get("type") == "image":
            data = c.get("data", "")
            if data:
                if img_path:
                    path = img_path
                else:
                    path = os.path.join(IMG_DIR, f"shot_{uuid.uuid4().hex[:8]}.jpg")
                with open(path, "wb") as f:
                    f.write(base64.b64decode(data))
                saved.append(path)
                print(f"[图片已保存: {path}]")
        else:
            print(json.dumps(c, ensure_ascii=False)[:3000])
    if saved:
        print("[SAVED]" + ",".join(saved))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "--list":
        result = rpc_call("tools/list", {})
        if result and "result" in result:
            for t in result["result"].get("tools", []):
                print(f"- {t['name']}: {t.get('description', '')[:80]}")
        else:
            print("!! 列出工具失败:", json.dumps(result, ensure_ascii=False)[:500])
        return
    if sys.argv[1] == "--screenshot":
        # --screenshot <page_id> [保存路径]
        page = int(sys.argv[2])
        img_path = sys.argv[3] if len(sys.argv) > 3 else None
        args = {"page": page}
        result = rpc_call("tools/call", {"name": "screenshot", "arguments": args})
        handle_content(result, img_path)
        return
    tool_name = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = rpc_call("tools/call", {"name": tool_name, "arguments": args})
    handle_content(result)


if __name__ == "__main__":
    main()