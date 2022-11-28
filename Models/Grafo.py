from collections import defaultdict, deque
from queue import PriorityQueue
from Models.Arista import *
from Models.Vertice import *
from copy import *
from tkinter import messagebox as MB


class Grafo:
    def __init__(self):
        self.listaVertices = []
        self.listaAristas = []
        self.visitadosCP = []
        self.visitadosCA = []
        self.adyacencias = {}
        self.vistadosCKruskal = []
        self.repetidos = 0
        self.listaAristasB = []
        self.visitadosDijkstra = []
        self.edges = defaultdict(list)
        self.weights = {}

    def getListaVertices(self):
        list = []
        for i in self.listaVertices:
            list.append(i.dato)
        return list

    def ingresarVertices(self, vertice):
        if not self.verificarExisteV(vertice, self.listaVertices):
            self.listaVertices.append(Vertice(vertice))

    def verificarExisteV(self, vertice, lista):
        for i in range(len(lista)):
            if vertice == lista[i].getDato():
                return True
        return False

    def gradoGrafo(self):
        return self.listaVertices.len()

    def ingresarArista(self, origen, destino, peso=0):
        if not self.verificarExisteA(origen, destino, self.listaAristas):
            if self.verificarExisteV(origen, self.listaVertices) and self.verificarExisteV(destino, self.listaVertices):
                self.listaAristas.append(Arista(origen, destino, peso))
                self.edges[origen].append(destino)
                self.edges[destino].append(origen)
                self.weights[(origen, destino)] = peso
                self.weights[(destino, origen)] = peso
                if not destino in self.obtenerOrigen(origen).listaAdyacentes:
                    self.obtenerOrigen(origen).listaAdyacentes.append(destino)
                if not origen in self.obtenerOrigen(destino).listaAdyacentes:
                    self.obtenerOrigen(destino).listaAdyacentes.append(origen)

    def obtenerOrigen(self, origen):
        for i in range(len(self.listaVertices)):
            if origen == self.listaVertices[i].getDato():
                return self.listaVertices[i]

    def obtenerArista(self, origen, destino):
        list = []
        for i in self.listaAristas:
            if (origen == i.origen and destino == i.destino) or (destino == i.origen and origen == i.destino):
                list.append(i)
        return list

    def bloquearArista(self, origen, destino):
        x = False
        if origen == destino:
            return MB.showerror("ERROR", "Origen y Destino no pueden ser iguales")
        for i in self.listaAristasB:
            if i.origen == origen and i.destino == destino:
                return MB.showerror("ERROR", "La ruta ya está bloqueada")
        for j in self.obtenerArista(origen, destino):
            index = self.listaAristas.index(j)
            self.listaAristasB.append(self.listaAristas.pop(index))
            self.obtenerOrigen(
                j.origen).listaAdyacentes.remove(j.destino)
            if not self.verificarCamino(origen, destino):
                self.listaAristas.append(self.listaAristasB.pop())
                self.obtenerOrigen(j.origen).listaAdyacentes.append(j.destino)
                return MB.showerror("ERROR", "Esta ruta no se puede bloquear")
            x = True
        if x == True:
            return MB.showinfo("ESTADO", f"Ruta entre {origen} y {destino} BLOQUEADA")
        return MB.showerror("ERROR", f"No existe una ruta entre {origen} y {destino}")

    def verificarCamino(self, origen, destino):
        self.visitadosCP.clear()
        #print("VISITADOS ORIGINAL:", self.visitadosCP)
        self.rProfundidad(origen)
        #print("VISITADOS MODIFICADO: ", self.visitadosCP)
        #print(origen, destino)
        if destino in self.visitadosCP and origen in self.visitadosCP:
            return True
        return False

    def verificarExisteA(self, origen, destino, lista):
        for i in range(len(lista)):
            if origen == lista[i].getOrigen and destino == lista[i].getDestino():
                return True
        return False

    def cantidadPozos(self):
        nV = len(self.listaVertices)
        nA = (nV*(nV-1))/2
        pozos = nA - len(self.listaAristas)
        return pozos

    def cantidadPozosV(self, origen):
        count = 0
        for i in self.listaVertices:
            if i.getDato() == origen:
                pass
            elif self.verificarPozo(origen, i.getDato()):
                count += 1
        return count

    def verificarPozo(self, origen, destino):
        print(f">>> {origen} a {destino}")
        for i in self.listaAristas:
            print(i.getOrigen(), i.getDestino())
            if i.getOrigen() == origen and i.getDestino() == destino:
                return False
        return True

    def obtenerAristas(self):
        for i in self.listaAristas:
            print(f"{i.origen} > {i.destino} - {i.peso}")

    def obtenerAristasB(self):
        for i in self.listaAristasB:
            print(f"{i.origen} > {i.destino} - {i.peso}")

    def mostrarVyA(self):
        print(f"VERTICE..........ADYACENCIAS")
        for i in self.listaVertices:
            print(f"{i.getDato()} - {i.getListaAdyacentes()}")

    def mayorPesoArista(self):
        arista = None
        mayor = 0
        for i in self.listaAristas:
            if i.getPeso() > mayor:
                mayor = i.getPeso()
                arista = i
        return arista

    def promedioArista(self):
        sum = 0.0
        for i in self.listaAristas:
            sum += i.getPeso()
        return sum/len(self.listaAristas)

    # Ordenamiento con metodo Bubble Sort
    def ordenarAristas(self):
        A = self.listaAristas
        for i in range(1, len(A)):
            for j in range(0, len(A)-i):
                if (A[j+1].getPeso() < A[j].getPeso()):
                    aux = A[j]
                    A[j] = A[j+1]
                    A[j+1] = aux
        for i in A:
            i.mostrar()

    def mayorFuentes(self):
        mayor = 0
        for i in self.listaVertices:
            if i.getListaAdyacentes() > mayor:
                mayor = i

    def ordenamiento(self, array):
        for i in range(len(array)):
            for j in range(0, len(array) - i - 1):
                if array[j].getPeso() > array[j + 1].getPeso():
                    temp = array[j]
                    array[j] = array[j+1]
                    array[j+1] = temp

    def Boruvka(self):
        copiaNodos = copy(self.listaVertices)  # copia de los nodos
        copiaAristas = copy(self.listaAristas)  # copia de las aristas

        AristasBorukvka = []
        ListaConjuntos = []
        bandera = True
        cantidad = 0
        while (cantidad > 1 or bandera):
            for Nodo in copiaNodos:
                self.OperacionesconjuntosB(
                    Nodo, ListaConjuntos, AristasBorukvka, copiaAristas)
            bandera = False
            cantidad = self.Cantidadconjuntos(ListaConjuntos)

        for dato in AristasBorukvka:
            print("Origen: {0} destino: {1} peso: {2}".format(
                dato.getOrigen(), dato.getDestino(), dato.getPeso()))

    def Cantidadconjuntos(self, ListaConjuntos):
        cantidad = 0
        for conjunto in ListaConjuntos:
            if len(conjunto) > 0:
                cantidad = cantidad+1
        return cantidad

    def OperacionesconjuntosB(self, Nodo, ListaConjuntos, AristasBorukvka, copiaAristas):
        encontrado1 = -1
        encontrado2 = -1
        menor = self.Buscarmenor(Nodo, copiaAristas)

        if not menor == None:  # si no esta vacio
            if not ListaConjuntos:  # si esta vacia
                ListaConjuntos.append({menor.getOrigen(), menor.getDestino()})
                AristasBorukvka.append(menor)
            else:
                for i in range(len(ListaConjuntos)):
                    if (menor.getOrigen() in ListaConjuntos[i]) and (menor.getDestino() in ListaConjuntos[i]):
                        return False  # Camino cicliclo

                for i in range(len(ListaConjuntos)):
                    if menor.getOrigen() in ListaConjuntos[i]:
                        encontrado1 = i
                    if menor.getDestino() in ListaConjuntos[i]:
                        encontrado2 = i

                if encontrado1 != -1 and encontrado2 != -1:
                    if encontrado1 != encontrado2:  # si pertenecen a dos conjuntos diferentes
                        # debo unir los dos conjuntos
                        ListaConjuntos[encontrado1].update(
                            ListaConjuntos[encontrado2])
                        # elimino el conjunto
                        ListaConjuntos[encontrado2].clear()
                        AristasBorukvka.append(menor)

                if encontrado1 != -1 and encontrado2 == -1:  # si va unido por un conjunto
                    ListaConjuntos[encontrado1].update(menor.getOrigen())
                    ListaConjuntos[encontrado1].update(menor.getDestino())
                    AristasBorukvka.append(menor)

                if encontrado1 == -1 and encontrado2 != -1:  # si va unido por un conjunto
                    ListaConjuntos[encontrado2].update(menor.getOrigen())
                    ListaConjuntos[encontrado2].update(menor.getDestino())
                    AristasBorukvka.append(menor)

                if encontrado1 == -1 and encontrado2 == -1:  # si no existe en los conjuntos
                    ListaConjuntos.append(
                        {menor.getOrigen(), menor.getDestino()})
                    AristasBorukvka.append(menor)

    def Buscarmenor(self, Nodo, copiaAristas):
        temp = []
        for adyacencia in Nodo.getListaAdyacentes():
            for Arista in copiaAristas:
                # busco las aristas de esa lista de adyacencia
                if Arista.getOrigen() == Nodo.getDato() and Arista.getDestino() == adyacencia:
                    temp.append(Arista)
        if temp:  # si no esta vacia
            # una vez obtenga todas las aristas, saco la menor
            self.ordenamiento(temp)  # ordeno las aristas
            # elimin ese destino porque ya lo voy a visitar
            # print("{0}-{1}:{2}".format(temp[0].getOrigen(), temp[0].getDestino(), temp[0].getPeso()))

            Nodo.getListaAdyacentes().remove(temp[0].getDestino())
            return temp[0]  # es la menor

        return None  # es la menor

    def Prim(self):
        copiaAristas = copy(self.listaAristas)
        conjunto = []  # * Vertices que voy visitando
        aristasTemp = []  # * Posibles candidatos, aristas en amarillo
        aristasPrim = []  # * Aristas prim, aristas en verde (Finales)

        self.ordenamiento(copiaAristas)  # * Ordeno las aristas por peso
        menor = copiaAristas[0]
        # * si es dirigido, lo convierto a dirigido
        self.dirigido(copiaAristas)
        conjunto.append(menor.getOrigen())  # * vertice para empezar

        terminado = False
        while (not terminado):
            # * Empieza el algoritmo y termina cuando el conjunto de vertices visitados sea igual a la cantidad de vertices visitados
            self.algoritmo(copiaAristas, conjunto, aristasTemp, aristasPrim)
            if (len(self.listaVertices) == len(conjunto)):
                terminado = True

        # * Muestro las aristas finales de Prim
        lista = []
        for i in range(len(aristasPrim)):
            lista.append([aristasPrim[i].getOrigen(),
                         aristasPrim[i].getDestino()])
        print(lista)
        return lista

    def algoritmo(self, copiaAristas, conjunto, aristasTemp, aristasPrim):
        ciclo = False

        # * Se recorren los vertices visitados y se buscan las aristas temporales
        for vertice in conjunto:
            self.agregarAristasTemporales(copiaAristas, aristasTemp, vertice)
        # * se toma la arista temporal con menor peso
        candidata = self.candidataPrim(aristasTemp)

        if (candidata != None):
            # * Si hay un ciclo marcamos como True
            if (candidata.getOrigen() in conjunto and candidata.getDestino() in conjunto):
                ciclo = True

            # * Si no hay ciclo añado la arista a las aristas finales
            # * y verifico si sus vertices ya han sido visitados y sino lo(s) agrego al conjunto
            if (ciclo == False):
                aristasPrim.append(candidata)
                if (not candidata.getOrigen() in conjunto):
                    conjunto.append(candidata.getOrigen())
                if (not candidata.getDestino() in conjunto):
                    conjunto.append(candidata.getDestino())

    # * Devuelve la arista candidata con menor peso (La más conveniente)
    def candidataPrim(self, aristasTemp):
        if (len(aristasTemp) > 0):
            menor = aristasTemp[len(aristasTemp)-1]
            for arista in aristasTemp:
                if arista.getPeso() < menor.getPeso():
                    menor = arista

            aristasTemp.pop(aristasTemp.index(menor))
            return menor
        return None

    # * Agrega las aristas temporales a la lista de aristas temporales basandonos en el vertice actual
    def agregarAristasTemporales(self, copiaAristas, aristasTemp, vertice):
        # * Verifica y añade aristas temporales
        for arista in copiaAristas:
            if (arista.getOrigen() == vertice or arista.getDestino() == vertice):  # * verifica la adyacencia
                # * agrega a la lista de temporales, lista amarilla
                aristasTemp.append(arista)
                # * elimino la arista original
                copiaAristas.pop(copiaAristas.index(arista))

    # * Si no es dirigido, lo convierte
    def dirigido(self, copiaAristas):
        for elemento in copiaAristas:
            for i in range(len(copiaAristas)):
                if (elemento.getOrigen() == copiaAristas[i].getDestino() and elemento.getDestino() == copiaAristas[i].getOrigen()):
                    copiaAristas.pop(i)
                    break

    def rProfundidad(self, origen):
        if origen in self.visitadosCP:
            return
        else:
            vertice = self.obtenerOrigen(origen)
            if vertice != None:
                self.visitadosCP.append(origen)
                for i in vertice.getListaAdyacentes():
                    self.rProfundidad(i)

    def rAnchura(self, origen):
        cola = deque()
        ruta = []
        vertice = self.obtenerOrigen(origen)
        if vertice != None:
            cola.append(vertice)
            self.visitadosCA.append(origen)
            ruta.append(vertice)
            while cola:
                elemento = cola.popleft()
                ruta.append(elemento)
                for dato in elemento.listaAdyacentes:
                    if not dato in self.visitadosCA:
                        vertice = self.obtenerOrigen(dato)
                        cola.append(vertice)
                        self.visitadosCA.append(dato)

    def dijsktra(graph, initial, end):
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()

        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = graph.weights[(
                    current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {
                node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations,
                               key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path
