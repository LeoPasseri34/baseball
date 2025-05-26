import copy
import itertools
import random
import warnings

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allTeams = []
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0

    def getBestPathV2(self, start):
        self._bestPath = []
        self._bestScore = 0

        parziale = [start]

        vicini = self._graph.neighbors(start)

        viciniTuples = [(v, self._graph[start][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        #for v in vicini:
        parziale.append(viciniTuples[0][0])
        self._ricorsioneV2(parziale)
        #parziale.pop()
        return self.getWeightOfPath(self._bestPath), self._bestScore

    def _ricorsioneV2(self, parziale):
        # 1) verifico che parziale sia una soluzione
            # e verifico che sia migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)
        # 2) verifico se poso aggiungere un nodo
        # 3) aggiungo nodo e faccio ricorsione

        vicini = self._graph.neighbors(parziale[-1])

        viciniTuples = [(v, self._graph[parziale[-1]][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        for t in viciniTuples:
            if (t[0] not in parziale and
                    self._graph[parziale[-2]][parziale[-1]]["weight"] > t[1]):
                parziale.append(t[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return

    def getWeightOfPath(self, path):
        pathTuple = [(path[0], 0)]
        for i in range(1, len(path)):
            pathTuple.append((path[i], self._graph[path[i-1]][path[i]]["weight"]))
        return pathTuple



    def getBestPath(self, start):
        self._bestPath = []
        self._bestScore = 0

        parziale = [start]

        vicini = self._graph.neighbors(start)
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        print(len(parziale))
        # 1) verifico che parziale sia una soluzione
            # e verifico che sia migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)
        # 2) verifico se poso aggiungere un nodo
        # 3) aggiungo nodo e faccio ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            if (v not in parziale and
                    self._graph[parziale[-2]][parziale[-1]]["weight"] >
                    self._graph[parziale[-1]][v]["weight"]):
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()


    def score(self, listOfnodes):
        if len(listOfnodes) < 2:
            warnings.warn("Errore in score, attesa lista lunga almeno 2")

        totPeso = 0
        for i in range(len(listOfnodes)-1):
            totPeso += self._graph[listOfnodes[i]][listOfnodes[i+1]]["weight"]
        return totPeso


    def buildGraph(self, year):
        self._graph.clear()

        if len(self._allTeams) == 0:
            print("No teams selected")
            return
        self._graph.add_nodes_from(self._allTeams)

        #for n1 in self._graph.nodes:
           # for n2 in self._graph.nodes:
               # if n1 != n2:
                   # self._graph.add_edge(n1, n2)

        myedges = list(itertools.combinations(self._allTeams, 2))
        self._graph.add_edges_from(myedges)

        salariesOfTeams = DAO.getSalaryofTeams(year, self._idMap)

        for e in self._graph.edges:
            self._graph[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]



    def getNeighborsSorted(self, source):
        vicini = nx.neighbors(self._graph, source) # [v0, v1, v2, ...]

        #vicini = self._graph.neighbors(source)
        viciniTuple = []

        for v in vicini:
            viciniTuple.append((v, self._graph[source][v]["weight"])) # [ (v0, p0) (v1,p1) () ]

        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple


    def printGraphDetails(self):
        print(f"Grafo creato correttamente")
        print(f"Grafo creato con {len(self._graph.nodes)} nodi e {len(self._graph.edges)} archi")

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._allTeams = DAO.getTeamsOfYear(year)
        self._idMap = {}
        for team in self._allTeams:
            self._idMap[team.ID] = team
        return self._allTeams

    def getRandomNode(self):
        index = random.randint(0, self._graph.number_of_nodes()-1)
        return list(self._graph.nodes)[index]