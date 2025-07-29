import os
import math
from pyraf import iraf

iraf.images()
iraf.set(overwrite='yes') # Esencial para que imcombine e imarith no fallen

FLAT_EXP_TIME_TO_USE = '3_2s'
bias_dir = 'datos/bias/0_1s'
flat_dir = os.path.join('datos/flat', FLAT_EXP_TIME_TO_USE)

B1_path = 'resultados/temp_B1.fits'
B2_path = 'resultados/temp_B2.fits'
delta_B_path = 'resultados/temp_delta_B.fits'
F1_path = 'resultados/temp_F1.fits'
F2_path = 'resultados/temp_F2.fits'
delta_F_path = 'resultados/temp_delta_F.fits'

def get_stats(image_path, region):
    """Usa imstatistics para obtener la media y la desviación estándar."""
    stats = iraf.imstatistics(images=image_path + region, fields="mean,stddev", format="no", Stdout=1)
    mean_str, stddev_str = stats[0].strip().split()
    return float(mean_str), float(stddev_str)

print("\n--- Procesando imágenes Bias ---")
bias_files = [os.path.join(bias_dir, f) for f in os.listdir(bias_dir)]
n_bias = len(bias_files)
if n_bias < 2:
    exit("[ERROR] Se necesitan al menos 2 imágenes bias.")

bias_group1 = bias_files[:n_bias//2]
bias_group2 = bias_files[n_bias//2:]

print("Combinando Bias Grupo 1 -> B1")
iraf.imcombine(input=','.join(bias_group1), output=B1_path, combine='average')
print("Combinando Bias Grupo 2 -> B2")
iraf.imcombine(input=','.join(bias_group2), output=B2_path, combine='average')

print("Calculando delta_B = B1 - B2")
iraf.imarith(operand1=B1_path, op='-', operand2=B2_path, result=delta_B_path)

print("\n--- Procesando imágenes Flat ---")
flat_files = [os.path.join(flat_dir, f) for f in os.listdir(flat_dir)]
n_flats = len(flat_files)
if n_flats < 2:
    exit(f"[ERROR] Se necesitan al menos 2 imágenes flat en {flat_dir}.")

flat_group1 = flat_files[:n_flats//2]
flat_group2 = flat_files[n_flats//2:]

print("Combinando Flat Grupo 1 -> F1")
iraf.imcombine(input=','.join(flat_group1), output=F1_path, combine='average')
print("Combinando Flat Grupo 2 -> F2")
iraf.imcombine(input=','.join(flat_group2), output=F2_path, combine='average')

print("Calculando delta_F = F1 - F2")
iraf.imarith(operand1=F1_path, op='-', operand2=F2_path, result=delta_F_path)

print("\n--- Obteniendo estadísticas de las imágenes combinadas ---")
hselect = iraf.hselect(images=F1_path, fields="naxis1,naxis2", expr="yes", Stdout=1)
w, h = map(int, hselect[0].strip().split())
region = f'[{w//4}:{3*w//4},{h//4}:{3*h//4}]'
print(f"Usando región de análisis: {region}")

media_B1, _ = get_stats(B1_path, region)
media_F1, _ = get_stats(F1_path, region)

_, stddev_delta_B = get_stats(delta_B_path, region)
_, stddev_delta_F = get_stats(delta_F_path, region)

print("\n--- Calculando Ganancia (G) y Ruido de Lectura (RN) ---")

media_B2, _ = get_stats(B2_path, region)
media_F2, _ = get_stats(F2_path, region)

variance_delta_B = stddev_delta_B ** 2
variance_delta_F = stddev_delta_F ** 2

numerador_G = (media_F1 + media_F2) - (media_B1 + media_B2)
denominador_G = variance_delta_F - variance_delta_B

if denominador_G <= 0:
    exit("[ERROR] El denominador para el cálculo de G es cero o negativo. Intenta con un flat de mayor exposición.")

G = numerador_G / denominador_G

RN = G * stddev_delta_B / math.sqrt(2)

print("\n" + "="*30)
print("      RESULTADOS FINALES")
print("="*30)
print(f"Ganancia (G)             : {G:.2f} e-/ADU")
print(f"Ruido de Lectura (RN)    : {RN:.2f} e-")
print("="*30)

print("\nLimpiando archivos temporales...")
for f in [B1_path, B2_path, delta_B_path, F1_path, F2_path, delta_F_path]:
    if os.path.exists(f):
        os.remove(f)
print("Limpieza completada.")