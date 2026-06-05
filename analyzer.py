from collections import Counter
from pathlib import Path
from scanner import scan_directory


def count_by_type(files):
    s = Counter(f["suffix"] for f in files)
    
    print("\n  FILE COUNT BY TYPE")
    print("─" * 35)
    for ext, count in s.most_common():
        print(f"  {ext:12} {count:>4} files")


def largest_files(files, n=10):
    by_size = lambda f: f["size_bytes"]
    sorted_files = sorted(files, key=by_size, reverse=True)
    
    print(f"\n  TOP {n} LARGEST FILES")
    print("─" * 55)
    print(f"  {'#':<4} {'Name':<30} {'Size':>10}")
    print("  " + "─" * 48)
    
    for i, f in enumerate(sorted_files[:n], 1):
        size_kb = f["size_bytes"] / 1024
        if size_kb > 1024:
            size_str = f"{size_kb/1024:.1f} MB"
        else:
            size_str = f"{size_kb:.1f} KB"
        print(f"  {i:<4} {f['name']:<30} {size_str:>10}")


def size_by_type(files):
    totals = {}
    for f in files:
        ext = f["suffix"]
        totals[ext] = totals.get(ext, 0) + f["size_bytes"]
    
    print("\n  TOTAL SIZE BY TYPE")
    print("─" * 45)
    print(f"  {'Extension':<12} {'Size':>10}")
    print("  " + "─" * 28)
    
    by_size = lambda x: x[1]
    for ext, size in sorted(totals.items(), key=by_size, reverse=True):
        size_mb = size / (1024 * 1024)
        if size_mb < 1:
            size_str = f"{size/1024:.1f} KB"
        else:
            size_str = f"{size_mb:.1f} MB"
        print(f"  {ext:<12} {size_str:>10}")


def oldest_newest(files):
    if not files:
        return
    
    oldest = min(files, key=lambda f: f["modified"])
    newest = max(files, key=lambda f: f["modified"])
    
    print("\n  FILE AGE RANGE")
    print("─" * 55)
    print(f"  Oldest : {oldest['name']:<30} {oldest['modified']}")
    print(f"  Newest : {newest['name']:<30} {newest['modified']}")


def empty_folders(folder_path):
    base = Path(folder_path)
    empties = [d for d in base.rglob("*") if d.is_dir() and not any(d.iterdir())]
    
    if empties:
        print(f"\n  EMPTY FOLDERS ({len(empties)})")
        print("─" * 60)
        for d in empties:
            print(f"  {d.name:<30} {str(d)}")
    else:
        print("\n  No empty folders found.")
    
    return empties