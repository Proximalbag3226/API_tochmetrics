from pydantic import BaseModel, Field, validator
from utils.validacion import eliminar_puntuacion, validar_nombre, validar_fecha, validar_hora

class Crear_estadistica(BaseModel):
    num_partido: int = Field(gt=0)
    lugar: str
    fecha: str
    hora: str
    anot: int
    ob: int 
    sack: int
    inter:int
    pex:int
    panot: int
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'num_partido': 2,
                'lugar': 'EjemploL',
                'fecha':'2024-12-05',
                'hora': '17:00',
                'anot':2,
                'ob' : 3,
                'sack' : 4,
                'inter' : 5,
                'pex' : 6,
                'panot': 7,
            }
        }
    }

    @validator('lugar')
    def validar_nombres(cls, value):
        value = eliminar_puntuacion(value)
        return validar_nombre(value)
    
    @validator('fecha')
    def validar_fecha(cls, value):
        return validar_fecha(value)
    
    @validator('hora')
    def validar_hora(cls, value):
        return validar_hora(value)