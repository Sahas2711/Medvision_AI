@echo off
echo Starting MedVision AI with Doctor Finder...

echo Starting main backend...
start "Main Backend" cmd /k "cd backend && python app.py"

timeout /t 2

echo Starting doctor finder backend...
start "Doctor Finder Backend" cmd /k "cd backend && python doctor_finder.py"

timeout /t 2

echo Starting frontend server...
start "Frontend Server" cmd /k "python serve_frontend.py"

echo All services started!
echo Main Backend: http://localhost:5000
echo Doctor Finder: http://localhost:5001
echo Frontend: http://localhost:8000
pause