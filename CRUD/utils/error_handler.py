#Importamos lo nesesario para el funcionamiento del middleware 
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
class HTTP_error_handler(BaseHTTPMiddleware):
    
    def  __init__(self, app: FastAPI,) -> None:
        super().__init__(app)
    async def dispath(self, request:Request, callnext)-> Response:
        try:
            return await callnext(request)
        except Exception as e:
            content = f"Error: {str(e)}"
            status_code = status.HTTP_403_FORBIDDEN
            return JSONResponse(content=content, status_code=status_code)            
        
        