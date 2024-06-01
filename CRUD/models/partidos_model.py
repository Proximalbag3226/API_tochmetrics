from pydantic import BaseModel, validator
import uuid
import re
from datetime import datetime

class CrearPartido(BaseModel):
    id: str = str(uuid.uuid4())
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
        'json_schema_extra': {
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

    @staticmethod
    def eliminar_puntuacion(texto: str) -> str:
        sin_signos = re.sub(r'[^\w\s]', '', texto)
        return sin_signos.strip().lower()

    @validator('campo', 'deportivo', 'liga', 'torneo', 'categoria', 'eq', 'ev', 'arbitro')
    def validar_nombre(cls, value):
        value = cls.eliminar_puntuacion(value)
        if not isinstance(value, str):
            raise ValueError("El campo debe ser un string")
        elif len(value) < 5 or len(value) > 25:
            raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
        return value

    @validator('fecha')
    def validar_fecha(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD")
        return value

    @validator('hora')
    def validar_hora(cls, value):
        if not re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', value):
            raise ValueError("La hora debe tener el formato HH:MM (24 horas)")
        return value