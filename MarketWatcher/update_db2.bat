rem @echo off
cd %~dp0
set ANACONDA_PATH=C:\Users\Administrator\anaconda3
set GIT_PATH=C:\Program Files\Git\cmd
set DROPBOX_PATH="C:\Program Files (x86)\Dropbox\Client"
set PATH=%PATH%;%ANACONDA_PATH%;%GIT_PATH%;%DROPBOX_PATH%

rem ##### kill dropbox #####
taskkill /im Dropbox.exe /F

rem ##### run backtest script #####
call %ANACONDA_PATH%\Scripts\activate.bat
python main.py
call conda deactivate

rem ##### push to github #####
cd ..
git add *
git commit -m "release html"
git push origin main

rem ##### remove output #####
del /S /Q .\MarketWatcher\output\backtest
del /S /Q .\MarketWatcher\output\forwardtest
timeout /t 240 > nul

rem ##### resume dropbox #####
start "Restart Dropbox" %DROPBOX_PATH%\Dropbox.exe -B
