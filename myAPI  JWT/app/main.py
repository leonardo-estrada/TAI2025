# Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


# Inicialización de APP
app= FastAPI(
    title='Mi Primer API',
    description="Leonardo Estrada",
    version='1.0.0'
)

# BD ficticia
usuarios=[
    {"id":1,"nombre":"Andrés","edad":"21"},
    {"id":2,"nombre":"Rafael","edad":"22"},
    {"id":3,"nombre":"Leonardo","edad":"20"},
]


# Modelo Pydantic, creación del modelo
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario") # Validaciones personalizadas
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")


@app.get("/", tags=['Inicio']) 
async def holaMundo():
    return  {"mensaje":"Hola mundo FASTAPI"}

# Seguridad OAuth2 con JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0.08


def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM], 
            options={"leeway": 0} 
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


@app.get("/bienvenida", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) 
    return {"Calificacion":"9",
            "Estatus":"200"
            }

@app.get("/v1/usuarioO/{id}", tags=['Parámetros']) 
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {"Resultado":"Usuario encontrado",
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
    

# LOGIN con OAuth2 
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # Validación simple
    if username != "admin" or password != "1234":
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token({"sub": username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
#Endpoint CRUD GET
@app.get("/v1/usuarios/", tags=['CRUD HTTP']) 
async def consultaUsuario():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }

#Endpoint CRUD POST
@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED) 
async def crearUsuario(usuario:crear_usuario): # Uso del modelo
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El ID ya existe"
            )
    usuarios.append(usuario.dict())  
    return{
        "mensaje":"Usuario agregado correctamente",
        "status":"200",
        "usuario":usuarios
    }


#Endpoint CRUD PUT
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizarUsuario(
    id: int,
    usuario_actualizado: dict,
    usuario: str = Depends(validar_token)
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": f"Usuario actualizado por {usuario}",
                "datos": usuarios[index]
            }

    raise HTTPException(status_code=400, detail="Usuario no encontrado")

#Endpoint CRUD DELETE
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminarUsuario(
    id: int,
    usuario: str = Depends(validar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado por {usuario}"
            }

    raise HTTPException(status_code=404, detail="No se encontró el usuario")