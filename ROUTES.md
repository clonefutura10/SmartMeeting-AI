# API Routes Documentation

Complete API documentation for SmartMeeting AI.

## 🔐 Authentication

All routes except `/auth` and `/api/health` require authentication.

## 📋 Core Routes

### Authentication

| Method | Route | Description | Request Body | Response |
|--------|-------|-------------|--------------|----------|
| `GET` | `/auth` | Login page | - | HTML page |
| `POST` | `/auth` | Login/Register | `{"action": "login", "email": "...", "password": "..."}` | `{"success": true, "redirect": "..."}` |
| `GET` | `/logout` | Logout user | - | Redirect to auth |

### Dashboard

| Method | Route | Description | Response |
|--------|-------|-------------|----------|
| `GET` | `/` | Main dashboard | HTML page with stats |

### Template Management

| Method | Route | Description | Request Body | Response |
|--------|-------|-------------|--------------|----------|
| `GET` | `/template-generator` | Template creation page | - | HTML page |
| `POST` | `/api/templates/generate` | Generate new template | Meeting details | `{"success": true, "template": "...", "template_id": "..."}` |
| `GET` | `/api/templates/available` | Get template types | - | `{"success": true, "templates": [...]}` |
| `GET` | `/api/templates/{id}/download` | Download template | - | HTML file |

### Distribution

| Method | Route | Description | Request Body | Response |
|--------|-------|-------------|--------------|----------|
| `GET` | `/distribution` | Distribution page | - | HTML page |
| `POST` | `/api/distribution/gmail` | Send Gmail invitation | `{"templateId": "...", "recipientEmails": [...], "subject": "..."}` | `{"success": true, "message": "..."}` |
| `POST` | `/api/distribution/whatsapp` | Send WhatsApp message | `{"templateId": "...", "phoneNumber": "..."}` | `{"success": true, "message": "..."}` |

## 📊 Data Management

### Meetings

| Method | Route | Description | Response |
|--------|-------|-------------|----------|
| `GET` | `/api/meetings` | Get all meetings | `{"success": true, "meetings": [...]}` |
| `GET` | `/api/meetings/{id}` | Get specific meeting | `{"success": true, "meeting": {...}}` |
| `GET` | `/api/meetings/upcoming` | Get upcoming meetings | `{"success": true, "meetings": [...]}` |

### Contacts

| Method | Route | Description | Query Params | Response |
|--------|-------|-------------|--------------|----------|
| `GET` | `/api/contacts` | Get all contacts | `member_type` (optional) | `{"success": true, "contacts": [...]}` |
| `GET` | `/api/contacts/internal` | Get internal members | - | `{"success": true, "contacts": [...]}` |
| `GET` | `/api/contacts/external` | Get external contacts | - | `{"success": true, "contacts": [...]}` |
| `POST` | `/api/contacts` | Add new contact | Contact details | `{"success": true, "contact": {...}}` |

### Organizations

| Method | Route | Description | Response |
|--------|-------|-------------|----------|
| `GET` | `/api/organizations` | Get all organizations | `{"success": true, "organizations": [...]}` |

## 🔧 System

| Method | Route | Description | Response |
|--------|-------|-------------|----------|
| `GET` | `/api/health` | Health check | `{"status": "OK", "timestamp": "...", "version": "..."}` |

## 📝 Request Examples

### Generate Template
```bash
curl -X POST http://localhost:5001/api/templates/generate \
  -H "Content-Type: application/json" \
  -d '{
    "meetingTopic": "Project Review",
    "speakerName": "John Doe",
    "date": "2024-01-15",
    "time": "14:00",
    "duration": "60 minutes",
    "templateType": "formal_internal"
  }'
```

### Send Gmail Invitation
```bash
curl -X POST http://localhost:5001/api/distribution/gmail \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "template-uuid",
    "recipientEmails": ["user@example.com"],
    "subject": "Meeting Invitation"
  }'
```

### Get Contacts
```bash
curl -X GET "http://localhost:5001/api/contacts?member_type=internal"
```

## 📊 Response Formats

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description"
}
```

### Template Response
```json
{
  "success": true,
  "template": "<html>...</html>",
  "template_id": "uuid",
  "message": "Template generated successfully"
}
```

### Contact Response
```json
{
  "success": true,
  "contacts": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "name": "User Name",
      "member_type": "internal",
      "status": "active"
    }
  ]
}
```

## 🔒 Authentication Details

### Login Process
1. User submits email/password to `/auth` (POST)
2. System creates/retrieves user from contacts table
3. User is logged in via Flask-Login
4. Redirected to dashboard

### Session Management
- Sessions managed by Flask-Login
- User ID stored in session
- Automatic logout on session expiry

## 🚨 Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `400` | Bad Request | Check request body format |
| `401` | Unauthorized | Login required |
| `404` | Not Found | Resource doesn't exist |
| `500` | Server Error | Check server logs |

## 🔧 Development Notes

### Database Integration
- All routes use Supabase service
- UUIDs for all primary keys
- Automatic error handling

### Frontend Integration
- AJAX calls for dynamic updates
- Real-time form validation
- Responsive design with Bootstrap 5

### Security
- CSRF protection enabled
- Input validation on all routes
- SQL injection prevention via Supabase

---

**Base URL**: `http://localhost:5001` (development)
**Content-Type**: `application/json` for POST requests
**Authentication**: Session-based via Flask-Login 