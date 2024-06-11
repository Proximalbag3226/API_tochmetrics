from typing import Optional
from pydantic import BaseModel

class Liga(BaseModel):
    id: str  
    nombre_liga: str
    fecha_creacion: str
    descripcion: str
    imagen: Optional[str] = None
    documento: Optional[str] = None

class CrearLiga(BaseModel):
    nombre_liga: str
    fecha_creacion: str
    descripcion: str
