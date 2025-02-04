import os
import streamlit as st
import pandas as pd
from src.processing import process_pdf_and_generate_results

# Streamlit app
def main():
    st.title("Equity Development Index (EDI) - Capstone Project")
    st.write("Upload a PDF to analyze and extract key development metrics.")

    # File Upload UI
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        file_path = os.path.join("data", uploaded_file.name)
        
        # Save uploaded PDF locally
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write(f"Uploaded: {uploaded_file.name}")

        # Process PDF and display results
        st.write("**Processing the uploaded PDF...**")
        results_df = process_pdf_and_generate_results(file_path)
        
        if results_df is not None:
            st.write("**Results extracted successfully:**")
            st.dataframe(results_df)  # Display the results table in Streamlit

            # Download option
            csv_file = "results.csv"
            results_df.to_csv(csv_file, index=False)
            with open(csv_file, "rb") as f:
                st.download_button("Download Results as CSV", f, file_name="results.csv")
        else:
            st.write("No results were found.")

if __name__ == "__main__":
    main()
