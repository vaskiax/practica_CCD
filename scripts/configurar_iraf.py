import os
from pyraf import iraf

os.chdir('..') # Moverse a la raíz del proyecto

iraf.imred()
iraf.ccdred()

bias_maestro = 'resultados/Zero.fits'
dark_maestro = 'resultados/Dark.fits'
flat_maestro = 'resultados/Flat.fits'

iraf.ccdproc.setParam('zero', bias_maestro)
iraf.ccdproc.setParam('dark', dark_maestro)
iraf.ccdproc.setParam('flat', flat_maestro)

iraf.set(overwrite='yes') 

print("--- Configuración de IRAF completada ---")
print(f"Bias maestro      -> {iraf.ccdproc.zero}")
print(f"Dark maestro      -> {iraf.ccdproc.dark}")
print(f"Flat maestro      -> {iraf.ccdproc.flat}")
print(f"Sobreescribir     -> {iraf.show('overwrite')}")
print("\n¡Listo para empezar el análisis!")