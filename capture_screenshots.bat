@echo off
echo Aarogya Drishti Screenshot Capture
echo ==================================
echo.
echo This will capture screenshots of your application for the README.
echo Make sure your application is running first!
echo.
pause

echo Installing required packages...
pip install selenium

echo.
echo Capturing screenshots...
python capture_screenshots.py

echo.
echo Screenshots captured! Check the screenshots folder.
pause