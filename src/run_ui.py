# run_ui.py
import os
import streamlit as st
from processing import (
    cleanup_generated_files,
    load_and_split_pdfs_from_directory,
    create_vectorstore,
    process_all_dictionary_questions,
    save_results_to_excel,
)
from langchain_openai import ChatOpenAI

# Title of the Streamlit application
st.title("Batch PDF Analysis with RAG Workflows")

# Text input for the parent directory path
directory = st.text_input("Enter parent directory with PDF subfolders:")

# Button to trigger the analysis
if st.button("Run Analysis"):
    if not directory or not os.path.isdir(directory):
        st.warning("Please enter a valid directory path!")
    else:
        # Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o-2024-05-13")

        # Discover subfolders; if none, process the directory itself
        subfolders = [
            os.path.join(directory, d)
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]
        if not subfolders:
            subfolders = [directory]

        # Iterate through each folder and run the pipeline
        for sub in subfolders:
            st.write(f"## Processing: {os.path.basename(sub)}")
            # 1) Cleanup old Excel if exists
            cleanup_generated_files(sub)

            # 2) Load and split PDFs
            splits = load_and_split_pdfs_from_directory(sub)
            if not splits:
                st.error(f"No PDFs found in {sub}, skipping.")
                continue

            # 3) Create vectorstore
            vs = create_vectorstore(splits)

            # 4) Run RAG queries and assemble DataFrame
            df = process_all_dictionary_questions(sub, vs, llm)
            if df.empty:
                st.error(f"No data extracted for {os.path.basename(sub)}.")
                continue

            # 5) Save to Excel and provide download link
            output_file = save_results_to_excel(df, sub)
            st.success(f"Results saved to {output_file}")
            with open(output_file, "rb") as f:
                st.download_button(
                    label=f"Download {os.path.basename(output_file)}",
                    data=f,
                    file_name=os.path.basename(output_file),
                )
