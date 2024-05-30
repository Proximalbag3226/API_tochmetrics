import re

def eliminar_puntuacion(texto: str)-> str:
    try:
        sin_signos = re.sub(r'[^\w\s]', '', texto)
        return sin_signos.strip().lower()
    except Exception as e:
        print(f"Error al eliminar la puntuacion {e}")
        return texto
        