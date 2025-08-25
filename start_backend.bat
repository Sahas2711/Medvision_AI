@echo off
echo Starting MedVision AI Backend Server...
echo.

cd backend

echo Installing dependencies...
pip install flask flask-cors tensorflow pillow opencv-python numpy

echo.
echo Starting Flask server...
python app.py

pause