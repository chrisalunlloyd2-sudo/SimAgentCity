@echo off
echo [GIT_SYNC] Initiating Add-Only Backup to chrisalunlloyd2-sudo...

:: Ensure backup directory exists
if not exist "C:\Users\viper\SimAgentCity_Backup" mkdir "C:\Users\viper\SimAgentCity_Backup"

:: Add-only copy: Copy all files to the backup dir, overwriting existing if changed, but never deleting absent files.
xcopy "C:\Users\viper\SimAgentCity" "C:\Users\viper\SimAgentCity_Backup" /S /E /Y /I

echo [GIT_SYNC] Backup Complete. History preserved.
