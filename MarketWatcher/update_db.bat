rem @echo off
cd %~dp0
set ANACONDA_PATH=C:\ProgramData\Anaconda3
set PATH=PATH;%ANACONDA_PATH%

call %ANACONDA_PATH%\Scripts\activate.bat
python main.py

pause