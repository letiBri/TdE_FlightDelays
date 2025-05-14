import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a  # associo l'aeroporto all'id

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
                    self._graph[e.aeroportoP][e.aeroportoD]["weight"] += e.peso
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
            neighbTuples.append((n,  self._graph[node][n]["weight"]))  # prendo il peso sull'arco da node a n
        neighbTuples.sort(key=lambda x: x[1], reverse=True)  # sorto utilizzando come chiave i pesi della tupla
        return neighbTuples

    def getPath(self, v0, v1):
        path = nx.dijkstra_path(self._graph, v0, v1, weight=None)

        # path = nx.shortest_path(self._graph, v0, v1)
        #
        # mydict = dict(nx.bfs_predecessors(self._graph, v0))  # iteratore su tutti gli archi predessori di v0
        # path = [v1]
        # while path[0] != v0:
        #     path.insert(0, mydict[path[0]])

        return path
