from pydantic import BaseModel, Field

# Modelo Pydantic, creación del modelo
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario") # Validaciones personalizadas
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")