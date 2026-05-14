@echo off
echo ==================================================
echo        SIM AGENT CITY - GENESIS EDITION
echo ==================================================
echo [INFO] Ensuring Ollama is running...
echo [INFO] Launching City Server and Retro UI...
echo [LINK] Navigate to http://localhost:8000/static/index.html after start.
echo ==================================================
dist\cli_wrapper.exe --start
pause
