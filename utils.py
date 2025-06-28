import re

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def formatear_nombre(cadena):
    # Divide la cadena en palabras, capitaliza la primera letra de cada palabra
    # y convierte el resto a minúsculas.
    palabras = cadena.split()
    nombre_formateado = []
    for palabra in palabras:
        if palabra:
            nombre_formateado.append(palabra[0].upper() + palabra[1:].lower())
    return " ".join(nombre_formateado)