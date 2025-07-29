# scripts/0_configurar_iraf.py
import os
from pyraf import iraf

os.chdir('..') # Moverse a la raíz del proyecto

iraf.imred()
iraf.ccdred()

# Rutas a los archivos maestros DENTRO de la carpeta de resultados
bias_maestro = 'resultados/Zero.fits'
dark_maestro = 'resultados/Dark.fits'
flat_maestro = 'resultados/Flat.fits'

# Configurar ccdproc para que sepa dónde están las calibraciones
# Esto es muy útil para tareas futuras
iraf.ccdproc.setParam('zero', bias_maestro)
iraf.ccdproc.setParam('dark', dark_maestro)
iraf.ccdproc.setParam('flat', flat_maestro)

# Permitir que las tareas sobreescriban archivos
# Esto es CLAVE para la automatización
iraf.set(overwrite='yes') 

print("--- Configuración de IRAF completada ---")
print(f"Bias maestro      -> {iraf.ccdproc.zero}")
print(f"Dark maestro      -> {iraf.ccdproc.dark}")
print(f"Flat maestro      -> {iraf.ccdproc.flat}")
print(f"Sobreescribir     -> {iraf.show('overwrite')}")
print("\n¡Listo para empezar el análisis!")