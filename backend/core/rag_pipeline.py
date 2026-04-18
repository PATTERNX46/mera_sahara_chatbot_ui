# backend/core/rag_pipeline.py
import os
import sys
import base64
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage # NEW: Needed for sending images

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("\n❌ CRITICAL ERROR: GOOGLE_API_KEY not found!")
    sys.exit(1)

DB_FAISS_PATH = "faiss_index"

def ingest_pdf(pdf_path: str):
    print(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    print("Creating embeddings and saving to database...")
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=API_KEY)
    
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    print("✅ Database built successfully with Gemini!")

def ask_sarkari_bot(user_query: str):
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=API_KEY)
    
    if not os.path.exists(DB_FAISS_PATH):
        return "System Error: No government schemes loaded yet. Please ingest a PDF first."
    
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key=API_KEY)

    system_prompt = (
        "You are 'Sarkari Sathi', an empathetic, multilingual assistant helping rural Indian citizens "
        "discover government schemes. Use the retrieved context to answer the user's question. "
        "If you don't know the answer, say so. Keep your answer simple, encouraging, and actionable.\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": user_query})
    return response["answer"]

# --- NEW OCR FEATURE ---
def scan_and_search(image_bytes: bytes):
    """Uses Gemini Vision to read a document, then searches schemes based on extracted info."""
    image_data = base64.b64encode(image_bytes).decode("utf-8")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)
    
    # 1. Ask Gemini to read the image
    msg = HumanMessage(
        content=[
            {"type": "text", "text": "Extract the person's state, income, and any demographic details from this document. Summarize it simply in one sentence like 'I am from [State] and my income is [Income]'."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
        ]
    )
    
    print("Scanning document with Gemini Vision...")
    extracted_text = llm.invoke([msg]).content
    print(f"Vision Extracted: {extracted_text}")
    
    # 2. Feed the extracted text to our existing RAG bot!
    final_answer = ask_sarkari_bot(f"Here is the data extracted from my uploaded document: '{extracted_text}'. What schemes am I eligible for?")
    
    return {
        "extracted_data": extracted_text,
        "answer": final_answer
    }