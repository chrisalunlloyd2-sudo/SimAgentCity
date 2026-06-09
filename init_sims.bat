@echo off
echo [INIT] Starting Infinite Persistence Protocol...

:: 1. Force kill existing stack
taskkill /F /IM ollama.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1

:: 2. Start Ollama Server
echo [INIT] Launching Ollama...
start /b "" "C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe" serve > ollama_log.txt 2>&1
timeout /t 10

:: 3. Verify/Pull Models
echo [INIT] Verifying Models...
C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe pull qwen:0.5b
C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe pull h2o-danube2:0.5b

:: 4. Start SimAgentCity Stack (Serial Governance)
echo [INIT] Launching Symphony-Chain...
start /low "" C:\Users\viper\python\python.exe C:\Users\viper\SimAgentCity\backend\main.py
timeout /t 5
start /low "" C:\Users\viper\python\python.exe C:\Users\viper\SimAgentCity\master_controller.py

echo [INIT] All systems active.
pause
