@echo off
title Memory Forge — SecOps Memory Agent
echo ========================================================
echo  Starting Memory Forge SecOps ^& Compliance Memory Agent...
echo ========================================================
cd /d "%~dp0"
python backend/run.py
pause

