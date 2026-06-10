@echo off
echo.
echo ========================================================
echo  Repositorio de Conocimiento — servidor local
echo ========================================================
echo.
echo Abre en el movil (misma WiFi):
echo.
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%i
    goto found
)
:found
set IP=%IP: =%
echo   http://%IP%:8080
echo.
echo Abre en este PC:
echo   http://localhost:8080
echo.
echo Pulsa Ctrl+C para parar el servidor.
echo ========================================================
echo.
start "" "http://localhost:8080"
python -m http.server 8080
