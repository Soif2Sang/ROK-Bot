@echo off

setlocal

set current_date=%date:~-4%-%date:~3,2%-%date:~0,2%
set new_directory=.\auth compiled\test environnement\bot_executable_%current_date%
set new_filename=%new_directory%\bot-%current_date%.exe

mkdir "%new_directory%"


powershell Compress-Archive -Path "%new_directory%" -DestinationPath "%new_directory%.zip"


endlocal
