# scripts/visualizar_mascara.py
import os
import sys
from pyraf import iraf

# --- CARGA DE PAQUETES Y CONFIGURACIÓN ---
# El paquete 'tv' contiene las tareas de visualización como 'display' y 'tvmark'
iraf.tv()

# --- RUTAS A LOS ARCHIVOS A VISUALIZAR ---
image_to_display = 'resultados/Flat.fits'
mask_file = 'resultados/bad_pixel_mask.pl'

# --- VERIFICACIÓN DE QUE LOS ARCHIVOS EXISTEN ---
if not os.path.exists(image_to_display):
    sys.exit(f"[ERROR] No se encuentra la imagen de referencia: {image_to_display}")
if not os.path.exists(mask_file):
    sys.exit(f"[ERROR] No se encuentra el archivo de máscara: {mask_file}")

print(f"Directorio actual: {os.getcwd()}")
print("--- Visualizando Máscara de Píxeles Malos ---")
print("Este script abrirá un visualizador de imágenes (como DS9).")

try:
    # --- PASO 1: Mostrar la imagen de referencia (el Flat Maestro) en el frame 1 ---
    print(f"\n1. Mostrando la imagen '{image_to_display}' en el frame 1...")
    iraf.display(image=image_to_display, frame=1)

    # --- PASO 2: Marcar los píxeles de la máscara sobre la imagen mostrada ---
    print(f"2. Superponiendo los píxeles del archivo '{mask_file}'...")
    iraf.tvmark(
        frame=1,                   # El frame sobre el cual dibujar (debe coincidir con display)
        coords=mask_file,          # El archivo de texto con las coordenadas de los píxeles
        mark="circle",             # La forma de la marca (otras opciones: "point", "cross", "box")
        radii=5,                   # El radio de los círculos en píxeles
        color=204,                 # El código de color (204 es rojo en la paleta estándar de DS9)
        label="no"                 # No escribir etiquetas de texto junto a las marcas
    )

    print("\n--- ¡Visualización Lista! ---")
    print("Revisa la ventana del visualizador de imágenes (DS9 o XImtool).")
    print("Deberías ver la imagen del Flat con círculos rojos sobre los píxeles defectuosos.")
    print("Puedes usar las herramientas del visualizador (zoom, pan, escala) para inspeccionar los defectos.")
    print("\nCIERRA LA VENTANA DEL VISUALIZADOR PARA QUE EL SCRIPT TERMINE Y VUELVAS A LA TERMINAL.")

except Exception as e:
    print(f"\n[ERROR] Ocurrió un problema durante la visualización.")
    print("Asegúrate de tener un visualizador como DS9 instalado y accesible.")
    print(f"Error original: {e}")