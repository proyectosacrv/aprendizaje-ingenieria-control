@echo off
cd /d "%~dp0"
echo ============================================================
echo   Acceso REMOTO (desde cualquier dispositivo y cualquier red)
echo ============================================================
echo.
echo Levanta un servidor web local y crea un enlace publico temporal
echo (tunel de Cloudflare). Sirve TODO: repositorio + los 3 informes.
echo.

REM --- 1) cloudflared: descargar la primera vez si no esta ---
if not exist cloudflared.exe (
  echo Descargando cloudflared (~50 MB, solo la primera vez)...
  curl -L -o cloudflared.exe https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
)
if not exist cloudflared.exe (
  echo.
  echo  [!] No se pudo descargar cloudflared automaticamente.
  echo      Descargalo a mano desde:
  echo        https://github.com/cloudflare/cloudflared/releases
  echo      guarda "cloudflared.exe" en ESTA carpeta y vuelve a ejecutar.
  echo.
  pause
  exit /b 1
)

REM --- 2) servidor web local (segundo plano) ---
echo Arrancando servidor web local en el puerto 8080...
start "servidor-web (no cerrar)" /min python -m http.server 8080
timeout /t 2 >nul

REM --- 3) tunel publico ---
echo.
echo ------------------------------------------------------------
echo  Copia la URL  https://XXXX.trycloudflare.com  que aparece abajo
echo  y abrela en el movil (datos u otra WiFi). Veras la portada con
echo  el repositorio y los informes.
echo.
echo  Mantén esta ventana abierta mientras lo uses. Ctrl+C para cerrar.
echo  (Cierra tambien la ventana "servidor-web" al terminar.)
echo ------------------------------------------------------------
echo.
cloudflared.exe tunnel --url http://localhost:8080
