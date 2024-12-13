import fitz  # PyMuPDF
from langchain_groq import ChatGroq
import requests
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set your Hugging Face API key

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key=GROQ_API_KEY
)

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print (text)
    return text



# Function to summarize text
def summarize_text(text):
    # Ensure the text is not too long, split if necessary
    chunk_size = 1024  # Maximum input size for BART
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    summaries = []
    for chunk in text_chunks:
        response = requests.post(API_URL, headers=headers, json={"inputs": chunk})

        if response.status_code == 200:
            summary = response.json()
            summaries.append(summary[0]['summary_text'])
        else:
            print(f"Error: {response.status_code}, Response: {response.text}")
            return None
    
    return " ".join(summaries)  # Join multiple summaries if the text was chunked

# Main function to process the PDF and summarize
def summarize_pdf(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(pdf_text)
    
    return summary




# Example usage

#summary = summarize_pdf(pdf_path)
#prompt="make a better summary for this in english:"+summary
#response = llm.invoke(prompt)
#exam=llm.invoke("generate an exam based on this:"+response.content)
#print("Summaryy:", response.content)
#print("Exam:", exam.content)
