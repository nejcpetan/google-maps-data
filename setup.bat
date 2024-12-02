@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python.exe -m pip install --upgrade pip

echo Installing wheel...
pip install wheel

echo Upgrading setuptools...
pip install --upgrade setuptools

echo Installing requirements...
pip install -r requirements.txt

echo Creating run script...
(
echo @echo off
echo call venv\Scripts\activate
echo uvicorn main:app --reload
echo pause
) > run.bat

echo Setup complete! You can now run the application by double-clicking run.bat
pause 