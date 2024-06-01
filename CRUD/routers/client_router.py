from fastapi import FastAPI, APIRouter, status, Depends, Request, Response
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from CRUD.models.users_model import *
import uuid
import re

empleados_list = []

empleados_route = APIRouter()

@empleados_route.post('/agregar_empleado', tags=["Empleados"], status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo empleado")
def create_empleado(empleado: Crear_empleado) -> Crear_empleado:
    empleados_list.append(empleado)
    content = [empleado.dict()]
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)

@empleados_route.options('/agregar_empleado', tags=["Empleados"])
def options_empleado():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)

@empleados_route.get('obtener_empleados', tags=["Empleados"], status_code=status.HTTP_200_OK, response_description="Obtener empleados registrados")
def obtener_empleado():
    content = [empleado.dict() for empleado in empleados_list]
    return JSONResponse(content = content)