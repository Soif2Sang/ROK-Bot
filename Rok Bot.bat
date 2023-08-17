@echo off

setlocal

set command=py -3.11 -m nuitka --clang --mingw64 --onefile --follow-imports --include-module=flet --windows-icon-from-ico=.\Item_Gem.ico --remove-output --output-filename=Bot --windows-company-name=Unknown --windows-product-version=1.0 --onefile-tempdir-spec=C:\Users\Default\AppData\Local\Temp\bot_unknown --nofollow-import-to=scipy  .\main_2.py

REM Exécution de la commande
%command%

set current_date=%date:~-4%-%date:~3,2%-%date:~0,2%
set new_filename=.\auth compiled\test environnement\bot_executable_%current_date%\bot-%current_date%.exe

mkdir ".\auth compiled\test environnement\bot_executable_%current_date%"

move .\bot.exe "%new_filename%"
xcopy /E /I /Y ".\resources" ".\auth compiled\test environnement\bot_executable_%current_date%\resources"


endlocal
