import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a  # associo l'aeroporto all'id
        self._bestPath = []
        self._bestObjFun = 0

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        # self.addAllArchiV1()
        # print("Modo 1: Numero nodi:", len(self._graph.nodes), " Numero archi:", len(self._graph.edges))
        # self._graph.clear_edges()
        self.addAllArchiV2()
        # print("Modo 2: Numero nodi:", len(self._graph.nodes), " Numero archi:", len(self._graph.edges))

    def addAllArchiV1(self):
        allEdges = DAO.getAllEdgesV1(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:  # controllo che i nodi siano nel grafo
                if self._graph.has_edge(e.aeroportoP, e.aeroportoD):  # controllo se esiste già l'arco
                    self._graph[e.aeroportoP][e.aeroportoD]["weight"] += e.peso  # aumento il peso se l'arco esiste già
                else:
                    self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)

    def addAllArchiV2(self):
        allEdges = DAO.getAllEdgesV2(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

    def getSortedNeighbors(self, node):
        neighbors = self._graph.neighbors(node)  # self._graph[node] prendo tutti i vicini
        neighbTuples = []
        for n in neighbors:
            neighbTuples.append((n,  self._graph[node][n]["weight"]))  # con il secondo elemento della tupla, prendo il peso sull'arco da node a n
        neighbTuples.sort(key=lambda x: x[1], reverse=True)  # sorto utilizzando come chiave i pesi della tupla
        return neighbTuples

    def getPath(self, v0, v1):
        path = nx.dijkstra_path(self._graph, v0, v1, weight=None)

        # path = nx.shortest_path(self._graph, v0, v1)
        #
        # mydict = dict(nx.bfs_predecessors(self._graph, v0))  # iteratore su tutti gli archi predecessori di v0
        # path = [v1]
        # while path[0] != v0:
        #     path.insert(0, mydict[path[0]])

        return path

    # per il punto 2
    def getCamminoOttimo(self, v0, v1, t):  # aeroportoP, aeroportoD e numero massimo di tratte t
        self._bestPath = []
        self._bestObjFun = 0
        parziale = [v0]  # il pirmo nodo del percorso è quello dato dall'utente
        self._ricorsione(parziale, v1, t)
        return self._bestPath, self._bestObjFun

    def _ricorsione(self, parziale, v1, t):  # ci servono v1 e t per capire se siamo arrivati alla fine o no
        # verificare se parziale è una possibile soluzione
            # verificare se parziale è meglio del best corrente
            # esco
        if parziale[-1] == v1:
            if self.getObjFun(parziale) > self._bestObjFun:  # controllo lo score
                self._bestObjFun = self.getObjFun(parziale)
                self._bestPath = copy.deepcopy(parziale)
        if len(parziale) == t+1:  # ho superato il numero massimo di tratte
            return
        # posso ancora aggiungere nodi
            # prendo i vicini e aggiungo un nodo alla volta
            # ricorsione
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale: # nodo non ancora visitato
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()

    def getObjFun(self, listOfNodes):
        objval = 0
        for i in range(0, len(listOfNodes) - 1):
            objval += self._graph[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return objval
