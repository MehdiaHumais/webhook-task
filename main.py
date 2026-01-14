from fastapi import FastAPI, HTTPException, Header, Depends, Response
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional

# --- CONFIGURATION ---
SECRET_TOKEN = "my-secret-key"
SQLALCHEMY_DATABASE_URL = "sqlite:///./webhook_data.db"

# --- DATABASE SETUP ---
# check_same_thread=False is required for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DATABASE MODEL ---
class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)  # Unique ID for Idempotency
    payload = Column(String)

# --- PYDANTIC MODEL (VALIDATION) ---
class WebhookPayload(BaseModel):
    event_id: str
    payload: str

# --- DEPENDENCIES ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_signature(x_signature: Optional[str] = Header(None)):
    if x_signature != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing X-Signature")
    return x_signature

# --- APP INITIALIZATION ---
Base.metadata.create_all(bind=engine) # Creates tables on startup

app = FastAPI(title="Webhook Receiver")

# --- ENDPOINTS ---
@app.post("/webhook", status_code=201)
def handle_webhook(
    data: WebhookPayload, 
    response: Response,
    db: Session = Depends(get_db), 
    _: str = Depends(verify_signature)
):
    # 1. Idempotency Check
    existing = db.query(WebhookEvent).filter(WebhookEvent.event_id == data.event_id).first()
    
    if existing:
        response.status_code = 200  # Return 200 OK for duplicates
        return {
            "status": "ignored", 
            "message": "Event already processed", 
            "event_id": data.event_id
        }

    # 2. Save Data
    new_event = WebhookEvent(event_id=data.event_id, payload=data.payload)
    try:
        db.add(new_event)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database write failed")
    
    return {"status": "success", "message": "Data saved", "event_id": data.event_id}

@app.get("/")
def home():
    return {"message": "Service is running."}