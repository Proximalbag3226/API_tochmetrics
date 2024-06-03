from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import uuid
from models.partidos_model import *

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
async def editar_partido(partido_id:uuid.UUID, editar_partido: EditarPartido) -> EditarPartido:
    try:
        id = str(partido_id)
        for partido in partidos_list:
            if partido.id == id:
                partido.campo = editar_partido.campo
                partido.deportivo = editar_partido.deportivo
                partido.ligar = editar_partido.liga
                partido.torneo = editar_partido.torneo
                partido.categoria = editar_partido.categoria
                partido.eq = editar_partido.eq
                partido.ev = editar_partido.ev
                partido.fecha = editar_partido.fecha
                partido.arbitro = editar_partido.arbitro
                partido.hora = editar_partido.hora
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Partido no encontrado")
            return editar_partido
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No se puede editar el partido")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@partidos_route.delete('/eliminar_partido/{id}', tags = ["Partidos"], status_code=status.HTTP_200_OK, response_description="Eliminar un partido existente")
async def eliminar_partido(id_partido: uuid.UUID) :
    try:
        id = str(id_partido)
        for partido in partidos_list:
            if partido.id == id:
                partidos_list.remove(partido)
        content = [partido.dict() for partido in partidos_list]
        
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")