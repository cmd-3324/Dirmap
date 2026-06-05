
from pathlib import Path
from datetime import datetime

def scan_directory(folder_path) -> list[dict]:
    results = []
    for file in Path(folder_path).rglob("*"):
        if file.is_file():
            results.append({
                "path": str(file),
                "name": file.name,
                "suffix": file.suffix,
                "size_bytes": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime)
            })
    by_size = lambda f: f["size_bytes"]
    return sorted(results, key=by_size, reverse=True)

def iter_files(folder_path):
    for files in Path(folder_path).rglob("*"):
        if files.is_file():
            yield{ "path": str(files),
                "name": files.name,
                "suffix": files.suffix.lower(),
                "size_bytes": files.stat().st_size,
                "modified": datetime.fromtimestamp(files.stat().st_mtime)}
            
