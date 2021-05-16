@echo off

REM Install python : https://www.python.org/downloads/
REM Activate pip : python -m ensurepip
REM Upgrade pip : python -m pip install --upgrade pip
REM Install packages : python -m pip install lxml pywin32 PyInstaller wmi distro

set PathInstall=%~dp0

if exist "%PathInstall%build" rd /S /Q "%PathInstall%build"
if exist "%PathInstall%dist" rd /S /Q "%PathInstall%dist"

pyinstaller -y --icon=updatengine.ico --version-file=version.txt --add-data "LICENSE.txt;." --add-data "updatengine.ico;." updatengine-client.py

