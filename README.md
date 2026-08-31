# Konane# Proyecto 1: Agente Inteligente para Kōnane

## Descripción y Arquitectura
Este repositorio contiene la implementación en Python del tradicional juego de tablero hawaiano **Kōnane**, desarrollado para el curso de Fundamentos de Inteligencia Artificial. El sistema presenta un diseño modular y estructurado (PEP-8) que incluye tanto el motor del juego como un agente autónomo capaz de competir contra un jugador humano.

* **Entorno Parametrizable:** Permite configurar el tamaño del tablero (n x n con n >= 6 y par) al inicio de cada partida.
* **Búsqueda Adversarial:** El agente toma decisiones utilizando el algoritmo Minimax optimizado mediante poda Alfa-Beta para reducir el espacio de búsqueda.
* **Función Heurística:** La evaluación de los estados terminales y no terminales se fundamenta en el diferencial de movilidad (cantidad de saltos legales disponibles) entre la Inteligencia Artificial y el oponente.

## Instrucciones de Ejecución
El código ha sido diseñado sin dependencias externas, utilizando únicamente bibliotecas estándar de Python (`copy`, `math`) para asegurar su portabilidad y facilitar la evaluación docente.

* **Requisitos Previos:** Contar con Python 3.x instalado en el entorno de trabajo.
* **Lanzamiento:** Ejecutar el archivo principal desde la terminal de comandos utilizando `python konane_ia.py`.
* **Interacción y Parámetros:** Al iniciar, el sistema solicitará definir el tamaño del tablero y la profundidad del árbol de búsqueda (se recomienda un valor de 3 o 4 para lograr un equilibrio óptimo entre dificultad y tiempo de respuesta del agente). Durante el turno del humano, las jugadas de captura deben ingresarse en formato `fila,columna`.