@echo off
setlocal

call .\venv\Scripts\activate.bat

REM Define the command to run import_verification.py
set verify_command=py -3.11 import_verification.py

REM Execute the import verification script and capture the error level
%verify_command%
set verification_status=%errorlevel%

REM Check the exit code (error level) of the verification script
if %verification_status% neq 0 (
    echo %verification_status%
    echo Import verification failed. Do you want to continue? (Press Enter to continue or Ctrl+C to abort)
    pause
)

REM Define the nuitka command
set nuitka_command=nuitka --clang --mingw64 --onefile --follow-imports --windows-icon-from-ico=.\Item_Gem.ico --remove-output --output-filename=Bot --windows-company-name=Unknown --windows-product-version=1.0 --onefile-tempdir-spec=C:\Users\Default\AppData\Local\Temp\bot_unknown .\app_upgrade.py

REM Execute the nuitka command
%nuitka_command%

set current_date=%date:~-4%-%date:~3,2%-%date:~0,2%
set new_filename=.\auth compiled\test environnement\bot_executable_%current_date%\bot-%current_date%.exe

mkdir ".\auth compiled\test environnement\bot_executable_%current_date%"

move .\bot.exe "%new_filename%"
xcopy /E /I /Y ".\resources" ".\auth compiled\test environnement\bot_executable_%current_date%\resources"

endlocal
