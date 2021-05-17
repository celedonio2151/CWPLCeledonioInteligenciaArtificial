from math import inf as infinity
import random
import platform
import time
from os import system
 #JUEGO TRES EN RAYA CON ALFA BETA PODA

def getTableroCopia(tablero): #recibe una tabla
    # Hace una copia del tablero y la retorna
    copiaTablero = []
    for i in tablero:
        copiaTablero.append(i)
    return copiaTablero

def DibujarTablero(tablero): #recibe un tablero
    # Esta funcion imprime el tablero
    # Un cuadro representado por una lista de 9 strings
    copiaTablero = getTableroCopia(tablero)

    # for i in range(1, 10):      # Original
    for i in range(1, 17):
        if tablero[i] == '':
            copiaTablero[i] = str(i)
        else:
            copiaTablero[i] = tablero[i]
    # print(' ' + copiaTablero[7] + '   ||   ' + copiaTablero[8] + '  ||   ' + copiaTablero[9]+'   ||   ')
    # print('-------------------')
    # print(' ' + copiaTablero[4] + '   ||   ' + copiaTablero[5] + '  ||   ' + copiaTablero[6]+'   ||   ')
    # print('-------------------')
    # print(' ' + copiaTablero[1] + '   ||   ' + copiaTablero[2] + '  ||   ' + copiaTablero[3]+'   ||   ')
    # print('-------------------')
# ===================================================================
    print(' ' + copiaTablero[13] + '   ||   ' + copiaTablero[14] + '  ||   ' + copiaTablero[15]+'   ||   '+copiaTablero[16]+'   ||   ')
    print('-------------------')
    print(' ' + copiaTablero[9] + '   ||   ' + copiaTablero[10] + '  ||   ' + copiaTablero[11]+'   ||   '+copiaTablero[12]+'   ||   ')
    print('-------------------')
    print(' ' + copiaTablero[5] + '   ||   ' + copiaTablero[6] + '  ||   ' + copiaTablero[7]+'   ||   '+copiaTablero[8]+'   ||   ')
    print('-------------------')
    print(' ' + copiaTablero[1] + '   ||   ' + copiaTablero[2] + '  ||   ' + copiaTablero[3]+'   ||   '+copiaTablero[4]+'   ||   ')
    print('-------------------')

def EntradaJuegadorLetra():
    # El jugador elige con que letra quiere jugar "X" u "O"
    # Devuelve una lista con una letra del juegador y una letra del computador
    letra = ''

    while not (letra == 'X' or letra == 'O'):
        print('Elija si quieres jugar con X u O')
        letra = input().upper() # una vez introducido lo convierte a Mayuscula
        if not (letra == 'X' or letra == 'O'):
            print('Eligio una letra que no es correcto!')

    # El primer elemento en la lista es el jugador y el segundo es el computador
    if letra == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def QuienVaPrimero():
    # Se elige aleatoriamente quien va primero humano o computador
    if random.randint(0, 1) == 0:
        return 'computador'
    else:
        return 'humano'

def HaceMover(tablero, letra, mover):
    # registra la jugada de un jugador sobre el tablero
    tablero[mover] = letra

def EsGanador(tablero, letra):
    #Dado un cuadro y una letterra, esta funcion retorn True si la letterra pasada vence el juego
    # return  ((tablero[7] == letra and tablero[8] == letra and tablero[9] == letra) or #linea de encima
    #          (tablero[4] == letra and tablero[5] == letra and tablero[6] == letra) or #linea de medio horizontal
    #          (tablero[1] == letra and tablero[2] == letra and tablero[3] == letra) or #linea de abajo
    #          (tablero[7] == letra and tablero[4] == letra and tablero[1] == letra) or #linea de izquierda
    #                                         #  ajdjasdkfadsnfajsd
    #          (tablero[8] == letra and tablero[5] == letra and tablero[2] == letra) or #linea de medio vertical
    #          (tablero[9] == letra and tablero[6] == letra and tablero[3] == letra) or #linea de derecha
    #          (tablero[7] == letra and tablero[5] == letra and tablero[3] == letra) or #linea diagonal derecha
    #          (tablero[9] == letra and tablero[5] == letra and tablero[1] == letra) #linea diagonal izquierda
    # )
# ===================================================================
                                              # Derecha izquierda
    return  ((tablero[14] == letra and tablero[15] == letra and tablero[16] == letra) or #linea de encima
             (tablero[13] == letra and tablero[14] == letra and tablero[15] == letra) or #linea de medio horizontal
             (tablero[10] == letra and tablero[11] == letra and tablero[12] == letra) or #linea de medio horizontal
             (tablero[9] == letra and tablero[10] == letra and tablero[11] == letra) or #linea de medio horizontal
             (tablero[6] == letra and tablero[7] == letra and tablero[8] == letra) or #linea de medio horizontal
             (tablero[5] == letra and tablero[6] == letra and tablero[7] == letra) or #linea de medio horizontal
             (tablero[1] == letra and tablero[2] == letra and tablero[3] == letra) or #linea de abajo
             (tablero[2] == letra and tablero[3] == letra and tablero[4] == letra) or #linea de abajo
                                #               Arriba abajo
             (tablero[1] == letra and tablero[5] == letra and tablero[9] == letra) or #linea de izquierda
             (tablero[5] == letra and tablero[9] == letra and tablero[13] == letra) or #linea de medio vertical
             (tablero[2] == letra and tablero[6] == letra and tablero[10] == letra) or #linea de derecha
             (tablero[6] == letra and tablero[10] == letra and tablero[14] == letra) or #linea de derecha
             (tablero[3] == letra and tablero[7] == letra and tablero[11] == letra) or #linea diagonal derecha
             (tablero[7] == letra and tablero[11] == letra and tablero[15] == letra) or#linea diagonal izquierda
             (tablero[4] == letra and tablero[8] == letra and tablero[12] == letra) or #linea diagonal derecha
             (tablero[8] == letra and tablero[12] == letra and tablero[16] == letra) or#linea diagonal izquierda
                                #               Diagonales
             (tablero[2] == letra and tablero[7] == letra and tablero[12] == letra) or #linea diagonal derecha
             (tablero[1] == letra and tablero[6] == letra and tablero[11] == letra) or #linea diagonal izquierda
             (tablero[6] == letra and tablero[11] == letra and tablero[16] == letra) or #linea diagonal derecha
             (tablero[5] == letra and tablero[10] == letra and tablero[15] == letra) or#linea diagonal izquierda
             (tablero[3] == letra and tablero[6] == letra and tablero[9] == letra) or #linea diagonal derecha
             (tablero[4] == letra and tablero[7] == letra and tablero[10] == letra) or #linea diagonal izquierda
             (tablero[7] == letra and tablero[10] == letra and tablero[13] == letra) or #linea diagonal derecha
             (tablero[8] == letra and tablero[11] == letra and tablero[14] == letra) #linea diagonal izquierda
    )
def LibreEspacio(tablero, mover):
    # Retorna True si un espacio solicitado esta libre en el tablero
    if tablero[mover] == '':
        return True
    else:
        return False

def getMovimientoDelJugador(tablero):
    # Recibe el movimiento del jugador
    mover = ''
    # while mover not in '1 2 3 4 5 6 7 8 9' .split() or not LibreEspacio(tablero,int(mover)):    # Original
    while mover not in '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16' .split() or not LibreEspacio(tablero,int(mover)):
        print('Cual es su proximo movimiento? (1-16)')
        mover = input()
        # if (mover not in '1 2 3 4 5 6 7 8 9'):      # Original
        if (mover not in '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16'):
            print('Movimiento Invalido!, El movimieno debe ser un valor entre 1 y 16!')

        # if (mover in '1 2 3 4 5 6 7 8 9'):     # Original
        if (mover in '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16'):
            if (not LibreEspacio(tablero, int(mover))):
                print('Espacio no disponible! Elija otro otro espacio entre 1 y 16 de los espacios disponibles!')

    return int(mover)

def getMovimientoAleatorioDeLista(tablero, listaMovimientos):
    # Retorna un movimento valido aleatorio
    # Retorna None si no existen movimentos validos posibles

    posiblesMovimientos = []
    for i in listaMovimientos:
        if LibreEspacio(tablero, i):
            posiblesMovimientos.append(i)

    if len(posiblesMovimientos) != 0:
        return random.choice(posiblesMovimientos)
    else:
        return None

def EsTableroLleno(tablero):
    # Retorna True si no existen espacios disponibles en el tablero
    # for i in range(1, 10):      # Original
    for i in range(1, 17):
        if LibreEspacio(tablero, i):
            return False
    return True

def EspaciosDisponibles(tablero):
    # Retorna una lista de todos los espacion disponibles en el tablero
    espacios = []

    # for i in range(1, 10):      # Original
    for i in range(1, 17):
        if LibreEspacio(tablero, i):
            espacios.append(i)
    return espacios

def FinalJuego(tablero, letraComputadora):
    # Verifica si el juego a llegado a su final
    # Retorna -1 si gana el jugador
    # Retorna 1 si gana el computador
    # Retorna 0 si el juego termina empatado
    # Retorna None si el juego no ha terminado
    if letraComputadora == 'X':
        jugadorLetra = 'O'
    else:
        jugadorLetra = 'X'

    if EsGanador(tablero, letraComputadora):
        return 1
    elif EsGanador(tablero, jugadorLetra):
        return -1
    elif EsTableroLleno(tablero):
        return 0
    else:
        return None

def AlfaBeta(tablero, letraComputador, turno, alfa, beta):
    # Fazemos aqui a poda alphabeta
    if letraComputador == 'X':
        jugadorLetra = 'O'
    else:
        jugadorLetra = 'X'

    if turno == letraComputador:
        turnoSiguiente = jugadorLetra
    else:
        turnoSiguiente = letraComputador

    final = FinalJuego(tablero, letraComputador)

    if(final != None):
        return final

    espacios = EspaciosDisponibles(tablero)

    if turno == letraComputador:
        for mover in espacios:
            HaceMover(tablero, turno, mover)
            valor = AlfaBeta(tablero, letraComputador, turnoSiguiente, alfa, beta)
            HaceMover(tablero, '', mover)
            if valor > alfa:
                alfa = valor

            if alfa >= beta:
                return alfa
        return alfa
    else:
        for mover in espacios:
            HaceMover(tablero, turno, mover)
            valor = AlfaBeta(tablero, letraComputador, turnoSiguiente, alfa, beta)
            HaceMover(tablero, '', mover)
            if valor < beta:
                beta = valor
            if alfa >= beta:
                return beta
        return beta
def getMovimientoComputador(tablero, turno, letraComputadora):
    # Definimos aqui cual sera el movimiento del computador
    a = -2
    opciones = []
    if letraComputadora == 'X':
        jugadoLetra = 'O'
    else:
        jugadorLetra = 'X'

    # Comenzamos aqui el MiniMax
    # primero checamos si podemos ganar el proximo movimiento

    # for i in range(1, 10):      # Original
    for i in range(1, 17):
        copia = getTableroCopia(tablero)
        if LibreEspacio(copia, i):
            HaceMover(copia, letraComputadora, i)
            if EsGanador(copia, letraComputadora):
                return i
    # Comprueba si el jugador puede ganar en el siguiente movimiento y bloquea

    # for i in range(1, 10):      # Original
    for i in range(1, 17):
        copia = getTableroCopia(tablero)
        if LibreEspacio(copia, i):
            HaceMover(copia, jugadorLetra, i)
            if EsGanador(copia, jugadorLetra):
                return i

    posiblesOpcionesEncedidos = EspaciosDisponibles(tablero)

    for mover in posiblesOpcionesEncedidos:
        HaceMover(tablero, letraComputadora, mover)
        valor = AlfaBeta(tablero, letraComputadora, jugadorLetra, -2, 2)
        HaceMover(tablero, '', mover)

        if valor > a:
            a = valor
            opciones = [mover]

        elif valor == a:
            opciones.append(mover)
    return random.choice(opciones)

print("Vamos a jugar Tres en Raya!")
jugar = True

while jugar:
    laTabla = [''] * 10
    letraJugador, letraComputadora = EntradaJuegadorLetra()
    turno = QuienVaPrimero()
    print(f'O {turno} juega primero')
    JuegoEstaJugando = True

    while JuegoEstaJugando:
        if turno == 'jugador':
            # Turno Jugador
            DibujarTablero(laTabla)
            mover = getMovimientoDelJugador(laTabla)
            HaceMover(laTabla, letraJugador, mover)

            if EsGanador(laTabla, letraJugador):
                DibujarTablero(laTabla)
                print("Woooo, Ganaste el Juego")
                JuegoEstaJugando = False
            else:
                if EsTableroLleno(laTabla):
                    DibujarTablero(laTabla)
                    print("Juego en Empate")
                    break
                else:
                    turno = 'computador'
        else:
            # Turno Computador
            mover = getMovimientoComputador(laTabla, letraJugador, letraComputadora)
            HaceMover(laTabla, letraComputadora, mover)

            if EsGanador(laTabla, letraComputadora):
                DibujarTablero(laTabla)
                print("Vencio la Computadora!  😥😫")
                JuegoEstaJugando = False
            else:
                if EsTableroLleno(laTabla):
                    DibujarTablero(laTabla)
                    print("Juego Empatado")
                    break
                else:
                    turno = 'jugador'
    nuevoLetra = ''
    while not (nuevoLetra == 'S' or nuevoLetra == 'N'):
        print("Quiere Jugar De Nuevo?? Digite S(para SI) o N(para NO)")
        nuevoLetra = input().upper()
        if nuevoLetra != 'S' and nuevoLetra != 'N':
            print('Entrada invalida! Digite S(para sim) ou N(para nao)!')
        if nuevoLetra == 'N':
            print('Hasta Luego')
            jugar = False


# Pregunta 2: Busqueda Informada a utilizar PODA ALFA BETA - Euristica, verificar las posiciones del ganador en en tablerp 4*4 tanto en verticales, en horizontales y diagonales
