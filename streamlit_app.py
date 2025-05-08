#!/usr/bin/env python3
import src.config    # load .env → os.environ
import os
import streamlit as st
import tempfile
import shutil
import zipfile 

from src.processing import (
    cleanup_generated_files,
    load_and_split_pdfs_from_directory,
    create_vectorstore,
    process_all_dictionary_questions,
    save_results_to_excel,
)
from src.libraries import ChatOpenAI

def main():
    password = st.text_input("Enter password", type="password")
    if password != "Jm@xBond":
        st.stop()

    api_key=st.text_input("Enter the API Key here: ") 
    os.environ["OPENAI_API_KEY"] = api_key
    
    st.title("Batch PDF Analysis with RAG Workflows")

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
            tmp = tempfile.mkdtemp(); _temp_dirs.append(tmp)
            pdf_path = os.path.join(tmp, uploaded_pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            directory = tmp
    elif input_mode == "ZIP Archive File":
        zip_path = st.file_uploader("Upload a ZIP archive:")
        if zip_path and os.path.isfile(zip_path) and zip_path.lower().endswith(".zip"):
            tmp = tempfile.mkdtemp(); _temp_dirs.append(tmp)
            try:
                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(tmp)
                directory = tmp
            except zipfile.BadZipFile:
                st.error("That doesn’t look like a valid ZIP file.")

    # --- Run Analysis ---
    if st.button("Run Analysis"):
        if not directory or not os.path.isdir(directory):
            st.warning("Please provide a valid directory, PDF upload, or ZIP path.")
        else:
            llm = ChatOpenAI(model="gpt-4o-2024-05-13")

            # find every PDF‐containing folder
            pdf_dirs = []
            for root, _, files in os.walk(directory):
                if any(f.lower().endswith(".pdf") for f in files):
                    pdf_dirs.append(root)

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

                    out = save_results_to_excel(df, sub)
                    st.success(f"Results saved to {out}")
                    with open(out, "rb") as f:
                        st.download_button(
                            label=f"Download {os.path.basename(out)}",
                            data=f,
                            file_name=os.path.basename(out),
                        )

            # clean up temp folders
            for td in _temp_dirs:
                shutil.rmtree(td, ignore_errors=True)

if __name__ == "__main__":
    main()
