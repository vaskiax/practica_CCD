# scripts/1_linealidad_iraf.py
import os
import matplotlib.pyplot as plt
from pyraf import iraf

# Cargamos los paquetes necesarios de IRAF
# IMAGES contiene hselect e imstatistics
iraf.images() 

flat_base_dir = 'datos/flat'
exposure_dirs = sorted(os.listdir(flat_base_dir), key=lambda x: float(x.replace('_', '.').rstrip('s')))

tiempos = []
medias_flujo = []

print(f"Directorio actual: {os.getcwd()}")
print("\nAnalizando linealidad con IRAF (hselect + imstatistics)...")
for exp_dir in exposure_dirs:
    try:
        tiempo_s = float(exp_dir.replace('_', '.').rstrip('s'))
        current_dir = os.path.join(flat_base_dir, exp_dir)
        
        flat_file_name = os.listdir(current_dir)[0]
        flat_file_path = os.path.join(current_dir, flat_file_name)
        
        # --- CÁLCULO DINÁMICO DE LA REGIÓN USANDO SÓLO IRAF ---
        # NUEVO: Usamos la tarea 'hselect' de IRAF para leer el tamaño de la imagen
        # $I se asegura de que no imprima el nombre del archivo, solo los valores
        hselect_output = iraf.hselect(
            images=flat_file_path,
            fields="naxis1,naxis2",
            expr="yes",
            Stdout=1
        )
        
        # El resultado es una lista de strings, ej: ['512\t512\n']
        # Lo procesamos para obtener los números
        size_str = hselect_output[0].strip()
        w_str, h_str = size_str.split()
        w, h = int(w_str), int(h_str)

        # Calculamos la región central (el 50% interior)
        x_start, x_end = w // 4, 3 * w // 4
        y_start, y_end = h // 4, 3 * h // 4
        
        # Construimos la cadena de la región para IRAF
        region = f'[{x_start}:{x_end},{y_start}:{y_end}]'
        
        print(f"  - Tiempo: {tiempo_s:.4f} s, Archivo: {flat_file_name}, Tamaño: {w}x{h}, Región: {region}")
        
        # Ejecutamos imstatistics con la región calculada dinámicamente
        imstat_output = iraf.imstatistics(images=flat_file_path + region, fields="mean", format="no", Stdout=1)
        
        mean_value = float(imstat_output[-1].strip())
        
        tiempos.append(tiempo_s)
        medias_flujo.append(mean_value)
        
    except (ValueError, IndexError):
        print(f"  [AVISO] Omitiendo el directorio {exp_dir} por un error.")
        continue

# --- Generar la gráfica (Sin cambios) ---
plt.figure(figsize=(10, 6))
plt.plot(tiempos, medias_flujo, 'o-', label='Flujo promedio (IRAF imstat)')
plt.title('Respuesta del CCD (Linealidad)')
plt.xlabel('Tiempo de Exposición (s)')
plt.ylabel('Flujo Promedio (ADU)')
plt.xscale('log')
plt.grid(True, which="both", ls="--")
plt.legend()

output_path = 'resultados/1_grafica_linealidad_iraf.png'
plt.savefig(output_path)
print(f"\nGráfica de linealidad guardada en: {output_path}")
plt.show()