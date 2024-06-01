from fastapi import FastAPI, APIRouter, status, Depends, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from models.partidos_model import *
import uuid
import re
from uuid import UUID

partidos_list = []

partidos_route = APIRouter()

@partidos_route.post('/agregar_partido', tags=["Partidos"], status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo partido")
async def create_partido(partido: CrearPartido) -> CrearPartido:
    try:
        partidos_list.append(partido)
        content = [partido.dict()]
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
@partidos_route.options('/agregar_partido', tags=["Partidos"])
async def options_partido():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)


@partidos_route.get('/obtener_partido', tags=["Partidos"], status_code=status.HTTP_200_OK, response_description="Obtener partidos")
async def obtener_partido():
    try:
        content = [partido.dict() for partido in partidos_list]
        return JSONResponse(content = content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@partidos_route.put('/editar_partido/{id}', tags=["Partidos"], status_code=status.HTTP_201_CREATED, response_description="Modificar un partido ya existente por ID")
async def editar_partido(partido_id:UUID, editar_partido: CrearPartido) -> CrearPartido:
    try:
        for index, partido in enumerate(partidos_list):
            if partido.id == str(partido_id):
                partidos_list[index] = editar_partido
                return editar_partido
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")

@partidos_route.delete('/eliminar_partido/{id}', tags = ["Partidos"], status_code=status.HTTP_200_OK, response_description="Eliminar un partido existente")
async def eliminar_partido(id_partido: UUID) :
    try:
        id = str(id_partido)
        for partido in partidos_list:
            if partido.id == id:
                partidos_list.remove(partido)
        content = [partido.dict() for partido in partidos_list]
        
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
        