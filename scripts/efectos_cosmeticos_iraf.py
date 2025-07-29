# scripts/4_efectos_cosmeticos_iraf.py
import os
from pyraf import iraf

# Cargamos los paquetes necesarios
iraf.noao()
iraf.imred()
iraf.ccdred()

# Permitimos sobreescribir el archivo de salida si ya existe
iraf.set(overwrite='yes')

# Rutas a los archivos
flat_maestro = 'resultados/Flat.fits'
bad_pixel_mask = 'resultados/bad_pixel_mask.pl' 

print(f"Directorio actual: {os.getcwd()}")
print("--- Creando Máscara de Píxeles Malos con 'ccdmask' ---")
print(f"Imagen de entrada: {flat_maestro}")
print(f"Máscara de salida: {bad_pixel_mask}")

# Configuramos los umbrales usando los nombres de parámetros correctos
iraf.ccdred.ccdmask.setParam('lsigma', 3.0) 
iraf.ccdred.ccdmask.setParam('hsigma', 3.0)

# ## CORRECCIÓN FINAL ##: Usamos los nombres de parámetros exactos de tu sistema
# 'image' en lugar de 'images'/'input'
# 'mask' en lugar de 'masks'/'output'
# Y llamamos a la tarea con la ruta completa para máxima seguridad
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