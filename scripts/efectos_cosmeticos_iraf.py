import os
from pyraf import iraf

iraf.noao()
iraf.imred()
iraf.ccdred()

iraf.set(overwrite='yes')

flat_maestro = 'resultados/Flat.fits'
bad_pixel_mask = 'resultados/bad_pixel_mask.pl' 

print(f"Directorio actual: {os.getcwd()}")
print("--- Creando Máscara de Píxeles Malos con 'ccdmask' ---")
print(f"Imagen de entrada: {flat_maestro}")
print(f"Máscara de salida: {bad_pixel_mask}")

iraf.ccdred.ccdmask.setParam('lsigma', 3.0) 
iraf.ccdred.ccdmask.setParam('hsigma', 3.0)

iraf.ccdred.ccdmask(
    image=flat_maestro,
    mask=bad_pixel_mask,
    # El parámetro 'ccdtype' no existe en tu versión, lo quitamos
)

print("\n--- ¡Máscara creada con éxito! ---")
print(f"El archivo '{bad_pixel_mask}' ha sido generado.")
print("Este es un archivo de texto en formato IRAF Pixel List (PL).")
print("\n¿Cómo usar los datos para encontrar píxeles muertos?")
print("1. Abre el archivo de texto y verás las coordenadas (columnas y filas) de los píxeles marcados como defectuosos.")
print("2. 'Píxeles muertos' son aquellos que tienen un flujo muy bajo. 'ccdmask' los encuentra con el umbral 'lsigma' (low sigma).")
print("\n¿Cómo puedes identificar otros defectos?")
print("1. 'Píxeles calientes' (flujo alto constante) se detectan con 'hsigma'. También se pueden ver muy bien en una imagen 'dark' de larga exposición.")
print("2. Para visualizar la máscara, puedes usar la tarea 'implot' de IRAF o herramientas como DS9, que pueden superponer regiones o máscaras sobre una imagen.")