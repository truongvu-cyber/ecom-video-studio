#!/bin/sh
# Launch the dedicated Chrome used for Google Flow automation.
#
# It is a separate Chrome profile (nothing from the user's daily Chrome), started
# with a DevTools port and WITHOUT automation flags, so Google sign-in works and
# stays signed in between runs. The chrome-live MCP server in .mcp.json attaches
# to this port.
PROFILE="$HOME/Library/Application Support/ecom-video-studio-chrome"
PORT=9222
if curl -s "http://127.0.0.1:$PORT/json/version" >/dev/null 2>&1; then
  echo "Flow Chrome đã chạy ở cổng $PORT"
  exit 0
fi
mkdir -p "$PROFILE"
open -na "Google Chrome" --args --remote-debugging-port=$PORT \
  --user-data-dir="$PROFILE" --no-first-run --no-default-browser-check \
  "${1:-https://flow.google.com/}"
sleep 4
curl -s "http://127.0.0.1:$PORT/json/version" | grep Browser || echo "Chưa thấy cổng $PORT, mở lại Chrome"
