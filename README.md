# Tasador Automático de Bienes Raíces 🏠📈

Este es un proyecto Full-Stack diseñado para demostrar la integración de un modelo de Machine Learning y gestión de persistencia bajo los principios de **Arquitectura Limpia (Clean Architecture)**, separando de manera estricta las responsabilidades del negocio de las tecnologías e infraestructuras externas.

## Arquitectura del Proyecto

El backend está estructurado en capas concéntricas (arquitectura de cebolla o Clean Architecture) donde las dependencias apuntan únicamente hacia el interior:

1. **Domain (Dominio):**
   - **Entities:** Modelos de negocio puros (`User`, `Property`, `Prediction`) libres de librerías externas o ORMs.
   - **Ports:** Interfaces abstractas que definen el comportamiento de almacenamiento y modelos de ML (`user_repository`, `property_repository`, `prediction_repository`, `ml_model_port`).

2. **Application (Aplicación):**
   - **Services:** Implementación de los casos de uso (`UserService`, `PropertyService`, `PredictionService`) que coordinan el flujo de datos desde y hacia el dominio.
   - **Initializer:** Orquestador de la inicialización de servicios y repositorios.

3. **Infrastructure (Infraestructura):**
   - **Persistence:** Base de datos relacional local en SQLite, incluyendo migraciones y repositorios concretos que implementan los puertos de dominio.
   - **ML (Machine Learning):** Generador sintético de datos realista y modelo de regresión lineal múltiple con Scikit-Learn.

4. **Adapters (Adaptadores de API):**
   - Controladores de API construidos sobre **FastAPI** que exponen los endpoints correspondientes para interactuar con la aplicación.

El **Frontend** está construido en **Streamlit** y se comunica directamente con la API RESTful.

---

## Estructura de Directorios

```text
c:\streamlit_stadistica\
├── backend/
│   ├── domain/                         # Capa de Dominio (Reglas e Interfaces del Negocio)
│   │   ├── entities/                   # Entidades de dominio (User, Property, Prediction)
│   │   └── ports/                      # Puertos / Interfaces abstractas de persistencia e IA
│   │
│   ├── application/                    # Capa de Aplicación (Casos de Uso)
│   │   ├── services/                   # Servicios del negocio
│   │   └── initializer.py              # Configuración y arranque de servicios
│   │
│   ├── infrastructure/                 # Capa de Infraestructura (Tecnologías Concretas)
│   │   ├── persistence/                # Base de datos SQLite y Repositorios SQL
│   │   └── ml/                         # Entrenamiento y predicciones del modelo Scikit-Learn
│   │
│   ├── adapters/                       # Capa de Adaptadores de Interfaz
│   │   └── api/                        # Configuración de FastAPI, Rutas y Dependencias
│   │
│   ├── main.py                         # Punto de entrada de la API FastAPI
│   └── requirements.txt                # Dependencias del backend
│
├── frontend/
│   ├── app.py                          # Dashboard e Interfaz de Usuario en Streamlit
│   └── requirements.txt                # Dependencias del frontend
│
├── README.md                           # Documentación del proyecto
└── run_project.bat                     # Script de arranque rápido (Backend + Frontend)
```

---

## Características Principales

- **Tasador en tiempo real**: Estima el valor comercial de una propiedad de acuerdo con sus metros cuadrados, antigüedad, número de habitaciones, baños, distancia al centro y si posee piscina.
- **Gestión de Usuarios**: Registro interactivo de usuarios y persistencia de sus sesiones en el frontend.
- **Historial de Predicciones**: Cada tasación realizada se vincula con el usuario activo y se almacena en SQLite, permitiendo filtrar y visualizar el historial general.
- **Mapa de Oportunidades**: Identificación automática de inmuebles subvaluados con potencial de inversión en el mercado actual.
- **Impacto y Factores**: Desglose visual del coeficiente de importancia de cada característica física del inmueble en el precio final.

---

## Cómo ejecutar el proyecto localmente

### 1. Requisitos previos
- Python 3.9 o superior.
- Git.

### 2. Instalación de dependencias
Abre dos terminales en la raíz del proyecto (`c:\streamlit_stadistica`).

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

Puedes levantar ambos servicios simultáneamente usando el script automatizado:
```cmd
run_project.bat
```

**Ejecución manual:**

- **Backend (FastAPI):**
  ```bash
  cd backend
  uvicorn main:app --reload
  ```
  La API estará disponible en `http://localhost:8000`. Acceso a documentación Swagger interactiva en `http://localhost:8000/docs`.

- **Frontend (Streamlit):**
  ```bash
  cd frontend
  streamlit run app.py
  ```
  Esto levantará el dashboard en `http://localhost:8501`.
