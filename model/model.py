import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def getYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, yearDa, yearA):
        self._graph.clear()
        self._idMap.clear()

        nodi = DAO.getAllConstructors(yearDa, yearA)

        for n in nodi:
            self._idMap[n.constructorId] = n

        self._graph.add_nodes_from(nodi)

        for id1, id2, weight in DAO.getConstructionsDriversPairs(yearDa, yearA):
            self._graph.add_edge(self._idMap[id1], self._idMap[id2], weight=weight)

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()

    def getAllNodi(self):
        return list(self._graph.nodes())

    def getArchiPesoMaggiore(self, n):
        edges = list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]["weight"], reverse=True)
        return edges[:n]

    def getNumComponenti(self):
        return len(list(nx.connected_components(self._graph)))

    def getComponentePiuGrandeOrdinataPerGrado(self):
        comp = list(nx.connected_components(self._graph))
        big = max(comp, key=len)
        con_grado = [(n, self._graph.degree(n)) for n in big]
        return big, sorted(con_grado, key=lambda x: x[1], reverse=True)

