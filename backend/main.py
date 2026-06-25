from fastapi import FastAPI
from adapters.primary.api.routers import property_router, user_router, prediction_router

app = FastAPI(
    title="Tasador Automático de Bienes Raíces API",
    description="API hexagonal con Machine Learning para tasación inmobiliaria.",
    version="2.0.0",
)

app.include_router(property_router.router)
app.include_router(user_router.router)
app.include_router(prediction_router.router)


@app.get("/")
def root():
    return {"message": "API de Tasador funcionando. Ve a /docs para más detalles."}
