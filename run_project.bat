@echo off
echo Iniciando el Tasador Automatico...
start cmd /k "cd backend && pip install -r requirements.txt && uvicorn main:app --reload"
timeout /t 5
start cmd /k "cd frontend && pip install -r requirements.txt && streamlit run app.py"
echo Todo se esta ejecutando. Cierra estas ventanas para terminar.
