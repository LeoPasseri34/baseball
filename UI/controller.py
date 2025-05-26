import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        year = self._view._ddAnno.value
        if year is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione selezionare anno.", color='red'))
            self._view.update_page()

            return

        self._model.buildGraph(int(year))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view._txt_result.controls.append(ft.Text(f"Numero vertici: {nNodes}, Numero archi: {nEdges}"))
        self._view.update_page()

    def handleDettagli(self, e):
        if self._selectedTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un team", color='red'))
            self._view.update_page()
            return

        # [ (v0, p0) (v1,p1) () ]
        viciniSorted = self._model.getNeighborsSorted(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il vicinato conta {len(viciniSorted)} squadre"))
        for v in viciniSorted:
            self._view._txt_result.controls.append(
                ft.Text(f"{v[0]} -- peso: {v[1]}"))
        self._view.update_page()


    def handlePercorso(self, e):
        if self._selectedTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un team", color='red'))
            self._view.update_page()
            return

        path, score = self._model.getBestPathV2(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Trovato un cammino che parte da {self._selectedTeam} con somma dei pesi uguale a {score}."))
        for v in path:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]}"))
        self._view.update_page()

    def handleDDYearSelection(self, e):
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(teams)} squadre che hanno giocato nel {self._view._ddAnno.value}"))

        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data = t, text=t.teamCode, on_click=self.readDDTeams))

        self._view.update_page()


    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f"readDDTeams called: {self._selectedTeam}")

    def fillDDYear(self):
        years = self._model.getYears()
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = yearsDD
        self._view.update_page()
        #yearsDD = []
        #for year in years:
            #yearsDD.append(ft.dropdown.Option(year))