from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
import secrets


app= FastAPI(
            title=" Mi primer API", 
             description= "Leonardo Estrada Lobera",
             version= "1.0.0"
             )

#BD Ficticia
reservas = [
    {"id": 1, "nombre": "Juan Perez", "fecha_entrada": "2024-07-01", "edad": 30, "estado": "pendiente"},
    {"id": 2, "nombre": "Maria Gomez", "fecha_entrada": "2024-07-05", "edad": 25, "estado": "confirmada"},
    {"id": 3, "nombre": "Carlos Sanchez", "fecha_entrada": "2024-07-10", "edad": 40, "estado": "cancelada"}
]



class Huespedes(BaseModel):
    nombre: str = Field(..., min_length=5, max_length=50)
    fecha_entrada: str = Field(..., description="Fecha de entrada no menor a fecha actual")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")


seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "hotel")
    passAuth = secrets.compare_digest(credenciales.password, "r2026")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    

@app.post("/v1/usuario/", tags= ["Sistema de reserva"])
async def crear_reserva(huesped: Huespedes, credenciales: HTTPBasicCredentials = Depends(verificar_peticion)):
    return{
        "status":"200",
        "message":f"Reserva creada exitosamente para {huesped.nombre} de {huesped.edad} años"
    }

@app.get("/v1/usuario/", tags= ["Sistema de reserva"])
async def listar_reservas(credenciales: HTTPBasicCredentials = Depends(verificar_peticion)):
    return{
        "status":"200",
        "message":"Listado de reservas obtenido exitosamente"
    } 

@app.get("/v1/usuario/{id}", tags= ["Sistema de reserva"]) 
async def consultar_reserva(id: int, credenciales: HTTPBasicCredentials = Depends(verificar_peticion)):
    return{
        "status":"200",
        "message":f"Reserva con id {id} obtenida exitosamente"
    }

@app.put("/v1/usuarios/{id}/confirmar", tags=['Sistema de reserva']) 
async def confirmar_reserva(id: int, userAuth:str=Depends(verificar_peticion)):
    return {
        "mensaje": f"Reserva con id {id} confirmada por {userAuth}"
    }

@app.put("/v1/usuarios/{id}/cancelar", tags=['Sistema de reserva']) 
async def cancelar_reserva(id: int, userAuth:str=Depends(verificar_peticion)):
    return {
        "mensaje": f"Reserva con id {id} cancelada por {userAuth}"
    }

