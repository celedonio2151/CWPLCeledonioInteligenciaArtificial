import os
import numpy as np
from matplotlib import pyplot
from scipy import optimize
import pandas as pd
import csv
import shutil
# Cargar datos
# data = np.loadtxt("pima-indians-diabetes_prepared.csv", delimiter=',')
data = np.loadtxt("win_mac_lin.csv", delimiter=',')
names = ['duracion','paginas','acciones','clickAnuncios','valor']
X, y = data[:, :5], data[:, 5]
print(names)
print(X," Array Xs")
print('-'*100)
print(y," Array Y")
print('-'*100)
# ============Funcion de la Sigmoide=====================================
def sigmoid(z):
    # Calcula la sigmoide de una entrada z
    # convierte la intrada a un arreglo numpy
    z = np.array(z)
    g = np.zeros(z.shape)
    g = 1 / (1 + np.exp(-z))    # Sigmoide

    return g

# Configurar la matriz adecuadamente, y agregar una columna de unos que corresponde al termino de intercepción.
m, n = X.shape
print(X.shape)
print(X[:5]," Array Xs sin la columna de 1s")
print('-'*100)
# Agraga el termino de intercepción a A
X = np.concatenate([np.ones((m, 1)), X], axis=1)
print(X[:5]," Array Xs con la columna de 1s")
print('-'*100)
# =============Funcion del Calculo del Costo===============================
def calcularCosto(theta, X, y):
    # Inicializar algunos valores utiles
    m = y.size  # numero de ejemplos de entrenamiento
    J = 0
    h = sigmoid(X.dot(theta.T))
    J = (1 / m) * np.sum(-y.dot(np.log(h)) - (1 - y).dot(np.log(1 - h)))

    return J

# =============Funcion de Desenso por el Gradiente==========================
def descensoGradiente(theta, X, y, alpha, num_iters):
    # Inicializa algunos valores
    m = y.shape[0]  # numero de ejemplos de entrenamiento
    # realiza una copia de theta, el cual será acutalizada por el descenso por el gradiente
    theta = theta.copy()
    J_history = []

    for i in range(num_iters):
        h = sigmoid(X.dot(theta.T))
        theta = theta - (alpha / m) * (h - y).dot(X)

        J_history.append(calcularCosto(theta, X, y))
    return theta, J_history

# Elegir algun valor para alpha (probar varias alternativas)
alpha = 0.00001
num_iters = 5000

# inicializa theta y ejecuta el descenso por el gradiente
theta = np.zeros(6)
# theta = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
theta, J_history = descensoGradiente(theta, X, y, alpha, num_iters)

# Grafica la convergencia del costo
pyplot.plot(np.arange(len(J_history)), J_history, lw=2)
pyplot.xlabel('Numero de iteraciones')
pyplot.ylabel('Costo J')
pyplot.show()

# Muestra los resultados del descenso por el gradiente
print('theta calculado por el descenso por el gradiente: {:s}'.format(str(theta)))
print('-'*100)
# verificar si es un usuario Windows o Mac
names = ['duracion','paginas','acciones','valor','clickAnuncios']
# X_array = [1, 50,4,8,5,5]
# X_array = [1, 93,2,12,96,7]   # 93,2,12,96,7,1
# X_array = [1, 145,2,10,30,3]   # 145,2,10,30,3,1
# X_array = [1,2,2,20,120,23]   # 2,2,20,120,23,0
# X_array = [1,14,2,12,36,8]    # 14,2,12,36,8,0
# X_array = [1,12,1,5,35,6]    # 12,1,5,35,6,1
# X_array = [1,7,2,4,8,0]    # 7,2,4,8,0,0
X_array = [1,700,21,40,81,81]    #
usuarioWM = sigmoid(np.dot(X_array, theta))   # Se debe cambiar esto

print(f"Un usuario con las caracteristicas: {X_array} hay una probabilidad de usar SO de:{usuarioWM}")
if usuarioWM >= 0.5:
    print(" Windows",end="")
else:
    print(" Mac",end="")
# print(f"con valores de theta: { theta }")
