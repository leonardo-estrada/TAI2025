from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List
from enum import Enum
from datetime import datetime

#Inicialización de app
app = FastAPI(
    title="API Biblioteca Digital",
    description="Práctica 5 - Biblioteca Digital",
    version="1.0.0"
)

class EstadoLibro(str, Enum):
    disponible = "disponible"
    prestado = "prestado"

class Libro(BaseModel):
    id: int
    nombre: str = Field(min_length=2, max_length=100)
    año: int
    paginas: int = Field(gt=1)
    estado: EstadoLibro = EstadoLibro.disponible

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr

class Prestamo(BaseModel):
    id: int
    libro_id: int
    usuario: Usuario

libros = []
prestamos = []


@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    
    año_actual = datetime.now().year
    
    if libro.año <= 1450 or libro.año > año_actual:
        raise HTTPException(
            status_code=400,
            detail="Año del libro inválido"
        )
    
    libros.append(libro)
    return libro

@app.get("/libros")
def listar_libros():
    return libros

@app.get("/libros/buscar/{nombre}")
def buscar_libro(nombre: str):
    resultado = [l for l in libros if l.nombre.lower() == nombre.lower()]
    return resultado

@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):
    
    for libro in libros:
        if libro.id == prestamo.libro_id:
            
            if libro.estado == EstadoLibro.prestado:
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )
            
            libro.estado = EstadoLibro.prestado
            prestamos.append(prestamo)
            return {"mensaje": "Préstamo registrado"}
    
    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

@app.put("/prestamos/{id}/devolver")
def devolver_libro(id: int):
    
    for prestamo in prestamos:
        if prestamo.id == id:
            
            for libro in libros:
                if libro.id == prestamo.libro_id:
                    libro.estado = EstadoLibro.disponible
                    return {"mensaje": "Libro devuelto correctamente"}
    
    raise HTTPException(
        status_code=409,
        detail="El préstamo no existe"
    )   

@app.delete("/prestamos/{id}")
def eliminar_prestamo(id: int):
    
    for i, prestamo in enumerate(prestamos):
        if prestamo.id == id:
            prestamos.pop(i)
            return {"mensaje": "Préstamo eliminado"}
    
    raise HTTPException(
        status_code=409,
        detail="El préstamo ya no existe"
    )