@echo off
title QR Shield - Public College Server
echo =======================================================
echo          QR SHIELD - COLLEGE PUBLIC SERVER
echo =======================================================
echo.

REM Optional: Set your Gemini API key below so college users need NO API key
REM set GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere

if "%GEMINI_API_KEY%"=="" (
    echo [INFO] No GEMINI_API_KEY environment variable detected.
    echo [INFO] QR Shield will run 16+ comprehensive static security checks.
    echo [INFO] To enable AI analysis without student keys, edit this file or run:
    echo        set GEMINI_API_KEY=your_key_here
    echo.
) else (
    echo [SUCCESS] Server-Side Gemini API Key configured!
    echo [SUCCESS] Students can use AI analysis without providing any key.
    echo.
)

echo Starting QR Shield server on port 5000 (accessible on your college network)...
python server.py
pause

