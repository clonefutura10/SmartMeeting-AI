from supabase import create_client, Client
from typing import List, Dict, Optional, Any
import json
from datetime import datetime, date
from config import config
import os

class SupabaseService:
    def __init__(self):
        config_name = os.environ.get('FLASK_ENV', 'production')
        app_config = config[config_name]
        
        self.supabase: Client = create_client(
            app_config.SUPABASE_URL,
            app_config.SUPABASE_ANON_KEY
        )
    
    # Contact Management
    def get_contacts(self, member_type: Optional[str] = None) -> List[Dict]:
        """Get all contacts, optionally filtered by member type"""
        query = self.supabase.table('contacts').select('*')
        
        if member_type:
            query = query.eq('member_type', member_type)
        
        response = query.execute()
        return response.data if response.data else []
    
    def get_internal_members(self) -> List[Dict]:
        """Get all internal members"""
        return self.get_contacts('internal')
    
    def get_external_contacts(self) -> List[Dict]:
        """Get all external contacts"""
        return self.get_contacts('external')
    
    def add_contact(self, email: str, name: str, member_type: str = 'external', 
                   organization_id: Optional[str] = None) -> Dict:
        """Add a new contact"""
        contact_data = {
            'email': email,
            'name': name,
            'member_type': member_type,
            'organization_id': organization_id
        }
        
        response = self.supabase.table('contacts').insert(contact_data).execute()
        return response.data[0] if response.data else None
    
    def update_contact(self, contact_id: str, **kwargs) -> Dict:
        """Update a contact"""
        response = self.supabase.table('contacts').update(kwargs).eq('id', contact_id).execute()
        return response.data[0] if response.data else None
    
    def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact"""
        response = self.supabase.table('contacts').delete().eq('id', contact_id).execute()
        return len(response.data) > 0 if response.data else False
    
    # Meeting Management (for Module 1)
    def get_meetings(self, organization_id: Optional[str] = None) -> List[Dict]:
        """Get all meetings, optionally filtered by organization"""
        query = self.supabase.table('meetings').select('*')
        
        if organization_id:
            query = query.eq('organization_id', organization_id)
        
        response = query.execute()
        return response.data if response.data else []
    
    def get_meeting(self, meeting_id: str) -> Optional[Dict]:
        """Get a specific meeting"""
        response = self.supabase.table('meetings').select('*').eq('id', meeting_id).execute()
        return response.data[0] if response.data else None
    
    def get_meeting_with_attendees(self, meeting_id: str) -> Optional[Dict]:
        """Get meeting details with attendee information"""
        # Get meeting details
        meeting_response = self.supabase.table('meetings').select('*').eq('id', meeting_id).execute()
        if not meeting_response.data:
            return None
        
        meeting = meeting_response.data[0]
        
        # Get attendees
        attendees_response = self.supabase.table('meeting_attendees').select('attendees').eq('meeting_id', meeting_id).execute()
        attendees = attendees_response.data[0]['attendees'] if attendees_response.data else []
        
        meeting['attendees'] = attendees
        return meeting
    
    def get_upcoming_meetings(self, organization_id: Optional[str] = None) -> List[Dict]:
        """Get upcoming meetings"""
        query = self.supabase.table('meetings').select('*').gte('scheduled_at', datetime.utcnow().isoformat())
        
        if organization_id:
            query = query.eq('organization_id', organization_id)
        
        response = query.order('scheduled_at').execute()
        return response.data if response.data else []
    
    def create_meeting(self, organization_id: str, meeting_code: str, title: str, 
                      scheduled_at: str, duration_mins: int = 30, description: str = None) -> Dict:
        """Create a new meeting"""
        meeting_data = {
            'organization_id': organization_id,
            'meeting_code': meeting_code,
            'title': title,
            'scheduled_at': scheduled_at,
            'duration_mins': duration_mins,
            'description': description
        }
        
        response = self.supabase.table('meetings').insert(meeting_data).execute()
        return response.data[0] if response.data else None
    
    def update_meeting(self, meeting_id: str, **kwargs) -> Dict:
        """Update a meeting"""
        response = self.supabase.table('meetings').update(kwargs).eq('id', meeting_id).execute()
        return response.data[0] if response.data else None
    
    def delete_meeting(self, meeting_id: str) -> bool:
        """Delete a meeting"""
        response = self.supabase.table('meetings').delete().eq('id', meeting_id).execute()
        return len(response.data) > 0 if response.data else False
    
    # Template Management (mapped to meetings and meeting_minutes)
    def create_template(self, user_id: str, title: str, content: str, **kwargs) -> Dict:
        """Create a new template (stored as meeting with minutes)"""
        try:
            # First create a meeting marked as template
            meeting_data = {
                'organization_id': None,  # Will be set later if needed
                'meeting_code': f"TEMPLATE_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                'title': title,
                'scheduled_at': kwargs.get('meeting_date', datetime.utcnow().isoformat()),
                'duration_mins': int(kwargs.get('duration', '30').split()[0]) if isinstance(kwargs.get('duration'), str) else kwargs.get('duration', 30),
                'description': kwargs.get('additional_notes', ''),
                'is_template': True,
                'template_type': 'meeting'
            }
            
            meeting_response = self.supabase.table('meetings').insert(meeting_data).execute()
            meeting = meeting_response.data[0] if meeting_response.data else None
            
            if meeting:
                # Create meeting minutes with the template content
                minutes_data = {
                    'meeting_id': meeting['id'],
                    'summary': kwargs.get('additional_notes', ''),
                    'full_mom': content,
                    'created_by': user_id
                }
                
                minutes_response = self.supabase.table('meeting_minutes').insert(minutes_data).execute()
                
                # Return combined data
                return {
                    'id': meeting['id'],
                    'title': title,
                    'content': content,
                    'user_id': user_id,
                    **kwargs
                }
            
            return None
        except Exception as e:
            if 'column meetings.is_template does not exist' in str(e):
                print("Warning: is_template column does not exist. Please add it to your meetings table.")
                print("SQL command to run in Supabase: ALTER TABLE meetings ADD COLUMN is_template BOOLEAN DEFAULT FALSE;")
                return None
            else:
                raise e
    
    def get_templates(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get templates (meetings with is_template=True)"""
        try:
            # Query meetings that are templates
            query = self.supabase.table('meetings').select('*, meeting_minutes(*)').eq('is_template', True)
            
            if user_id:
                # Filter by created_by in meeting_minutes
                minutes_query = self.supabase.table('meeting_minutes').select('meeting_id, created_by').eq('created_by', user_id).execute()
                meeting_ids = [item['meeting_id'] for item in minutes_query.data] if minutes_query.data else []
                
                if meeting_ids:
                    response = query.in_('id', meeting_ids).execute()
                else:
                    return []
            else:
                response = query.execute()
            
            templates = []
            for meeting in response.data if response.data else []:
                if meeting.get('meeting_minutes'):
                    minutes = meeting['meeting_minutes']
                    templates.append({
                        'id': meeting['id'],
                        'title': meeting['title'],
                        'content': minutes.get('full_mom', ''),
                        'user_id': minutes.get('created_by'),
                        'meeting_topic': meeting['title'],
                        'meeting_date': meeting['scheduled_at'],
                        'duration': f"{meeting['duration_mins']} minutes",
                        'additional_notes': minutes.get('summary', '')
                    })
            
            return templates
        except Exception as e:
            if 'column meetings.is_template does not exist' in str(e):
                print("Warning: is_template column does not exist. Please add it to your meetings table.")
                print("SQL command to run in Supabase: ALTER TABLE meetings ADD COLUMN is_template BOOLEAN DEFAULT FALSE;")
                return []
            else:
                raise e
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get a specific template"""
        try:
            response = self.supabase.table('meetings').select('*, meeting_minutes(*)').eq('id', template_id).eq('is_template', True).execute()
            if response.data:
                meeting = response.data[0]
                if meeting.get('meeting_minutes'):
                    minutes = meeting['meeting_minutes']
                    return {
                        'id': meeting['id'],
                        'title': meeting['title'],
                        'content': minutes.get('full_mom', ''),
                        'user_id': minutes.get('created_by'),
                        'meeting_topic': meeting['title'],
                        'meeting_date': meeting['scheduled_at'],
                        'duration': f"{meeting['duration_mins']} minutes",
                        'additional_notes': minutes.get('summary', '')
                    }
            return None
        except Exception as e:
            if 'column meetings.is_template does not exist' in str(e):
                print("Warning: is_template column does not exist. Please add it to your meetings table.")
                print("SQL command to run in Supabase: ALTER TABLE meetings ADD COLUMN is_template BOOLEAN DEFAULT FALSE;")
                return None
            else:
                raise e
    
    def update_template(self, template_id: str, **kwargs) -> Dict:
        """Update a template"""
        # Update meeting
        meeting_updates = {}
        if 'title' in kwargs:
            meeting_updates['title'] = kwargs['title']
        if 'meeting_date' in kwargs:
            meeting_updates['scheduled_at'] = kwargs['meeting_date']
        if 'duration' in kwargs:
            duration_str = kwargs['duration']
            if isinstance(duration_str, str) and 'minutes' in duration_str:
                meeting_updates['duration_mins'] = int(duration_str.split()[0])
        
        if meeting_updates:
            self.supabase.table('meetings').update(meeting_updates).eq('id', template_id).execute()
        
        # Update meeting minutes
        minutes_updates = {}
        if 'content' in kwargs:
            minutes_updates['full_mom'] = kwargs['content']
        if 'additional_notes' in kwargs:
            minutes_updates['summary'] = kwargs['additional_notes']
        
        if minutes_updates:
            self.supabase.table('meeting_minutes').update(minutes_updates).eq('meeting_id', template_id).execute()
        
        return self.get_template(template_id)
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template"""
        # Delete meeting minutes first
        self.supabase.table('meeting_minutes').delete().eq('meeting_id', template_id).execute()
        # Delete meeting
        response = self.supabase.table('meetings').delete().eq('id', template_id).execute()
        return len(response.data) > 0 if response.data else False
    
    # Distribution Management
    def create_distribution(self, user_id: str, template_id: str, method: str, 
                          recipients: List[str], **kwargs) -> Dict:
        """Create a new distribution record"""
        
        # Insert into social_posts table
        distribution_data = {
            'meeting_id': template_id,
            'platforms': json.dumps([method]),
            'status': kwargs.get('status', 'pending'),
            'published_at': kwargs.get('sent_at') if kwargs.get('status') == 'sent' else None
        }
        
        response = self.supabase.table('social_posts').insert(distribution_data).execute()
        
        if response.data:
            distribution_id = response.data[0]['id']
            
            # Store recipients in meeting_attendees table
            recipients_data = kwargs.get('formatted_recipients')
            if recipients_data:
                try:
                    recipients_list = json.loads(recipients_data) if isinstance(recipients_data, str) else recipients_data
                    
                    # Check if attendees record exists for this meeting
                    existing_response = self.supabase.table('meeting_attendees').select('*').eq('meeting_id', template_id).execute()
                    
                    if existing_response.data:
                        # Update existing record
                        attendee_record = existing_response.data[0]
                        current_attendees = attendee_record.get('attendees', [])
                        # Add new recipients to existing attendees
                        current_attendees.extend(recipients_list)
                        
                        self.supabase.table('meeting_attendees').update({
                            'attendees': current_attendees
                        }).eq('meeting_id', template_id).execute()
                    else:
                        # Create new attendees record
                        attendee_data = {
                            'meeting_id': template_id,
                            'attendees': recipients_list
                        }
                        self.supabase.table('meeting_attendees').insert(attendee_data).execute()
                        
                except Exception as e:
                    print(f"Error storing recipients: {e}")
            
            return response.data[0]
        
        return None
    
    def get_distributions(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get distributions with recipients"""
        
        # Get distributions from social_posts
        query = self.supabase.table('social_posts').select('*')
        response = query.execute()
        
        distributions = []
        for post in response.data if response.data else []:
            # Get recipients from meeting_attendees
            attendees_response = self.supabase.table('meeting_attendees').select('attendees').eq('meeting_id', post['meeting_id']).execute()
            
            recipients = []
            if attendees_response.data and attendees_response.data[0].get('attendees'):
                recipients = attendees_response.data[0]['attendees']
            
            # Get the user_id from meeting_minutes to filter by user if needed
            if user_id:
                minutes_response = self.supabase.table('meeting_minutes').select('created_by').eq('meeting_id', post['meeting_id']).execute()
                if minutes_response.data:
                    created_by = minutes_response.data[0]['created_by']
                    if created_by != user_id:
                        continue
                else:
                    continue
                user_id_for_record = created_by
            else:
                # Get user_id for the record
                minutes_response = self.supabase.table('meeting_minutes').select('created_by').eq('meeting_id', post['meeting_id']).execute()
                user_id_for_record = minutes_response.data[0]['created_by'] if minutes_response.data else None
            
            distributions.append({
                'id': post['id'],
                'template_id': post['meeting_id'],
                'method': json.loads(post['platforms'])[0] if post['platforms'] else 'unknown',
                'recipients': json.dumps(recipients),
                'status': post['status'],
                'sent_at': post['published_at'],
                'created_at': post['created_at'],
                'updated_at': post['updated_at'],
                'user_id': user_id_for_record
            })
        
        return distributions
    
    def update_distribution_status(self, distribution_id: str, status: str, **kwargs) -> Dict:
        """Update distribution status"""
        update_data = {'status': status}
        if status == 'sent':
            update_data['published_at'] = datetime.utcnow().isoformat()
        
        response = self.supabase.table('social_posts').update(update_data).eq('id', distribution_id).execute()
        return response.data[0] if response.data else None
    
    # User Management (mapped to contacts)
    def create_user(self, username: str, email: str, password_hash: str) -> Dict:
        """Create a new user (stored as contact)"""
        user_data = {
            'email': email,
            'name': username,
            'member_type': 'internal',
            'status': 'active'
        }
        
        response = self.supabase.table('contacts').insert(user_data).execute()
        return response.data[0] if response.data else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        response = self.supabase.table('contacts').select('*').eq('email', email).execute()
        if response.data:
            contact = response.data[0]
            return {
                'id': contact['id'],
                'username': contact['name'],
                'email': contact['email'],
                'password_hash': 'hashed_password',  # We'll need to handle this differently
                'created_at': contact['created_at']
            }
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username (name in contacts)"""
        response = self.supabase.table('contacts').select('*').eq('name', username).execute()
        if response.data:
            contact = response.data[0]
            return {
                'id': contact['id'],
                'username': contact['name'],
                'email': contact['email'],
                'password_hash': 'hashed_password',  # We'll need to handle this differently
                'created_at': contact['created_at']
            }
        return None
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        response = self.supabase.table('contacts').select('*').eq('id', user_id).execute()
        if response.data:
            contact = response.data[0]
            return {
                'id': contact['id'],
                'username': contact['name'],
                'email': contact['email'],
                'password_hash': 'hashed_password',  # We'll need to handle this differently
                'created_at': contact['created_at']
            }
        return None
    
    # Organization Management
    def get_organizations(self) -> List[Dict]:
        """Get all organizations"""
        response = self.supabase.table('organizations').select('*').execute()
        return response.data if response.data else []
    
    def get_organization(self, organization_id: str) -> Optional[Dict]:
        """Get a specific organization"""
        response = self.supabase.table('organizations').select('*').eq('id', organization_id).execute()
        return response.data[0] if response.data else None
    
    def create_organization(self, name: str, domain: str = None) -> Dict:
        """Create a new organization"""
        org_data = {
            'name': name,
            'domain': domain
        }
        
        response = self.supabase.table('organizations').insert(org_data).execute()
        return response.data[0] if response.data else None
    
    # Demo data initialization
    def initialize_demo_contacts(self):
        """Initialize demo contacts for testing"""
        # First, ensure we have a demo organization
        try:
            org_response = self.supabase.table('organizations').select('id').eq('name', 'Demo Company').execute()
            if not org_response.data:
                org_response = self.supabase.table('organizations').insert({
                    'name': 'Demo Company',
                    'domain': 'demo.com'
                }).execute()
                organization_id = org_response.data[0]['id']
            else:
                organization_id = org_response.data[0]['id']
        except Exception as e:
            print(f"Error with organization: {e}")
            organization_id = None
        
        demo_contacts = [
            # Internal members
            {'email': 'john.doe@company.com', 'name': 'John Doe', 'member_type': 'internal', 'organization_id': organization_id},
            {'email': 'jane.smith@company.com', 'name': 'Jane Smith', 'member_type': 'internal', 'organization_id': organization_id},
            {'email': 'mike.johnson@company.com', 'name': 'Mike Johnson', 'member_type': 'internal', 'organization_id': organization_id},
            {'email': 'sarah.wilson@company.com', 'name': 'Sarah Wilson', 'member_type': 'internal', 'organization_id': organization_id},
            {'email': 'david.brown@company.com', 'name': 'David Brown', 'member_type': 'internal', 'organization_id': organization_id},
            
            # External contacts
            {'email': 'client1@external.com', 'name': 'Client One', 'member_type': 'external', 'organization_id': organization_id},
            {'email': 'client2@external.com', 'name': 'Client Two', 'member_type': 'external', 'organization_id': organization_id},
            {'email': 'partner1@partner.com', 'name': 'Partner One', 'member_type': 'external', 'organization_id': organization_id},
            {'email': 'partner2@partner.com', 'name': 'Partner Two', 'member_type': 'external', 'organization_id': organization_id},
            {'email': 'vendor1@vendor.com', 'name': 'Vendor One', 'member_type': 'external', 'organization_id': organization_id},
            {'email': 'consultant@consulting.com', 'name': 'External Consultant', 'member_type': 'external', 'organization_id': organization_id},
            {'email': 'investor@investments.com', 'name': 'Investor Contact', 'member_type': 'external', 'organization_id': organization_id},
        ]
        
        for contact in demo_contacts:
            try:
                # Check if contact already exists
                existing = self.supabase.table('contacts').select('id').eq('email', contact['email']).execute()
                if not existing.data:
                    self.add_contact(**contact)
            except Exception as e:
                # Contact might already exist, skip silently
                continue

    def ensure_database_schema(self):
        """Ensure all required database columns exist"""
        try:
            # Check if is_template column exists in meetings table
            # We'll try to query it and see if it fails
            test_query = self.supabase.table('meetings').select('is_template').limit(1).execute()
            print("Database schema is up to date")
        except Exception as e:
            if 'column meetings.is_template does not exist' in str(e):
                print("⚠️  Missing database column detected!")
                print("The 'is_template' column is missing from your meetings table.")
                print("")
                print("To fix this, please run the following SQL command in your Supabase dashboard:")
                print("")
                print("ALTER TABLE meetings ADD COLUMN is_template BOOLEAN DEFAULT FALSE;")
                print("")
                print("After running this command, restart your application.")
                print("The application will continue to work but template functionality will be limited.")
            else:
                print(f"Database schema check error: {e}")

# Global instance
supabase_service = SupabaseService() 