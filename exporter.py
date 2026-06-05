
import json
import csv 
from scanner import scan_directory
def export_csv(files, filename="results.csv"):
    fieldnames = ["name", "suffix", "size_bytes", "path", "modified"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(files)
        print(f"Saved Files to {filename} - saved {len(files)} rows to {filename}")
        
        
def export_json(files, filename="result.json"):
    clean = [{**f, "modified": str(f["modified"])} for f in files]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)
    print(f"Saved to {filename}")
    
