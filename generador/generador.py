import random

tiposInstancias = ["Pequena", "Mediana", "Grande"]

categorias = ["Muro", "Techo", "Piso", "Ventana", "Puerta"]

totalInstancias = 15

semilla = 50
random.seed(semilla)

instanciasPorTipo = 5
#Rellenar con valores Max o podria ser un rango de x a y
uMax = [  ]

categoriasDeElementos = {
    "Pequena": (3, 4),
    "Mediana": (5, 5),
    "Grande": (5, 5)
}

alternativasPorCategoria = {
    "Pequena": (5, 10),
    "Mediana": (11, 25),
    "Grande": (26, 50)
}

elementosLibresPorTipo = {
    "Pequena": (2, 4),
    "Mediana": (5, 8),
    "Grande": (9, 15)
}

areaCasa = {
    "min": ,
    "max": 
}

alturaCasa = {
    "min": ,
    "max": 
}

areaPorCategoria = {
    "Muro": ( , ),
    "Techo": ( , ),
    "Piso": ( , ),
    "Ventana": ( , ),
    "Puerta": ( , )
}

transmitancia = {
    "min": ,
    "max": 
}

costo = {
    "min": ,
    "max": 
}

def generarVivienda():
    largo = random.uniform(largoCasa["min"], largoCasa["max"])
    ancho = random.uniform(anchoCasa["min"], anchoCasa["max"])
    altura = random.uniform(alturaCasa["min"], alturaCasa["max"])
    area = largo * ancho
    volumen = area * altura
    return largo, ancho, altura, area, volumen

#ideas de funciones: 
def generarElementos(tipoInstancia, largo, ancho, altura):
    pass

def generarCatalogo(tipoInstancia, categorias):
    pass

def generarUMax(...):
    pass

def validarInstancia(...):
    pass

def generarInstancia(tipoInstancia):
    pass

def generarInstancias():
    pass
