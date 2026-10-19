#!/usr/bin/env bash
# 首次推送最小验收：逐项执行 mineru Skill 对外声明的核心能力。
# 用法：bash docs/release/run-acceptance.sh
# 任一项失败以非零退出，不放宽判据。
set -uo pipefail

MINERU=/Volumes/D/toolchain-cache/mineru-venv/bin/mineru
PASS=0
FAIL=0

ok()   { printf 'PASS | %s\n' "$1"; PASS=$((PASS+1)); }
bang() { printf 'FAIL | %s\n' "$1"; FAIL=$((FAIL+1)); }

echo "== acceptance run $(date -u '+%Y-%m-%dT%H:%M:%SZ') =="

# A1 CLI 可执行
V="$("$MINERU" --version 2>&1)"
printf '%s\n' "$V" | grep -q '4\.0\.' && ok "A1 mineru CLI 4.0.x" || bang "A1 mineru CLI version"

# A2/A3 server + remote health
ST="$("$MINERU" server status --json 2>&1)"
printf '%s' "$ST" | grep -q '"running": *true' && ok "A2 doclib server running" || bang "A2 doclib server running"
printf '%s' "$ST" | grep -q '"remote": {' && printf '%s' "$ST" | grep -q '"healthy": *true' \
  && ok "A3 remote parse service healthy" || bang "A3 remote parse service healthy"

# A4 access level
U="$("$MINERU" usage --json 2>&1)"
LV="$(printf '%s' "$U" | sed -n 's/.*"access_level": *"\([a-z]*\)".*/\1/p')"
case "$LV" in
  registered|anonymous) ok "A4 access_level=$LV" ;;
  *) bang "A4 access_level unreadable" ;;
esac

# A5 remote parse of a small generated PDF
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
PDF="$TMP/sample.pdf"
/Volumes/D/toolchain-cache/mineru-venv/bin/python - "$PDF" <<'PY'
import sys
from reportlab.pdfgen import canvas
p = sys.argv[1]
c = canvas.Canvas(p)
c.drawString(72, 720, "MinerU acceptance sample document")
c.save()
PY
OUT="$("$MINERU" parse "$PDF" --remote --json --wait 180 2>&1)"
if printf '%s' "$OUT" | grep -q '"error"'; then
  bang "A5 remote parse"
else
  ok "A5 remote parse"
fi
printf '%s' "$OUT" | head -c 400; echo

# A6 read by locator
SID="$(printf '%s' "$OUT" | sed -n 's/.*"short_id": *"\([0-9a-f]*\)".*/\1/p' | head -1)"
if [ -n "$SID" ]; then
  R="$("$MINERU" read "doc:$SID/tier:standard/page:1" --json 2>&1)"
  printf '%s' "$R" | grep -q '"error"' && bang "A6 read by locator" || ok "A6 read by locator"
else
  bang "A6 read by locator (no short_id)"
fi

# A7 chunk params (static)
S=~/.agents/skills/mineru/scripts/parse_large.py
if grep -q -- '--pages' "$S" && grep -q -- '--limit' "$S" && grep -qE '100_000_000|100000000' "$S"; then
  ok "A7 parse_large.py page-range + large limit"
else
  bang "A7 parse_large.py params"
fi

# A8 JSON contract
printf '%s' "$OUT" | /Volumes/D/toolchain-cache/mineru-venv/bin/python -c \
  'import json,sys
d=json.load(sys.stdin)
raise SystemExit(0 if ("parse" in d or "error" in d) else 1)' \
  && ok "A8 JSON control-flow contract" || bang "A8 JSON control-flow contract"

echo "== summary: PASS=$PASS FAIL=$FAIL =="
[ "$FAIL" -eq 0 ]
