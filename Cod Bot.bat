@echo off
setlocal

set command=py -3.11 -m nuitka --clang --mingw64 --onefile --follow-imports --include-module=flet --windows-icon-from-ico=.\Item_Gem.ico --remove-output --output-filename=Bot --windows-company-name=Unknown --windows-product-version=1.0 --onefile-tempdir-spec=C:\Users\Default\AppData\Local\Temp\bot_unknown --nofollow-import-to=scipy  .\main.py

REM Execution of the command

set current_date=%date:~-4%-%date:~3,2%-%date:~0,2%
set new_directory=.\auth compiled\test environnement\bot_executable_%current_date%
set new_filename=%new_directory%\bot-%current_date%.exe

mkdir "%new_directory%"

move .\bot.exe "%new_filename%"
xcopy /E /I /Y ".\resources" "%new_directory%\resources"

powershell Compress-Archive -Path "%new_directory%\*" -DestinationPath "%new_directory%.zip"

endlocal
