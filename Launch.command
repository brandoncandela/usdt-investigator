#!/bin/bash
cd "$(dirname "$0")" || exit 1
BUNDLED="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
if [ -x "$BUNDLED" ]; then
  PYTHON="$BUNDLED"
elif python3 --version >/dev/null 2>&1; then
  PYTHON=python3
else
  echo 'Install Python 3.10+ from https://www.python.org/downloads/ and try again.'
  read -r -p 'Press Enter to close.'
  exit 1
fi
open http://127.0.0.1:8000
"$PYTHON" app.py
read -r -p 'Press Enter to close.'
