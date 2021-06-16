import random

class GenesMutantes():
    """docstring for GenesMutantes."""

    def __init__(self, modelo,largo,num,selecioin,mutar):
        self.modelo  = modelo   # Objeto a alcanzar
        self.largo = largo  # Longitud de genes
        self.num = num # Numero de individuos en la poblacion
        self.selecioin = selecioin  # Numero que se selecionara para su reproduccion
        self.mutacion_valor = mutar

    def individual(self,min,max):
        """
            Crea un individual
        """
        individuo = [random.randint(min, max) for i in range(self.largo)]
        return individuo
# ===================================================================
# Extrae de 8 binarios en vectores del vector principal y devuelve en otro vector
    def caracterAsciiLetra(self,individual):
        asciiLetra = []
        inicio = 0
        fin = 0
        for i in range(4):
            ocho = []
            fin += 8
            ocho = individual[inicio:fin]
            asciiLetra.append(ocho)
            inicio +=8
        return asciiLetra
# ===================================================================
# Convierte de numeros binarios a numeros decimales
    def binario_a_decimal(self,individual8):
        suma = 0
        for i,x in enumerate(individual8[::-1]):
            suma += int(x * 2 ** i)
        return suma
# ===================================================================
# Decodifica un individuo de numero decimal a binario
    def dec_to_bin(self,x):
        return int(bin(x)[2:])

# ===================================================================
# Devuelve en un de vector los numeros decimales convertidos a binarios
    def binarios(self,modelo):
        vector = []
        for x in modelo:
            vector.append(self.dec_to_bin(x))
        return vector


# ===================================================================
# Devuele un vector de un individuo de numero binario a decimal
    def decimales(self,individuo):
        matrix = self.caracterAsciiLetra(individuo)
        decimalVector = []
        for x in matrix:
            decimalVector.append(self.binario_a_decimal(x))
        return decimalVector
# Crea la poblacion de individuos
# ===================================================================
    def crearPoblacion(self):
        """
            Crea una poblacion nueva de individuos
        """
        return [self.individual(0,9) for i in range(self.num)]       # Llama a crear individuos num veces y guarda en un array
# ===================================================================
    def calcularFitness(self,individual):
        """
            Calcula el fitness de un individuo concreto.
        """
        fitness = 0
        for i in range(len(individual)):
            if individual[i] == self.modelo[i]:
                fitness += 1
        return fitness

    def selection_and_reproduction(self,population):
        """
            Puntua todos los elementos de la poblacion (population) y se queda con los mejores
            guardandolos dentro de 'selected'.
            Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
            llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
            modificar).

            Por ultimo muta a los individuos.

        """
        puntuados = [ (self.calcularFitness(i), i) for i in population]
        '''Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])'''
        puntuados = [i[1] for i in sorted(puntuados)] # Ordena los pares ordenados y se queda solo con el array de valores
        population = puntuados


        selected =  puntuados[(len(puntuados)-self.selecioin):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'

        #Se mezcla el material genetico para crear nuevos individuos
        for i in range(len(population)-self.selecioin):
            punto = random.randint(1,self.largo-1) #Se elige un punto para hacer el intercambio
            padre = random.sample(selected, 2) #Se eligen dos padres
            population[i][:punto] = padre[0][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
            population[i][punto:] = padre[1][punto:]

        return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven
# ===================================================================
    def mutation(self,population):
        """
            Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria
            alcanzarse la solucion.
        """
        for i in range(len(population)-self.selecioin):
            if random.random() <= self.mutacion_valor: #Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
                # print(random.random())
                punto = random.randint(0,self.largo-1) #Se elgie un punto al azar
                nuevo_valor = random.randint(0,9) #y un nuevo valor para este punto

                #Es importante mirar que el nuevo valor no sea igual al viejo
                while nuevo_valor == population[i][punto]:
                    nuevo_valor = random.randint(0,9)

                #Se aplica la mutacion reemplazamos con el nuevo valor en valor anterior
                population[i][punto] = nuevo_valor

        return population
# ===================================================================
    def evolucionDePoblacion(self,poblacion):
        for x in range(100):
            poblacion = self.selection_and_reproduction(poblacion)
            poblacion = self.mutation(poblacion)
        return poblacion
# ===================================================================
# ===================================================================
class ConvertirPINaVector32bits():
    """docstring for ConvertirPINaVector32bits."""

    # def __init__(self, arg):
    #     super(ConvertirPINaVector32bits, self).__init__()
    #     self.arg = arg

# ===================================================================
# Extrae de 8 binarios en vectores del vector principal y devuelve en otro vector
    def caracterAsciiLetra(self,individual):
        asciiLetra = []
        inicio = 0
        fin = 0
        for i in range(4):
            ocho = []
            fin += 8
            ocho = individual[inicio:fin]
            asciiLetra.append(ocho)
            inicio +=8
        return asciiLetra
# ===================================================================
# Devuele un vector de un individuo de numero binario a decimal
    def decimales(self,individuo):
        matrix = self.caracterAsciiLetra(individuo)
        decimalVector = []
        for x in matrix:
            decimalVector.append(self.binario_a_decimal(x))
        return decimalVector
# ===================================================================
# Decodifica un individuo de numero decimal a binario
    def dec_to_bin(self,x):
        return int(bin(x)[2:])

# ===================================================================
# Devuelve en un de vector los numeros decimales convertidos a binarios
    def binarios(self,modelo):
        vector = []
        for x in modelo:
            vector.append(self.dec_to_bin(x))
        return vector
# ===================================================================
# Convierte de numeros binarios a numeros decimales
    def binario_a_decimal(self,individual8):
        suma = 0
        for i,x in enumerate(individual8[::-1]):
            suma += int(x * 2 ** i)
        return suma
# ===================================================================
#                                                 Programa Principal
# ===================================================================
modelo = []
print("Ingrese los valores entre 128 y 255 para los 4 codigos:")
for x in range(1,5):
    print("Ingrese el PIN ",x,": ",end='')
    llave = int(input(""))
    modelo.append(llave)
model = ConvertirPINaVector32bits()
# model8 = model.caracterAsciiLetra(modelo) # Devuelve el modelo en fragmentos de 8
binario = model.binarios(modelo) # Devuelve de fragmentos de 8 decimal, en binario fragmento 8
# Creando un modelo para enviar como modelo a seguir
union = []
for value in binario:
    union.append(str(value))
cadena = str(''.join(union))
modeloF = []
for x in cadena:
    modeloF.append(int(x))
# ===================================================================
ngenes = 32 # Longitud de Genes
kpoblacion = 100 # Numero de poblacion inicial
selecionar = 3  # Seleecion prematura para su reproduccion
valor_mutacion = 0.2    # Valor de mutacion
poblacion = GenesMutantes(modeloF,ngenes,kpoblacion,selecionar,valor_mutacion)# Objeto de Genes
print("======================================================")
print("Modelo o PIN: ",modelo)
print("======================================================")
poblacionF = poblacion.crearPoblacion()     #Devuelve la poblacion inicial
print("Poblacion Inicial: ")
for x in poblacionF:
    print(x,"= Primeros padres")
print("================================================================")
# poblacion.crearPoblacion()
pobla = poblacion.evolucionDePoblacion(poblacionF)  # Devuele poblacion  final
print("Poblacion Final: ")
for x in pobla:
    print(x,"= Ultima generacion")
print("================================================================")
ultimo = pobla.pop()
print(ultimo,"= El mejor adaptado hasta ahora")
# Resultado Final
pa = poblacion.caracterAsciiLetra(ultimo)
print(modelo," == PIN o modelo en decimal")  # muestra el PIN en numero decimal
p = poblacion.decimales(ultimo) # resultado final en decimal convergido
print(p," == resultado final reproducido, mutado,etc")
print(pa," == resultado final en binario reproducido, mutado,etc")
