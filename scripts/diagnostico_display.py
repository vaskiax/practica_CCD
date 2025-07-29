# scripts/diagnostico_display.py
from pyraf import iraf

# Cargamos el paquete que contiene la tarea 'display'
iraf.tv()

print("="*50)
print(" PARÁMETROS REALES PARA LA TAREA 'TV.DISPLAY'")
print("="*50)
print("Por favor, copia todo el texto que aparece debajo de esta línea y pégalo en la respuesta.")
print("\n")

# Esta es la función de PyRAF para listar los parámetros de la tarea 'display'.
iraf.tv.display.lParam()