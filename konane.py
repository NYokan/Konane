"""
Proyecto N°1: Fundamentos de Inteligencia Artificial
Juego: Konane (Fase 1 - Entorno para 2 jugadores humanos)
"""

def mostrar_instrucciones():
    """Imprime un resumen de las reglas y el formato de entrada para los usuarios."""
    print("\nINSTRUCCIONES DE JUEGO:")
    print("- Tablero: Utiliza coordenadas del 1 al N (Fila, Columna).")
    print("- Movimiento: Todo movimiento debe ser un salto ortogonal (arriba, abajo, izquierda o derecha) sobre una pieza rival hacia una casilla vacia[cite: 2].")
    print("- Capturas Multiples: Estan permitidas en un mismo turno. Ingrese la coordenada de la pieza y la casilla de aterrizaje final. Todos los saltos deben mantener la misma direccion[cite: 2].")
    print("- Fin del Juego: El jugador que inicie su turno sin capturas legales pierde inmediatamente[cite: 2].\n")
    print("-" * 50)

def crear_tablero(n):
    """
    Genera el tablero inicial nxn con el patron alternado y ejecuta la apertura.
    A ocupa las casillas donde (fila + columna) es par[cite: 2].
    B ocupa las restantes[cite: 2].
    """
    tablero = []
    for i in range(n):
        fila = []
        for j in range(n):
            if (i + j) % 2 == 0:
                fila.append('A')
            else:
                fila.append('B')
        tablero.append(fila)
    
    # Apertura obligatoria del proyecto: A retira (1,1) y B retira (1,2)[cite: 2]
    tablero[0][0] = '.'
    tablero[0][1] = '.'
    
    return tablero

def imprimir_tablero(tablero):
    """Imprime el tablero en consola con coordenadas 1-based para los usuarios."""
    n = len(tablero)
    print("\n   " + " ".join([str(i+1).rjust(2) for i in range(n)]))
    for i in range(n):
        fila_str = f"{str(i+1).rjust(2)} "
        for j in range(n):
            fila_str += f" {tablero[i][j]} "
        print(fila_str)
    print()

def es_salto_valido(tablero, f1, c1, f2, c2, jugador):
    """
    Verifica si el movimiento desde (f1, c1) hasta (f2, c2) es un salto legal.
    Soporta saltos multiples si estan en la misma linea ortogonal[cite: 2].
    """
    n = len(tablero)
    rival = 'B' if jugador == 'A' else 'A'

    if not (0 <= f1 < n and 0 <= c1 < n and 0 <= f2 < n and 0 <= c2 < n):
        return False
    
    if tablero[f1][c1] != jugador or tablero[f2][c2] != '.':
        return False

    if f1 != f2 and c1 != c2:
        return False

    dist_f = abs(f2 - f1)
    dist_c = abs(c2 - c1)
    dist_total = max(dist_f, dist_c)

    if dist_total % 2 != 0 or dist_total == 0:
        return False

    paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
    paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)

    for paso in range(1, dist_total + 1):
        f_actual = f1 + paso * paso_f
        c_actual = c1 + paso * paso_c
        
        if paso % 2 != 0:
            if tablero[f_actual][c_actual] != rival:
                return False
        else:
            if tablero[f_actual][c_actual] != '.':
                return False

    return True

def ejecutar_salto(tablero, f1, c1, f2, c2, jugador):
    """Ejecuta el salto, moviendo la pieza y capturando las intermedias[cite: 2]."""
    dist_total = max(abs(f2 - f1), abs(c2 - c1))
    paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
    paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)

    tablero[f1][c1] = '.'
    
    for paso in range(1, dist_total, 2):
        tablero[f1 + paso * paso_f][c1 + paso * paso_c] = '.'
        
    tablero[f2][c2] = jugador

def tiene_movimientos_legales(tablero, jugador):
    """Escanea el tablero para verificar si el jugador tiene al menos un salto valido."""
    n = len(tablero)
    direcciones = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    
    for i in range(n):
        for j in range(n):
            if tablero[i][j] == jugador:
                for df, dc in direcciones:
                    if es_salto_valido(tablero, i, j, i + df, j + dc, jugador):
                        return True
    return False

def obtener_coordenadas(mensaje, n):
    """Solicita y formatea las coordenadas ingresadas por el usuario."""
    while True:
        try:
            entrada = input(mensaje).strip().split(',')
            if len(entrada) != 2:
                raise ValueError
            f, c = int(entrada[0]), int(entrada[1])
            if 1 <= f <= n and 1 <= c <= n:
                return f - 1, c - 1
            else:
                print(f"[ERROR] Las coordenadas deben estar entre 1 y {n}.")
        except ValueError:
            print("[FORMATO INVALIDO] Ingrese fila y columna separadas por coma (ej: 3,1).")

def main():
    print("=== PROYECTO 1: KONANE ===")
    mostrar_instrucciones()
    
    while True:
        try:
            n = int(input("Ingrese el tamano del tablero (n par, mayor o igual a 6): "))
            if n >= 6 and n % 2 == 0:
                break
            print("[ERROR] El tamano debe ser un numero par mayor o igual a 6.")
        except ValueError:
            print("[ERROR] Ingrese un numero entero valido.")

    tablero = crear_tablero(n)
    turno = 'A'
    
    while True:
        imprimir_tablero(tablero)
        
        if not tiene_movimientos_legales(tablero, turno):
            rival = 'B' if turno == 'A' else 'A'
            print(f"\nFIN DEL JUEGO. El jugador {turno} no tiene movimientos legales[cite: 2].")
            print(f"EL JUGADOR {rival} GANA LA PARTIDA[cite: 2].")
            break

        print(f"Turno del Jugador {turno}")
        print("-" * 23)
        
        f1, c1 = obtener_coordenadas("Ingrese origen (fila,columna): ", n)
        f2, c2 = obtener_coordenadas("Ingrese destino final (fila,columna): ", n)

        if es_salto_valido(tablero, f1, c1, f2, c2, turno):
            ejecutar_salto(tablero, f1, c1, f2, c2, turno)
            turno = 'B' if turno == 'A' else 'A'
        else:
            print("\n[!] MOVIMIENTO INVALIDO. Asegurese de realizar saltos ortogonales sobre piezas rivales.")

if __name__ == "__main__":
    main()