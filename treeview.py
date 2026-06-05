
from pathlib import Path

def print_tree(folder_path: str, prefix: str = "", max_depth: int = 3):
    """Print folder tree structure."""
    base = Path(folder_path)
    
    if max_depth == 0:
        return
    
    items = sorted(base.iterdir(), key=lambda p: (p.is_file(), p.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item.name}")
        
        if item.is_dir() and max_depth > 1:
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension, max_depth - 1)