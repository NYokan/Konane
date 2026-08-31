"""
Proyecto N°1: Fundamentos de Inteligencia Artificial
Juego: Konane (Fase 2 - Agente Inteligente con Minimax y Poda Alfa-Beta)
Integrantes: Matías Muñoz, Javier Marchant y Daniel Rivera
"""

import copy
import math

# ==========================================
# MÓDULO 1: INTERFAZ Y CONFIGURACIÓN VISUAL
# ==========================================

def mostrar_instrucciones():
    """Imprime un resumen de las reglas y formato de entrada en consola."""
    print("\n" + "="*50)
    print(" INSTRUCCIONES DE JUEGO - KONANE VS IA")
    print("="*50)
    print("- Tablero: Coordenadas del 1 al N (Fila, Columna).")
    print("- Movimiento: Saltos ortogonales sobre piezas rivales hacia casillas vacias.")
    print("- Capturas Multiples: Ingrese la coordenada inicial y el destino final.")
    print("- Fin del Juego: Pierde el jugador que se quede sin movimientos.")
    print("="*50 + "\n")

def imprimir_tablero(tablero):
    """Renderiza el estado actual del tablero con indicadores numéricos 1-based."""
    n = len(tablero)
    print("\n   " + " ".join([str(i+1).rjust(2) for i in range(n)]))
    for i in range(n):
        fila_str = f"{str(i+1).rjust(2)} "
        for j in range(n):
            fila_str += f" {tablero[i][j]} "
        print(fila_str)
    print()

def obtener_coordenadas(mensaje, n):
    """Captura y valida la entrada del usuario, traduciéndola a base 0."""
    while True:
        try:
            entrada = input(mensaje).strip().split(',')
            if len(entrada) != 2:
                raise ValueError
            f, c = int(entrada[0]), int(entrada[1])
            if 1 <= f <= n and 1 <= c <= n:
                return f - 1, c - 1
            else:
                print(f"[!] Error: Coordenadas fuera de rango (1 a {n}).")
        except ValueError:
            print("[!] Formato invalido. Use 'fila,columna' (ej: 3,1).")

# ==========================================
# MÓDULO 2: LÓGICA Y MOTOR DEL JUEGO
# ==========================================

def crear_tablero(n):
    """
    Genera el tablero inicial nxn con patrón alternado y ejecuta la apertura.
    Apertura: Jugador A retira (1,1) y Jugador B retira (1,2).
    """
    tablero = [['A' if (i + j) % 2 == 0 else 'B' for j in range(n)] for i in range(n)]
    tablero[0][0] = '.'
    tablero[0][1] = '.'
    return tablero

def es_salto_valido(tablero, f1, c1, f2, c2, jugador):
    """
    Verifica matemáticamente la legalidad de un salto (simple o múltiple).
    """
    n = len(tablero)
    rival = 'B' if jugador == 'A' else 'A'

    # Validación de límites y ocupación básica
    if not (0 <= f1 < n and 0 <= c1 < n and 0 <= f2 < n and 0 <= c2 < n):
        return False
    if tablero[f1][c1] != jugador or tablero[f2][c2] != '.':
        return False
    
    # Validación de ortogonalidad (no diagonal)
    if f1 != f2 and c1 != c2:
        return False

    dist_f, dist_c = abs(f2 - f1), abs(c2 - c1)
    dist_total = max(dist_f, dist_c)

    # La distancia de salto siempre debe ser un número par > 0
    if dist_total == 0 or dist_total % 2 != 0:
        return False

    # Determinar el vector de dirección
    paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
    paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)

    # Verificar casillas intermedias
    for paso in range(1, dist_total + 1):
        f_actual = f1 + paso * paso_f
        c_actual = c1 + paso * paso_c
        
        if paso % 2 != 0:
            if tablero[f_actual][c_actual] != rival:
                return False  # Falta pieza rival para saltar
        else:
            if tablero[f_actual][c_actual] != '.':
                return False  # Casilla de aterrizaje ocupada

    return True

def ejecutar_salto(tablero, f1, c1, f2, c2, jugador):
    """Aplica el movimiento en el tablero, eliminando las piezas capturadas."""
    dist_total = max(abs(f2 - f1), abs(c2 - c1))
    paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
    paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)

    tablero[f1][c1] = '.'
    for paso in range(1, dist_total, 2):
        tablero[f1 + paso * paso_f][c1 + paso * paso_c] = '.'
    tablero[f2][c2] = jugador

def obtener_movimientos_legales(tablero, jugador):
    """
    Retorna una lista de tuplas con todos los movimientos válidos (f1, c1, f2, c2).
    Genera el espacio de búsqueda para el algoritmo Minimax.
    """
    n = len(tablero)
    movimientos = []
    saltos_posibles = range(2, n, 2)
    direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):
        for j in range(n):
            if tablero[i][j] == jugador:
                for df, dc in direcciones:
                    for salto in saltos_posibles:
                        f2, c2 = i + (df * salto), j + (dc * salto)
                        if es_salto_valido(tablero, i, j, f2, c2, jugador):
                            movimientos.append((i, j, f2, c2))
    return movimientos

# ==========================================
# MÓDULO 3: INTELIGENCIA ARTIFICIAL
# ==========================================

def evaluar_estado(tablero, jugador_max, jugador_min):
    """
    Función heurística basada en el diferencial de movilidad.
    Retorna un valor positivo si favorece a MAX, negativo si favorece a MIN.
    """
    movs_max = len(obtener_movimientos_legales(tablero, jugador_max))
    movs_min = len(obtener_movimientos_legales(tablero, jugador_min))
    
    # Detección inmediata de nodos terminales
    if movs_max == 0:
        return -10000  # MAX pierde
    if movs_min == 0:
        return 10000   # MAX gana
        
    return movs_max - movs_min

def minimax(tablero, profundidad, alfa, beta, es_maximizador, jugador_max, jugador_min):
    """
    Algoritmo Minimax optimizado con poda Alfa-Beta para la toma de decisiones.
    """
    jugador_actual = jugador_max if es_maximizador else jugador_min
    movimientos = obtener_movimientos_legales(tablero, jugador_actual)

    # Condición de corte: límite de profundidad o fin del juego
    if profundidad == 0 or not movimientos:
        return evaluar_estado(tablero, jugador_max, jugador_min), None

    mejor_movimiento = None

    if es_maximizador:
        max_eval = -math.inf
        for mov in movimientos:
            # Simular el movimiento
            tablero_simulado = copy.deepcopy(tablero)
            ejecutar_salto(tablero_simulado, mov[0], mov[1], mov[2], mov[3], jugador_max)
            
            # Llamada recursiva
            evaluacion, _ = minimax(tablero_simulado, profundidad - 1, alfa, beta, False, jugador_max, jugador_min)
            
            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = mov
                
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break  # Poda Alfa-Beta
        return max_eval, mejor_movimiento

    else:
        min_eval = math.inf
        for mov in movimientos:
            # Simular el movimiento
            tablero_simulado = copy.deepcopy(tablero)
            ejecutar_salto(tablero_simulado, mov[0], mov[1], mov[2], mov[3], jugador_min)
            
            # Llamada recursiva
            evaluacion, _ = minimax(tablero_simulado, profundidad - 1, alfa, beta, True, jugador_max, jugador_min)
            
            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = mov
                
            beta = min(beta, evaluacion)
            if beta <= alfa:
                break  # Poda Alfa-Beta
        return min_eval, mejor_movimiento

# ==========================================
# MÓDULO 4: BUCLE PRINCIPAL DE EJECUCIÓN
# ==========================================

def main():
    mostrar_instrucciones()
    
    # 1. Configuración de parámetros iniciales
    while True:
        try:
            n = int(input("Tamaño del tablero (n par, >= 6): "))
            if n >= 6 and n % 2 == 0:
                break
            print("[!] El tamaño debe ser un número par mayor o igual a 6.")
        except ValueError:
            print("[!] Ingrese un número entero válido.")

    while True:
        try:
            profundidad = int(input("Profundidad de analisis de la IA (recomendado 3 o 4): "))
            if profundidad > 0:
                break
            print("[!] La profundidad debe ser un entero positivo.")
        except ValueError:
            print("[!] Ingrese un número entero válido.")

    tablero = crear_tablero(n)
    
    # Jugador A (Humano) inicia siempre la partida por regla general
    turno_actual = 'A'
    jugador_humano = 'A'
    jugador_ia = 'B'
    
    # 2. Ciclo de partida
    while True:
        imprimir_tablero(tablero)
        
        # Verificar derrota antes de pedir jugada
        if not obtener_movimientos_legales(tablero, turno_actual):
            rival = 'B' if turno_actual == 'A' else 'A'
            print(f"\n[!] FIN DEL JUEGO: El jugador {turno_actual} no tiene movimientos legales.")
            ganador = "HUMANO" if rival == jugador_humano else "AGENTE IA"
            print(f">>> ¡EL {ganador} ({rival}) GANA LA PARTIDA! <<<")
            break

        print(f"Turno actual: {'HUMANO' if turno_actual == jugador_humano else 'AGENTE IA'} ({turno_actual})")
        print("-" * 40)
        
        if turno_actual == jugador_humano:
            while True:
                f1, c1 = obtener_coordenadas("Coordenada de origen (fila,columna): ", n)
                f2, c2 = obtener_coordenadas("Coordenada de destino (fila,columna): ", n)

                if es_salto_valido(tablero, f1, c1, f2, c2, turno_actual):
                    ejecutar_salto(tablero, f1, c1, f2, c2, turno_actual)
                    break
                else:
                    print("\n[!] Movimiento invalido. Revise las reglas e intente nuevamente.\n")
        else:
            print("Analizando posibles jugadas...")
            # Llamada al Minimax: es_maximizador = True porque la IA busca maximizar su puntaje
            _, mejor_mov = minimax(tablero, profundidad, -math.inf, math.inf, True, jugador_ia, jugador_humano)
            
            if mejor_mov:
                f1, c1, f2, c2 = mejor_mov
                ejecutar_salto(tablero, f1, c1, f2, c2, turno_actual)
                print(f"-> La IA salto de la coordenada ({f1+1},{c1+1}) a la ({f2+1},{c2+1})")
        
        # Cambio de turno
        turno_actual = 'B' if turno_actual == 'A' else 'A'

if __name__ == "__main__":
    main()
