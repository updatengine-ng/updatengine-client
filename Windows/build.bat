@echo off

REM Install python : https://www.python.org/downloads/
REM Install packages : python -m pip install lxml pywin32 PyInstaller

set path=c:\python27;c:\python27\scripts;%path%

set PathInstall=%~dp0

rd /S /Q "%PathInstall%build"
rd /S /Q "%PathInstall%dist"

pyinstaller -y --icon=updatengine.ico --version-file=version.txt --add-data "LICENSE.txt;." --add-data "updatengine.ico;." updatengine-client.py

rem OR :
rem   pyi-makespec --icon=updatengine.ico --version-file=version.txt --add-data "LICENSE.txt;." --add-data "updatengine.ico;." updatengine-client.py
rem   pyinstaller updatengine-client.spec

rem python build_cxfreeze.py build
rem python build_py2exe.py py2exe -p lxml
