@echo off
REM Change directory to the folder where this batch file is located
cd /d "%~dp0"

echo Installing required packages...
py -m pip install pynput keyboard pyinstaller --quiet

echo Compiling data.py with PyInstaller...
py -m PyInstaller --onefile --noconsole --name build data.py --clean --noconfirm

echo Compilation finished.
echo Moving executable to root directory...
move "dist\build.exe" "%~dp0build.exe" >nul 2>&1

echo Cleaning up compilation files...
rd /s /q build >nul 2>&1
rd /s /q dist >nul 2>&1
del /q data.spec >nul 2>&1

echo Starting the compiled program...
start "" "build.exe"

echo Done.
pause
