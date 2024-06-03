from pydantic import BaseModel, Field, validator
import uuid
from utils.validacion import eliminar_puntuacion, validar_nombre, validar_fecha, validar_hora

class Crear_usuario(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    usuario: str
    contraseña: str
    nombre: str
    apellidos: str
    correo: str
    tipo: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': str(uuid.uuid4()),
                'usuario': 'EjemploU',
                'contraseña':'EjemploC',
                'nombre': 'Ejemplo',
                'apellidos':'EjemploAp',
                'correo' : 'ejemplo@gmail.com',
                'tipo' : 'Ejemplotipo'
            }
        }
    }

    @validator('nombre', 'apellidos', 'tipo')
    def validiar_nombres(cls, value):
        value = eliminar_puntuacion(value)
        return validar_nombre(value)
    
class EditarUsuario(BaseModel):
    usuario: str
    contraseña: str
    nombre: str
    apellidos: str
    correo: str
    tipo: str
    
    model_config = {
        'json_schema_extra':{
            'example':{
                'usuario' : 'EjemploU',
                'contraseña' : 'EjemploC',
                'nombre' : 'Ejemplo',
                'apellidos' : 'EjemploAp',
                'correo' : 'ejemplo@gmail.com',
                'tipo' :'Ejemplotipo'
            }
        }
    }
    
    @validator('nombre', 'apellidos', 'tipo')
    def validiar_nombres(cls, value):
        value = eliminar_puntuacion(value)
        return validar_nombre(value)
    