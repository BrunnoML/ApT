@echo off
REM ============================================================
REM Build de release do ApT — PyInstaller + modulo premium
REM
REM Pre-requisitos:
REM   1. apt-privado\ com pdf_report.py completo em:
REM      C:\Users\BrunnoML\Documents\apt-privado\pdf_report.py
REM   2. .venv ativado ou usar caminhos completos abaixo
REM
REM Uso:
REM   build_release.bat
REM ============================================================

setlocal

set VENV=.venv\Scripts
set PYINSTALLER=%VENV%\pyinstaller.exe

set PDF_STUB=core\pdf_report.py
set PDF_BACKUP=core\pdf_report.py.stub_bak
set PDF_COMPLETO=..\apt-privado\pdf_report.py

echo.
echo [1/4] Verificando modulo premium...
if not exist %PDF_COMPLETO% (
    echo [ERRO] Nao encontrado: %PDF_COMPLETO%
    echo Certifique-se de que o repositorio apt-privado esta em:
    echo   C:\Users\BrunnoML\Documents\apt-privado\
    exit /b 1
)
echo OK — pdf_report.py completo encontrado.

echo.
echo [2/4] Limpando build anterior...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo.
echo [3/4] Substituindo stub pelo modulo premium...
copy /Y %PDF_STUB% %PDF_BACKUP% >nul
copy /Y %PDF_COMPLETO% %PDF_STUB% >nul

echo Empacotando com PyInstaller...
%PYINSTALLER% apt.spec --noconfirm

set BUILD_EXIT=%ERRORLEVEL%

echo.
echo [4/4] Restaurando stub publico...
copy /Y %PDF_BACKUP% %PDF_STUB% >nul
del %PDF_BACKUP%

if %BUILD_EXIT% neq 0 (
    echo [ERRO] PyInstaller falhou. Stub restaurado.
    exit /b 1
)

echo.
echo ============================================================
echo Build concluido: dist\ApT\ApT.exe
echo Gere o instalador: compile apt-installer.iss no Inno Setup
echo ============================================================

endlocal
