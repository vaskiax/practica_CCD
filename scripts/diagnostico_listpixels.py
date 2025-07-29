# scripts/diagnostico_listpixels.py
from pyraf import iraf
import sys

# Cargamos los paquetes necesarios para llegar a la tarea
try:
    iraf.images()
    iraf.imutil()
except Exception as e:
    print(f"[ERROR] No se pudo cargar un paquete esencial: {e}")
    sys.exit()

print("="*50)
print(" PARÁMETROS REALES PARA LA TAREA 'IMAGES.IMUTIL.LISTPIXELS'")
print("="*50)
print("Por favor, copia todo el texto que aparece debajo de esta línea y pégalo en la respuesta.")
print("\n")

# Esta función nos mostrará la lista de todos los parámetros
# y sus nombres correctos para la tarea 'listpixels'.
iraf.images.imutil.listpixels.lParam()