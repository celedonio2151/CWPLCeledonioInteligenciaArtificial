from Gameboard import Gameboard
import random
from Tictactoe import *
from Minimax import minimax
from AlphaBeta import alpha_beta_search

EASY = 1
MEDIUM = 4
HARD = 11

def randomEval(board, player, opponent):
    """
    Obtener score aleatoria
    """
    return random.randint(-10, 10)

def randomMoves(snapshot, isPlayer):
    """
    Generar hijos aleatorios
    """
    return random.randint(1, 10) * [1]

if __name__ == "__main__":
    # === Obtener información básica ===
    print("Introduce tu nombre: ")
    name = input()
    print("=== Bienvenid@ {} ===".format(name))
    print("Vamos a jugar gato, tú vs yo")
    user = ""
    while user != "X" and user != "O":
        print("Selecciona tu ficha 'X' u 'O'")
        user = input()
    machine = "X" if user == "O" else "O"
    # === DIFICULTAD del juego ===
    level = 0
    while level == 0:
        try:
            print("Selecciona la dificultad: EASY(1) MEDIUM(2) HARD(3)")
            level = int(input())
            if level == 1:
                level = EASY
            elif level == 2:
                level = MEDIUM
            else:
                level = HARD
        except KeyboardInterrupt:
            print("Fin abrupto del programa")
            quit()
        except:
            print("Hubo un error, creo que no tecleaste un número")
    # === Ver quien INICIA ===
    print("Voy a lanzar una moneda para ver quien inicia...")
    turn = random.choice(["X", "O"])
    print("Obtuve {}".format(turn))
    game = Gameboard(3, 3, machine, user)
    game.print()
    if turn == machine:
        game.addChip(True, random.randint(0, 2), random.randint(0, 2))
        turn = user
        game.print()
    # === Ciclo del juego entre jugador vs máquina ===
    winner = 0
    while canMove(game.board) and winner == 0:
        if turn == user:
            print("Es TU turno")
            valid = False
            while not valid:
                try:
                    print("¿Qué FILA seleccionas? [0 (Hasta arriba), 2(Hasta abajo)]")
                    x = int(input())
                    print("¿Qué COLUMNA seleccionas? [0 (Hasta arriba), 2(Hasta abajo)]")
                    y = int(input())
                    valid = game.addChip(False, x, y)
                except KeyboardInterrupt:
                    print("Fin abrupto del programa")
                    quit()
                except:
                    print("Hubo un error, creo que no tecleaste un número")
            turn = machine
        else:
            print("Es MI turno")
            res = minimax(game, level, True, evaluate, generateMoves)
            #res = alpha_beta_search(game, level, True, evaluate, generateMoves,-float('inf'),float('inf'))
            print("Moveré la pieza a {1} (Score: {0})".format(res[0], res[1]))
            game.addChip(True, res[1][0], res[1][1])
            turn = user
        winner = evaluate(game.board, game.getPlayerFormat(), game.getOpponentFormat())
        game.print()
    print("Fin del juego")
    if winner > 0:
        print("¡Gané yo! ¡QUÉ FELICIDAD!")
    elif winner < 0:
        print("Ganó {}, vaya sorpresa".format(name))
    else:
        print("Empate")
