import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP-2025 Flights Manager"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_result = None
        self._btnCerca = None
        self._txtInTratteMax = None
        self._ddAeroportoD = None
        self._btnConnessi = None
        self._ddAeroportoP = None
        self._btnAnalizza = None
        self._txtInCMin = None

    def load_interface(self):
        # title
        self._title = ft.Text("Welcome to the TdP Flights Manager", color="blue", size=24)
        self._page.controls.append(self._title)

        # row 1
        self._txtInCMin = ft.TextField(label="Numero compagnie minime")
        self._btnAnalizza = ft.ElevatedButton(text="Analizza aeroporti", on_click=self._controller.handleAnalizza)

        row1 = ft.Row([ft.Container(None, width=250), ft.Container(self._txtInCMin, width=250), ft.Container(self._btnAnalizza, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        # row 2
        self._ddAeroportoP = ft.Dropdown(label="Aeroporto di partenza")
        self._btnConnessi = ft.ElevatedButton(text="Aeroporti connessi", on_click=self._controller.handleConnessi)

        row2 = ft.Row([ft.Container(None, width=250), ft.Container(self._ddAeroportoP, width=250), ft.Container(self._btnConnessi, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        # row 3
        self._ddAeroportoD = ft.Dropdown(label="Aeroporto di destinazione")
        self._txtInTratteMax = ft.TextField(label="Numero tratte massime")
        self._btnCerca = ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handleCerca)

        row3 = ft.Row([ft.Container(self._ddAeroportoD, width=250), ft.Container(self._txtInTratteMax, width=250), ft.Container(self._btnCerca, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        self._page.add(row1, row2, row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
