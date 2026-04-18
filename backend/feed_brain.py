from core.rag_pipeline import ingest_pdf
import os

print("Checking for PDF...")
if os.path.exists("scheme.pdf"):
    print("Found scheme.pdf! Vectorizing and feeding it to Gemini...")
    ingest_pdf("scheme.pdf")
    print("\n✅ Brain successfully fed! The faiss_index database has been created.")
else:
    print("\n❌ Could not find scheme.pdf. Make sure you ran make_pdf.py first!")