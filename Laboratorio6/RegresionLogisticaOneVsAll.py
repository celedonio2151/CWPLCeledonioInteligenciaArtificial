import os
import numpy as np
from matplotlib import pyplot
from scipy import optimize

data = np.loadtxt("identificación del vidrio.csv", delimiter=',')
# X, y = data[:, :9], data[:, 9]
X, y = data[:-2, :9], data[:-2, 9]
print(X," Matriz de las Xs")
print("-"*100)
print(y," Matriz de las Ys")
print("-"*100)
print(X.shape," Tamaño de las Xs")
print(y.shape," Tamaño de las Ys")
print("-"*100)
input_layer_size  = 9      # Cantidad de caracteristicas o columnas
num_labels = 6              # Cantidad de salidas o clasificaciones Ys
m = y.size                      # Cantida de ejemplos o numero de filas Xs
# =============Funcion Sigmoide========================================
def sigmoid(z):
    # Calcula la sigmoide de z.
    return 1.0 / (1.0 + np.exp(-z))
# =============Funcion calculo del costo===================================
def lrCostFunction(theta, X, y, lambda_):
    # Inicializa algunos valores utiles
    m = y.size  # Calculamos de nuevo el numero de filas de Y o usar la global
    # convierte las etiquetas a valores enteros si son boleanos
    if y.dtype == bool: # de boleanos
        y = y.astype(int) # a enteros

    J = 0
    grad = np.zeros(theta.shape)    # Inicializamos las thetas

    h = sigmoid(X.dot(theta.T))     # Calculo de la hipotesis -> probabilidad

    temp = theta
    temp[0] = 0     # Se pone 0 para que no lo tome (regularizacion)

    J = (1 / m) * np.sum(-y.dot(np.log(h)) - (1 - y).dot(np.log(1 - h))) + (lambda_ / (2 * m)) * np.sum(np.square(temp))    # Calculo del costo

    grad = (1 / m) * (h - y).dot(X)
    grad = grad + (lambda_ / m) * temp
    return J, grad
# =============Fin funcion de costo=======================================

# ==================valores de prueba para los parámetros theta===============
# theta_t = np.array([-2, -1, 1, 2], dtype=float)     # Original
theta_t = np.array([-2, -1, 1, 2], dtype=float)
# print(theta_t)
# valores de prueba para las entradas
X_t = np.concatenate((np.ones((5, 1)), np.arange(1, 16).reshape(5, 3, order='F')/10.0), axis=1)
print("----------Testeo -----------------------------------------------------------------------------------")
print(X_t," Esto es X_t")
print("-"*100)
# valores de testeo para las etiquetas
y_t = np.array([1, 0, 1, 0, 1])
print(y_t," Esto es y_t ")
print("-"*100)

# valores de testeo para el parametro de regularizacion
lambda_t = 3

J, grad = lrCostFunction(theta_t, X_t, y_t, lambda_t)

print('Costo         : {:.6f}'.format(J))
print('Costo esperadot: 2.534819')
print('------------------------------------')
print('Gradientes:')
print(' [{:.6f}, {:.6f}, {:.6f}, {:.6f}]'.format(*grad))
print('Gradientes esperados:')
print(' [0.146561, -0.548558, 0.724722, 1.398003]');
print("-"*100)
# =============Fin del testeo============================================
def oneVsAll(X, y, num_labels, lambda_):    # Calculo de las thetas

    m, n = X.shape

    all_theta = np.zeros((num_labels, n + 1))

    # Agrega una columna de unos a la matriz X
    X = np.concatenate([np.ones((m, 1)), X], axis=1)
    print(X," Columna de 1s ya agregado a X")
    print("-"*100)

    for c in np.arange(num_labels):
        initial_theta = np.zeros(n + 1)     # Inicializa los thetas del tamano adecuado
        options = {'maxiter': 50}
        res = optimize.minimize(lrCostFunction,
                                initial_theta,
                                (X, (y == (c + 1)), lambda_),
                                jac=True,
                                method='BFGS',
                                options=options)

        all_theta[c] = res.x

    return all_theta

lambda_ = 0.1
all_theta = oneVsAll(X, y, num_labels, lambda_)     # Atrapamos las thetas calculadas
print("-"*100)
print(all_theta," Todas las thetas ya predichas para las 7 clases")
# ==============Prediccion One vs All para
def predictOneVsAll(all_theta, X):  # Recibe los mismos datos X para entrenamiento
    m = X.shape[0];
    num_labels = all_theta.shape[0]

    p = np.zeros(m)

    # Add ones to the X data matrix
    X = np.concatenate([np.ones((m, 1)), X], axis=1)    # Agregar una columna de 1s a la matrix X
    p = np.argmax(sigmoid(X.dot(all_theta.T)), axis = 1)    # Devuelve la probabilidad mas alta de las tres clasificadas

    return p + 1

print(X.shape)
pred = predictOneVsAll(all_theta, X)    # Pasamos las thetas calculadas y el dataset sin la Y
print("-"*100)
print(pred," Esto es lo que predijo con el dataset de la X sin Y ")
print("-"*100)
print('Precision del conjuto de entrenamiento: {:.2f}%'.format(np.mean(pred == y) * 100))
XPrueba = X[-3:, :].copy()  # Las tres entradas
yPrueba = y[-3:].copy()
print("-"*100)
print(XPrueba," Xs de prueba")  # Visualizando las X de prueba
print("-"*100)
print(yPrueba," Ys de prueba")  # Visualizando las Y de prueba que debeia sacar
print("-"*100)
print(XPrueba.shape)
print(len(XPrueba))
print("-"*100)
XPrueba = np.concatenate((np.ones((3, 1)), XPrueba), axis=1)    # Agrega una fila 1s
p = np.argmax(sigmoid(XPrueba.dot(all_theta.T)), axis = 1)
print(p + 1," Son las Y predichas")    # esto es lo que predice para las tres entradas de X
# ====================Probando con nuevos valores ========================
print()
print("="*100)
print("Prediciendo con nuevos valores o entradas nuevas las caracteristicas")
print("="*100)
Xnuevo = [[1.51316,13.02,0.00,3.04,70.48,6.21,6.96,0.00,0.00]]  # Deberia ser de la clase 4
# cambiar estos valores
Xnuevo = np.concatenate((np.ones((1, 1)), Xnuevo), axis=1)     # Agrega una fila 1s
p = np.argmax(sigmoid(Xnuevo.dot(all_theta.T)), axis = 1)         # Calcula la mayor probabilidad
# print(Xnuevo)
print("Es de la clase: ",p + 1)
