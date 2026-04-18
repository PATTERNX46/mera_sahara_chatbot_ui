# 🇮🇳 Mera Sahara AI - Unified DPI for Rural Empowerment
> **Sarkari Sathi**: An AI-driven Digital Public Infrastructure (DPI) to bridge the gap between complex government schemes and rural Indian citizens.

![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%20Flash-blue?style=for-the-badge&logo=googlegemini)
![LangChain](https://img.shields.io/badge/Framework-LangChain-white?style=for-the-badge&logo=langchain)

---

## 🚀 The Problem
Millions of eligible rural citizens miss out on life-changing government schemes due to:
- **Complex Language:** Scheme documents are long and full of jargon.
- **Language Barrier:** Most information is not available in local dialects.
- **Digital Literacy:** Navigating complex portals is difficult for non-tech users.

## ✨ Our Solution: Mera Sahara AI
Mera Sahara is an intelligent, multilingual assistant that acts as a bridge. Users can talk to the bot, upload their documents, and get personalized scheme recommendations instantly.

### 🌟 Key Features
- **RAG-based AI Engine:** Uses **Gemini 1.5 Flash** with **LangChain** and **FAISS** to provide accurate answers from real government PDF documents.
- **OCR Smart Scan:** Upload an Aadhaar card or Income Certificate, and the AI automatically extracts details (State, Income, Age) to check eligibility.
- **Real-time Match Probability:** Shows a dynamic **Match Score** for each scheme based on the user's profile.
- **Multilingual Support:** One-click translation (English, Hindi, Bengali) powered by **Google Translate API**.
- **Voice-First Design:** Integrated Speech-to-Text and Text-to-Speech for low-literacy users.

---

## 🛠️ Tech Stack
- **Frontend:** Next.js 14, Tailwind CSS, Framer Motion (for smooth UI).
- **Backend:** Python, FastAPI, Uvicorn.
- **AI/ML:** Google Gemini API (Flash & Embedding models), LangChain.
- **Vector Database:** FAISS (Facebook AI Similarity Search).
- **OCR:** Gemini Vision capabilities for document extraction.

---

## 📂 Project Structure
```text
mera_sahara/
├── frontend/             # Next.js Dashboard & Chat UI
├── backend/              
│   ├── core/
│   │   └── rag_pipeline.py  # AI Logic, RAG, and OCR
│   ├── main.py              # FastAPI Routes
│   ├── faiss_index/         # Vector Database
│   └── .env                 # API Keys (Excluded from Git)
└── README.md
⚙️ Installation & Setup
1. Backend Setup
Bash
cd backend
python -m venv venv
source venv/Scripts/activate  # For Windows
pip install -r requirements.txt
python test_script.py         # To build the Vector DB from PDFs
uvicorn main:app --reload
2. Frontend Setup
Bash
cd frontend
npm install
npm run dev
🛡️ Impact & Future Scope
Impact: Can be deployed in Common Service Centres (CSCs) or as a mobile app to help 100M+ rural Indians.

Future: Direct integration with DigiLocker and UMANG for one-click application submission.
