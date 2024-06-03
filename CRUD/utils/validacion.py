import re
from datetime import datetime

def eliminar_puntuacion(texto: str) -> str:
    sin_signos = re.sub(r'[^\w\s]', '', texto)
    return sin_signos.strip().lower()

def validar_nombre(value: str) -> str:
    value = eliminar_puntuacion(value)
    if not isinstance(value, str):
        raise ValueError("El campo debe ser un string")
    elif len(value) < 5 or len(value) > 25:
        raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
    return value

def validar_fecha(value: str) -> str:
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError("La fecha debe tener el formato YYYY-MM-DD")
    return value

def validar_hora(value: str) -> str:
    if not re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', value):
        raise ValueError("La hora debe tener el formato HH:MM (24 horas)")
    return value
