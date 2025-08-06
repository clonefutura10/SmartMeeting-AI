import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smartmeeting-ai-production-secret-key-2024')
    
    # Supabase Configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://your-project.supabase.co')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', 'your-anon-key')
    SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', 'your-service-role-key')
    
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Template Configuration
    DEFAULT_TEMPLATE_TYPE = 'formal_internal'
    
    # Gmail Integration
    GMAIL_USER = os.environ.get('GMAIL_USER', 'your-email@gmail.com')
    GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', 'your-app-password')
    
    # WhatsApp Integration
    WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY', 'your-whatsapp-api-key')
    WHATSAPP_PHONE_NUMBER = os.environ.get('WHATSAPP_PHONE_NUMBER', 'your-whatsapp-phone-number')

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
} 