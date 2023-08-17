@echo off

setlocal

set command=py -3.10 -m nuitka --clang --mingw64 --onefile --follow-imports --include-module=flet --windows-icon-from-ico=.\Item_Gem.ico --remove-output --output-filename=Bot_upgrade --windows-company-name=Unknown --windows-product-version=1.0 --onefile-tempdir-spec=C:\Users\Default\AppData\Local\Temp\bot_unknown .\main_upgrade.py

REM Exécution de la commande
%command%

REM Déplacer le fichier bot.exe vers le répertoire souhaité
set current_date=%date:~-4%-%date:~3,2%-%date:~0,2%
set new_filename=.\auth compiled\test environnement\bot-upgrade-%current_date%.exe
move .\bot_upgrade.exe "%new_filename%"

REM Copier le contenu du dossier resources
xcopy /E /I /Y ".\resources" ".\auth compiled\test environnement\resources"

endlocal
