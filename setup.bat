@echo off
setlocal

REM Get current directory
set "CWD=%cd%"

REM Get existing user PATH from registry
for /f "usebackq tokens=3*" %%A in (`reg query HKCU\Environment /v PATH 2^>nul`) do (
    set "OLDPATH=%%A %%B"
)

REM Check if already added
echo %OLDPATH% | find /i "%CWD%" >nul
if not errorlevel 1 (
    echo Already in PATH.
    goto :EOF
)

REM Add current folder to PATH
set "NEWPATH=%OLDPATH%;%CWD%"
reg add HKCU\Environment /v PATH /d "%NEWPATH%" /f

taskkill /f /im explorer.exe >nul 2>&1
start explorer.exe
echo Done, open a new terminal
endlocal
