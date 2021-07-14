import os
import numpy as np
from matplotlib import pyplot
from scipy import optimize

#  datos de entrenamiento almacenados en los arreglos X, y
# data = np.loadtxt("wine.csv", delimiter=',')
data = np.loadtxt(os.path.join('11. Thyroid', 'new-thyroid.csv'), delimiter=',')

print(data.shape)
X = data[50:, :5]
XP = data[:50, :5]

y = data[50:, 5]
YP = data[:50, 5]
y = np.array([int(e) for e in y])   # Convierte los valores de Y en enteros
# y = np.squeeze(y)         # No se que hace
#  Reemplamos valores de salida para precicion
y[y == 1] = 0
y[y == 2] = 1
y[y == 3] = 2
# ======================
YP[YP == 1] = 0
YP[YP == 2] = 1
YP[YP == 3] = 2
print(X.shape," Dimensiones de Xs")
print(y.shape," Dimensiones de Y")
print("-"*100)
print(X[:10]," Matriz X")
print("-"*100)
print(y[:]," Matriz Y")
print("-"*100)
# Configurando parametros necesario
input_layer_size  = 5  # Entrada de 5 caracteristicas
hidden_layer_size = 10   # 10 unidades ocultas
num_labels = 3          # 3 etiquetas, de 0 a 2

# Me invento los pesos o thetas aleatorios
pesos = {}                  # No olvidar de aumentar el bias en los tamañós
pesos['Theta1'] = np.random.rand(10, 6)# Tamaño sera de entradas * unidades hidden T +1
pesos['Theta2'] = np.random.rand(3, 11)# Tamaño sera de entradas * unidades hidden T +1

Theta1, Theta2 = pesos['Theta1'], pesos['Theta2']# Asignamos a nuevos nombres por comun
# Desenrollar parámetros
print(Theta1.shape)
print(Theta1.ravel().shape," Thetas 1 desenrrolladas")  # Convierte la matriz en un vector
print(Theta2.ravel().shape," Thetas 2 desenrrolladas")  # Pone filas a continuacion de otra

nn_params = np.concatenate([Theta1.ravel(), Theta2.ravel()])    # Une las dos thetas
print(nn_params.shape," nn parametros Dimension")
# print(nn_params," nn o no se que es numero de parametros")
print("-"*100)
# =========Funcion de la sigmoide o activacion===============================
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

# =========Funcion Gradiente Sigmoide o la derivada se sigmoide=================
def sigmoidGradient(z):
    g = np.zeros(z.shape)
    g = sigmoid(z) * (1 - sigmoid(z))   # Derivada de la Sigmoide
    return g
# =========Funcion de costo RN==========================================
def nnCostFunction(nn_params,   # Todas las thetas
                   input_layer_size,
                   hidden_layer_size,
                   num_labels,
                   X, y, lambda_=0.0):
    # desde nn_params  desenrrollamos en las dos thetas
    Theta1 = np.reshape(nn_params[:hidden_layer_size * (input_layer_size + 1)],
                        (hidden_layer_size, (input_layer_size + 1)))    # Primera Capa

    Theta2 = np.reshape(nn_params[(hidden_layer_size * (input_layer_size + 1)):],
                        (num_labels, (hidden_layer_size + 1)))      # Segunda Capa

    m = y.size

    J = 0   # Inicio del costo
    Theta1_grad = np.zeros(Theta1.shape)    # inicializa las theta1 primera capa
    Theta2_grad = np.zeros(Theta2.shape)    # inicializa las theta2 segunda capa
    # Primera capa
    a1 = np.concatenate([np.ones((m, 1)), X], axis=1)   # Agregamos una columna de 1s capa 1
                                                                                     # Capa 1
    a2 = sigmoid(a1.dot(Theta1.T))      # Capa oculta
    a2 = np.concatenate([np.ones((a2.shape[0], 1)), a2], axis=1)    # Agregamos 1s a capa 2

    a3 = sigmoid(a2.dot(Theta2.T))      # Capa de salida

    y_matrix = y.reshape(-1)    # Vuelve toda la Y en una lista simple
    # print(y.shape)
    y_matrix = np.eye(num_labels)[y_matrix]     # Crea una matriz de diagonal 1
    # print(y_matrix)

    temp1 = Theta1      # Variables temporales de theta
    temp2 = Theta2      # Variables temporales de theta

    # Agregar el termino de regularización   --> para evitar sobre ajuste================
    reg_term = (lambda_ / (2 * m)) * (np.sum(np.square(temp1[:, 1:])) + np.sum(np.square(temp2[:, 1:])))

    J = (-1 / m) * np.sum((np.log(a3) * y_matrix) + np.log(1 - a3) * (1 - y_matrix)) + reg_term
# ===================================================================
    # Backpropogation

    delta_3 = a3 - y_matrix
    delta_2 = delta_3.dot(Theta2)[:, 1:] * sigmoidGradient(a1.dot(Theta1.T))

    Delta1 = delta_2.T.dot(a1)
    Delta2 = delta_3.T.dot(a2)

    # Agregar regularización al gradiente

    Theta1_grad = (1 / m) * Delta1
    Theta1_grad[:, 1:] = Theta1_grad[:, 1:] + (lambda_ / m) * Theta1[:, 1:]

    Theta2_grad = (1 / m) * Delta2
    Theta2_grad[:, 1:] = Theta2_grad[:, 1:] + (lambda_ / m) * Theta2[:, 1:]
    grad = np.concatenate([Theta1_grad.ravel(), Theta2_grad.ravel()])

    return J, grad
# ===================================================================
lambda_ = 0
J, _ = nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, lambda_)
print('Costo en parametros (cargado de ex4weights): %.6f ' % J)
print('El costo debe esta cercano a               : 0.287629')

z = np.array([-1, -0.5, 0, 0.5, 1])
g = sigmoidGradient(z)
print('Gradiente sigmoide evaluada con [-1 -0.5 0 0.5 1]:\n  ')
print(g)
print("-"*100)
# ========Funcion que Inicializa thetas randomicos============================
def randInitializeWeights(L_in, L_out, epsilon_init=0.12):
    W = np.zeros((L_out, 1 + L_in))
    W = np.random.rand(L_out, 1 + L_in) * 2 * epsilon_init - epsilon_init

    return W

# =======Fin de la funcion de Pesos randomicos===============================
print('Inicialización de parámetros de redes neuronales...')

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size) # Random
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels)   # Random
# Unir las dos thetas
initial_nn_params = np.concatenate([initial_Theta1.ravel(), initial_Theta2.ravel()], axis=0)
# ===================================================================
#  After you have completed the assignment, change the maxiter to a larger
#  value to see how more training helps.
options= {'maxiter': 300}
lambda_ = 1 # Coeficiente de parendizaje

# Create "short hand" for the cost function to be minimized
costFunction = lambda p: nnCostFunction(p, input_layer_size,
                                        hidden_layer_size,
                                        num_labels, X, y, lambda_)

# Now, costFunction is a function that takes in only one argument
# (the neural network parameters)
res = optimize.minimize(costFunction,
                        initial_nn_params,
                        jac=True,
                        method='TNC',
                        options=options)

# get the solution of the optimization
nn_params = res.x

# Obtain Theta1 and Theta2 back from nn_params
Theta1 = np.reshape(nn_params[:hidden_layer_size * (input_layer_size + 1)],
                    (hidden_layer_size, (input_layer_size + 1)))

Theta2 = np.reshape(nn_params[(hidden_layer_size * (input_layer_size + 1)):],
                    (num_labels, (hidden_layer_size + 1)))

# =======Funcion de prediccion===========================================
def predict(Theta1, Theta2, X):
    # Useful values
    m = X.shape[0]
    num_labels = Theta2.shape[0]

    # You need to return the following variables correctly
    p = np.zeros(m)
    h1 = sigmoid(np.dot(np.concatenate([np.ones((m, 1)), X], axis=1), Theta1.T))    # Capa 1
    h2 = sigmoid(np.dot(np.concatenate([np.ones((m, 1)), h1], axis=1), Theta2.T))   # Capa 2
    p = np.argmax(h2, axis=1)
    return p
# =========Fin de la funcion de predicicon===================================
# print(Theta1," Thetas de la primera capa")
# print("-"*100)
# print(Theta2," Thetas de la segunda capa")
print("-"*100)
print("-"*100)
pred = predict(Theta1, Theta2, X[:,:])
print(pred)
print("-"*100)
print('Precicion con el dataset: %f' % (np.mean(pred == y[:]) * 100))
# ========Prediccion con el dataset nuevo===================================
print("-"*100)
pred = predict(Theta1, Theta2, XP[:,:])
print(pred)
print("-"*100)
print('Precicion con dataset nuevos: %f' % (np.mean(pred == YP[:]) * 100))
# ========Predecir con una fiila nueva======================================
