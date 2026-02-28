@echo off
echo Starting Attendance App Server...
echo Hosting at http://psod.local.app/attendance (if DNS is configured)
echo Or access via IP: http://YOUR_IP_ADDRESS:80/attendance
echo Note: This script requires Administrator privileges to bind to port 80.

AttendanceApp.exe --server.port=80 --server.address=0.0.0.0 --server.baseUrlPath=attendance --server.headless=true
pause
