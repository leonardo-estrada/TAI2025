# Importacion fastapi, status, HTTPException, Depends
from fastapi import FastAPI
from app.routers import usuarios, varios 

# Inicialización de APP
app= FastAPI(
    title='Mi Primer API',
    description="Leonardo Estrada",
    version='1.0.0'
)

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
    
