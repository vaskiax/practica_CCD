# scripts/3_ganancia_ruido_evolucion.py
import os
import math
from pyraf import iraf
import matplotlib.pyplot as plt
import numpy as np

# --- CARGA DE PAQUETES Y CONFIGURACIÓN ---
iraf.images()

# --- RUTAS A LOS ARCHIVOS ---
bias_dir = 'datos/bias/0_1s'
flat_base_dir = 'datos/flat'

# --- RUTAS A ARCHIVOS TEMPORALES ---
B1_path = 'resultados/temp_B1.fits'
B2_path = 'resultados/temp_B2.fits'
delta_B_path = 'resultados/temp_delta_B.fits'
F1_path = 'resultados/temp_F1.fits'
F2_path = 'resultados/temp_F2.fits'
delta_F_path = 'resultados/temp_delta_F.fits'
# Lista de archivos temporales de los flats para limpiar en cada bucle
temp_flat_files = [F1_path, F2_path, delta_F_path]
# Lista completa de archivos a limpiar al final
temp_files_to_clean = [B1_path, B2_path, delta_B_path] + temp_flat_files

# --- FUNCIÓN AUXILIAR PARA OBTENER ESTADÍSTICAS ---
def get_stats(image_path, region):
    """Usa imstatistics para obtener la media y la desviación estándar."""
    stats = iraf.imstatistics(images=image_path + region, fields="mean,stddev", format="no", Stdout=1)
    mean_str, stddev_str = stats[0].strip().split()
    return float(mean_str), float(stddev_str)

try:
    # --- PASO 1: PROCESAR IMÁGENES BIAS (se hace una sola vez) ---
    print("\n--- Procesando imágenes Bias (una sola vez) ---")
    bias_files = [os.path.join(bias_dir, f) for f in os.listdir(bias_dir)]
    n_bias = len(bias_files)
    if n_bias < 2: exit("[ERROR] Se necesitan al menos 2 imágenes bias.")
    
    # Limpiar archivos de bias temporales si existen de una corrida anterior
    for f in [B1_path, B2_path, delta_B_path]:
        if os.path.exists(f): os.remove(f)

    bias_group1 = bias_files[:n_bias//2]
    bias_group2 = bias_files[n_bias//2:]
    iraf.imcombine(input=','.join(bias_group1), output=B1_path, combine='average')
    iraf.imcombine(input=','.join(bias_group2), output=B2_path, combine='average')
    iraf.imarith(operand1=B1_path, op='-', operand2=B2_path, result=delta_B_path)
    
    # Definir la región de análisis usando una imagen de referencia
    hselect = iraf.hselect(images=bias_files[0], fields="naxis1,naxis2", expr="yes", Stdout=1)
    w, h = map(int, hselect[0].strip().split())
    region = f'[{w//4}:{3*w//4},{h//4}:{3*h//4}]'
    
    media_B1, _ = get_stats(B1_path, region)
    media_B2, _ = get_stats(B2_path, region)
    _, stddev_delta_B = get_stats(delta_B_path, region)
    variance_delta_B = stddev_delta_B ** 2
    
    print(f"Valores de Bias calculados y fijos para todo el análisis:")
    print(f"  - Media B1: {media_B1:.2f}, Media B2: {media_B2:.2f}")
    print(f"  - Varianza(delta_B): {variance_delta_B:.2f}")

    # --- PASO 2: ITERAR SOBRE CADA TIEMPO DE EXPOSICIÓN DE LOS FLATS ---
    # Se seleccionan los tiempos de exposición que están en la zona lineal del detector
    exposure_dirs = ['0_05s', '0_1s', '0_2s', '0_4s', '0_8s', '1_6s', '3_2s', '6_4s', '12_8s', '25_6s']
    resultados = []
    
    print("\n--- Iniciando bucle sobre los tiempos de exposición de los Flats ---")
    for exp_dir in exposure_dirs:
        try:
            # Solución al error: Limpiar los archivos temporales de la iteración anterior
            for f in temp_flat_files:
                if os.path.exists(f):
                    os.remove(f)

            tiempo_s = float(exp_dir.replace('_', '.').rstrip('s'))
            flat_dir = os.path.join(flat_base_dir, exp_dir)
            flat_files = [os.path.join(flat_dir, f) for f in os.listdir(flat_dir)]
            n_flats = len(flat_files)

            if n_flats < 2: continue

            print(f"\nProcesando tiempo de exposición: {tiempo_s} s...")
            
            flat_group1 = flat_files[:n_flats//2]
            flat_group2 = flat_files[n_flats//2:]

            iraf.imcombine(input=','.join(flat_group1), output=F1_path, combine='average')
            iraf.imcombine(input=','.join(flat_group2), output=F2_path, combine='average')
            iraf.imarith(operand1=F1_path, op='-', operand2=F2_path, result=delta_F_path)
            
            media_F1, _ = get_stats(F1_path, region)
            media_F2, _ = get_stats(F2_path, region)
            _, stddev_delta_F = get_stats(delta_F_path, region)
            variance_delta_F = stddev_delta_F ** 2

            numerador_G = (media_F1 + media_F2) - (media_B1 + media_B2)
            denominador_G = variance_delta_F - variance_delta_B

            if denominador_G <= 0: continue

            G = numerador_G / denominador_G
            RN = G * stddev_delta_B / math.sqrt(2)
            
            resultados.append({'t': tiempo_s, 'media_F1': media_F1, 'media_F2': media_F2, 'G': G, 'RN': RN})
            print(f"  - G estimada: {G:.2f} e-/ADU, RN estimado: {RN:.2f} e-")
            
        except (ValueError, IndexError, FileNotFoundError) as e:
            print(f"  - Omitiendo {exp_dir} debido a un error: {e}")
            continue

    # --- PASO 3: MOSTRAR TABLA Y GRÁFICAS DE RESULTADOS ---
    print("\n" + "="*85)
    print(" " * 30 + "TABLA DE RESULTADOS FINALES")
    print("="*85)
    print(f"{'Tiempo (s)':<12} | {'Media F1':<12} | {'Media F2':<12} | {'Media B1':<12} | {'Media B2':<12} | {'G (e-/ADU)':<12} | {'RN (e-)'}")
    print("-" * 85)
    for r in resultados:
        print(f"{r['t']:<12.2f} | {r['media_F1']:<12.2f} | {r['media_F2']:<12.2f} | {media_B1:<12.2f} | {media_B2:<12.2f} | {r['G']:<12.2f} | {r['RN']:.2f}")
    print("-" * 85)

    # --- CÁLCULO DE PROMEDIOS MEJORADO ---
    print("\n--- ANÁLISIS DE PROMEDIOS ---")

    # Promedio Global (usando todos los puntos)
    avg_G_global = np.mean([r['G'] for r in resultados])
    print(f"Valor Promedio Global de Ganancia (G) (usando {len(resultados)} puntos): {avg_G_global:.2f} e-/ADU")

    # Promedio Filtrado (usando solo los puntos con señal alta, que son más estables)
    umbral_adu = 5000  # Umbral ajustable
    ganancias_estables = [r['G'] for r in resultados if r['media_F1'] > umbral_adu]
    avg_G_filtrado = np.mean(ganancias_estables) if ganancias_estables else np.nan
    print(f"Valor Promedio Filtrado de Ganancia (G) (usando flats con >{umbral_adu} ADU, {len(ganancias_estables)} puntos): {avg_G_filtrado:.2f} e-/ADU")

    # El Ruido de Lectura debería ser constante, por lo que se promedian todos los valores
    avg_RN = np.mean([r['RN'] for r in resultados])
    print(f"Valor Promedio de Ruido de Lectura (RN) (usando {len(resultados)} puntos): {avg_RN:.2f} e-")

    # --- SECCIÓN DE GRÁFICAS MEJORADA ---
    tiempos_plot = [r['t'] for r in resultados]
    ganancias_plot = [r['G'] for r in resultados]
    ruidos_plot = [r['RN'] for r in resultados]

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)
    fig.suptitle('Caracterización del Detector: Ganancia y Ruido de Lectura', fontsize=16, y=0.98)

    # Gráfico de Ganancia con AMBOS promedios para comparación
    ax1.plot(tiempos_plot, ganancias_plot, 'o-', color='royalblue', label='G por tiempo de exp.')
    ax1.axhline(avg_G_global, color='orange', linestyle=':', label=f'Promedio Global G = {avg_G_global:.2f} e-/ADU')
    ax1.axhline(avg_G_filtrado, color='red', linestyle='--', label=f'Promedio Filtrado G = {avg_G_filtrado:.2f} e-/ADU')
    ax1.set_title('Evolución de la Ganancia (G)', fontsize=12)
    ax1.set_ylabel('Ganancia (e-/ADU)')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend()
    ax1.set_xscale('log')

    # Gráfico de Ruido de Lectura
    ax2.plot(tiempos_plot, ruidos_plot, 'o-', color='seagreen', label='RN por tiempo de exp.')
    ax2.axhline(avg_RN, color='red', linestyle='--', label=f'Promedio RN = {avg_RN:.2f} e-')
    ax2.set_title('Evolución del Ruido de Lectura (RN)', fontsize=12)
    ax2.set_xlabel('Tiempo de Exposición (s)')
    ax2.set_ylabel('Ruido de Lectura (e-)')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend()

    # Ajustar el espaciado para evitar superposiciones
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.1, right=0.95, hspace=0.35)
    
    output_path = 'resultados/3_grafica_ganancia_ruido_evolucion.png'
    plt.savefig(output_path, dpi=150) # Guardar con mayor resolución
    print(f"\nGráficas mejoradas guardadas en: {output_path}")
    
    plt.show()

finally:
    # --- PASO 4: LIMPIEZA FINAL ---
    print("\nLimpiando archivos temporales...")
    for f in temp_files_to_clean:
        if os.path.exists(f):
            os.remove(f)
    print("Limpieza completada.")