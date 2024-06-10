from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4
from utils.validacion import validar_fecha

class Crear_liga(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nombre_liga: str
    fecha_creacion: str
    descripcion: str
    imagen: str

    class Config:
        schema_extra = {
            'example': {
                'id': '123e4567-e89b-12d3-a456-426614174000',
                'nombre_liga': 'EjemploL',
                'fecha_creacion': '2024-12-05',
                'descripcion': 'EjemploD',
                'imagen': 'http://example.com/imagen.jpg'
            }
        }

    @validator('fecha_creacion')
    def validar_fecha(cls, value):
        return validar_fecha(value)
