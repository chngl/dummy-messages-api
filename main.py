from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import time
import random

app = FastAPI(title="Dummy Messages API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class Context(BaseModel):
    user_id: str
    sys_prompt: Optional[str] = None
    historical_messages: Optional[List[str]] = []

class MessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    channel: str
    attachment_1: Optional[str] = None
    attachment_2: Optional[str] = None
    context: Context

# Response Model
class MessageResponse(BaseModel):
    message_id: str
    response: str
    conversation_id: str
    page_id: str
    timestamp: int
    handoff_reason: Optional[str] = None
    quick_reply_pills: List[str]
    images: List[str]
    admin_text: str

# Mock data generators
def generate_response(message: str, channel: str) -> str:
    templates = [
        f"Thank you for your message: '{message}'. How can I assist you further?",
        f"I received your inquiry via {channel}. Let me help you with that.",
        f"Based on your message, here's what I found...",
        f"Great question! Regarding '{message}', I can provide the following information.",
        f"I understand you're asking about this via {channel}. Here's my response."
    ]
    return random.choice(templates)

def generate_handoff_reason() -> Optional[str]:
    if random.random() < 0.3:  # 30% chance
        reasons = ["complex_inquiry", "escalation_requested", "technical_support_needed", "billing_issue"]
        return random.choice(reasons)
    return None

def generate_quick_replies() -> List[str]:
    all_replies = ["Yes, please", "No, thanks", "Tell me more", "Contact support", 
                   "Check status", "View details", "Get help", "Learn more"]
    count = random.randint(2, 4)
    return random.sample(all_replies, count)

def generate_images() -> List[str]:
    if random.random() < 0.4:  # 40% chance
        count = random.randint(1, 2)
        return [f"https://picsum.photos/400/300?random={random.randint(1, 1000)}" for _ in range(count)]
    return []

def generate_admin_text(user_id: str, channel: str, conversation_id: str) -> str:
    templates = [
        f"New message received from user {user_id}",
        f"User inquiry via {channel} - response sent",
        f"Conversation {conversation_id} updated",
        f"Message processed for user {user_id} on {channel}"
    ]
    return random.choice(templates)

@app.get("/")
def read_root():
    return {
        "message": "Dummy Messages API",
        "version": "1.0.0",
        "endpoints": {
            "POST /{page_id}/messages": "Send a message and receive a response"
        }
    }

@app.post("/{page_id}/messages", response_model=MessageResponse)
def create_message(page_id: str, request: MessageRequest):
    # Generate or use existing conversation_id
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    # Generate message_id
    message_id = str(uuid.uuid4())
    
    # Generate timestamp
    timestamp = int(time.time())
    
    # Generate response
    response_text = generate_response(request.message, request.channel)
    
    # Generate optional handoff reason
    handoff_reason = generate_handoff_reason()
    
    # Generate quick reply pills
    quick_reply_pills = generate_quick_replies()
    
    # Generate images
    images = generate_images()
    
    # Generate admin text
    admin_text = generate_admin_text(
        request.context.user_id,
        request.channel,
        conversation_id
    )
    
    return MessageResponse(
        message_id=message_id,
        response=response_text,
        conversation_id=conversation_id,
        page_id=page_id,
        timestamp=timestamp,
        handoff_reason=handoff_reason,
        quick_reply_pills=quick_reply_pills,
        images=images,
        admin_text=admin_text
    )

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": int(time.time())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
