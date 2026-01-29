#1. Importaciones
from fastapi import FastAPI

#2.Inicialización APP
app= FastAPI()

#3.Endpoints
@app.get("/bienvenidos")
async def bien():
    return {"mensaje":"Bienvenidos"}
