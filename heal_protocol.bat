@echo off
echo [HEAL_PROTOCOL] Initiating System Reset...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM ollama.exe >nul 2>&1
timeout /t 5
start /b "" "C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe" serve > ollama_log.txt 2>&1
timeout /t 10
start /low "" C:\Users\viper\python\python.exe C:\Users\viper\SimAgentCity\backend\main.py
start /low "" C:\Users\viper\python\python.exe C:\Users\viper\SimAgentCity\master_controller.py
echo [HEAL_PROTOCOL] System Restored.
