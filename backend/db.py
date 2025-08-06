from utils.supabase_service import supabase_service

# Initialize Supabase service
def init_db(app):
    """Initialize database with Flask app"""
    # Supabase is already initialized in supabase_service
    return supabase_service

def get_db():
    """Get database instance"""
    return supabase_service 