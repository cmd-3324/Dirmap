"""Interactive menu framework (box-drawing CLI)."""

import os
import platform
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class MenuItem:
    key: str
    label: str
    action: Callable
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)


class Menu(ABC):
    def __init__(self, title):
        self.title = title
        self.items = []
        self.running = True

    def add_item(self, key, label, action, *args, **kwargs):
        self.items.append(MenuItem(key, label, action, args, kwargs))

    @staticmethod
    def clear_screen():
        os.system("cls" if platform.system() == "Windows" else "clear")

    @abstractmethod
    def render(self):
        pass

    def handle_choice(self, choice):
        for item in self.items:
            if choice.lower() == item.key.lower():
                item.action(*item.args, **item.kwargs)
                return True
        return False

    def run(self):
        while self.running:
            self.clear_screen()
            self.render()
            choice = input("\n  Choice: ").strip()
            if not self.handle_choice(choice):
                print("Invalid")
                input("Press Enter .. ")


class BoxMenu(Menu):
    WIDTH = 44

    def _line(self, char="═", corners=("╔", "╗", "╝", "╚")):
        return f"{corners[0]}{char * self.WIDTH}{corners[1]}"  # does not print str alone - interactive func

    def render(self):
        print(self._line())
        print(f"║{self.title.center(self.WIDTH)}║")
        print(self._line("═", ("╠", "╣", "╝", "╚")))
        for item in self.items:
            print(f"║  {item.key}. {item.label:<{self.WIDTH-5}}║")
        print(self._line("═", ("╚", "╝", "╝", "╚")))
