@echo off
REM ============================================================
REM Build de release do ApT com proteção PyArmor + PyInstaller
REM
REM Pré-requisitos:
REM   1. PyArmor com licença ativa (pyarmor reg pyarmor-regfile.zip)
REM      Adquira em: https://pyarmor.readthedocs.io/en/latest/license.html
REM   2. .venv ativado ou usar caminhos completos abaixo
REM
REM Uso:
REM   build_release.bat
REM ============================================================

setlocal

set VENV=.venv\Scripts
set PYARMOR=%VENV%\pyarmor.exe
set PYINSTALLER=%VENV%\pyinstaller.exe
set OBFDIR=_obf_build

echo.
echo [1/3] Limpando build anterior...
if exist %OBFDIR% rmdir /s /q %OBFDIR%
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [2/3] Ofuscando codigo com PyArmor...
%PYARMOR% gen ^
    --output %OBFDIR% ^
    --recursive ^
    --exclude .venv ^
    --exclude installer ^
    --exclude build ^
    --exclude dist ^
    --exclude _obf_build ^
    main.py

if errorlevel 1 (
    echo [ERRO] PyArmor falhou. Verifique a licenca ativa.
    exit /b 1
)

echo.
echo [3/3] Empacotando com PyInstaller...
%PYINSTALLER% apt.spec --noconfirm

if errorlevel 1 (
    echo [ERRO] PyInstaller falhou.
    exit /b 1
)

echo.
echo ============================================================
echo Build concluido: dist\ApT\ApT.exe
echo Gere o instalador: compile apt-installer.iss no Inno Setup
echo ============================================================

endlocal
