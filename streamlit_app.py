#!/usr/bin/env python3
import src.config    # load .env → os.environ
import os
import io
import pandas as pd
import streamlit as st
import tempfile
import shutil
import zipfile

from src.processing import (
    cleanup_generated_files,
    load_and_split_pdfs_from_directory,
    create_vectorstore,
    process_all_dictionary_questions,
)
from src.libraries import ChatOpenAI

def main():
    # --- Auth & API Key ---
    password = st.text_input("Enter password", type="password")
    if password != "Jm@xBond":
        st.stop()

    api_key = st.text_input("Enter the API Key here:")
    os.environ["OPENAI_API_KEY"] = api_key

    st.title("Batch PDF Analysis with RAG Workflows")

    # --- Input Mode Selector ---
    input_mode = st.radio(
        "Select input mode:",
        ("Directory", "Upload PDF", "ZIP Archive File")
    )

    directory = None
    _temp_dirs = []

    # --- Input Modes ---
    if input_mode == "Directory":
        directory = st.text_input("Enter parent directory with PDF subfolders:")
    elif input_mode == "Upload PDF":
        uploaded_pdf = st.file_uploader("Upload a single PDF file", type="pdf")
        if uploaded_pdf:
            tmp = tempfile.mkdtemp()
            _temp_dirs.append(tmp)
            pdf_path = os.path.join(tmp, uploaded_pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            directory = tmp
    elif input_mode == "ZIP Archive File":
        zip_file = st.file_uploader("Upload a ZIP archive:", type=["zip"])
        if zip_file:
            tmp = tempfile.mkdtemp()
            _temp_dirs.append(tmp)
            try:
                # Read uploaded bytes into memory, then extract
                zip_bytes = zip_file.read()
                with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
                    zf.extractall(tmp)
                directory = tmp
            except zipfile.BadZipFile:
                st.error("That doesn’t look like a valid ZIP file.")

    # --- Run Analysis ---
    if st.button("Run Analysis"):
        if not directory or not os.path.isdir(directory):
            st.warning("Please provide a valid directory, PDF upload, or ZIP path.")
            return

        llm = ChatOpenAI(model="gpt-4o-2024-05-13")

        # find every PDF-containing folder
        pdf_dirs = [
            root
            for root, _, files in os.walk(directory)
            if any(f.lower().endswith(".pdf") for f in files)
        ]

        if not pdf_dirs:
            st.error("No PDFs found under that path.")
        else:
            for sub in pdf_dirs:
                st.write(f"## Processing: {os.path.relpath(sub, directory)}")
                cleanup_generated_files(sub)

                splits = load_and_split_pdfs_from_directory(sub)
                if not splits:
                    st.error(f"No PDFs loaded from {sub}, skipping.")
                    continue

                vs = create_vectorstore(splits)
                df = process_all_dictionary_questions(sub, vs, llm)
                if df.empty:
                    st.error(f"No data extracted for {os.path.basename(sub)}.")
                    continue

                # --- Generate Excel in memory ---
                buffer = io.BytesIO()
                sheet_name = os.path.basename(sub)[:31]  # Excel limit
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
                buffer.seek(0)

                # --- Download button ---
                st.download_button(
                    label=f"Download {sheet_name}.xlsx",
                    data=buffer.getvalue(),
                    file_name=f"{sheet_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # clean up temp folders
            for td in _temp_dirs:
                shutil.rmtree(td, ignore_errors=True)

if __name__ == "__main__":
    main()
