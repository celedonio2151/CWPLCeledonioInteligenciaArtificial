import os
import numpy as np
from matplotlib import pyplot
from scipy import optimize
# Lemos el dataset y guardamos en data
data = np.loadtxt(os.path.join('11. Thyroid', 'new-thyroid.csv'), delimiter=',')

X, y = data[50:, :5], data[50:, 5]    # Separando el dataset en X y Y (entrenamiento)
XP = data[:50, :5]     # Para prueba X          50 valores
YP = data[:50, 5]     # Para prueba Y           50 valores
# print(X[X==0]," Estos valores son iguales a cero")
print(X[:10]," Matriz de las Xs")
print("-"*100)
print(y[:10]," Matriz de las Ys")
print("-"*100)
print(data.shape," Estos son las dimensiones de todo el dataet")
print(X.shape," Dimensiones de las Xs")
print(y.shape," Dimensiones de las Ys")
print("-"*100)
input_layer_size  = 5      # Cantidad de caracteristicas o columnas
num_labels = 3              # Cantidad de salidas o clasificaciones Ys
m = y.size                      # Cantida de ejemplos o numero de filas Xs
# =============Funcion Sigmoide========================================
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z)) # Calcula la sigmoide de z.

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
print("-"*100)
print(XP[:10]," Para prueba X")
print("-"*100)
print(YP[:10]," Para prueba Y")
print("-"*100)
# =============Funcion One vs All========================================
def oneVsAll(X, y, num_labels, lambda_):    # Calculo de las thetas

    m, n = X.shape

    all_theta = np.zeros((num_labels, n + 1))   # 3 filas 6 columnas

    # Agrega una columna de unos a la matriz X
    X = np.concatenate([np.ones((m, 1)), X], axis=1)
    print(X[:5]," Columna de 1s ya agregado a X")
    print("-"*100)

    for c in np.arange(num_labels):     # Por cada etiqueta
        initial_theta = np.zeros(n + 1)     # Inicializa los thetas del tamano adecuado
        options = {'maxiter': 100}
        res = optimize.minimize(lrCostFunction,
                                initial_theta,
                                (X, (y == (c + 1)), lambda_),
                                jac=True,
                                # method='BFGS',
                                method='TNC',
                                # method='Powell',
                                # method='Newton-CG',
                                options=options)

        all_theta[c] = res.x

    return all_theta
# ========Fin de la funcion One vs All======================================
lambda_ = 0.1   # Coeficiente de aprendizaje
all_theta = oneVsAll(X, y, num_labels, lambda_)     # Atrapamos las thetas calculadas
print("-"*100)
print(all_theta," Todas las thetas ya predichas para las 3 clases")
# ==============Funcion de prediccion One vs All============================
def predictOneVsAll(all_theta, X):  # Recibe los mismos datos X para entrenamiento
    m = X.shape[0];
    num_labels = all_theta.shape[0]

    p = np.zeros(m)

    X = np.concatenate([np.ones((m, 1)), X], axis=1)    # Agregar una columna de 1s a la matrix X
    # print(X.shape," Nueva dimesion de X mas 1")
    p = np.argmax(sigmoid(X.dot(all_theta.T)), axis = 1)    # Devuelve la probabilidad mas alta de las tres clasificadas

    return p + 1
# ========Fin de la funcion  de prediccion===================================
# ========Prediciendo con valores inexistentes===============================
print("-"*100)
pred = predictOneVsAll(all_theta, X)    # Pasamos las thetas calculadas y el dataset sin la Y
pred1 = predictOneVsAll(all_theta, XP)    # Datos que no vio aun el programa
print("-"*100)
print(y," Vector Y original")
print("-"*100)
print(pred," Resultado con el dataset de la X sin Y ")
print("-"*100)
print(pred1," Resultado con nuevos datos sin Y ")
print("-"*100)
print('Precision del conjuto de entrenamiento: {:.2f}%'.format(np.mean(pred == y) * 100),"      -> Con los mismo datos aprendidos")
print('Precision del conjuto de entrenamiento: {:.2f}%'.format(np.mean(pred1 == YP) * 100),"      -> Con nuevos datos que no vio el programa")
print("                 ")
print("="*100)
print("             Prediciendo con nuevos valores o entradas nuevas las caracteristicas")
print("="*100)
# ===================================================================
#                                Para predecir valores nuevos
# ===================================================================
Xnuevo = [[100,9.5,2.5,1.3,-0.2]]  # Deberia ser de la clase 1
# cambiar estos valores
Xnuevo = np.concatenate((np.ones((1, 1)), Xnuevo), axis=1)     # Agrega una fila 1s
p = np.argmax(sigmoid(Xnuevo.dot(all_theta.T)), axis = 1)         # Calcula la mayor probabilidad
# print(" Es de la clase: ",p+1)
if p+1 == 1:
    print("Clase 1: (normal) 150: ",p + 1)
elif p+1 == 2:
    print("Clase 2: (hiper) 35: ",p + 1)
else:
    print("Clase 3: (hipo) 30: ",p + 1)

# ====Valores de prueba que los vio durante la evaluacion
# 123,8.1,2.3,1.0,5.1,1
# 107,8.4,1.8,1.5,0.8,1
# 109,10.0,1.3,1.8,4.3,1
# 120,6.8,1.9,1.3,1.9,1
# 100,9.5,2.5,1.3,-0.2,1
# 118,8.1,1.9,1.5,13.7,1
