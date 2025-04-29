#!/usr/bin/env python3
import argparse
import src.config   # ← this will read .env and set OPENAI_API_KEY 

def run_ui():
    # call the UI entrypoint
    from run_ui import main as ui_main
    ui_main()

def run_cli(directory):
    # call your CLI pipeline
    from src.processing import main_cli
    main_cli(directory)

def main():
    parser = argparse.ArgumentParser(
        description="RAG PDF processor: UI (default) or CLI."
    )
    parser.add_argument(
        "--cli", "-c",
        metavar="PDF_DIR",
        help="Run in pure-Python mode on a directory of PDFs."
    )
    args = parser.parse_args()

    if args.cli:
        run_cli(args.cli)
    else:
        run_ui()

if __name__ == "__main__":
    main()
