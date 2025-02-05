# Equity Development Index (EDI) 🌍
LLM-driven framework using HyDE, RAG Fusion, and LangChain for extracting, structuring, and scoring data from Environmental Impact Studies (EIS) to support urban planning decisions. This tool automates the extraction of key metrics such as residential units, parking spaces, gross square footage, and other development-related insights from large PDF documents.

📖 Table of Contents
Features
Project Structure
Installation
How to Run
Usage
Customization
Sample Output
Contributing

## 🚀 Features
Automated PDF Parsing: Easily upload large PDFs and automatically extract key metrics.
RAG Workflows: Retrieve context and extract relevant answers using LangChain and RAG Fusion.
Regex-based Extraction: Extract numerical and structured information like gross square footage (GSF), affordable residential units, and parking spaces.
Streamlit UI: Interactive user interface for PDF uploads and on-the-fly processing.
Download Results: Export extracted data as CSV files for easy integration into other systems.

## 📁 Project Structure
Equity-Development-Index/
├── data/                         # Folder containing uploaded and sample PDF files
│   ├── sample.pdf                # Example PDF for testing
│   └── other uploaded PDFs...
├── src/
│   ├── main.py                   # Streamlit app for file upload and interaction
│   ├── processing.py             # PDF processing and regex extraction logic
├── requirements.txt              # Dependencies for setting up the project
├── README.md                     # Project documentation

## 🔧 Installation
### 1. Clone the repository:
git clone https://github.com/masrar000/Equity-Development-Index.git
cd Equity-Development-Index
### 2. Set up a virtual environment (optional but recommended):
python3 -m venv env
source env/bin/activate   # For Linux/Mac
env\Scripts\activate      # For Windows
### 3. Install dependencies:
pip install -r requirements.txt

## 🏃 How to Run

### 1. Navigate to the project directory and run the Streamlit app:
python -m streamlit run src/main.py
### 2.Open Streamlit in your browser:
python -m streamlit run src/main.py

## 🎯 Usage
### 1. Upload a PDF:
Use the Streamlit file uploader to upload a PDF from your local machine. The file will be saved in the data/ folder for processing.

### 2. Process the PDF:
Once uploaded, the app will automatically extract key metrics and display them as a table.

### 3. Download Results:
Download the extracted results as a CSV file directly from the Streamlit app.

## ✏️ Customization
You can customize the project by:
Adding new extraction queries: Modify the queries dictionary in processing.py to extract additional metrics.
Improving regex patterns: Improve or add new patterns in _extract_relevant_info_from_split() to handle different PDF formats.

Example:
queries = {
    "Affordable residential units": "How many affordable residential units are listed?",
    "Gross square footage (GSF)": "What is the total GSF mentioned?",
    "Parking spaces": "How many parking spaces are allocated?",
    "Healthcare space": "How many square feet of space is allocated to healthcare facilities?"
}

## 📊 Sample Output
When you upload a PDF and process it, the app displays the results in a table like:

Component                    | Extracted Value
Affordable residential units | 45
Gross square footage (GSF)	 | 120,000
Parking spaces	             | 150
You can download the results as a CSV file for further analysis.

## 🤝 Contributing
We welcome contributions! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch:
   git checkout -b feature/your-feature-name
3. Make your changes and commit them:
   git commit -m "Add your message"
4. Push to your branch:
   git push origin feature/your-feature-name
5. Submit a pull request



