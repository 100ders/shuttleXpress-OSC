@echo off
REM Double-clic pour lancer la passerelle (Windows). Arguments optionnels : --port 9000 --debug
cd /d "%~dp0"
uv run shuttle_osc.py %*
pause
