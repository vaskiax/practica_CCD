import os
import matplotlib.pyplot as plt
from pyraf import iraf
from scipy.stats import linregress

iraf.images()

dark_base_dir = 'datos/dark'
bias_master_path = 'resultados/Zero.fits'
temp_image = 'resultados/temp_dark_sub.fits' # Imagen temporal para la resta

exposure_dirs = sorted(os.listdir(dark_base_dir), key=lambda x: float(x.replace('_', '.').rstrip('s')))

tiempos = []
medias_dark = []

print(f"Directorio actual: {os.getcwd()}")
print("\nAnalizando corriente oscura con IRAF...")
for exp_dir in exposure_dirs:
    try:
        tiempo_s = float(exp_dir.replace('_', '.').rstrip('s'))
        current_dir = os.path.join(dark_base_dir, exp_dir)
        
        dark_file_name = os.listdir(current_dir)[0]
        dark_file_path = os.path.join(current_dir, dark_file_name)
        
        hselect_output = iraf.hselect(
            images=dark_file_path,
            fields="naxis1,naxis2",
            expr="yes",
            Stdout=1
        )
        size_str = hselect_output[0].strip()
        w_str, h_str = size_str.split()
        w, h = int(w_str), int(h_str)
        
        x_start, x_end = w // 4, 3 * w // 4
        y_start, y_end = h // 4, 3 * h // 4
        region = f'[{x_start}:{x_end},{y_start}:{y_end}]'
        
        print(f"  - Tiempo: {tiempo_s:7.4f} s, Archivo: {dark_file_name}, Región: {region}")
        
        # ## NUEVA LÓGICA A PRUEBA DE FALLOS ##
        # Antes de llamar a imarith, nos aseguramos de que el archivo de salida no existe.
        if os.path.exists(temp_image):
            os.remove(temp_image)
            
        # 1. Restar el bias con imarith. Ahora nunca encontrará un archivo existente.
        iraf.imarith(
            operand1=dark_file_path,
            op='-',
            operand2=bias_master_path,
            result=temp_image
        )
        
        # 2. Obtener la media del dark corregido
        imstat_output = iraf.imstatistics(images=temp_image + region, fields="mean", format="no", Stdout=1)
        mean_value = float(imstat_output[-1].strip())
        
        tiempos.append(tiempo_s)
        medias_dark.append(mean_value)
        
    except (ValueError, IndexError):
        print(f"  [AVISO] Omitiendo el directorio {exp_dir} por un error.")
        continue

if os.path.exists(temp_image):
    os.remove(temp_image)

slope, intercept, r_value, p_value, std_err = linregress(tiempos, medias_dark)
dark_current = slope

print(f"\nCorriente Oscura (Pendiente): {dark_current:.4f} ADU/s")
print(f"Factor de correlación (R^2): {r_value**2:.4f}")

plt.figure(figsize=(10, 6))
plt.plot(tiempos, medias_dark, 'o', label='Media de Darks (corregidos)')
plt.plot(tiempos, [intercept + slope * t for t in tiempos], 'r-', 
         label=f'Ajuste lineal\nDark Current = {dark_current:.4f} ADU/s')
plt.title('Corriente Oscura del CCD (con IRAF)')
plt.xlabel('Tiempo de Exposición (s)')
plt.ylabel('Flujo Promedio (ADU)')
plt.grid(True)
plt.legend()

output_path = 'resultados/2_grafica_dark_current_iraf.png'
plt.savefig(output_path)
print(f"Gráfica guardada en: {output_path}")
plt.show()