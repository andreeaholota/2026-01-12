import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._sceltaAnno1 = None
        self._sceltaAnno2 = None

    def fillDDYears(self):
        for year in self._model.getYears():
            self._view._ddAnno1.options.append(ft.dropdown.Option(data=year, text=str(year), on_click = self._pickAnno1))
            self._view._ddAnno2.options.append(ft.dropdown.Option(data=year, text=str(year), on_click = self._pickAnno2))
        self._view.update_page()

    def _pickAnno1(self, e):
        self._sceltaAnno1 = e.control.data

    def _pickAnno2(self, e):
        self._sceltaAnno2 = e.control.data


    def handleCreaGrafo(self, e):
        if self._sceltaAnno1 is None or self._sceltaAnno2 is None:
            self._view.create_alert("Inserisci entrambi gli anni")
            return

        if self._sceltaAnno1 > self._sceltaAnno2:
            self._view.create_alert("Anno Da deve essere minore di Anno A")

        try:
            self._model.creaGrafo(self._sceltaAnno1, self._sceltaAnno2)
        except Exception as e:
            self._view.create_alert(f"Errore: {e}")

        nodi = self._model.getNumNodi()
        archi = self._model.getNumArchi()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {archi}"))

        self._view.update_page()

    def handleDettagli(self, e):
        if self._model.getAllNodi() == []:
            self._view.create_allert("Crea prima il grafo")
            return

        try:
            top_archi = self._model.getArchiPesoMaggiore(3)
            self._view.txt_result.controls.append(ft.Text("Top 3 archi:"))
            for n1, n2, dati in top_archi:
                self._view.txt_result.controls.append(
                    ft.Text(f"{n1} - {n2}: peso {dati['weight']}"))

            n_comp = self._model.getNumComponenti()
            self._view.txt_result.controls.append(ft.Text(f"Numero componenti connesse: {n_comp}"))

            componente, con_grado = self._model.getComponentePiuGrandeOrdinataPerGrado()
            self._view.txt_result.controls.append(
                ft.Text(f"Componente connessa più grande: {len(componente)} nodi"))
            for nodo, grado in con_grado:
                self._view.txt_result.controls.append(
                    ft.Text(f"{nodo} (grado {grado})"))

        except Exception as ex:
            self._view.create_alert(f"Errore: {ex}")

        self._view.update_page()







    def handleCerca(self, e):
        pass

