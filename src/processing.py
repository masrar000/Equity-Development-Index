# src/processing.py

from .libraries import os, re, glob, pd, defaultdict, Workbook, dataframe_to_rows, st
from .libraries import PyPDFLoader, RecursiveCharacterTextSplitter
from .libraries import ChatOpenAI, OpenAIEmbeddings, LanceDB
from .prompts import (
    rag_fusion_with_no_action,
    rag_fusion_with_action,
    rag_with_no_action,
    rag_with_action,
    component_units_map,
)
from langchain.schema import HumanMessage  # wns everything related to constructing and sending prompts and not general utilities so NOT libraries.py


###############################################################################
# 1. CLEANUP OLD FILES
###############################################################################
def cleanup_generated_files(directory_path):
    """
    Deletes only the Excel file that matches the new generated file name.
    """
    dir_name = os.path.basename(os.path.normpath(directory_path))
    generated_file = f"{dir_name}.xlsx"
    file_path = os.path.join(directory_path, generated_file)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted old file: {generated_file}")
        except Exception as e:
            print(f"Error deleting {generated_file}: {e}")
    else:
        print(f"No previous {generated_file} found. Skipping cleanup.")


###############################################################################
# 3. LOADING, SPLITTING, VECTORSTORE
###############################################################################
def load_and_split_pdfs_from_directory(directory_path):
    all_splits = []
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
    if not pdf_files:
        st.error(f"No PDF files found in {directory_path}")
        return []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        all_splits.extend(splits)
    return all_splits


def create_vectorstore(splits):
    # collect just the text and the page number metadata
    texts = [doc.page_content for doc in splits]
    metadatas = [{"page": doc.metadata.get("page", "N/A")} for doc in splits]
    # build the LanceDB index on those texts + metadata
    return LanceDB.from_texts(
        texts,
        embedding=OpenAIEmbeddings(),
        metadatas=metadatas,
    )


###############################################################################
# 4. RAG QUERY (Modified to return page numbers for terminal logging)
###############################################################################
def rag_query(query, vectorstore, llm):
    retriever = vectorstore.as_retriever()
    documents = retriever.get_relevant_documents(query)
    context_parts = []
    pages = []
    for doc in documents:
        page = doc.metadata.get("page", "N/A")
        try:
            page = str(int(page))
        except Exception:
            page = "N/A"
        pages.append(page)
        context_parts.append(f"Page {page}:\n{doc.page_content}")
    context = "\n\n".join(context_parts)

    # wrap your prompt in a HumanMessage
    messages = [
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}\nAnswer:")
    ]
    response = llm(messages)
    # response is an AIMessage with .content
    return response.content.strip(), context, pages


###############################################################################
# 5. EXTRACTION FUNCTIONS (Using simple text.split approach)
###############################################################################
def extract_numeric_value(text, component):
    """
    Extracts the numeric value from the LLM's response for the given component.
    
    Special handling:
      - For "Greenhouse Gas Emissions": Checks if the value is in pounds and converts to tons (2000 pounds = 1 ton).
      - For "Open Space Ratio": 
           * If active and/or passive values are provided, sums them.
           * Otherwise, finds the first numeric value after a colon.
      - Otherwise: Uses the value after the last colon.
    """
    try:
        # ----- Special handling for Greenhouse Gas Emissions -----
        if component.lower() == "greenhouse gas emissions":
            value_str = text.rsplit(":", 1)[1].strip()
            tokens = value_str.split()
            numeric_value = float(tokens[0].replace(",", ""))
            unit = "tons"  # default assumption
            for token in tokens[1:]:
                token_lower = token.lower()
                if "pound" in token_lower or "lb" in token_lower:
                    unit = "pounds"
                    break
                elif "ton" in token_lower:
                    unit = "tons"
                    break
            if unit == "pounds":
                return float(numeric_value / 2000)
            return float(numeric_value)
        
        # ----- Special handling for Open Space Ratio -----
        if component.lower() == "open space ratio":
            active_match = re.search(r"active(?:\s*[:\-]\s*|\s+)([\d\.]+)", text, re.IGNORECASE)
            passive_match = re.search(r"passive(?:\s*[:\-]\s*|\s+)([\d\.]+)", text, re.IGNORECASE)
            if active_match or passive_match:
                active_value = float(active_match.group(1)) if active_match else 0.0
                passive_value = float(passive_match.group(1)) if passive_match else 0.0
                return active_value + passive_value
            match = re.search(r":\s*([\d\.]+)", text)
            if match:
                return float(match.group(1))
            else:
                raise ValueError("No numeric value found for Open Space Ratio")
        
        # ----- Default extraction for other components -----
        value_str = text.rsplit(":", 1)[1].strip().replace(",", "")
        return float(value_str.split()[0])
    
    except Exception as e:
        print(f"Failed to extract numeric value for component '{component}'. Error: {e}\nContext:\n{text}")
        return 0


def extract_value_rag_fusion(text, component):
    """Extraction function for RAG Fusion responses using the common helper."""
    return extract_numeric_value(text, component)


def extract_value_rag(text, component):
    """Extraction function for Agentic RAG responses using the common helper."""
    return extract_numeric_value(text, component)


###############################################################################
# 7. PROCESSING ALL DICTIONARY-BASED QUESTIONS
###############################################################################
def process_all_dictionary_questions(directory, vectorstore, llm):
    """
    Build a DataFrame with columns: [Component, No Action, With Action, Units].
    The 'No Action' and 'With Action' columns are numeric, 'Units' is text.
    """
    final_data = defaultdict(lambda: {"No Action": 0, "With Action": 0, "Units": ""})

    def handle_query(component, question, action_label, use_fusion):
        response, context, pages = rag_query(question, vectorstore, llm)
        print("==========================================================")
        print(f"COMPONENT: {component}\n")
        print(f"ACTION TYPE: {action_label}\n")
        print(f"QUERY:\n{question}\n")
        print(f"CONTEXT (first 500 chars):\n{context[:500]}...\n")
        print(f"RESPONSE:\n{response}")

        if use_fusion:
            extracted_val = extract_value_rag_fusion(response, component)
        else:
            extracted_val = extract_value_rag(response, component)

        print(f"EXTRACTED NUMERIC VALUE: {extracted_val}")
        print("==========================================================\n")

        if extracted_val == 0 or extracted_val == "0":
            final_data[component][action_label] = "Value not found"
        else:
            final_data[component][action_label] = extracted_val

        if not final_data[component]["Units"]:
            final_data[component]["Units"] = component_units_map.get(component, "")

    # 1) RAG-Fusion No Action
    for category, list_of_dicts in rag_fusion_with_no_action.items():
        for question_dict in list_of_dicts:
            for component, question in question_dict.items():
                handle_query(component, question, "No Action", use_fusion=True)

    # 2) RAG-Fusion With Action
    for category, list_of_dicts in rag_fusion_with_action.items():
        for question_dict in list_of_dicts:
            for component, question in question_dict.items():
                handle_query(component, question, "With Action", use_fusion=True)

    # 3) Agentic RAG No Action
    for category, list_of_dicts in rag_with_no_action.items():
        for question_dict in list_of_dicts:
            for component, question in question_dict.items():
                handle_query(component, question, "No Action", use_fusion=False)

    # 4) Agentic RAG With Action
    for category, list_of_dicts in rag_with_action.items():
        for question_dict in list_of_dicts:
            for component, question in question_dict.items():
                handle_query(component, question, "With Action", use_fusion=False)

    # Build final DataFrame with columns: Component, No Action, With Action, Units
    rows = []
    for comp, values in final_data.items():
        row = {
            "Component": comp,
            "No Action": values["No Action"],
            "With Action": values["With Action"],
            "Units": values["Units"],
        }
        rows.append(row)

    df = pd.DataFrame(rows, columns=["Component", "No Action", "With Action", "Units"])
    df.sort_values("Component", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


###############################################################################
# 8. SAVE RESULTS TO EXCEL
###############################################################################
def save_results_to_excel(df, directory_path):
    dir_name = os.path.basename(os.path.normpath(directory_path))
    output_path = f"D:\LLM_with_RAG_workflows\Final_LLM\Results_test\{dir_name}.xlsx"
    
    # make a copy so we don't alter the df you print in the terminal
    df_excel = df.copy()
    # replace any numeric 0 in the two columns with "Value not found"
    df_excel["No Action"]   = df_excel["No Action"].apply(lambda x: "Value not found" if x == 0 else x)
    df_excel["With Action"] = df_excel["With Action"].apply(lambda x: "Value not found" if x == 0 else x)

    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    for r_idx, row in enumerate(dataframe_to_rows(df_excel, index=False, header=True)):
        for c_idx, value in enumerate(row):
            ws.cell(row=r_idx + 1, column=c_idx + 1, value=value)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    return output_path


def main_cli(directory):
    from .libraries import ChatOpenAI
    # 1) Discover which folders to process
    subfolders = [
        os.path.join(directory, d)
        for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ]
    # If no subfolders, treat 'directory' itself as the folder
    if not subfolders:
        subfolders = [directory]

    # 2) Initialize your LLM once
    llm = ChatOpenAI(model="gpt-4o-2024-05-13")

    # 3) Iterate and run the same pipeline you have in Streamlit
    for sub in subfolders:
        print(f"\n--- Processing {sub} ---")
        cleanup_generated_files(sub)

        splits = load_and_split_pdfs_from_directory(sub)
        if not splits:
            print(f"No PDFs found in {sub}. Skipping.")
            continue

        vs = create_vectorstore(splits)
        df = process_all_dictionary_questions(sub, vs, llm)
        print(df.to_string(index=False))

        output_file = save_results_to_excel(df, sub)
        print(f"Results saved to {output_file}")
