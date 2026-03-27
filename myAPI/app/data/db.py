from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. Definir la url de conexión con el contenedor
DATABASE_URL= os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2. Crear el motor de conexión
engine= create_engine(DATABASE_URL)

#3. Definimos el manejo de sesiones
SessionLocal= sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

#4. Instanciamos la Base declarativa del modelo
Base = declarative_base()

#5. Funcion para manejo de sesiones por partición
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()