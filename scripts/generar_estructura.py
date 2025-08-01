import os

root_dir = os.path.abspath('.')
output_file = 'estructura_proyecto.txt'

def generar_arbol(directorio, prefijo=''):
    contenido = []
    entradas = sorted(os.listdir(directorio))
    
    for i, nombre in enumerate(entradas):
        ruta = os.path.join(directorio, nombre)
        es_ultimo = i == len(entradas) - 1
        conector = '└── ' if es_ultimo else '├── '
        linea = f"{prefijo}{conector}{nombre}"
        contenido.append(linea)
        if os.path.isdir(ruta):
            extension_prefijo = '    ' if es_ultimo else '│   '
            contenido += generar_arbol(ruta, prefijo + extension_prefijo)
    return contenido

arbol = generar_arbol(root_dir)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"📁 {os.path.basename(root_dir)}/\n")
    f.write('\n'.join(arbol))

print(f"Estructura guardada en: {output_file}")
