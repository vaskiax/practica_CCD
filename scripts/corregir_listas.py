import os

def renombrar_subcarpetas(directorio_raiz):
    for carpeta_actual, subcarpetas, archivos in os.walk(directorio_raiz, topdown=False):
        for subcarpeta in subcarpetas:
            if ',' in subcarpeta:
                subcarpeta_vieja = os.path.join(carpeta_actual, subcarpeta)
                subcarpeta_nueva = os.path.join(carpeta_actual, subcarpeta.replace(',', '_'))
                print(f"Renombrando: {subcarpeta_vieja} -> {subcarpeta_nueva}")
                os.rename(subcarpeta_vieja, subcarpeta_nueva)

if __name__ == "__main__":
    ruta_base = os.getcwd()  # Usa el directorio actual
    renombrar_subcarpetas(ruta_base)
