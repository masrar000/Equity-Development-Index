#!/usr/bin/env python3
import src.config    # load .env → os.environ
import os
import io
import pandas as pd
import streamlit as st
import tempfile
import shutil
import zipfile
import glob

from src.processing import (
    cleanup_generated_files,
    load_and_split_pdfs_from_directory,
    create_vectorstore,
    process_all_dictionary_questions,
)
from src.libraries import ChatOpenAI

def main():
    # ──────────────────────────────────────────
    # 0) Initialize session state
    # ──────────────────────────────────────────
    if "downloads" not in st.session_state:
        st.session_state.downloads = {}          # { base_name: excel_bytes }
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False   # have we run at least once?

    # ──────────────────────────────────────────
    # 1) Auth & API Key
    # ──────────────────────────────────────────
    password = st.text_input("Enter password", type="password")
    if password != "Jm@xBond":
        st.stop()

    api_key = st.text_input("Enter the API Key here:")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    st.title("Batch PDF Analysis with RAG Workflows")

    # ──────────────────────────────────────────
    # 2) Input Mode & Uploads
    # ──────────────────────────────────────────
    input_mode = st.radio(
        "Select input mode:",
        ("Directory", "Upload PDF", "ZIP Archive File")
    )

    directory = None
    _temp_dirs = []
    upload_base = None

    if input_mode == "Directory":
        directory = st.text_input("Enter parent directory with PDF subfolders:")

    elif input_mode == "Upload PDF":
        uploaded_pdf = st.file_uploader("Upload a single PDF file", type="pdf")
        if uploaded_pdf:
            tmp = tempfile.mkdtemp(); _temp_dirs.append(tmp)
            pdf_path = os.path.join(tmp, uploaded_pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            directory = tmp
            upload_base = os.path.splitext(uploaded_pdf.name)[0]

    else:  # ZIP Archive File
        zip_file = st.file_uploader("Upload a ZIP archive:", type=["zip"])
        if zip_file:
            tmp = tempfile.mkdtemp(); _temp_dirs.append(tmp)
            try:
                zip_bytes = zip_file.read()
                with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
                    zf.extractall(tmp)
                directory = tmp
                # **do not** set upload_base here, so each subfolder names itself
            except zipfile.BadZipFile:
                st.error("That doesn’t look like a valid ZIP file.")

    # ──────────────────────────────────────────
    # 3) Run Analysis
    # ──────────────────────────────────────────
    if st.button("Run Analysis"):
        # Clear out any previous run
        st.session_state.downloads.clear()
        st.session_state.analysis_done = False

        if not directory or not os.path.isdir(directory):
            st.warning("Please provide a valid directory, PDF upload, or ZIP path.")
        else:
            llm = ChatOpenAI(model="gpt-4o-2024-05-13")

            # find every PDF‐containing folder
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

                    # decide filename:
                    # - single‐PDF upload uses upload_base
                    # - otherwise each folder names itself
                    if upload_base:
                        base = upload_base
                    else:
                        base = os.path.basename(sub)

                    # build Excel in-memory
                    buffer = io.BytesIO()
                    sheet_name = base[:31]  # Excel limit
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name=sheet_name)
                    buffer.seek(0)

                    # stash it in session_state
                    st.session_state.downloads[base] = buffer.getvalue()

                # mark that we did run
                st.session_state.analysis_done = True

        # cleanup temp dirs
        for td in _temp_dirs:
            shutil.rmtree(td, ignore_errors=True)

    # ──────────────────────────────────────────
    # 4) Always render downloads if we’ve run once
    # ──────────────────────────────────────────
    if st.session_state.analysis_done and st.session_state.downloads:
        st.markdown("### 📥 Your Results")
        for name, data in st.session_state.downloads.items():
            st.download_button(
                label=f"Download {name}.xlsx",
                data=data,
                file_name=f"{name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=name,
            )

if __name__ == "__main__":
    main()
