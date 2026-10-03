import random

tiposInstancias = ["Pequeña", "Mediana", "Grande"]
categorias = ["Muro", "Techo", "Piso", "Ventana", "Puerta"]
totalInstancias = 15

#Cambiar la semilla para obtener diferentes instancias
semilla = 50
random.seed(semilla)

instanciasPorTipo = 5

uMax = {
    "holgura_min": 0.1, 
    "holgura_max": 0.35 
}

categoriasDeElementos = {
    "Pequeña": (3, 4),
    "Mediana": (5, 5),
    "Grande": (5, 5)
}

alternativasPorCategoria = {
    "Pequeña": (5, 10),
    "Mediana": (11, 25),
    "Grande": (26, 50)
}

elementosLibresPorTipo = {
    "Pequeña": (2, 4),
    "Mediana": (5, 8),
    "Grande": (9, 15)
}

largoCasa = {"min": 5.0, "max": 12.0}
anchoCasa = {"min": 5.0, "max": 10.0}
alturaCasa = {"min": 2.3, "max": 2.8}
areaCasa = {"min": 25.0, "max": 120.0}

areaPorCategoria = {
    "Muro": (8.0, 25.0),
    "Techo": (25.0, 120.0),
    "Piso": (25.0, 120.0),
    "Ventana": (1.0, 3.5),
    "Puerta": (1.6, 2.5)
}

transmitancia = {"min": 0.2, "max": 5.0}
costo = {"min": 5000, "max": 65000}

def generarVivienda():
    largo = random.uniform(largoCasa["min"], largoCasa["max"])
    ancho = random.uniform(anchoCasa["min"], anchoCasa["max"])
    altura = random.uniform(alturaCasa["min"], alturaCasa["max"])
    area = largo * ancho
    volumen = area * altura
    return round(largo, 2), round(ancho, 2), round(altura, 2), round(area, 2), round(volumen, 2)

def generarElementos(tipoInstancia, largo, ancho, altura):
    elementos = []
    num_cat = random.randint(categoriasDeElementos[tipoInstancia][0], categoriasDeElementos[tipoInstancia][1])
    cats_seleccionadas = random.sample(categorias, num_cat)
    
    min_libres = elementosLibresPorTipo[tipoInstancia][0]
    max_libres = elementosLibresPorTipo[tipoInstancia][1]
    total_libres_objetivo = random.randint(min_libres, max_libres)
    
    cantidad_total_elementos = max(15, total_libres_objetivo + 5)
    
    for i in range(cantidad_total_elementos):
        cat = random.choice(cats_seleccionadas)
        area_el = random.uniform(areaPorCategoria[cat][0], areaPorCategoria[cat][1])
        elementos.append({
            "id": f"{cat}_{i+1}", 
            "categoria": cat, 
            "area": round(area_el, 2), 
            "estado": "fijo"
        })
        
    indices_libres = random.sample(range(len(elementos)), total_libres_objetivo)
    for i in indices_libres:
        elementos[i]["estado"] = "libre"
        
    return elementos, cats_seleccionadas

def generarCatalogo(tipoInstancia, cats_seleccionadas):
    catalogo = {}
    for cat in cats_seleccionadas:
        num_alt = random.randint(alternativasPorCategoria[tipoInstancia][0], alternativasPorCategoria[tipoInstancia][1])
        us = [round(random.uniform(transmitancia["min"], transmitancia["max"]), 2) for _ in range(num_alt)]
        costos = [round(random.uniform(costo["min"], costo["max"]), 0) for _ in range(num_alt)]
        
        us.sort(reverse=True)
        costos.sort()
        
        catalogo[cat] = [{"id_alt": f"Alt_{j+1}", "U": u, "costo": c} for j, (u, c) in enumerate(zip(us, costos))]
        
    return catalogo

def generarUMax(elementos, catalogo):
    area_total = sum(el["area"] for el in elementos)
    suma_u_min = 0
    suma_u_max = 0
    
    for el in elementos:
        cat = el["categoria"]
        valores_u_cat = [alt["U"] for alt in catalogo[cat]]
        u_mejor = min(valores_u_cat)
        u_peor = max(valores_u_cat)
        
        if el["estado"] == "libre":
            suma_u_min += u_mejor * el["area"]
            suma_u_max += u_peor * el["area"]
        else:
            u_fijo = random.choice(valores_u_cat)
            el["U_fijo"] = u_fijo 
            suma_u_min += u_fijo * el["area"]
            suma_u_max += u_fijo * el["area"]
            
    u_eq_min = suma_u_min / area_total
    u_eq_max = suma_u_max / area_total
    
    holgura = random.uniform(uMax["holgura_min"], uMax["holgura_max"])
    umax_calculado = u_eq_min + holgura * (u_eq_max - u_eq_min)
    
    return round(umax_calculado, 3), round(u_eq_min, 3)

def validarInstancia(umax_calculado, u_eq_min):
    return umax_calculado >= u_eq_min

def generarInstancia(tipoInstancia, id_instancia):
    largo, ancho, altura, area, volumen = generarVivienda()
    elementos, cats_seleccionadas = generarElementos(tipoInstancia, largo, ancho, altura)
    catalogo = generarCatalogo(tipoInstancia, cats_seleccionadas)
    
    umax_calculado, u_eq_min = generarUMax(elementos, catalogo)
    es_factible = validarInstancia(umax_calculado, u_eq_min)
    
    return {
        "id_instancia": f"{tipoInstancia}_{id_instancia}",
        "tipo": tipoInstancia,
        "dimensiones": {"area": area, "volumen": volumen},
        "UMax_exigido": umax_calculado,
        "factible": es_factible,
        "catalogo": catalogo,
        "elementos": elementos
    }

def generarInstancias():
    lista_instancias = []
    id_contador = 1
    
    for tipo in tiposInstancias:
        for _ in range(instanciasPorTipo):
            instancia = generarInstancia(tipo, id_contador)
            lista_instancias.append(instancia)
            id_contador += 1
            
    return lista_instancias

# === BLOQUE DE EJECUCIÓN ===
if __name__ == "__main__":
    instancias_finales = generarInstancias()
    
    with open("instancias.txt", "w", encoding="utf-8") as archivo:
        for inst in instancias_finales:
            id_latex = inst['id_instancia'].replace("_", "\\_")
            tipo = inst['tipo']
            num_cat = len(inst['catalogo'])
            num_libres = sum(1 for el in inst['elementos'] if el['estado'] == 'libre')
            umax = inst['UMax_exigido']
            factible = "S\\'i" if inst['factible'] else "No"
            
            linea = f"{id_latex} & {tipo} & {num_cat} & {num_libres} & {umax} & {factible} \\\\ \\hline\n"
            archivo.write(linea)
            
    print("Archivo 'instancias.txt' generado.")
