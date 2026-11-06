
import json
import os
import subprocess
import time

rutaActual = os.path.dirname(os.path.abspath(__file__))
rutaInstancias = os.path.join(rutaActual, "..", "instancias", "instancias.json")
rutaLp = os.path.join(rutaActual, "solveando.lp")
rutaResultados = os.path.join(rutaActual, "resultados")

os.makedirs(rutaResultados, exist_ok=True)

with open(rutaInstancias, "r", encoding="utf-8") as archivo:
    instancias = json.load(archivo)

def generarModelo(instancia):
    elementos = instancia["elementos"]
    catalogo = instancia["catalogo"]
    fijos = [el for el in elementos if el["estado"] == "fijo"]
    libres = [el for el in elementos if el["estado"] == "libre"]

    variables = []
    objetivo = []
    restriccionU = []
    restricciones = []
    datosVariables = {}

    areaTotal = sum(el["area"] for el in elementos)
    sumaUFijos = sum(el["area"] * el["U_fijo"] for el in fijos)
    costoFijos = sum(el["area"] * el["C_fijo"] for el in fijos)

    for i, el in enumerate(libres):
        variablesElemento = []

        for j, alt in enumerate(catalogo[el["categoria"]]):
            nombre = f"x_{i+1}_{j+1}"
            variables.append(nombre)
            objetivo.append(f"{el['area'] * alt['costo']:.8f} {nombre}")
            restriccionU.append(f"{el['area'] * alt['U']:.8f} {nombre}")
            variablesElemento.append(nombre)
            datosVariables[nombre] = (el, alt, j + 1)

        restricciones.append(" + ".join(variablesElemento) + " = 1;")

    limiteU = instancia["UMax_exigido"] * areaTotal - sumaUFijos

    modelo = "min: " + " + ".join(objetivo) + ";\n\n"
    modelo += "\n".join(restricciones) + "\n\n"
    modelo += " + ".join(restriccionU) + f" <= {limiteU:.8f};\n\n"
    modelo += "bin " + ", ".join(variables) + ";\n"

    return modelo, datosVariables, costoFijos

def resolverInstancia(instancia):
    nombre = instancia["id_instancia"]
    rutaSalida = os.path.join(rutaResultados, nombre + ".txt")
    modelo, datosVariables, costoFijos = generarModelo(instancia)

    with open(rutaLp, "w", encoding="utf-8") as archivo:
        archivo.write(modelo)

    inicio = time.perf_counter()
    resultado = subprocess.run(["lp_solve", rutaLp], capture_output=True, text=True)
    tiempo = time.perf_counter() - inicio
    salida = resultado.stdout

    costoLibres = 0
    sumaU = 0
    reporte = f"Instancia: {nombre}\n"

    if "This problem is infeasible" in salida:
        reporte += "Estado: Infactible\n"
    else:
        reporte += "Estado: Óptimo\n\n"
        seleccionadas = []

        for linea in salida.splitlines():
            partes = linea.split()
            if len(partes) == 2 and partes[0] in datosVariables and float(partes[1]) > 0.5:
                seleccionadas.append(datosVariables[partes[0]])

        reporte += "Elementos fijos:\n"
        for el in instancia["elementos"]:
            if el["estado"] == "fijo":
                costo = el["area"] * el["C_fijo"]
                sumaU += el["area"] * el["U_fijo"]
                reporte += f"- {el['id']}: U={el['U_fijo']}, costo={costo}\n"

        reporte += "\nElementos seleccionados:\n"
        for el, alt, numero in seleccionadas:
            costo = el["area"] * alt["costo"]
            costoLibres += costo
            sumaU += el["area"] * alt["U"]
            reporte += f"- {el['id']}: alternativa {numero}, U={alt['U']}, costo={costo}\n"

        areaTotal = sum(el["area"] for el in instancia["elementos"])
        uEquivalente = sumaU / areaTotal
        umax = instancia["UMax_exigido"]

        reporte += f"\nCosto libres: {costoLibres}\n"
        reporte += f"Costo fijos: {costoFijos}\n"
        reporte += f"Costo total: {costoLibres + costoFijos}\n"
        reporte += f"U equivalente: {uEquivalente:.6f}\n"
        reporte += f"U máxima: {umax:.6f}\n"
        reporte += f"Margen térmico: {umax - uEquivalente:.6f}\n"

    reporte += f"Tiempo: {tiempo:.6f} segundos\n"

    with open(rutaSalida, "w", encoding="utf-8") as archivo:
        archivo.write(reporte)

def resolverInstancias():
    for instancia in instancias:
        resolverInstancia(instancia)

if __name__ == "__main__":
    resolverInstancias()
