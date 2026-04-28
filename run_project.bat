@echo off
echo Iniciando el Tasador Automatico...
start cmd /k "cd backend && ..\.venv\Scripts\python.exe -m pip install -r requirements.txt && ..\.venv\Scripts\python.exe -m uvicorn main:app --reload"
timeout /t 5
start cmd /k "cd frontend && ..\.venv\Scripts\python.exe -m pip install -r requirements.txt && ..\.venv\Scripts\python.exe -m streamlit run app.py"
echo Todo se esta ejecutando. Cierra estas ventanas para terminar.
