#!/bin/bash
# Double-clic pour lancer la passerelle (Linux). Arguments optionnels : --port 9000 --debug
cd "$(dirname "$0")"
uv run shuttle_osc.py "$@"
