"""Application shell that runs a registered menu."""


class App:
    def __init__(self):
        self.menu = None

    def register_menu(self, menu):
        self.menu = menu

    def start(self):
        if self.menu is None:
            raise RuntimeError("No menu")
        self.menu.run()
