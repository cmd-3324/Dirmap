from collections import defaultdict
from pathlib import Path
from scanner import scan_directory

def duplicates_by_name(files) -> list[dict]:
    if not files:
        raise Exception("No File Found")
    groups = defaultdict(list) #create a dic where missing keys get empty values
    for f in files:
        if f["size_bytes"] > 0: 
            groups[f["name"]].append(f["path"])
    dupes = {name: paths for name, paths in groups.items() if len(paths) > 1}
    print(f"\n  Duplicate Files \t ")
    print("-" * 44)
    if not dupes:
        print("No Duplicate Files(by name)")
    else:
        for i, j in dupes.items():
            print(f"{i} \t {j}")

def duplicates_by_size(files) -> list[dict]:
    groups = defaultdict(list)
    for f in files:
        if f["size_bytes"] > 0: 
            groups[f["size_bytes"]].append(f["path"])
    dupes = {size: paths for size, paths in groups.items() if len(paths) > 1}
    print(f"\n  Duplicate Files \t ")
    print("-" * 44)
    if not dupes:
        print("No Duplicate Files(by size)")
    else:
        for i, j in dupes.items():
            print(f"{i} KiloBytes \t {j}")
