import os

# Carpeta raíz donde están los datos (ajusta si es necesario)
base_dir = os.path.join(os.getcwd(), "datos")
tipos_calibracion = ["bias", "dark", "flat"]
extensiones_validas = [".fit", ".fits", ".fts"]

print(f"📂 Buscando dentro de: {base_dir}")

for tipo in tipos_calibracion:
    ruta_carpeta = os.path.join(base_dir, tipo)
    lista_archivos = []

    print(f"\n🔍 Explorando tipo: {tipo} en {ruta_carpeta}")

    for root, dirs, files in os.walk(ruta_carpeta):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensiones_validas):
                ruta_relativa = os.path.relpath(os.path.join(root, file), start=os.getcwd())
                lista_archivos.append(ruta_relativa)
                print(f"  ➕ Agregado: {ruta_relativa}")

    salida = f"{tipo}.lst"
    with open(salida, "w") as f:
        for item in lista_archivos:
            f.write(item + "\n")

    print(f"✅ {salida} generado con {len(lista_archivos)} archivos.")
