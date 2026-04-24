# Tasador Automático de Bienes Raíces 🏠📈

Este es un proyecto Full-Stack diseñado para demostrar la integración de un modelo estadístico dentro de una arquitectura moderna, separando claramente las responsabilidades en Backend, Middleware y Frontend.

## Arquitectura

El proyecto está compuesto por tres partes fundamentales:

1. **Frontend (Streamlit):** Una interfaz gráfica de usuario interactiva y de aspecto moderno que permite a los usuarios visualizar el mercado inmobiliario, obtener insights accionables y calcular tasaciones en tiempo real.
2. **Backend (FastAPI):** Una API veloz y robusta que expone los datos de propiedades y los resultados del análisis a través de endpoints RESTful.
3. **Middleware Estadístico (Scikit-Learn & Pandas):** El núcleo analítico de la aplicación. Se encarga de:
   - Entrenar un modelo de Regresión Lineal Múltiple.
   - Calcular la influencia matemática (importancia) de cada característica sobre el precio de las viviendas.
   - Detectar anomalías e identificar propiedades sistemáticamente "infravaloradas" (oportunidades de inversión).

## Estructura de Directorios

```text
c:\streamlit_stadistica\
├── backend/
│   ├── data_generator.py        # Script para generar un dataset de bienes raíces realista.
│   ├── statistical_middleware.py # Lógica de Machine Learning (Regresión lineal, ANOVA, etc).
│   ├── main.py                  # API en FastAPI con los endpoints de conexión.
│   └── requirements.txt         # Dependencias del lado del backend.
│
├── frontend/
│   ├── app.py                   # Dashboard y aplicación interactiva en Streamlit.
│   └── requirements.txt         # Dependencias del lado del frontend.
│
├── README.md                    # Documentación del proyecto.
└── run_project.bat              # Script de un solo clic para correr todo localmente.
```

## Cómo ejecutar el proyecto localmente

### 1. Requisitos previos
- Python 3.9 o superior.
- Git (opcional).

### 2. Instalación de dependencias
Puedes abrir dos terminales en la raíz del proyecto (`c:\streamlit_stadistica`).

**Terminal 1 (Backend):**
```bash
cd backend
pip install -r requirements.txt
```

**Terminal 2 (Frontend):**
```bash
cd frontend
pip install -r requirements.txt
```

### 3. Ejecución
Puedes ejecutar ambos a la vez usando el script incluido:
```cmd
run_project.bat
```

**O de forma manual:**
- **Paso 1:** En la Terminal 1 (Backend), ejecuta:
  ```bash
  uvicorn main:app --reload
  ```
  La API estará disponible en `http://localhost:8000`. Puedes ver la documentación interactiva en `http://localhost:8000/docs`.

- **Paso 2:** En la Terminal 2 (Frontend), ejecuta:
  ```bash
  streamlit run app.py
  ```
  Esto abrirá automáticamente el dashboard interactivo en tu navegador por defecto (normalmente en `http://localhost:8501`).
