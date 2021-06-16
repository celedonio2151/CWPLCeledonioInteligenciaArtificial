"""
Programa que implementa reglas básicas para jugar el juego de Gato (Tic-Tac-Toe)
"""
from Gameboard import Gameboard
from copy import deepcopy
SCORE = 10


def canMove(board):
    """
    Checar si hay movimientos disponibles
    """
    for i in range(3):
        for j in range(3):
            if (board[i][j] == "\t"):
                return True
    return False


def evaluate(board, player, opponent):
    """
    Evaluar el tablero actual\n
    player es el jugador que pierde (-SCORE) o gana (-SCORE)
    """
    # if not canMove(board):
    #     return 0

    # Victoria para player en una fila
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == player:
                return SCORE
            elif board[row][0] == opponent:
                return -SCORE

    # Victoria para player en una columna
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == player:
                return SCORE
            elif board[0][col] == opponent:
                return -SCORE

    # Victoria para player en una diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == player:
            return SCORE
        elif board[0][0] == opponent:
            return -SCORE

    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == player:
            return SCORE
        elif board[0][2] == opponent:
            return -SCORE

    # Else if none of them have won then return 0
    return 0


def generateMoves(snapshot, isPlayer):
    """
    Crear tableros con nuevos movimientos para evaluar nuevos escenarios
    """
    output = []
    for x in range(3):
        for y in range(3):
            if (snapshot.board[x][y] == "\t"):
                game = Gameboard(snapshot.width, snapshot.height,
                                 snapshot.player, snapshot.opponent)
                game.board = deepcopy(snapshot.board)
                game.addChip(isPlayer, x, y)
                output.append(game)
    return output
