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
        # print(individuo,"========= Padres ==========")
        return individuo

    def crearPoblacion(self):
        """
            Crea una poblacion nueva de individuos
        """
        return [self.individual(0,9) for i in range(self.num)]       # Llama a crear individuos num veces y guarda en un array

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
        # print("***************************************")
        # print(puntuados)
        # print("***************************************")
        puntuados = [i[1] for i in sorted(puntuados)] # Ordena los pares ordenados y se queda solo con el array de valores
        # print("===========================")
        # print(puntuados)
        # print("===========================")
        population = puntuados


        seleccionado =  puntuados[(len(puntuados)-self.selecioin):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'



        #Se mezcla el material genetico para crear nuevos individuos
        for i in range(len(population)-self.selecioin):
            punto = random.randint(0,self.largo-1) #Se elige un punto para hacer el intercambio
            padre = random.sample(seleccionado, 2) #Se eligen dos padres
            # print(population)
            # print("===============================")
            population[i][:punto] = padre[0][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
            population[i][punto:] = padre[1][punto:]

        return population #El array 'poblacion' tiene ahora una nueva poblacion de individuos, que se devuelven
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
modelo = [1,0,1,0,1,0]
modelo2 = [0,1,0,1,0,1]
ngenes = 6
kpoblacion = 6
selecionar = 3
valor_mutacion = 0.2
poblacion = GenesMutantes(modelo,ngenes,kpoblacion,selecionar,valor_mutacion)#Inicializar una poblacion
poblacion2 = GenesMutantes(modelo2,ngenes,kpoblacion,selecionar,valor_mutacion)#Inicializar una poblacion 2
print("======================================================")
print("Modelo: ",modelo)
print("======================================================")
poblacionF = poblacion.crearPoblacion()     #Devuelve la poblacion inicial
poblacionF2 = poblacion2.crearPoblacion()   #Devuelve la poblacion inicial
print("Poblacion Inicial: ")
for x in poblacionF:
    print(x,"========= Primeros padres =========")
# print("Poblacion Inicial:\n%s"%(poblacionF)) #Se muestra la poblacion inicial
print("======================================================")
# poblacion.crearPoblacion()
# print("Poblacion Final: ")
pobla = poblacion.evolucionDePoblacion(poblacionF)  # Devuele poblacion  final
print("Poblacion Final: ")
for x in pobla:
    print(x,"========= Ultima generacion =======")
# print("Poblacion Inicial:\n%s"%(poblacionF)) #Se muestra la poblacion inicial
print("======================================================")
pobla2 = poblacion2.evolucionDePoblacion(poblacionF2)   # Devuele poblacion  final
# print(pobla)
ultimo = pobla.pop()
print(ultimo,"========= El mejor adaptado hasta ahora")
ultimo2 = pobla2.pop()
print(ultimo2,"========= El mejor adaptado hasta ahora")
print("\nTablero de ajedrez")
bandera = 0
for i in range(4):
    if bandera == 0:
        for j in range(len(ultimo)):
                # if ultimo[j] == 1:
                #     print(" X ",end="")
                # else:
                #     print(" . ",end="")
                if ultimo[ j ] == 1:
                    print(" X ",end="")
                elif ultimo[ j ] == 0:
                    print(" . ",end="")
                else:
                    print(" ! ",end="")
        bandera = 1
    else:
        for j in range(len(ultimo2)):
            if ultimo2[j] == 1:
                print(" X ",end="")
            elif ultimo2[j] == 0:
                print(" . ",end="")
            else:
                print(" ! ",end="")
        bandera = 0
    print("")
