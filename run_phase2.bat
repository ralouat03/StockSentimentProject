@echo off

echo Running preprocess_data.py...
python scripts\preprocess_data.py
if %errorlevel% neq 0 goto error
echo preprocess_data.py finished. Press Enter to continue...
pause > nul

echo Running clean_sentiment.db.py...
python scripts\clean_sentiment.db.py
if %errorlevel% neq 0 goto error
echo clean_sentiment.db.py finished. Press Enter to continue...
pause > nul

echo Running calculate_sentiment.py...
python scripts\calculate_sentiment.py
if %errorlevel% neq 0 goto error
echo calculate_sentiment.py finished. Press Enter to continue...
pause > nul

echo All scripts executed successfully.
pause
goto end

:error
echo An error occurred during script execution.
pause

:end
