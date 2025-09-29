@echo off
REM Quick demo script for USB PD Parser

echo 🚀 USB PD Parser Demo
echo =====================

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Install dependencies if needed
if not exist ".venv\installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo. > .venv\installed
)

REM Run extraction on sample PDF (mode 3 for quick demo)
echo Running extraction (mode 3 - first 200 pages)...
python main.py --mode 3

REM Show results
echo.
echo 📊 Results:
echo ===========
if exist "outputs\usb_pd_content.jsonl" (
    echo ✅ Content extracted successfully!
    echo First 3 content items:
    for /f "tokens=1* delims=:" %%a in ('findstr /n "^" outputs\usb_pd_content.jsonl') do (
        if %%a leq 3 echo %%b
    )
    echo.
    echo 📈 Statistics:
    for /f %%i in ('find /c /v "" ^< outputs\usb_pd_content.jsonl') do echo Content items: %%i
    if exist "outputs\usb_pd_toc.jsonl" (
        for /f %%i in ('find /c /v "" ^< outputs\usb_pd_toc.jsonl') do echo TOC entries: %%i
    )
) else (
    echo ❌ No output files found. Check for errors above.
)

echo.
echo 🔍 Try searching content:
echo python search_content.py "USB"
echo python search_content.py "Power Delivery"