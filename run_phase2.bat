@echo off
echo Running preprocess_data.py...
python preprocess_data.py
if %errorlevel% neq 0 goto error

echo Running clean_sentiment_text.py...
python clean_sentiment_text.py
if %errorlevel% neq 0 goto error

echo Running calculate_sentiment.py...
python calculate_sentiment.py
if %errorlevel% neq 0 goto error

echo All scripts executed successfully!
goto end

:error
echo An error occurred during script execution.

:end
pause