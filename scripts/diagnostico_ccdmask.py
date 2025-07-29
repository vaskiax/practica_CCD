# scripts/diagnostico_ccdmask.py
from pyraf import iraf

# Cargamos los paquetes necesarios para llegar a la tarea ccdmask
iraf.noao()
iraf.imred()
iraf.ccdred()

print("="*50)
print(" PARÁMETROS REALES PARA LA TAREA 'CCDRED.CCDMASK'")
print("="*50)
print("Por favor, copia todo el texto que aparece debajo de esta línea y pégalo en la respuesta.")
print("\n")

# Esta es la función de PyRAF equivalente a 'lpar ccdmask' en la terminal de IRAF.
# Nos mostrará la lista de todos los parámetros y sus nombres correctos.
iraf.ccdred.ccdmask.lParam()