import sys
from src.cli import setup_parser, handle_interactive, run_extract, run_merge, list_files, setup_workspace, WORKSPACE_ARB, WORKSPACE_CSV

def main():
    setup_workspace()
    
    if len(sys.argv) == 1:
        handle_interactive()
    else:
        parser = setup_parser()
        args = parser.parse_args()

        try:
            if args.list == 'arb':
                list_files("arb", WORKSPACE_ARB)
            elif args.list == 'csv':
                list_files("csv", WORKSPACE_CSV)
            elif args.select:
                run_extract(args.select, WORKSPACE_CSV)
            elif args.command == "extract":
                run_extract(args.dir, args.out)
            elif args.command == "merge":
                run_merge(args.dir, args.base, args.out)
                
        except Exception as e:
            print(f"Process failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()