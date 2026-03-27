from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion


from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB

routerU=APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)

#Endpoint CRUD GET
@routerU.get("/") 
async def leer_usuarios(db: Session = Depends(get_db)):        
    query = db.query(UsuarioDB).all()
    return{
        "status":"200", 
        "total": len(query),
        "data": query
    }

#Endpoint CRUD POST
@routerU.post("/", status_code=status.HTTP_201_CREATED) 
async def crearUsuario(usuarioP:crear_usuario, db: Session = Depends(get_db)): # Uso del modelo
    
    usuarioNuevo= UsuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)

    return{
        "mensaje":"Usuario agregado",
        "usuario":usuarioP
    }


#Endpoint CRUD PUT
@routerU.put("/") 
async def actualizarUsuario(id: str, usuario_actualizado: dict):
    # Buscamos el usuario por su ID
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            # Reemplazamos los datos del usuario en esa posición
            usuarios[index] = usuario_actualizado
            return {
                "mensaje":"Usuario actualizado correctamente",
                "datos":usuarios[index]
            }
    
    # En caso de no encontrar al usuario, lanzamos un error
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )

#Endpoint CRUD DELETE
@routerU.delete("/{id}", status_code=status.HTTP_200_OK) 
async def eliminarUsuario(id: int, userAuth:str=Depends(verificar_peticion)):
    # Buscamos el usuario en la lista
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado por {userAuth}"
            }
    
    # Si no lo encuentra manda error
    raise HTTPException(
        status_code=404,
        detail="No se encontró el usuario para eliminar"
    )