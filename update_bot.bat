@echo off
cd /d C:\Users\s-ryu\Projects\EQFast-for-discord

git pull origin main

taskkill /im python.exe /f

venv\Scripts\python.exe -m eew_bot