from mlxtend.data import loadlocal_mnist
import platform
import os
import numpy as np
from matplotlib import pyplot
from scipy import optimize
from scipy.io import loadmat
# =============Datos de entrenamiento ===================================
if not platform.system() == 'Windows':
    X, y = loadlocal_mnist(
            images_path='train-images-idx3-ubyte',
            labels_path='train-labels-idx1-ubyte')

else:
    X, y = loadlocal_mnist(
            images_path='train-images.idx3-ubyte',
            labels_path='train-labels.idx1-ubyte')
# =============Datos de evaluacion======================================
if not platform.system() == 'Windows':
    XP, yP = loadlocal_mnist(
            images_path='t10k-images-idx3-ubyte',
            labels_path='t10k-labels-idx1-ubyte')

else:
    XP, yP = loadlocal_mnist(
            images_path='t10k-images.idx3-ubyte',
            labels_path='t10k-labels.idx1-ubyte')
# ===================================================================
print(X[:10],"Matriz de las Xs")
print("-"*100)
print(y[:10],"Matriz de las Ys")
print("-"*100)
print(X.shape," Dimensiones de la matris Xs")
print(y.shape," Dimensiones de Ys")
print("-"*100)
m, n = X.shape
print(m," Cantidad de ejercicios o filas")
print(n," Cantidad de caracteristicas o columnas")
print("-"*100)
print("Dimensiones de los datos de evaluacion y otras:")
print(XP.shape)
print(yP.shape)
print("-"*100)
num_labels = 10
# ============Funcion que grafica 100 imagenes al azar=======================
def displayData(X, example_width=None, figsize=(10, 10)):
    """
    Muestra datos 2D almacenados en X en una cuadrícula apropiada.
    """
    if X.ndim == 2:
        m, n = X.shape
    elif X.ndim == 1:
        n = X.size
        m = 1
        X = X[None]  # Promocionar a una matriz bidimensional
    else:
        raise IndexError('La entrada X debe ser 1 o 2 dimensinal.')

    example_width = example_width or int(np.round(np.sqrt(n)))
    example_height = n / example_width

    # Calcula el numero de elementos a mostrar
    display_rows = int(np.floor(np.sqrt(m)))
    display_cols = int(np.ceil(m / display_rows))

    fig, ax_array = pyplot.subplots(display_rows, display_cols, figsize=figsize)
    fig.subplots_adjust(wspace=0.025, hspace=0.025)

    ax_array = [ax_array] if m == 1 else ax_array.ravel()

    for i, ax in enumerate(ax_array):
        ax.imshow(X[i].reshape(example_width, example_width, order='F'),
                  cmap='Greys', extent=[0, 1, 0, 1])
        ax.axis('off')
# =====================Fin de la funcion graficadora========================

# Selecciona aleatoriamente 100 puntos de datos para mostrar
rand_indices = np.random.choice(m, 80, replace=False)
sel = X[rand_indices, :]
print(sel.shape," Dimensiones del la matriz aleatoria de X")
print("-"*100)
displayData(sel)
pyplot.show()

# ===========Valores de prueba o testeando=================================
# valores de prueba para los parámetros theta
theta_t = np.array([-2, -1, 1, 2], dtype=float)
# valores de prueba para las entradas
X_t = np.concatenate([np.ones((5, 1)), np.arange(1, 16).reshape(5, 3, order='F')/10.0], axis=1)
# valores de testeo para las etiquetas
y_t = np.array([1, 0, 1, 0, 1])
# valores de testeo para el parametro de regularizacion
lambda_t = 3
# ===========Funcion de la sigmoide=======================================
def sigmoid(z):
    """
    Calcula la sigmoide de z.
    """
    return 1.0 / (1.0 + np.exp(-z))
# ===========Funcion de calculo del costo===================================
def lrCostFunction(theta, X, y, lambda_):
    # Inicializa algunos valores utiles
    m = y.size
    # convierte las etiquetas a valores enteros si son boleanos
    if y.dtype == bool:     # Si el booleano
        y = y.astype(int)   # Pasa a entero

    J = 0
    grad = np.zeros(theta.shape)

    h = sigmoid(X.dot(theta.T))

    temp = theta
    temp[0] = 0

    J = (1 / m) * np.sum(-y.dot(np.log(h)) - (1 - y).dot(np.log(1 - h))) + (lambda_ / (2 * m)) * np.sum(np.square(temp))

    grad = (1 / m) * (h - y).dot(X)
    grad = grad + (lambda_ / m) * temp

    return J, grad
# =============Fin de la funcion de costo===================================
J, grad = lrCostFunction(theta_t, X_t, y_t, lambda_t)

print('Costo         : {:.6f}'.format(J))
print('Costo esperadot: 2.534819')
print('-----------------------')
print('Gradientes:')
print(' [{:.6f}, {:.6f}, {:.6f}, {:.6f}]'.format(*grad))
print('Gradientes esperados:')
print(' [0.146561, -0.548558, 0.724722, 1.398003]');
print("-"*100)
# ==========Funcion One vs All===========================================
def oneVsAll(X, y, num_labels, lambda_):

    # algunas variables utiles
    m, n = X.shape      # Numero de filas y columnas de X
    all_theta = np.zeros((num_labels, n + 1))   # Inicializa las thetas con el tamaño adecuado
    # print(all_theta," Todas las thetas")
    # Agrega unos a la matriz X
    X = np.concatenate([np.ones((m, 1)), X], axis=1)    # Agrega una columna de 1s a  X
    for c in np.arange(num_labels):
        initial_theta = np.zeros(n + 1)
        options = {'maxiter': 100}
        res = optimize.minimize(lrCostFunction,
                                initial_theta,
                                (X, (y == c), lambda_),
                                jac=True,
                                # method='CG',
                                # method='BFGS',
                                method='TNC',
                                # method='Powell',
                                # method='Newton-CG',
                                options=options)

        all_theta[c] = res.x

    return all_theta
# ===================================================================
lambda_ = 0.09
# print(X.shape)
# print(y.shape)
all_theta = oneVsAll(X, y, num_labels, lambda_)     # Devuelde todas las thetas para los 10 numeros
# print(all_theta.shape," Todas las thetas ya econtradas")
def predictOneVsAll(all_theta, X):

    m = X.shape[0];
    num_labels = all_theta.shape[0]

    p = np.zeros(m)

    # Add ones to the X data matrix
    X = np.concatenate([np.ones((m, 1)), X], axis=1)
    p = np.argmax(sigmoid(X.dot(all_theta.T)), axis = 1)

    return p
# =================Precicion con los datos de entrenamiento===================
pred = predictOneVsAll(all_theta, X)    # Pasamos todas las thetas y matriz X
print('Precision del conjuto de entrenamiento: {:.2f}%'.format(np.mean(pred == y) * 100))
print("-"*100)
# ===================================================================
# =================Precicion con datos nuevos=============================
pred = predictOneVsAll(all_theta, XP)    # Pasamos todas las thetas y matriz XP
print('Precision del conjuto de entrenamiento: {:.2f}%'.format(np.mean(pred == yP) * 100))
print("-"*100)
print("-"*100)

# ======Imprimimos un valor para ver si es cierto lo que predijo===================
vector = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle boot']
# XPrueba = XP[5010:5011, :].copy()    # Mandamos la prueba una fila
# displayData(XP[5010:5011, :])    # Imprime Camiseta
XPrueba = XP[5005:5006, :].copy()    # Mandamos la prueba una fila
displayData(XP[5005:5006, :])    # Imprime Vestido
pyplot.show()
XPrueba = np.concatenate([np.ones((1, 1)), XPrueba], axis=1)    # Una columna de 1
print(XPrueba.shape," Dimensiones de la fila de predicción mas 1:")
p = np.argmax(sigmoid(XPrueba.dot(all_theta.T)), axis = 1) # Devuelde la probabilidad maxima
# print(p," Valor predicho:")     #Deberia imprimir
if p == 0:
    print(p," T-shirt/Top")
elif p == 1:
    print(p," Trouser")
elif p == 2:
    print(p," Pullover")
elif p == 3:
    print(p," Dress")
elif p == 4:
    print(p," Coat")
elif p == 5:
    print(p," Sandal")
elif p == 6:
    print(p," Shirt")
elif p == 7:
    print(p," Sneaker")
elif p == 8:
    print(p," Bag")
elif p == 9:
    print(p," Ankle boot")
print("-"*100)


# Tarda unos minutos antes de finalizar la ejecucion
