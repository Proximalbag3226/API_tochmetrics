from pydantic import BaseModel, Field, validator
from utils.validacion import validar_fecha

class Crear_reporte(BaseModel):
    num_partido: int = Field(gt=0)
    lugar: str
    fecha: str
    equipos: str
    descripcion: str
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'num_partido': 2,
                'lugar': 'EjemploL',
                'fecha':'2024-12-05',
                'equipos': 'EjemploE',
                'descripcion': 'EjemploD'
            }
        }
    }
    
    @validator('fecha')
    def validar_fecha(cls, value):
        return validar_fecha(value)