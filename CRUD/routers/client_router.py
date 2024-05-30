from fastapi import Path, Query, APIRouter, status
from fastapi.responses import JSONResponse
from typing import List, Union
from CRUD.models.users_model import *
from CRUD.utils.vaidacion import eliminar_puntuacion as ep

empleados_list: List[Empleado] = []

empleados_route = APIRouter()
@empleados_route.get('/empleados', tags=["Empleados"])
def get_empleados() -> List[Empleado]:
    content = [empleado.model_dump() for empleado in empleados_list]
    return JSONResponse(content=content)

@empleados_route.get('/empleados/{nombre}', tags=["Empleados"], status_code=status.HTTP_200_OK, response_description="Buscar empleados por nombre")
def get_nombre(nombre: str) -> Union[Empleado, dict]:
    nombre = ep(nombre)
    try:
        empleados_encontrados = [empleado for empleado in empleados_list if empleado.nombre== nombre]
        if empleados_encontrados:
            return JSONResponse(content=[empleado.model_dump() for empleado in empleados_encontrados], status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@empleados_route.get('/empleados/{salario}', tags=["Empleados"], status_code=status.HTTP_200_OK, response_description="Obtener los empleados por su salario")
def get_salario(salario: float) -> Union[Empleado, dict]:
    try:
        salarios_encontrados = [empleado_salario for empleado_salario in empleados_list if empleado_salario.salario == salario]
        if salarios_encontrados:
            return JSONResponse(content=[empleado_salario.model_dump() for empleado_salario in salarios_encontrados], status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@empleados_route.post('/agregar_empleado', tags=["Empleados"], status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo empleado")
def create_empleado(empleado: Crear_empleado) -> Empleado:
    empleados_list.append(empleado)
    content = [empleado.model_dump()]
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@empleados_route.options('/agregar_empleado', tags=["Empleados"])
def options_empleado():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)


@empleados_route.put('/empleados_modificar/{nombre}', tags=["Empleados"], status_code=status.HTTP_201_CREATED, response_description="Modifica un empleado ya creado")
def modifica_empleado(nombre: str, empleado: Subir_empleado) -> Union[Empleado, dict]:
    try:
        for i in empleados_list:
            if i.nombre == nombre:
                i.edad = empleado.edad
                i.salario = empleado.salario
                i.puesto = empleado.puesto
                
        content = [i.model_dump() for i in empleados_list]
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@empleados_route.delete('/empleados_borrar/{nombre}', tags=["Empleados"], status_code=status.HTTP_200_OK)
def delete_empleados_borrar(nombre: str) -> Union[List[Empleado], dict]:
    try:
        nombre = ep(nombre)
        empleados_borrados = [empleado for empleado in empleados_list if empleado.nombre == nombre]
        if empleados_borrados:
            empleados_list = [empleado for empleado in empleados_list if empleado.nombre != nombre]
            content = [empleado.model_dump() for empleado in empleados_list]
            return JSONResponse(content=content, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Empleado no registrado"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
