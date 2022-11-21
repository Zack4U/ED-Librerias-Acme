from Arista import *
from Vertice import *
from copy import *


class Grafo:
    def __init__(self):
        self.listaVertices = []
        self.listaAristas = []
        self.visitadosCP = []
        self.visitadosCA = []
        self.adyacencias = {}
        self.vistadosCKruskal = []
        self.repetidos = 0

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
                self.obtenerOrigen(origen).listaAdyacentes.append(destino)
                self.obtenerOrigen(destino).listaAdyacentes.append(origen)

    def obtenerOrigen(self, origen):
        for i in range(len(self.listaVertices)):
            if origen == self.listaVertices[i].getDato():
                return self.listaVertices[i]

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