@echo off
setlocal
set PYTHON_CMD=

where python >nul 2>nul
if not errorlevel 1 set PYTHON_CMD=python

if not defined PYTHON_CMD (
    where python3 >nul 2>nul
    if not errorlevel 1 set PYTHON_CMD=python3
)

if not defined PYTHON_CMD (
    where py >nul 2>nul
    if not errorlevel 1 set PYTHON_CMD=py
)

if not defined PYTHON_CMD (
    echo Python interpreter not found. Please install Python.
    exit /b 1
)

@echo on
%PYTHON_CMD% "%~dp0/zpkg" %*
