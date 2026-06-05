

## DIRMAP - Directory Analyzer

A **Python-based command-line tool** that scans, analyzes, and reports on directory structures and file metadata. It provides insights into file systems without requiring external dependencies.

### Core Capabilities:

| Feature | Description |
|---------|-------------|
| **File Scanning** | Recursively traverses directories collecting file metadata (name, size, type, modified date) |
| **File Analysis** | Counts by type, identifies largest files, calculates total size by extension, and shows oldest/newest files |
| **Duplicate Detection** | Finds duplicate files by both name and file size |
| **Empty Folder Detection** | Identifies empty directories in the scanned hierarchy |
| **Tree Visualization** | Displays folder structure as an ASCII tree diagram |
| **Data Export** | Exports scan results to both CSV and JSON formats |
| **Interactive Menu** | Box-drawing character interface for user interaction |

### Key Files:

- `scanner.py` - Core scanning engine
- `analyzer.py` - Statistical analysis functions
- `duplicates.py` - Duplicate file detection
- `exporter.py` - CSV/JSON export functionality
- `treeview.py` - ASCII tree generator
- `main.py` - Menu system and application entry point

### Primary Use Case:
System administrators, developers, or users who need to quickly understand disk usage patterns, find duplicate files, or audit directory structures from the command line without installing heavy GUI tools.
