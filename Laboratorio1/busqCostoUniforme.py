# Búsqueda Coste Uniforme - Uniform Cost Search
from Nodos import Nodo

def Comparar(nodo):
    return nodo.get_costo()

def busqueda_BCU(conecciones, estado_inicial, solucion):
    resuelto = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_raiz = Nodo(estado_inicial)
    nodo_raiz.set_costo(0)
    nodos_frontera.append(nodo_raiz)
    while (not resuelto) and len(nodos_frontera) != 0:
        # Ordenar lista de nodos frontera
        nodos_frontera = sorted(nodos_frontera, key=Comparar)
        nodo_actual = nodos_frontera[0]
        # Extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodos_frontera.pop(0))
        if nodo_actual.get_estado() == solucion:
            # Solucion encontrada
            resuelto = True
            return nodo_actual
        else:
            # Expandir nodos hijo (ciudades con conexion)
            datos_nodo = nodo_actual.get_estado()
            lista_hijos = []
            for achild in conecciones[datos_nodo]:
                hijo = Nodo(achild)
                costo = conecciones[datos_nodo][achild]
                hijo.set_costo(nodo_actual.get_costo() + costo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados):
                    # Si está en la lista lo sustituimos con el nuevo valor de coste si es menor
                    if hijo.en_lista(nodos_frontera):
                        for n in nodos_frontera:
                            if n.equal(hijo)  and n.get_costo() > hijo.get_costo():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                    else:
                        nodos_frontera.append(hijo)
            nodo_actual.set_hijo(lista_hijos)


if __name__ == "__main__":
    #=============
    # 26 conecciones
    #=============
    conecciones = {
        'Cobija' : {'Porvenir' : 30},
        'Porvenir' : {'Riberalta' : 379, 'Rurrenabaque' : 449, 'Cobija' : 30},
        'Riberalta' : {'Rurrenabaque' : 501, 'Porvenir' : 379},
        'Rurrenabaque' : {'Riberalta' : 501, 'Yucumo' : 103, 'Porvenir' : 449},
        'Yucumo' : {'San Ignacio' : 185, 'La Paz' : 227, 'Rurrenabaque' : 103},
        'San Ignacio' : {'Trinidad' : 91, 'Villa Tunari' : 322, 'Yucumo' : 185},
        'Trinidad' : {'San Ramon' : 346, 'San Ignacio' : 91},
        'Villa Tunari' : {'Montero' : 248, 'Cochabamba' : 133, 'San Ignacio' : 322},
        'San Ramon' : {'Concepcion' : 98, 'Montero' : 130, 'Trinidad' : 346},
        'Montero' : {'San Ramon' : 130, 'Santa Cruz' : 55, 'Villa Tunari' : 248},
        'Cochabamba' : {'Epizana' : 69, 'Oruro' : 172, 'Villa Tunari' : 133},
        'Concepcion' : {'San Ramon' : 98},
        'Santa Cruz' : {'Palizada' : 181, 'Ipatiti' : 223, 'Montero' : 55},
        'Epizana' : {'Palizada' : 113, 'Ayquile' : 69, 'Cochabamba' : 118},
        'Oruro' : {'La Paz' : 221, 'Potosi' : 281, 'Cochabamba' : 172},
        'Palizada' : {'Epizana' : 113, 'Ayquile' : 106, 'Santa Cruz' : 181},
        'Ipatiti' : {'Boyuibe' : 139, 'Sucre' : 471, 'Santa Cruz' : 223},
        'Ayquile': {'Palizada' : 106, 'Sucre' : 112, 'Epizana' : 69},
        'La Paz' : {'Desaguadero' : 89, 'Yucumo' : 227, 'Oruro' : 221},
        'Potosi' : {'Sucre' : 135, 'Oruro' : 281},
        'Boyuibe' : {'Villamontes' : 97, 'Ipatiti' : 139},
        'Sucre' : {'Ayquile' : 112, 'Tarija' : 393, 'Potosi' : 135, 'Ipatiti' : 471},
        'Desaguadero' : {'La Paz' : 89},
        'Villamontes' : {'Tarija' : 177, 'Boyuibe' : 97},
        'Tarija' : {'Villamontes' : 177, 'Bermejo' : 162, 'Sucre' : 393},
        'Bermejo' : {'Tarija' : 162}
    }
    estado_inicial = 'Cobija'
    solucion = 'Villamontes'
    nodo_solucion = busqueda_BCU(conecciones, estado_inicial, solucion)
    # Mostrar resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_estado())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
    print("Costo: %s" % str(nodo_solucion.get_costo()))
