# Equity Development Index (EDI) 🌍: Batch PDF Analysis with RAG Workflows
Equity Development Index (EDI) is a Large Language Model (LLM)-driven Python toolkit that leverages HYpothetical Document Embedding (HyDE), Retrieveal Augmented Generation (RAG) Fusion, Agentic RAG and LangChain—powered by OpenAI’s GPT-4o—to batch-process Environmental Impact Studies (EIS) and similar PDFs. It automates the extraction, structuring, and scoring of key development metrics (e.g., residential unit counts, parking spaces, gross square footage, displacement estimates, open-space ratios, and waste/emissions forecasts) and compiles them into per-folder Excel reports. EDI offers both an interactive Streamlit web User Interface (UI) for point-and-click use and a headless Command Line Interface (CLI) mode for scripted batch runs, making it a flexible decision-support solution for equity-focused urban planning.

📋 Table of Contents

🌟 Features

⚙️ Prerequisites

💻 Installation

🔧 Configuration

🚀 Usage

   🔍 Streamlit Web UI
   
   💻 CLI Mode

📂 Project Structure

🗂️ File Descriptions

🤖 How It Works

⚙️ Customization & Tuning

🐞 Troubleshooting

🤝 Contributing

📄 License

## 🚀 Features
### Dual Interfaces
   Streamlit Web UI for interactive, point-and-click analysis in the browser
   CLI Mode (python run.py --cli) for headless batch runs
### Automated PDF Parsing & RAG Pipelines
   Splits large PDFs into 1 000-character chunks with overlap
   Applies HyDE, RAG Fusion, and Agentic RAG (via LangChain) to retrieve context and extract metrics
### Advanced Extraction Logic
   Regex-based numeric parsing (e.g. pounds→tons)
   Captures development metrics such as square footage (GSF), affordable and market-rate residential units, parking spaces, open-space ratios, waste generation, and greenhouse gas emissions
### LanceDB Vector Store
Fast, on-disk similarity search over document embeddings
### Configurable Prompts
All domain-specific question templates and response formats live in prompts.py for easy editing
### Automated Cleanup & Reporting
   Deletes stale Excel outputs before each run
   Assembles results into .xlsx reports (one file per PDF folder) and provides download links in the UI

## ⚙️ Prerequisites
Python 3.9+
OpenAI API Key (GPT-4o access)
git (for cloning)
Windows / macOS / Linux

**1. Clone the repository**
git clone https://github.com/yourusername/batch-pdf-rag.git

In the terminal: cd batch-pdf-rag

**2. Create & activate a virtual environment**

python -m venv .venv

#Windows (PowerShell)

.\.venv\Scripts\Activate.ps1

#macOS/Linux

source .venv/bin/activate

**3. Install dependencies**

pip install --upgrade pip

pip install -r requirements.txt

## 🔧 Configuration
**1. Environment Variables**
   
   Rename .env.example → .env
   
   Populate with your OpenAI key: OPENAI_API_KEY=sk-…

**2. config.py**

Automatically loads .env and injects OPENAI_API_KEY into os.environ.

## 🚀 Usage
### 🔍 Streamlit Web UI

In terminal: #From project root, with venv active:

streamlit run run_ui.py

1. Open your browser at http://localhost:8501.
2. Enter the path to a parent directory containing one or more subfolders of PDFs.
3. Click Run Analysis.
4. As each subfolder processes, you’ll see progress messages.
5. When complete, download per-folder .xlsx via on-page buttons.

Tip: the UI auto-cleans old FolderName.xlsx before re-running.

### 💻 CLI Mode
#Headless batch run:

python run.py --cli "/full/path/to/parent_directory"
* If the specified directory has subfolders, each is processed in turn.
* If no subfolders, the directory itself is treated as one batch.
* Output:
  Console table of results
  Excel files saved to Results/<FolderName>.xlsx (or configured path)


## 📁 Project Structure
Batch-pdf-rag/

├── .venv/                     # Virtual environment

├── .env                       # env file (has the API key)

├── config.py                  # Loads .env, sets OPENAI_API_KEY

├── libraries.py               # Centralized imports & utilities

├── Documents                  # All documents


├── prompts.py                 # All RAG question templates & unit map

├── processing.py              # Core: cleanup, PDF-split, RAG, extraction, Excel

├── run_ui.py                  # Streamlit front-end entrypoint

├── run.py                     # Dispatcher: UI default, CLI with --cli

├── requirements.txt           # Pinned dependencies via pip freeze

└── Results/                   # Generated Excel outputs per folder

## 🗂️ File Descriptions
**.env**
Stores OPENAI_API_KEY; loaded by config.py.

**config.py**
Uses dotenv to load .env; raises error if key missing.

**libraries.py**
Standard & third-party imports (os, glob, pandas, openpyxl, streamlit, nest_asyncio, LangChain classes).

Applies nest_asyncio.apply() for Streamlit+async compat.

**prompts.py**
Four dictionaries:
   
   rag_fusion_with_no_action, rag_fusion_with_action
   
   rag_with_no_action, rag_with_action

Defines component_units_map for labeling results.

**processing.py**
1. cleanup_generated_files
2. load_and_split_pdfs_from_directory (PyPDFLoader + RecursiveCharacterTextSplitter)
3. create_vectorstore (LanceDB.from_texts with metadata)
4. rag_query (retrieval + ChatOpenAI prompt wrapper + HumanMessage)
5. extract_numeric_value (parsing & unit conversion logic)
6. process_all_dictionary_questions (loops through all prompts, builds DataFrame)
7. save_results_to_excel (writes .xlsx, replaces zeros)
8. main_cli (mirrors Streamlit pipeline for CLI)

**run_ui.py**
1. Text input, button, and per-folder progress in Streamlit.
2. Calls processing.py functions, shows success/errors, offers download.

**run.py**
1. Uses argparse to detect --cli.

2. No args → launches Streamlit UI; --cli PATH → calls main_cli(PATH).

**requirements.txt**
All Python deps pinned for reproducibility.

## 🤖 How It Works

**1. Cleanup**
Deletes any existing FolderName.xlsx in each batch folder.

**2. PDF Load & Chunk**
PyPDFLoader reads full PDF → LangChain splits into ~1 000-char chunks with 200-char overlap.

**3. Vector Store**
Each chunk → text embedding via text-embedding-ada-002 → stored in LanceDB with page metadata.

**4. RAG Queries**

For each component prompt: retrieve top-k chunks → assemble context → call GPT-4o with HumanMessage.

Two modes:

   **RAG Fusion** (multi-retriever + Reciprocal Rank Fusion (RRF))
   
   **Agentic RAG** (single retriever + potential calculation agent)

**5. Extraction**
Parse returned answer string to float (handling pounds→tons, summing active/passive OSR).

**6. Results Assembly**
   
   Populate a pandas DataFrame with Component, No Action, With Action, Units.
   
   Zero or failed extractions marked "Value not found".

**7.Excel Export**
Write .xlsx via openpyxl, one sheet named by the same name as processed directory.

## ⚙️ Customization & Tuning
**Prompts**
Edit prompts.py to add/remove components or change the instruction formats.

**Chunking**
In processing.py, adjust chunk_size & chunk_overlap to suit document density.

**VectorStore Persistence**
By default LanceDB uses an in-memory or temp store. Pass a path="my_lancedb_dir" to from_texts() to persist on disk.

**Model & Parameters**

Swap ChatOpenAI(model="gpt-4o-2024-05-13") for any supported OpenAI model.

Tweak top-k retriever settings via vectorstore.as_retriever(search_kwargs={...}).

## 🐞 Troubleshooting

**ModuleNotFoundError: pypdf**
pip install pypdf cryptography

**Rate limits / timeouts**
Catch exceptions around llm(messages) and retry with backoff.

**Encrypted PDFs**
Ensure your PDFs are not password-protected; LangChain’s loader doesn’t handle encryption.

**Disk space errors**
Clean up large LanceDB cache directories or mount on a larger volume.

## 🤝 Contributing
**1. Fork the repo**

**2. Create a feature branch:**
git checkout -b feat/my-awesome-feature

**3. Install dev dependencies & run tests (if any)**

**4. Commit & push**

**5. Open a Pull Request against main**


## 📄 License
See LICENSE for details.
