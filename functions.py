import random
import msboard as ms
import msgame as mg

def seleccionar_probabilidad(cpd, valor, evidencia):
    padres = [v for v in cpd.variables if v != cpd.variable]
    valores_evidencia = tuple(evidencia[var] for var in padres)
    return cpd.values[valor][valores_evidencia]

def generar_valor_aleatorio(cardinalidad, probabilidades):
    p = random.random()
    acumuladas = 0
    for valor in range(cardinalidad):
        acumuladas += probabilidades[valor]
        if p <= acumuladas:
            return valor


