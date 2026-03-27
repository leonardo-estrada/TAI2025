# Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios 
from app.data.db import engine, Base

# Inicialización de APP
app= FastAPI(
    title='Mi Primer API',
    description="Leonardo Estrada",
    version='1.0.0'
)

@app.on_event("startup")
def startup_event():
    # Crear tablas cuando la app inicie y la DB esté lista
    Base.metadata.create_all(bind=engine)

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
    
