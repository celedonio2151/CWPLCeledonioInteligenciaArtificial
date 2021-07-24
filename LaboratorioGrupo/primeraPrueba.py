import torch
from mlxtend.data import loadlocal_mnist
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, roc_auc_score
import numpy as np
from matplotlib import pyplot
import platform
import os

# =============Datos de entrenamiento ===================================
if not platform.system() == 'Windows':
    X, Y = loadlocal_mnist(
            images_path='train-images-idx3-ubyte',
            labels_path='train-labels-idx1-ubyte')

else:
    X, Y = loadlocal_mnist(
            images_path='train-images.idx3-ubyte',
            labels_path='train-labels.idx1-ubyte')
# =============Datos de evaluacion======================================
if not platform.system() == 'Windows':
    XP, YP = loadlocal_mnist(
            images_path='t10k-images-idx3-ubyte',
            labels_path='t10k-labels-idx1-ubyte')

else:
    XP, YP = loadlocal_mnist(
            images_path='t10k-images.idx3-ubyte',
            labels_path='t10k-labels.idx1-ubyte')
# ===================================================================
print(X[:10],"Matriz de las Xs")
print("-"*100)
print(Y[:10],"Matriz de las Ys")
print("-"*100)
print(X.shape," Dimensiones de la matris Xs")
print(Y.shape," Dimensiones de Ys")
print("-"*100)
m, n = X.shape
print(m," Cantidad de ejercicios o filas")
print(n," Cantidad de caracteristicas o columnas")
print("-"*100)
print("Dimensiones de los datos de evaluacion y otras:")
print(XP.shape)
print(YP.shape)
print("-"*100)
X.shape, Y.shape
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
# rand_indices = np.random.choice(m, 80, replace=False)
rand_indices = np.arange(0,80)
# rand_indices = [0,1,2,3,4,5,6,7,8,9]
print(rand_indices," Estos son los indices")
sel = X[rand_indices, :]
print(sel.shape," Dimensiones del la matriz aleatoria de X")
print("-"*100)
displayData(sel)
# pyplot.show()
# =====================normalización y split===============================
X_train, X_test, y_train, y_test = X[:60000] / 255., XP[:] / 255., Y[:60000].astype(np.int), YP[:].astype(np.int)

# ===============convertimos datos a tensores y copiamos en gpu===============
X_t = torch.from_numpy(X_train).float()
Y_t = torch.from_numpy(y_train).long()
# ===================función de pérdida y derivada==========================
def softmax(x):
    return torch.exp(x) / torch.exp(x).sum(axis=-1,keepdims=True)

def cross_entropy(output, target):
    logits = output[torch.arange(len(output)), target]
    loss = - logits + torch.log(torch.sum(torch.exp(output), axis=-1))
    loss = loss.mean()
    return loss
# =========Funcion de evaluacion=========================================
def evaluate(x):
    model.eval()    # Evita cambiar los tethas
    y_pred = model(x)
    y_probas = softmax(y_pred)
    return torch.argmax(y_probas, axis=1)
#============creamos una clase que hereda de `torch.nn.Module================
class Model(torch.nn.Module):

    # constructor
    def __init__(self, D_in, H1, H2, D_out):# entradas entradaOculta entradaOculta2 salida

        # llamamos al constructor de la clase madre
        super(Model, self).__init__()

        # definimos nuestras capas
        self.fc1 = torch.nn.Linear(D_in, H1)    # Automatico agrega columna 1
        self.relu1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(H1, H2)      # Automatico agrega columna 1
        self.relu2 = torch.nn.ReLU()
        self.fc3 = torch.nn.Linear(H2, D_out)

    # lógica para calcular las salidas de la red
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x
# =========Fin de la clase modelo=========================================
model = Model(784, 50, 100, 10)
outputs = model(torch.randn(64, 784))
print(outputs.shape," Dimensiones de la capa de salida")
print('-'*100)
print(model," Esto es el modelo capas ")
print('-'*100)


"""Ahora, podemos entrenar nuestra red de la misma forma que lo hemos hecho anteriormente."""

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

epochs = 500   # 1500
log_each = 10
l = []
model.train()
for e in range(1, epochs+1):

    # forward
    y_pred = model(X_t)

    # loss
    loss = criterion(y_pred, Y_t)
    l.append(loss.item())

    # ponemos a cero los gradientes
    optimizer.zero_grad()

    # Backprop (calculamos todos los gradientes automáticamente)
    loss.backward()

    # update de los pesos
    optimizer.step()

    if not e % log_each:
        print(f"Epoch {e}/{epochs} Loss {np.mean(l):.5f}")

y_pred = evaluate(torch.from_numpy(X_test).float())
print(y_pred,' Estos son las ys predichas')
print(accuracy_score(y_test, y_pred.cpu().numpy())," Precision del modelo")
print(y_train[-10:]," Y Originales")
print(y_pred[-10:]," Yes predichas")
print("-"*100)
print(l[-10:]," Que es esto????????????")


# ===================================================================
# XPrueba = XP[5005:5006, :].copy()    # Mandamos la prueba una fila
# displayData(XP[5005:5006, :])    # Imprime Vestido
# pyplot.show()
# XPrueba = np.concatenate([np.ones((1, 1)), XPrueba], axis=1)    # Una columna de 1
# print(XPrueba.shape," Dimensiones de la fila de predicción mas 1:")
# p = np.argmax(sigmoid(XPrueba.dot(all_theta.T)), axis = 1) # Devuelde la probabilidad maxima
# # print(p," Valor predicho:")     #Deberia imprimir
# if p == 0:
#     print(p," Cero")
# elif p == 1:
#     print(p," Uno")
# elif p == 2:
#     print(p," Dos")
# elif p == 3:
#     print(p," Tres")
# elif p == 4:
#     print(p," Cuatro")
# elif p == 5:
#     print(p," Cinco")
# elif p == 6:
#     print(p," Seis")
# elif p == 7:
#     print(p," Siete")
# elif p == 8:
#     print(p," Ocho")
# elif p == 9:
#     print(p," Nueve")
# print("-"*100)
