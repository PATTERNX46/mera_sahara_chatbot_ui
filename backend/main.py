# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.rag_pipeline import ask_sarkari_bot, scan_and_search

app = FastAPI(title="Sarkari Sathi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Backend is running!"}

# --- EXISTING UI ENDPOINTS ---
@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        ai_response = ask_sarkari_bot(request.message)
        return {"reply": ai_response}
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "Sorry, an internal error occurred."}

@app.post("/api/scan")
async def scan_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = scan_and_search(contents)
        return {"reply": result["answer"], "extracted": result["extracted_data"]}
    except Exception as e:
        print(f"OCR Error: {e}")
        return {"reply": "Sorry, I could not read that document.", "extracted": ""}

# ==========================================
# --- NEW MULTI-CHANNEL ENDPOINTS ---
# ==========================================

# 1. WHATSAPP ENDPOINT
@app.post("/api/whatsapp")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    print(f"WhatsApp Message from {From}: {Body}")
    ai_reply = ask_sarkari_bot(Body)
    
    # Twilio expects an XML response (TwiML)
    twiml_response = f"""
    <Response>
        <Message>{ai_reply}</Message>
    </Response>
    """
    return Response(content=twiml_response, media_type="application/xml")

# 2. SMS ENDPOINT
@app.post("/api/sms")
async def sms_webhook(Body: str = Form(...), From: str = Form(...)):
    print(f"SMS from {From}: {Body}")
    ai_reply = ask_sarkari_bot(Body)
    
    # SMS must be short. Cut it to 150 characters if it's too long.
    short_reply = ai_reply[:150] + "..." if len(ai_reply) > 150 else ai_reply
    
    twiml_response = f"""
    <Response>
        <Message>SarkariSathi: {short_reply}</Message>
    </Response>
    """
    return Response(content=twiml_response, media_type="application/xml")

# 3. VOICE IVR - ENTRY POINT (When they call)
@app.post("/api/voice")
async def voice_webhook():
    print("Incoming Call...")
    # Greet the user in Hindi and listen for their speech
    twiml_response = """
    <Response>
        <Gather input="speech" action="/api/voice-process" language="hi-IN" speechTimeout="auto">
            <Say language="hi-IN" voice="Polly.Aditi">
                Namaskar, Mera Sahara mein aapka swagat hai. Kripya apna sawaal poochein.
            </Say>
        </Gather>
    </Response>
    """
    return Response(content=twiml_response, media_type="application/xml")

# 4. VOICE IVR - PROCESSING POINT (When they finish speaking)
@app.post("/api/voice-process")
async def voice_process(SpeechResult: str = Form(None)):
    if not SpeechResult:
        ai_reply = "Mujhe kuch sunai nahi diya. Kripya line par bane rahein."
    else:
        print(f"User Spoke on Phone: {SpeechResult}")
        ai_reply = ask_sarkari_bot(SpeechResult)
    
    # Speak the AI's answer back over the phone
    twiml_response = f"""
    <Response>
        <Say language="hi-IN" voice="Polly.Aditi">{ai_reply}</Say>
    </Response>
    """
    return Response(content=twiml_response, media_type="application/xml")