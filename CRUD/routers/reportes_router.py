from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.reportes_model import Crear_reporte

reportes_list = []
reportes_route = APIRouter()

@reportes_route.post('/agregar_reporte', tags=["reportes"], status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo reporte")
async def create_reporte(reporte: Crear_reporte) -> Crear_reporte:
    try:
        reportes_list.append(reporte)
        content = reporte.model_dump()
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except ValueError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No se puede registrar el reporte")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@reportes_route.options('/agregar_reporte', tags=["reportes"])
async def options_reporte():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)

@reportes_route.get('/obtener_reportes', tags=["reportes"], status_code=status.HTTP_200_OK, response_description="Obtener reportes registrados")
async def obtener_reportes():
    try:
        content = [reporte.model_dump() for reporte in reportes_list]
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
