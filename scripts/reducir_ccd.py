
from pyraf import iraf
import os
import sys

cwd = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.abspath(os.path.join(cwd, ".."))
os.chdir(root_dir)

print(f"[INFO] Directorio de trabajo: {os.getcwd()}")


output_dir = "resultados"
lista_bias = "bias.lst"
lista_dark = "dark.lst"
lista_flat = "flat.lst"

output_bias_path = os.path.join(output_dir, "Zero.fits")
output_dark_path = os.path.join(output_dir, "Dark.fits")
output_flat_path = os.path.join(output_dir, "Flat.fits")

os.makedirs(output_dir, exist_ok=True)
print(f"[INFO] Los resultados se guardarán en: ./{output_dir}/")


def delete_if_exists(filepath):
    if os.path.exists(filepath):
        print(f"  [AVISO] El archivo '{filepath}' ya existe. Borrando para sobreescribir.")
        os.remove(filepath)

iraf.imred()
iraf.ccdred()

def check_lista(nombre_lista):
    if not os.path.exists(nombre_lista):
        sys.exit(f"[ERROR] No se encuentra la lista: {nombre_lista}")
    else:
        print(f"[OK] Lista encontrada: {nombre_lista}")

check_lista(lista_bias)
check_lista(lista_dark)
check_lista(lista_flat)

print(f"Reduciendo bias... -> {output_bias_path}")
delete_if_exists(output_bias_path)
iraf.zerocombine(
    input=f"@{lista_bias}",
    output=os.path.splitext(output_bias_path)[0],
    combine="average",
    ccdtype="",
    process="no"
)

print(f"Reduciendo dark... -> {output_dark_path}")
delete_if_exists(output_dark_path)
iraf.darkcombine(
    input=f"@{lista_dark}",
    output=os.path.splitext(output_dark_path)[0],
    combine="average",
    reject="minmax",
    scale="mode",
    ccdtype="",
    process="no"
)

print(f"Reduciendo flat... -> {output_flat_path}")
delete_if_exists(output_flat_path)
iraf.flatcombine(
    input=f"@{lista_flat}",
    output=os.path.splitext(output_flat_path)[0],
    combine="average",
    reject="minmax",
    scale="mode",
    ccdtype="",
    process="no"  
)

print(f"\n[ÉXITO] Reducción completada. Revisa la carpeta '{output_dir}'.")