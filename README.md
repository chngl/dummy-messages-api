# Dummy Messages API

A dummy API endpoint for testing message handling with mock responses.

## API Endpoint

**Base URL:** `https://your-render-url.onrender.com`

### POST `/{page_id}/messages`

Send a message and receive a mock response.

#### Request Body

```json
{
  "conversation_id": "optional-conversation-id",
  "message": "Your message here",
  "channel": "Messenger",
  "attachment_1": "optional-url",
  "attachment_2": "optional-url",
  "context": {
    "user_id": "user123",
    "sys_prompt": "optional system prompt",
    "historical_messages": ["message1", "message2"]
  }
}
```

#### Response

```json
{
  "message_id": "uuid",
  "response": "Mock response text",
  "conversation_id": "uuid",
  "page_id": "page123",
  "timestamp": 1234567890,
  "handoff_reason": "optional reason",
  "quick_reply_pills": ["Yes, please", "No, thanks"],
  "images": ["https://example.com/image.jpg"],
  "admin_text": "Admin notification text"
}
```

## Deployment

This API is deployed on Render.com using the free tier.

## Local Development

```bash
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`
