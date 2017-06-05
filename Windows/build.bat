@echo off

set PathInstall=%~dp0

rd /S /Q "%PathInstall%build"
rd /S /Q "%PathInstall%dist"
python build_cxfreeze.py build
rem python build_py2exe.py py2exe -p lxml
