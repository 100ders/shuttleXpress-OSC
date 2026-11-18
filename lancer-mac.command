#!/bin/bash
# Double-clic pour lancer la passerelle (macOS). Arguments optionnels : --port 9000 --debug
cd "$(dirname "$0")"
uv run shuttle_osc.py "$@"
