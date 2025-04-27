# run.py
import sys
import argparse

def run_ui():
    # If you run “python run.py” without --cli, we want Streamlit
    import streamlit as st
    from run_ui import main as ui_main
    ui_main()

def run_cli(directory):
    # Delegate to processing.main_cli
    import processing
    processing.main_cli(directory)

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
        # e.g. python run.py --cli D:\Final_Capstone\MyPdfs
        run_cli(args.cli)
    else:
        # e.g. python run.py
        run_ui()

if __name__ == "__main__":
    main()
