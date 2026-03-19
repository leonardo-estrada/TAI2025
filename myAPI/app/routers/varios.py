from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(tags=["INICIO"])


@routerV.get("/") 
async def holaMundo():
    return  {"mensaje":"Hola mundo FASTAPI"}


@routerV.get("/bienvenida")
async def bien():
    return {"mensaje":"Bienvenidos"}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(3) 
    return {"Calificacion":"9",
            "Estatus":"200"
            }

@routerV.get("/v1/usuarioO/{id}") 
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {"Resultado":"Usuario encontrado",
            "Estatus":"200"
            }


@routerV.get("/v1/usuarios_op/",) 
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario ["id"] == id:
                return {"Usuario encontrado":id, "Datos":usuario}
        return{"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso":"No se proporcionó ID"}