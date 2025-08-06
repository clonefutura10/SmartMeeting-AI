from datetime import datetime
from flask_login import UserMixin
from utils.supabase_service import supabase_service

def init_models(db):
    """Initialize models with database instance"""
    
    # Define models as classes that will work with Supabase
    class User(UserMixin):
        def __init__(self, id, username, email, password_hash, created_at=None):
            self.id = id
            self.username = username
            self.email = email
            self.password_hash = password_hash
            self.created_at = created_at or datetime.utcnow()
        
        @staticmethod
        def get(user_id):
            """Get user by ID"""
            user_data = supabase_service.get_user(user_id)
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    created_at=user_data.get('created_at')
                )
            return None
        
        @staticmethod
        def get_by_email(email):
            """Get user by email"""
            user_data = supabase_service.get_user_by_email(email)
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    created_at=user_data.get('created_at')
                )
            return None

    class Template:
        def __init__(self, id, title, content, meeting_topic=None, speaker_name=None, 
                     meeting_date=None, meeting_time=None, duration=None, meeting_link=None,
                     location=None, attendees=None, additional_notes=None, meeting_type=None,
                     priority=None, created_at=None, user_id=None):
            self.id = id
            self.title = title
            self.content = content
            self.meeting_topic = meeting_topic
            self.speaker_name = speaker_name
            self.meeting_date = meeting_date
            self.meeting_time = meeting_time
            self.duration = duration
            self.meeting_link = meeting_link
            self.location = location
            self.attendees = attendees
            self.additional_notes = additional_notes
            self.meeting_type = meeting_type
            self.priority = priority
            self.created_at = created_at or datetime.utcnow()
            self.user_id = user_id
        
        @staticmethod
        def query():
            """Return a query-like object for templates"""
            return TemplateQuery()
        
        def save(self):
            """Save template to database"""
            if self.id:
                # Update existing template
                return supabase_service.update_template(self.id, **self.__dict__)
            else:
                # Create new template
                return supabase_service.create_template(self.user_id, self.title, self.content, **self.__dict__)

    class TemplateQuery:
        def __init__(self):
            self.filters = {}
        
        def filter_by(self, **kwargs):
            """Add filters to query"""
            self.filters.update(kwargs)
            return self
        
        def count(self):
            """Count templates matching filters"""
            templates = supabase_service.get_templates()
            # Apply filters (simplified implementation)
            if 'user_id' in self.filters:
                templates = [t for t in templates if t.get('user_id') == self.filters['user_id']]
            return len(templates)
        
        def all(self):
            """Get all templates matching filters"""
            templates = supabase_service.get_templates()
            # Apply filters (simplified implementation)
            if 'user_id' in self.filters:
                templates = [t for t in templates if t.get('user_id') == self.filters['user_id']]
            return [Template(**t) for t in templates]

    class Distribution:
        def __init__(self, id, template_id, method, recipients=None, status='pending',
                     sent_at=None, created_at=None, user_id=None, updated_at=None, **kwargs):
            self.id = id
            self.template_id = template_id
            self.method = method
            self.recipients = recipients
            self.status = status
            self.sent_at = sent_at
            self.created_at = created_at or datetime.utcnow()
            self.user_id = user_id
            self.updated_at = updated_at
        
        @staticmethod
        def query():
            """Return a query-like object for distributions"""
            return DistributionQuery()
        
        def save(self):
            """Save distribution to database"""
            if self.id:
                # Update existing distribution
                return supabase_service.update_distribution_status(self.id, self.status, **self.__dict__)
            else:
                # Create new distribution
                recipients_list = self.recipients if isinstance(self.recipients, list) else []
                return supabase_service.create_distribution(self.user_id, self.template_id, self.method, recipients_list, **self.__dict__)

    class DistributionQuery:
        def __init__(self):
            self.filters = {}
        
        def filter_by(self, **kwargs):
            """Add filters to query"""
            self.filters.update(kwargs)
            return self
        
        def count(self):
            """Count distributions matching filters"""
            distributions = supabase_service.get_distributions()
            # Apply filters (simplified implementation)
            if 'user_id' in self.filters:
                distributions = [d for d in distributions if d.get('user_id') == self.filters['user_id']]
            if 'status' in self.filters:
                distributions = [d for d in distributions if d.get('status') == self.filters['status']]
            if 'method' in self.filters:
                distributions = [d for d in distributions if d.get('method') == self.filters['method']]
            return len(distributions)
        
        def all(self):
            """Get all distributions matching filters"""
            distributions = supabase_service.get_distributions()
            # Apply filters (simplified implementation)
            if 'user_id' in self.filters:
                distributions = [d for d in distributions if d.get('user_id') == self.filters['user_id']]
            if 'status' in self.filters:
                distributions = [d for d in distributions if d.get('status') == self.filters['status']]
            if 'method' in self.filters:
                distributions = [d for d in distributions if d.get('method') == self.filters['method']]
            return [Distribution(**d) for d in distributions]
    
    # Return the model classes
    return User, Template, Distribution 