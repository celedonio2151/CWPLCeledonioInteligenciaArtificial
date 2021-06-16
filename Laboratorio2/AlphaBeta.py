"""
g.print()
Archivo para crear el algoritmo MinMax para automatizar un juego
"""
from Gameboard import Gameboard
from Tictactoe import *


def alpha_beta_search(snapshot, depth, isMaximizing, checkScore, getChildren,alpha,beta):
    """
    Implementación básica de alpha_beta_search que genera un árbol de decisión
    Un snapshot implica una fotografía del tablero, con sus fichas actuales
    """
    if depth == 0:
        if snapshot is not None:
            return [checkScore(snapshot.board, snapshot.getPlayerFormat(), snapshot.getOpponentFormat()), snapshot.lastMove]
        return [checkScore(snapshot, snapshot, snapshot), snapshot]
    bestMove = snapshot.lastMove
    if isMaximizing:
        maxScore = float('-inf')
        children = getChildren(snapshot, True)
        for child in children:
            result = alpha_beta_search(child, depth - 1, False, checkScore, getChildren,alpha,beta)
            maxScore = max(result[0], maxScore)
            alpha = max(alpha,maxScore)
            if maxScore == result[0]:
                bestMove = child.lastMove
            if beta<=alpha:
                break
        if len(children) == 0:
            if snapshot is not None:
                return [checkScore(snapshot.board, snapshot.getPlayerFormat(), snapshot.getOpponentFormat()), snapshot.lastMove]
            return [checkScore(snapshot, snapshot, snapshot), snapshot]
        return [maxScore, bestMove]
    else:
        minScore = float('inf')
        children = getChildren(snapshot, False)
        for child in children:
            result = alpha_beta_search(child, depth - 1, True, checkScore, getChildren,alpha,beta)
            minScore = min(result[0], minScore)
            beta = min(beta,minScore)
            if minScore == result[0]:
                bestMove = child.lastMove
            if beta<=alpha:
                break
        if len(children) == 0:
            if snapshot is not None:
                return [checkScore(snapshot.board, snapshot.getPlayerFormat(), snapshot.getOpponentFormat()), snapshot.lastMove]
            return [checkScore(snapshot, snapshot, snapshot), snapshot]
        return [minScore, bestMove]


if __name__ == "__main__":
    print("==== Tablero 3x3 ====")
    g = Gameboard(3, 3, "X", "O")
    # g = Gameboard(4, 4, "X", "O")
    g.addChip(True, 0, 0)
    g.addChip(False, 1, 1)
    g.addChip(False, 2, 2)
    g.addChip(True, 0, 2)
    g.print()
    print("==== MOVIMIENTO ====")
    res = alpha_beta_search(g, 3, True, evaluate, generateMoves,-float('inf'),float('inf'))
    print("Mover la pieza a {1} (Score: {0})".format(res[0], res[1]))
    g.addChip(False, res[1][0], res[1][1])
    g.print()
    print("==== MOVIMIENTO ====")
