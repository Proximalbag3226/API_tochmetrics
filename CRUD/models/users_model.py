from fastapi import FastAPI, APIRouter, status, Depends, Request, Response
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uuid
import re


class Crear_empleado(BaseModel):
    id: str = str(uuid.uuid4())
    usuario: str
    contraseña: str
    nombre: str
    apellidos: str
    correo: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'usuario': 'EjemploU',
                'contraseña':'EjemploC',
                'nombre': 'Ejemplo',
                'apellidos':'EjemploAp',
                'correo' : 'ejemplo@gmail.com'
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
    
    @validator('apellidos')
    def validar_apellidos(cls, value):
        value = cls.eliminar_puntuacion(value)
        if not isinstance(value, str):
            raise ValueError("El campo debe ser un string")
        elif len(value) < 5 or len(value) > 25:
            raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
        return value
    