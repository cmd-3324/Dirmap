#fffffffffffffffffffffffff

import sys
import os
import platform
from abc import ABC, abstractmethod
from typing import Callable
from dataclasses import dataclass, field
from scanner import scan_directory
from analyzer import count_by_type, largest_files, size_by_type, oldest_newest, empty_folders
from duplicates import duplicates_by_name, duplicates_by_size
from exporter import export_csv, export_json
from treeview import print_tree
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
    def render():
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
                print("Invlaid")
                input("Press Enter .. ") 
class BoxMenu(Menu):
    WIDTH = 44
    def _line(self, char="═", corners=("╔","╗","╝","╚")):
            return f"{corners[0]}{char * self.WIDTH}{corners[1]}" # does not print str alone - interactive func
    
    def render(self):
        print(self._line())
        print(f"║{self.title.center(self.WIDTH)}║")
        print(self._line("═", ("╠","╣","╝","╚")))
        for item in self.items:
            print(f"║  {item.key}. {item.label:<{self.WIDTH-5}}║")
        print(self._line("═", ("╚","╝","╝","╚")))
class App:
    def __init__(self):
        self.menu = None
    def register_menu(self, menu):
        self.menu = menu
    def start(self):
        if self.menu is None:
            raise RuntimeError("No menu")
        self.menu.run()
def action_scan():
    path = input("  Folder path: ").strip()
    if not path:
        path = "."
    files = scan_directory(path)
    print(f"\n  Found {len(files)} files.")
    
    input("\n  Press Enter to continue...")
    
def action_analyze():
    path = input(" FOlder Path: ").strip() or "."
    files = scan_directory(path)
    count_by_type(files)
    largest_files(files, 5)
    size_by_type(files)
    oldest_newest(files)
    empty_folders(path)
    input("\n Press Enter ...")
    
def action_duplicates():
    path = input("  Folder path: ").strip() or "."
    files = scan_directory(path)
    duplicates_by_name(files)
    duplicates_by_size(files)
    input("\n  Press Enter...")  
def action_export():
    path = input("  Folder path: ").strip() or "."
    files = scan_directory(path)
    export_csv(files)
    export_json(files)
    input("\n  Press Enter...")

def action_exit():
    print("\n  Done.\n")
    sys.exit(0)



def action_empty():
    path = input("  Folder path: ").strip()
    if not path:
        path = "."
    empty_folders(path)
    
def action_tree():
    path = input("  Folder path: ").strip() or "."
    depth = input("  Max depth (default 3): ").strip()
    depth = int(depth) if depth.isdigit() else 3
    
    print(f"\n  {path}")
    print_tree(path, max_depth=depth)
    input("\n  Press Enter...")
# ---- Main ----
def main():
    menu = BoxMenu("DIRMAP - Directory Analyzer")
    menu.add_item("1", "Scan Folder", action_scan)
    menu.add_item("2", "Analyze Files", action_analyze)
    menu.add_item("3", "Find Duplicates", action_duplicates)
    menu.add_item("4", "Export Report", action_export)
    menu.add_item("5", "Show Tree", action_tree)
    menu.add_item("6", "Exit", action_exit)
    
    app = App()
    app.register_menu(menu)
    app.start()
if __name__ == "__main__":
    main()
