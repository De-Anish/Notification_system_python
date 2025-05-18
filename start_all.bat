@echo off
echo === Starting Notification System ===

echo.
echo 1. Starting RabbitMQ Server...
net start RabbitMQ
timeout /t 5

echo.
echo 2. Starting FastAPI Server...
start cmd /k "python -m uvicorn main:app --reload --port 8000"
timeout /t 5

echo.
echo 3. Starting Notification Consumers...
start cmd /k "python start_consumers.py"

echo.
echo === All Services Started ===
echo.
echo Access points:
echo - Frontend: Open index.html in browser
echo - RabbitMQ Dashboard: http://localhost:15672
echo - FastAPI Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul 