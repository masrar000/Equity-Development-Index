import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def process_pdf_and_generate_results(pdf_file_path):
    # Step 1: Load and split the PDF using LangChain
    loader = PyPDFLoader(pdf_file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    
    # Step 2: Sample questions to process (customize as needed)
    queries = {
        "Affordable residential units": "How many affordable residential units are listed?",
        "Gross square footage (GSF)": "What is the total GSF mentioned?",
        "Parking spaces": "How many parking spaces are allocated?"
    }
    
    # Step 3: Simulate query responses with regex extractions (for demonstration)
    results = {"Component": [], "Extracted Value": []}
    for query_title, query_text in queries.items():
        # Simulate extracting relevant text (for now, just using the first split)
        matched_text = _extract_relevant_info_from_split(splits[0].page_content, query_title)
        
        # Append results
        results["Component"].append(query_title)
        results["Extracted Value"].append(matched_text or "Not found")

    # Step 4: Return results as a DataFrame
    return pd.DataFrame(results)

def _extract_relevant_info_from_split(text, component):
    # Simplified regex patterns (you can improve them based on your needs)
    patterns = {
        "Affordable residential units": r"\b(\d+)\s+affordable\s+units\b",
        "Gross square footage (GSF)": r"\b(\d{1,3}(?:,\d{3})*)\s+GSF\b",
        "Parking spaces": r"\b(\d+)\s+parking\s+spaces\b"
    }
    
    # Apply regex for the given component
    if component in patterns:
        match = re.search(patterns[component], text, re.IGNORECASE)
        if match:
            return match.group(1)  # Return the matched value
    return None  # Return None if no match
