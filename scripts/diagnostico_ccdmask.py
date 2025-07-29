from pyraf import iraf

iraf.noao()
iraf.imred()
iraf.ccdred()

print("="*50)
print(" PARÁMETROS REALES PARA LA TAREA 'CCDRED.CCDMASK'")
print("="*50)
print("Por favor, copia todo el texto que aparece debajo de esta línea y pégalo en la respuesta.")
print("\n")

iraf.ccdred.ccdmask.lParam()