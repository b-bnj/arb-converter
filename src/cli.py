import argparse
import os
import glob
import sys
from src.file_io import load_json, save_json, write_csv, read_csv, ensure_dir
from src.parser import extract_translations, merge_translations

WORKSPACE_ARB = "workspace/arbs_in"
WORKSPACE_CSV = "workspace/csvs_out"
WORKSPACE_MERGED = "workspace/arbs_out"

def setup_workspace() -> None:
    ensure_dir(WORKSPACE_ARB)
    ensure_dir(WORKSPACE_CSV)
    ensure_dir(WORKSPACE_MERGED)

def list_files(file_type: str, directory: str) -> None:
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    files = glob.glob(os.path.join(directory, f"*.{file_type}"))
    print(f"\nFound {len(files)} .{file_type} file(s) in '{directory}':")
    for f in files:
        print(f"  - {os.path.basename(f)}")
    print("")

def run_extract(input_path: str, output_dir: str) -> None:
    ensure_dir(output_dir)
    arb_files = []
    
    if os.path.isfile(input_path):
        if input_path.endswith('.arb'):
            arb_files.append(input_path)
        else:
            print(f"Error: '{input_path}' is not an .arb file.")
            return
    elif os.path.isdir(input_path):
        arb_files = glob.glob(os.path.join(input_path, "*.arb"))
    else:
        print(f"Error: Path '{input_path}' does not exist.")
        return

    if not arb_files:
        print(f"No .arb files found in '{input_path}'.")
        return

    for arb_path in arb_files:
        filename = os.path.basename(arb_path)
        csv_filename = filename.replace(".arb", ".csv")
        csv_path = os.path.join(output_dir, csv_filename)
        
        print(f"Processing: {filename}...")
        arb_data = load_json(arb_path)
        translations, metadata = extract_translations(arb_data)
        
        write_csv(csv_path, ["Key", "Source Text", "Translation"], translations)
        print(f"  -> Extracted {len(translations)} keys to {csv_path}")

def run_merge(input_path: str, base_path: str, output_dir: str) -> None:
    ensure_dir(output_dir)
    csv_files = []
    
    if os.path.isfile(input_path):
        if input_path.endswith('.csv'):
            csv_files.append(input_path)
        else:
            print(f"Error: '{input_path}' is not a .csv file.")
            return
    elif os.path.isdir(input_path):
        csv_files = glob.glob(os.path.join(input_path, "*.csv"))
    else:
        print(f"Error: Path '{input_path}' does not exist.")
        return

    if not csv_files:
        print(f"No .csv files found in '{input_path}'.")
        return

    for csv_path in csv_files:
        filename = os.path.basename(csv_path)
        arb_filename = filename.replace(".csv", ".arb")
        output_arb_path = os.path.join(output_dir, arb_filename)
        
        if os.path.isfile(base_path):
            base_arb_path = base_path
        else:
            base_arb_path = os.path.join(base_path, arb_filename)
        
        print(f"Merging: {filename}...")
        
        if not os.path.exists(base_arb_path):
            print(f"  -> Warning: Base ARB '{base_arb_path}' not found. Skipping.")
            continue
            
        csv_rows, _ = read_csv(csv_path)
        base_data = load_json(base_arb_path)
        _, metadata = extract_translations(base_data)
        
        merged_data = merge_translations(csv_rows, metadata)
        save_json(output_arb_path, merged_data)
        print(f"  -> Created {arb_filename} in {output_dir}")

def handle_interactive() -> None:
    setup_workspace()
    
    while True:
        print("\n--- ARB Converter Menu ---")
        print("1. Extract Workspace ARBs to CSVs")
        print("2. Merge Workspace CSVs to ARBs")
        print("3. Extract a Custom File or Directory")
        print("4. Merge a Custom File or Directory")
        print("5. List Workspace Files")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            run_extract(WORKSPACE_ARB, WORKSPACE_CSV)
        elif choice == '2':
            run_merge(WORKSPACE_CSV, WORKSPACE_ARB, WORKSPACE_MERGED)
        elif choice == '3':
            custom_in = input("Enter path to the .arb file or directory: ").strip()
            custom_out = input(f"Enter output directory (default: {WORKSPACE_CSV}): ").strip() or WORKSPACE_CSV
            run_extract(custom_in, custom_out)
        elif choice == '4':
            custom_in = input("Enter path to the .csv file or directory: ").strip()
            custom_base = input(f"Enter path to the base .arb file or directory (default: {WORKSPACE_ARB}): ").strip() or WORKSPACE_ARB
            custom_out = input(f"Enter output directory (default: {WORKSPACE_MERGED}): ").strip() or WORKSPACE_MERGED
            run_merge(custom_in, custom_base, custom_out)
        elif choice == '5':
            handle_list_menu()
        elif choice == '6':
            sys.exit(0)
        else:
            print("Invalid choice.")

def handle_list_menu() -> None:
    print("\n1. Workspace .arb files")
    print("2. Workspace .csv files")
    list_choice = input("Select file type (1-2): ").strip()
    
    if list_choice == '1':
        list_files("arb", WORKSPACE_ARB)
    elif list_choice == '2':
        list_files("csv", WORKSPACE_CSV)
    else:
        print("Invalid choice.")

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ARB and CSV Converter")
    parser.add_argument("-l", "--list", choices=['arb', 'csv'], help="List files of a specific type in the workspace")
    parser.add_argument("-s", "--select", help="Run extraction on a custom file or directory path")
    
    subparsers = parser.add_subparsers(dest="command")
    
    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("-d", "--dir", default=WORKSPACE_ARB, help="Input file or directory")
    extract_parser.add_argument("-o", "--out", default=WORKSPACE_CSV, help="Output directory")
    
    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("-d", "--dir", default=WORKSPACE_CSV, help="Input file or directory")
    merge_parser.add_argument("-b", "--base", default=WORKSPACE_ARB, help="Base ARB file or directory")
    merge_parser.add_argument("-o", "--out", default=WORKSPACE_MERGED, help="Output directory")
    
    return parser