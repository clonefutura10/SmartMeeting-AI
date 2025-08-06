# SmartMeeting AI

A modern meeting management application with AI-powered template generation and multi-channel distribution.

## 🚀 Features

- **AI Template Generation**: Create professional meeting invitations
- **Multi-Channel Distribution**: Send via Gmail, WhatsApp, and more
- **Contact Management**: Internal and external contact organization
- **Cloud Database**: Supabase-powered scalable backend
- **Modern UI**: Responsive design with Bootstrap 5

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.10+
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **Email**: Gmail API integration
- **Messaging**: WhatsApp API integration

## 📋 Quick Start

### Prerequisites
- Python 3.10+
- Supabase account
- Gmail account (for email distribution)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartMeeting-AI
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Create .env file in backend/
   SUPABASE_URL=your-supabase-url
   SUPABASE_ANON_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   GMAIL_USER=your-email@gmail.com
   GMAIL_PASSWORD=your-app-password
   ```

4. **Set up database**
   - Run the SQL commands from `SUPABASE_MIGRATION.md` in your Supabase SQL Editor

5. **Start the application**
   ```bash
   python main.py
   ```

6. **Access the application**
   - Open http://localhost:5001
   - Login with any email/password (demo mode)

## 📖 Usage

### Template Generation
1. Navigate to "Template Generator"
2. Fill in meeting details
3. Select template type
4. Generate professional invitation

### Distribution
1. Go to "Distribution" page
2. Select a template
3. Choose recipients (contacts or manual emails)
4. Send via Gmail or WhatsApp

### Contact Management
- Internal members: Company employees
- External contacts: Clients, partners, vendors
- Automatic categorization and filtering

## 🔧 Configuration

### Environment Variables
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
WHATSAPP_API_KEY=your-whatsapp-api-key
WHATSAPP_PHONE_NUMBER=your-whatsapp-number
```

### Database Schema
- **contacts**: User and contact management
- **meetings**: Meeting and template storage
- **meeting_minutes**: Template content and summaries
- **social_posts**: Distribution tracking
- **organizations**: Company/team management

## 🚀 Deployment

### Local Development
```bash
cd backend
python main.py
```

### Production
```bash
cd backend
python run.py
```

## 📚 Documentation

- [API Routes](ROUTES.md) - Complete API documentation
- [Database Schema](SUPABASE_MIGRATION.md) - Database setup and schema
- [Migration Guide](MIGRATION_SUMMARY.md) - SQLite to Supabase migration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with details

---

**SmartMeeting AI** - Making meeting management effortless with AI-powered automation.
