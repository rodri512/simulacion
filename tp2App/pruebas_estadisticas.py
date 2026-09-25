import math
from collections import Counter

def prueba_promedios(numeros):
    n = len(numeros)
    media = sum(numeros) / n
    z0 = abs(media - 0.5) * math.sqrt(n) / math.sqrt(1/12)
    aceptado = z0 < 1.96
    return media, z0, aceptado

def prueba_rachas(numeros):
    n = len(numeros)
    signos = []
    for i in range(n - 1):
        if numeros[i] < numeros[i+1]:
            signos.append('+')
        else:
            signos.append('-')
            
    rachas = 1
    for i in range(1, len(signos)):
        if signos[i] != signos[i-1]:
            rachas += 1
            
    mu = (2 * n - 1) / 3
    sigma = math.sqrt((16 * n - 29) / 90)
    z0 = abs(rachas - mu) / sigma
    aceptado = z0 < 1.96
    return rachas, z0, aceptado

def prueba_poker(numeros):
    n = len(numeros)
    probs = {
        "Par": 0.50400, "Dos Pares": 0.10800, "Tercia": 0.07200, 
        "Póker": 0.00450, "Escalera": 0.00010, "Full": 0.00900, "Todos diferentes": 0.30240
    }
    fo = {k: 0 for k in probs.keys()}
    
    for u in numeros:
        val = int(round(u % 1, 5) * 100000)
        digitos = str(val).zfill(5)
        conteos = sorted(list(Counter(digitos).values()), reverse=True)
        
        if conteos == [5]: fo["Escalera"] += 1 
        elif conteos == [4, 1]: fo["Póker"] += 1
        elif conteos == [3, 2]: fo["Full"] += 1
        elif conteos == [3, 1, 1]: fo["Tercia"] += 1
        elif conteos == [2, 2, 1]: fo["Dos Pares"] += 1
        elif conteos == [2, 1, 1, 1]: fo["Par"] += 1
        else: fo["Todos diferentes"] += 1
        
    chi_cuadrado = 0
    for k in probs.keys():
        fe = n * probs[k]
        if fe > 0:
            chi_cuadrado += ((fo[k] - fe)**2) / fe
            
    aceptado = chi_cuadrado < 12.592
    return chi_cuadrado, aceptado

def prueba_series(numeros):
    n = len(numeros)
    fo = [[0]*5 for _ in range(5)]
    pares_totales = n - 1
    
    for i in range(pares_totales):
        x = min(int(numeros[i] / 0.2), 4)
        y = min(int(numeros[i+1] / 0.2), 4)
        fo[x][y] += 1
        
    fe = pares_totales / 25
    chi_cuadrado = 0
    for i in range(5):
        for j in range(5):
            chi_cuadrado += ((fo[i][j] - fe)**2) / fe
            
    aceptado = chi_cuadrado < 36.415
    return chi_cuadrado, aceptado

def prueba_corridas_promedio(numeros):
    n = len(numeros)
    # Generar secuencia binaria: 0 si Ui < 0.5 y 1 si Ui > 0.5
    secuencia = [1 if u > 0.5 else 0 for u in numeros]
    
    # Contar Frecuencia Observada (FO) de cada longitud de corrida
    fo = {}
    longitud_actual = 1
    for i in range(1, n):
        if secuencia[i] == secuencia[i-1]:
            longitud_actual += 1
        else:
            fo[longitud_actual] = fo.get(longitud_actual, 0) + 1
            longitud_actual = 1
    fo[longitud_actual] = fo.get(longitud_actual, 0) + 1
    
    chi_cuadrado = 0
    # Calcular FE_i = (N - i + 3) / (2^(i+1))
    for i, obs in fo.items():
        fe = (n - i + 3) / (2**(i+1))
        if fe > 0:
            chi_cuadrado += ((obs - fe)**2) / fe
            
    # Comparación usando X^2_{0.05, 2} = 5.991
    aceptado = chi_cuadrado < 5.991
    return chi_cuadrado, aceptado, fo

def prueba_corridas_arriba_abajo(numeros):
    n = len(numeros)
    if n < 2:
        return 0, False, {}
        
    # Generar secuencia binaria: 0 si Ui < Ui+1 y 1 si Ui > Ui+1
    secuencia = []
    for i in range(n - 1):
        secuencia.append(1 if numeros[i] > numeros[i+1] else 0)
        
    fo = {}
    longitud_actual = 1
    for i in range(1, len(secuencia)):
        if secuencia[i] == secuencia[i-1]:
            longitud_actual += 1
        else:
            fo[longitud_actual] = fo.get(longitud_actual, 0) + 1
            longitud_actual = 1
    fo[longitud_actual] = fo.get(longitud_actual, 0) + 1
    
    chi_cuadrado = 0
    for i, obs in fo.items():
        # FE_i = 2 * [ ((i^2 + 3i + 1)N - (i^3 + 3i^2 - i - 4)) / (i + 3)! ]
        numerador = ((i**2 + 3*i + 1)*n) - (i**3 + 3*(i**2) - i - 4)
        denominador = math.factorial(i + 3)
        fe = 2 * (numerador / denominador)
        
        if fe > 0:
            chi_cuadrado += ((obs - fe)**2) / fe
            
    # Comparación usando X^2_{0.05, 2} = 5.991
    aceptado = chi_cuadrado < 5.991
    return chi_cuadrado, aceptado, fo