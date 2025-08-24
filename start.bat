@echo off
echo Starting MedVision AI Application...

echo Installing Python dependencies...
cd backend
pip install -r requirements.txt

echo Starting Flask backend...
start "Backend" python app.py

echo Starting frontend...
cd ../frontend
start "Frontend" index.html

echo Application started successfully!
echo Backend: http://localhost:5000
echo Frontend: Open index.html in browser
pause