
import json
import os
import re
import matplotlib.pyplot as plt

rutaActual = os.path.dirname(os.path.abspath(__file__))
rutaBase = os.path.dirname(rutaActual)
rutaPng = os.path.join(rutaActual, "png")
os.makedirs(rutaPng, exist_ok=True)

with open(os.path.join(rutaBase, "instancias", "instancias.json"), "r", encoding="utf-8") as f:
    instancias = json.load(f)

rutaResultados = os.path.join(rutaBase, "Solver", "resultados")

nombres = []
costos = []
transmitancias = []
transmitanciasMax = []
tiempos = []
variables = []
restricciones = []

for instancia in instancias:
    nombre = instancia["id_instancia"]
    ruta = os.path.join(rutaResultados, nombre + ".txt")
    if not os.path.exists(ruta):
        continue
    with open(ruta, "r", encoding="utf-8") as f:
        texto = f.read()
    if "Estado: Óptimo" not in texto:
        continue
    nombres.append(nombre)
    costos.append(float(re.search(r"Costo total: ([\d.]+)", texto).group(1)))
    transmitancias.append(float(re.search(r"U equivalente: ([\d.]+)", texto).group(1)))
    transmitanciasMax.append(instancia["UMax_exigido"])
    tiempos.append(float(re.search(r"Tiempo: ([\d.]+)", texto).group(1)))
    cantidadVariables = 0
    cantidadLibres = 0
    
    for elemento in instancia["elementos"]:
        if elemento["estado"] == "libre":
            cantidadLibres += 1
            categoria = elemento["categoria"]
            cantidadVariables += len(instancia["catalogo"][categoria])

    variables.append(cantidadVariables)
    restricciones.append(cantidadLibres + 1)

graficos = [
    (costos, "Costo total", "costos.png"),
    (tiempos, "Tiempo de ejecución (segundos)", "tiempos.png"),
    (variables, "Variables binarias existentes", "variables.png"),
    (restricciones, "Restricciones existentes", "restricciones.png")
]

for valores, titulo, archivo in graficos:
    plt.figure()
    plt.bar(nombres, valores)
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(rutaPng, archivo))
    plt.close()

plt.figure()
margenes = [maximo - equivalente for maximo, equivalente in zip(transmitanciasMax, transmitancias)]

plt.bar(nombres, margenes)
plt.title("Diferencia U Maximo y U obtenido")
plt.xlabel("Instancia")
plt.ylabel("U máxima - U obtenido")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(rutaPng, "transmitancia.png"))
plt.close()

print("Gráficos generados")
