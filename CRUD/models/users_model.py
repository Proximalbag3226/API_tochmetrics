from pydantic import BaseModel, Field, validator
import uuid
import re

class Empleado(BaseModel):
    nombre: str
    edad: int
    puesto: str
    salario: float

class Crear_empleado(BaseModel):
    id: str = str(uuid.uuid4())
    nombre: str
    edad: int = Field(ge=18, le=70, description="Edad del empleado debe ser mayor a 18 y menor a 70 años")
    puesto: str
    salario: float

    model_config = {
        'json_schema_extra': {
            'example': {
                'nombre': 'Ejemplo',
                'edad': 25,
                'puesto': 'Ejemplo',
                'salario': 30000.00
            }
        }
    }   

    @staticmethod
    def eliminar_puntuacion(texto: str) -> str:
        sin_signos = re.sub(r'[^\w\s]', '', texto)
        return sin_signos.strip().lower()

    @validator('nombre')
    def validar_nombre(cls, value):
        value = cls.eliminar_puntuacion(value)
        if not isinstance(value, str):
            raise ValueError("El campo debe ser un string")
        elif len(value) < 5 or len(value) > 25:
            raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
        return value

    @validator('salario')
    def validar_salario(cls, value):
        if value < 7468 or value > 40000:
            raise ValueError("El salario debe estar entre 7468 y 40000")
        return value
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())


class Subir_empleado(BaseModel):
    nombre: str
    edad: int = Field(ge=18, le=70, description="La edad modificada debe ser mayor que 18 y menor que 70")
    puesto: str
    salario: float
    
    model_config = {
        'json_schema_extra':{
            'example':
                {
                    'nombre' : 'Nombre modificado',
                    'edad' : 'Edad nueva',
                    'puesto' : 'Nuevo puesto',
                    'salario' : 'Salario nuevo'
                }
        }
    }
    
    @staticmethod
    def eliminar_puntuacion(texto: str) -> str:
        sin_signos = re.sub(r'[^\w\s]', '', texto)
        return sin_signos.strip().lower()

    @validator('nombre')
    def validar_nombre(cls, value):
        value = cls.eliminar_puntuacion(value)
        if not isinstance(value, str):
            raise ValueError("El campo debe ser un string")
        elif len(value) < 5 or len(value) > 25:
            raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
        return value

    @validator('salario')
    def validar_salario(cls, value):
        if value < 7468 or value > 40000:
            raise ValueError("El salario debe estar entre 7468 y 40000")
        return value
    
