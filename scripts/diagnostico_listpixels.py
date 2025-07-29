from pyraf import iraf
import sys

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

iraf.images.imutil.listpixels.lParam()