# RAG API Endpoints Guide

## Two Different Endpoints

Your RAG API has **two different endpoints** for queries:

### 1. `/api/chat` - Public Chat Endpoint (For Laravel Widget)
- **Purpose**: Used by the Laravel chat widget
- **Authentication**: None required (public)
- **Field Name**: `query`
- **Use Case**: Frontend chat widget

**Example:**
```json
POST /api/chat
{
  "query": "What programs do you offer?"
}
```

**Response:**
```json
{
  "answer": "We offer two main programs..."
}
```

---

### 2. `/query` - Authenticated Query Endpoint
- **Purpose**: For authenticated API calls
- **Authentication**: Required (`X-API-Key` header)
- **Field Name**: `question` (not `query`!)
- **Use Case**: Backend integrations, admin tools

**Example:**
```bash
POST /query
Headers:
  X-API-Key: htcodehub-2024
  Content-Type: application/json

Body:
{
  "question": "What programs do you offer?",
  "dataset_name": "htcodehub"
}
```

**Response:**
```json
{
  "answer": "We offer two main programs...",
  "sources": [
    {
      "content": "...",
      "metadata": {...}
    }
  ]
}
```

---

## Key Differences

| Feature | `/api/chat` | `/query` |
|---------|-------------|----------|
| **Auth Required** | ❌ No | ✅ Yes (X-API-Key) |
| **Field Name** | `query` | `question` |
| **Dataset Name** | Optional (defaults to htcodehub) | Required |
| **Sources** | ❌ No | ✅ Yes |
| **Use Case** | Frontend widget | Backend/admin |

---

## Common Errors

### Error: "Missing 'question' field"
**Cause**: Using `/query` endpoint but sending `query` instead of `question`
**Fix**: Change field name to `question`

### Error: "Invalid API key"
**Cause**: Missing or wrong `X-API-Key` header for `/query`
**Fix**: Add header: `X-API-Key: htcodehub-2024`

### Error: "Missing 'dataset_name' field"
**Cause**: Using `/query` without `dataset_name`
**Fix**: Add `dataset_name: "htcodehub"` to request body

---

## Testing

### Test `/api/chat` (Public):
```powershell
# PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query":"What programs do you offer?"}'
```

### Test `/query` (Authenticated):
```powershell
# PowerShell
$headers = @{
    "X-API-Key" = "htcodehub-2024"
    "Content-Type" = "application/json"
}
$body = @{
    question = "What programs do you offer?"
    dataset_name = "htcodehub"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/query" `
  -Method POST `
  -Headers $headers `
  -Body $body
```

Or use the test scripts:
```powershell
# Test /api/chat
python test_chat_api.py

# Test /query
python test_query_endpoint.py
```

---

## For Laravel Widget

**Use `/api/chat`** - It's already configured correctly in:
- `ChatController.php` - Calls `/api/chat`
- `chat-widget.js` - Sends `query` field

No changes needed! ✅

