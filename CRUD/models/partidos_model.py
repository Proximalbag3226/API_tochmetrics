from pydantic import BaseModel, validator, Field
import uuid
from utils.validacion import eliminar_puntuacion, validar_nombre, validar_fecha, validar_hora



class CrearPartido(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    campo: str
    deportivo: str
    liga: str
    torneo: str
    categoria: str
    eq: str
    ev: str
    fecha: str
    arbitro: str
    hora: str
    
    model_config = {
        'json_schema_extra':{
            'example': {
                'id': str(uuid.uuid4()),
                'campo': 'CampoEjemplo',
                'deportivo': 'DeportivoEjemplo',
                'liga': 'LigaDeMiCasa',
                'torneo': 'TorneoEjemplo',
                'categoria': 'CategoriaEjemplo',
                'eq': 'EquipoLocal',
                'ev': 'EquipoVisitante',
                'fecha': '2024-12-05',
                'arbitro': 'ArbitroEjemplo',
                'hora': '17:00'
            }
        }
    }

    @validator('campo', 'deportivo', 'liga', 'torneo', 'categoria', 'eq', 'ev', 'arbitro')
    def validar_nombres(cls, value):
        value = eliminar_puntuacion(value)
        return validar_nombre(value)

    @validator('fecha')
    def validar_fecha_field(cls, value):
        return validar_fecha(value)

    @validator('hora')
    def validar_hora_field(cls, value):
        return validar_hora(value)

class EditarPartido(BaseModel):
    campo: str
    deportivo: str
    liga: str
    torneo: str
    categoria: str
    eq: str
    ev: str
    fecha: str
    arbitro: str
    hora: str
    
    model_config = {
        'json_schema_extra':{
            'example': {
                'campo': 'CampoEjemplo',
                'deportivo': 'DeportivoEjemplo',
                'liga': 'LigaDeMiCasa',
                'torneo': 'TorneoEjemplo',
                'categoria': 'CategoriaEjemplo',
                'eq': 'EquipoLocal',
                'ev': 'EquipoVisitante',
                'fecha': '2024-12-05',
                'arbitro': 'ArbitroEjemplo',
                'hora': '17:00'  
            }
        }
    }

    @validator('campo', 'deportivo', 'liga', 'torneo', 'categoria', 'eq', 'ev', 'arbitro')
    def validar_nombre_field(cls, value):
        value = eliminar_puntuacion(value)
        return validar_nombre(value)

    @validator('fecha')
    def validar_fecha_field(cls, value):
        return validar_fecha(value)

    @validator('hora')
    def validar_hora_field(cls, value):
        return validar_hora(value)