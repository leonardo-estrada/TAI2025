#1. Importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio

#2.Inicialización APP
app= FastAPI(
            title=" Mi primer API", 
             description= "Leonardo Estrada Lobera",
             version= "1.0.0"
             )
#BD Ficticia 
usuarios = [
    {"id": "1", "nombre" : "Leo", "edad":"20"},
    {"id": "2", "nombre" : "Danna", "edad":"18"},
    {"id": "3", "nombre" : "Santiago", "edad":"25"},
    {"id": "4", "nombre" : "Daniel", "edad":"24"},
    {"id": "5", "nombre" : "Danna", "edad":"18"},
    {"id": "6", "nombre" : "Paula", "edad":"25"},
]

#3.Endpoints
@app.get("/", tags= ["Inicio"])
async def holaMundo():
    return{"mensaje" : "Hola mundo FastAPI"}

@app.get("/bienvenidos", tags= ["Inicio"])
async def bien():
    return {"mensaje":"Bienvenidos"}

@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3)#simulación petición a otra API, consulta a BD...
    return {
        "Calificación" : "10",
        "Estatus":"200"
            }

@app.get("/v1/usuario/{id}", tags= ["Parametros"])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resultado" : "usuario encontrado",
        "Estatus":"200"
            }

@app.get("/v1/usuarios_op/", tags=['Parámetro Opcional']) # Endpoint con parámetro opcional
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario ["id"] == id:
                return {"Usuario encontrado":id, "Datos":usuario}
        return{"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso":"No se proporcionó ID"}


@app.get("/v1/usuario/", tags= ["CRUD HTTP"])
async def consultaUno():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios

    }

@app.post("/v1usuarios/", tags=["CRUD HTTP"])
async def crea_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "usuario agregado correctamente",
        "status": "200",
        "usuario": usuario
    }    

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, datos: dict):
    for usuario in usuarios:
        if usuario["id"] == str(id):  
            usuario.update(datos)
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id: int):
    for i, usuario in enumerate(usuarios):
        if int(usuario["id"]) == id:
            usuarios.pop(i)
            return {
                "mensaje": "Usuario eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )