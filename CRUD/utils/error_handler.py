# Middleware para manejar errores HTTP (si es necesario)
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

app = APIRouter()

@app.middleware('http')
async def http_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
