import networkx as nx
from database.DAO import DAO
import copy

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

    def getSelezioneScartoMinimo(self, k):
        mappa = self._assegnaComponenti()
        isole_distinte = set(mappa.values())
        if len(isole_distinte) < k:
            return None, None, None, None

        tutti = []
        for v in self._graph.nodes():
            if v.oldest_driver_dob is not None:
                tutti.append(v)

        self._migliorScarto = None
        self._migliorSelezione = []
        self._ricorsioneScarto([], set(), tutti, mappa, k)

        veterano_giovane, veterano_anziano = self._trovaEstremi(self._migliorSelezione)
        return self._migliorSelezione, self._migliorScarto, veterano_giovane, veterano_anziano

    def _assegnaComponenti(self):
        comp = list(nx.connected_components(self._graph))
        mappa = {}
        for indice_isola, componente in enumerate(comp):
            for nodo in componente:
                mappa[nodo] = indice_isola
        return mappa

    def _trovaEstremi(self, selezione):
        veterano_anziano = None  # dob PIÙ PICCOLA = pilota più vecchio
        veterano_giovane = None  # dob PIÙ GRANDE = pilota più giovane
        for costruttore in selezione:
            if veterano_anziano is None or costruttore.oldest_driver_dob < veterano_anziano.oldest_driver_dob:
                veterano_anziano = costruttore
            if veterano_giovane is None or costruttore.oldest_driver_dob > veterano_giovane.oldest_driver_dob:
                veterano_giovane = costruttore
        return veterano_giovane, veterano_anziano

    def _ricorsioneScarto(self, parziale, componenti_usate, tutti, mappa, k):
        if len(parziale) == k:
            veterano_giovane, veterano_anziano = self._trovaEstremi(parziale)
            scarto = (veterano_giovane.oldest_driver_dob - veterano_anziano.oldest_driver_dob).days
            if self._migliorScarto is None or scarto < self._migliorScarto:
                self._migliorScarto = scarto
                self._migliorSelezione = copy.deepcopy(parziale)
            return
        for candidato in tutti:
            isola = mappa[candidato]
            if candidato not in parziale and isola not in componenti_usate:
                parziale.append(candidato)
                componenti_usate.add(isola)
                self._ricorsioneScarto(parziale, componenti_usate, tutti, mappa, k)
                componenti_usate.remove(isola)
                parziale.pop()




