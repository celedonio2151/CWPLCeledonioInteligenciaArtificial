import os
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
# Cargar datos
# data = np.loadtxt(os.path.join('Datasets', 'ventas.txt'), delimiter=',')
data = np.loadtxt(os.path.join('Datasets', 'ventas2.txt'), delimiter=',')
X = data[:, :4]
Y = data[:, 4]
m = Y.size
# imprimir algunos puntos de datos
print('{:>8s}{:>8s}{:>8s}{:>8s}{:>10s}'.format('X[:,0]', 'X[:, 1]','X[:, 2]','X[:, 3]', 'Y'))
print('-'*52)
for i in range(10):
    print('{:8.0f}{:8.0f}{:8.0f}{:8.0f}{:10.0f}'.format(X[i, 0], X[i, 1],X[i, 2],X[i, 3], Y[i]))
print('-'*52)
# ===========Normalizar => Desviacion estandar=============================
def  featureNormalize(X):
    X_norm = X.copy()
    mu = np.zeros(X.shape[1])
    sigma = np.zeros(X.shape[1])

    mu = np.mean(X, axis = 0)
    sigma = np.std(X, axis = 0)
    X_norm = (X - mu) / sigma

    return X_norm, mu, sigma
# ==========Funcion Graficadora con cada una de las X , Y======================
def graficarLasXs(X, Y,mesX,mesY):
    #Grafica los puntos x e y en una figura nueva.
    fig = pyplot.figure()  # abre una nueva figura
    pyplot.title('Grafica de cantidad vendida de Televidores')
    pyplot.plot(X, Y, 'ro', ms=10, mec='k')
    pyplot.ylabel(mesY)
    pyplot.xlabel(mesX)
# ==========Llamada a la funcion graficadora================================
graficarLasXs(X[: , 0],Y,'Tamaño en pulgadas (in)','Cantidad Vendida')
graficarLasXs(X[: , 1],Y,'Peso en Kg','Cantidad Vendida')
graficarLasXs(X[: , 2],Y,'Temporada meses','Cantidad Vendida')
graficarLasXs(X[: , 3],Y,'Fabricante','Cantidad Vendida')
pyplot.show()
# llama featureNormalize con los datos cargados
X_norm, mu, sigma = featureNormalize(X)
#
# print(X)
# print(Y)
print('Media calculada:', mu)
print('Desviación estandar calculada:', sigma)
print(X_norm[:10]," Matriz Normalizada Xs")
print('-'*100)
print(Y[:10]," Vector Ys")
print('-'*100)

# Añade el termino de interseccion a X
# (Columna de unos para X0)
X = np.concatenate([np.ones((m, 1)), X_norm], axis=1)   # Agrega columna 1
print(X[:10]," Columna de 1s agregado Xs")
print('-'*100)
# ===========Funcion del Calculo del Costo==================================
def computeCostMulti(X, y, theta):
    # Inicializa algunos valores utiles
    m = y.shape[0] # numero de ejemplos de entrenamiento
    J = 0
    h = np.dot(X, theta)
    J = (1/(2 * m)) * np.sum(np.square(np.dot(X, theta) - y))
    return J
# ============Funcion de Descenso por el Gradiente==========================
def gradientDescentMulti(X, y, theta, alpha, num_iters):
    # Inicializa algunos valores
    m = y.shape[0] # numero de ejemplos de entrenamiento
    # realiza una copia de theta, el cual será acutalizada por el descenso por el gradiente
    theta = theta.copy()
    J_history = []
    for i in range(num_iters):
        theta = theta - (alpha / m) * (np.dot(X, theta) - y).dot(X)
        J_history.append(computeCostMulti(X, y, theta))

    return theta, J_history
# ===================================================================
"""#### 3.2.1 Seleccionando coheficientes de aprendizaje
"""
# Elegir algun valor para alpha (probar varias alternativas)
alpha = 0.01
num_iters = 1500

# inicializa theta y ejecuta el descenso por el gradiente
# theta = np.zeros(3)
theta = [0, 0, 0, 0, 0]     # inicializa tethas con ceros u otros numeros
theta, J_history = gradientDescentMulti(X, Y, theta, alpha, num_iters)  # ejecuta GDM

# Grafica la convergencia del costo
pyplot.plot(np.arange(len(J_history)), J_history, lw=2)
pyplot.xlabel('Numero de iteraciones')
pyplot.ylabel('Costo J')
pyplot.show()
# Muestra los resultados del descenso por el gradiente
print('theta calculado por el descenso por el gradiente: {:s}'.format(str(theta)))
print('-'*100)

# Estimar la cantidad a vender : valores reales
# 130,21.8,9,90,193
# 140,21.9,10,100,199
# 145,22,8,80,187
# 160,22.4,9,100,201
names = ['interseccion => X0','Tamaño => X1', 'peso => X2', 'meses => X3', 'marca => X4', 'Cantidad vendida => Y']    # Columnas
# X_array = [1, 170, 26, 10, 100] # mas 1 (opcional) y caracteristicas una fila literal  preuba 1
# X_array = [1, 50, 7.5, 6, 50] # mas 1 (opcional) y caracteristicas una fila literal   prueba 2
X_array = [1, 19, 4.6, 2,10 ] # mas 1 (opcional) y caracteristicas una fila literal = 20,4,1,10,115     real
print("Tamaño: ",X_array[1],",Peso: ",X_array[2],",Mes: ",X_array[3],",Marca: ",X_array[4])
X_array[1:5] = (X_array[1:5] - mu) / sigma
price = np.dot(X_array, theta)   # Se debe cambiar esto
print('Predicinedo la cantidad a vender de televisores: (usando el descenso por el gradiente): $ {:.0f}'.format(price))
print()
print('='*100)
print('='*100)
# ===================================================================
#                         Calculo con la Ecuacion de la Normal
# ===================================================================
# Cargar datos  para calcular con la ecuacion de la normal
print("Calculo con la ecuacion de la normal")
print('-'*100)
data = np.loadtxt(os.path.join('Datasets', 'ventas2.txt'), delimiter=',')
X = data[:, :4]
y = data[:, 4]
m = y.size
X = np.concatenate([np.ones((m, 1)), X], axis=1)    # Agrega una columna de 1s
# ==============Ecuacion de la normal====================================
def normalEqn(X, y):
    theta = np.zeros(X.shape[1])
    theta = np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),y)
    return theta
# ===================================================================
# Calcula los parametros con la ecuación de la normal
theta = normalEqn(X, y);
# Muestra los resultados optenidos a partir de la aplicación de la ecuación de la normal
print('Theta calculado a partir de la ecuación de la normal: {:s}'.format(str(theta)));
print('-'*100)
# Estimar la cantidad a vender de Televisores
names = ['interseccion => X0','Tamaño => X1', 'peso => X2', 'meses => X3', 'marca => X4', 'Cantidad vendida => Y']    # Columnas
X_array = [1, 19, 4.6, 2,10 ]
price = np.dot(X_array, theta)
print("Tamaño: ",X_array[1],",Peso: ",X_array[2],",Mes: ",X_array[3],",Marca: ",X_array[4])
print('Predicinedo la cantidad a vender de televisores: (usando la ecuación de la normal): $ {:.0f}'.format(price))
