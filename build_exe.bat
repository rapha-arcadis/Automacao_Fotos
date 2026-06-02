@echo off
echo ================================
echo  Gerando executavel: Validador EDD
echo ================================

REM (Opcional) Ativar .venv
IF EXIST .venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
)

REM Limpa builds antigos
echo Limpando builds anteriores...
rmdir /s /q build
rmdir /s /q dist
del /q "Renomeador de arquivos.spec" 2>nul

REM Build do executavel
echo Iniciando PyInstaller...

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name "Renomeador de arquivos" ^
  --icon="Assets\arcadis_logo.ico" ^
  --paths="." ^
  --add-data "Theme;Theme" ^
  --add-data "Assets;Assets" ^
  --collect-all customtkinter ^
  main.py

echo.
echo ================================
echo Build finalizado!
echo Executavel em: dist\Renomeador de arquivos.exe
echo ================================
pause