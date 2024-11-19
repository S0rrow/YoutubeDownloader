@echo off
python -m venv venv
venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt

echo installation sucess
pause