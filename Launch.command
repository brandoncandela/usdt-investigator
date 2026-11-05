#!/bin/bash
# Double-click on macOS to start the dashboard at http://127.0.0.1:8000
cd "$(dirname "$0")" || exit 1
if ! python3 --version >/dev/null 2>&1; then
  echo 'Install Python 3.10+ from https://www.python.org/downloads/ and try again.'
  read -r -p 'Press Enter to close.'
  exit 1
fi
open http://127.0.0.1:8000
python3 app.py
read -r -p 'Press Enter to close.'
