@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements...
pip install -r requirements.txt

echo Creating run script...
(
echo @echo off
echo call venv\Scripts\activate.bat
echo streamlit run main.py
echo pause
) > run.bat

echo Setup complete! You can now run the application by double-clicking run.bat
pause 