@echo off
echo ========================================
echo  Building PyMedia Player Executable
echo ========================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Building the .exe file...
python build.py
echo.

echo ========================================
echo  BUILD COMPLETE!
echo ========================================
echo.
echo Your .exe file is in: dist\PyMediaPlayer.exe
echo.
echo IMPORTANT: You still need libmpv-2.dll
echo Download from: https://mpv.io/installation/
echo.
pause
