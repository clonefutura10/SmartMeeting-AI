import json
from datetime import datetime
from typing import Dict, Any, List
import re

class TemplateGenerator:
    """Professional template generator for meeting invitations"""
    
    def __init__(self):
        self.templates = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize all templates"""
        self.templates = {
            'formal_internal': {
                'name': 'Formal Internal Meeting',
                'subject': 'Meeting Invitation: {meeting_topic}',
                'content': self._get_formal_internal_template()
            },
            'casual_internal': {
                'name': 'Casual Internal Meeting',
                'subject': 'Quick Chat: {meeting_topic}',
                'content': self._get_casual_internal_template()
            },
            'client_meeting': {
                'name': 'Client Meeting',
                'subject': 'Meeting Request: {meeting_topic}',
                'content': self._get_client_meeting_template()
            },
            'partner_meeting': {
                'name': 'Partner Meeting',
                'subject': 'Partnership Discussion: {meeting_topic}',
                'content': self._get_partner_meeting_template()
            },
            'vendor_meeting': {
                'name': 'Vendor Meeting',
                'subject': 'Vendor Discussion: {meeting_topic}',
                'content': self._get_vendor_meeting_template()
            },
            'investor_meeting': {
                'name': 'Investor Meeting',
                'subject': 'Investor Update: {meeting_topic}',
                'content': self._get_investor_meeting_template()
            },
            'team_standup': {
                'name': 'Team Standup',
                'subject': 'Daily Standup: {meeting_topic}',
                'content': self._get_team_standup_template()
            },
            'project_review': {
                'name': 'Project Review',
                'subject': 'Project Review: {meeting_topic}',
                'content': self._get_project_review_template()
            }
        }
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get list of available templates"""
        return [
            {'id': key, 'name': template['name']} 
            for key, template in self.templates.items()
        ]
    
    def generate_template(self, template_type: str, **kwargs) -> Dict[str, Any]:
        """Generate a template with the given parameters"""
        if template_type not in self.templates:
            raise ValueError(f"Template type '{template_type}' not found")
        
        # Create the template content directly
        content = self._create_modern_template(
            meeting_topic=kwargs.get('meeting_topic', ''),
            speaker_name=kwargs.get('speaker_name', ''),
            meeting_date=kwargs.get('meeting_date', ''),
            meeting_time=kwargs.get('meeting_time', ''),
            duration=kwargs.get('duration', '30 minutes'),
            meeting_link=kwargs.get('meeting_link', ''),
            location=kwargs.get('location', ''),
            attendees=kwargs.get('attendees', ''),
            additional_notes=kwargs.get('additional_notes', ''),
            priority=kwargs.get('priority', 'Medium'),
            template_type=template_type
        )
        
        # Get the subject from the template
        template = self.templates[template_type]
        subject = template['subject'].format(**kwargs)
        
        return {
            'title': kwargs.get('meeting_topic', 'Meeting Invitation'),
            'content': content,
            'subject': subject,
            'meeting_topic': kwargs.get('meeting_topic', ''),
            'speaker_name': kwargs.get('speaker_name', ''),
            'meeting_date': kwargs.get('meeting_date', ''),
            'meeting_time': kwargs.get('meeting_time', ''),
            'duration': kwargs.get('duration', '30 minutes'),
            'meeting_link': kwargs.get('meeting_link', ''),
            'location': kwargs.get('location', ''),
            'attendees': kwargs.get('attendees', ''),
            'additional_notes': kwargs.get('additional_notes', ''),
            'meeting_type': template_type,
            'priority': kwargs.get('priority', 'Medium')
        }
    
    def _get_formal_internal_template(self) -> str:
        return ""

    def _get_casual_internal_template(self) -> str:
        return ""

    def _get_client_meeting_template(self) -> str:
        return ""

    def _get_partner_meeting_template(self) -> str:
        return ""

    def _get_vendor_meeting_template(self) -> str:
        return ""

    def _get_investor_meeting_template(self) -> str:
        return ""

    def _get_team_standup_template(self) -> str:
        return ""

    def _get_project_review_template(self) -> str:
        return ""

    def _create_modern_template(self, **kwargs) -> str:
        """Create a modern, card-based template with inline CSS for email compatibility"""
        
        # Get template type for styling
        template_type = kwargs.get('template_type', 'formal_internal')
        
        # Determine meeting type label
        meeting_type_labels = {
            'formal_internal': 'TEAM MEETING',
            'casual_internal': 'QUICK CHAT',
            'client_meeting': 'CLIENT MEETING',
            'partner_meeting': 'PARTNER MEETING',
            'vendor_meeting': 'VENDOR MEETING',
            'investor_meeting': 'INVESTOR MEETING',
            'team_standup': 'TEAM STANDUP',
            'project_review': 'PROJECT REVIEW'
        }
        
        meeting_type_label = meeting_type_labels.get(template_type, 'MEETING')
        
        # Get priority color
        priority = kwargs.get('priority', 'Medium')
        if isinstance(priority, str):
            priority = priority.strip()
        priority_colors = {
            'Low': '#28a745',
            'Medium': '#ffc107',
            'High': '#dc3545',
            'Urgent': '#dc3545'
        }
        priority_color = priority_colors.get(priority, '#ffc107')
        
        # Format attendees
        attendees = kwargs.get('attendees', '')
        if isinstance(attendees, list):
            attendees = ', '.join(attendees)
        
        # Get current date for calendar icon
        current_date = datetime.now().day
        
        return f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); overflow: hidden; border: 1px solid #e9ecef;">
            <!-- Header Section -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; color: white;">
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
                    <div style="position: relative; width: 60px; height: 60px; background: rgba(255, 255, 255, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px);">
                        <span style="font-size: 1.5rem; color: white;">📅</span>
                        <span style="position: absolute; top: -5px; right: -5px; background: #dc3545; color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: bold;">{current_date}</span>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <h1 style="font-size: 2rem; font-weight: 700; margin: 0 0 0.5rem 0; color: white;">Meeting Invitation</h1>
                        <p style="font-size: 0.9rem; opacity: 0.9; margin: 0;">SmartMeetingAI • Professional Meeting Coordination</p>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; backdrop-filter: blur(10px);">
                        {meeting_type_label}
                    </div>
                </div>
            </div>
            
            <!-- Meeting Overview -->
            <div style="padding: 2rem; background: #f8f9fa; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #2c3e50; margin: 0; flex: 1; min-width: 200px;">{kwargs.get('meeting_topic', 'Meeting')}</h2>
                <div style="background-color: {priority_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    {priority.upper()} PRIORITY
                </div>
            </div>
            
            <!-- Meeting Details Grid -->
            <div style="padding: 2rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="color: #667eea; font-size: 1.2rem;">📋</span>
                    <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Meeting Details</h3>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                    <div style="background: #f8f9fa; border-radius: 12px; padding: 1.5rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #e9ecef;">
                        <span style="color: #667eea; font-size: 1.5rem; width: 30px; text-align: center;">📅</span>
                        <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                            <span style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">DATE</span>
                            <span style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{kwargs.get('meeting_date', 'TBD')}</span>
                        </div>
                    </div>
                    <div style="background: #f8f9fa; border-radius: 12px; padding: 1.5rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #e9ecef;">
                        <span style="color: #667eea; font-size: 1.5rem; width: 30px; text-align: center;">🕐</span>
                        <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                            <span style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">TIME</span>
                            <span style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{kwargs.get('meeting_time', 'TBD')}</span>
                        </div>
                    </div>
                    <div style="background: #f8f9fa; border-radius: 12px; padding: 1.5rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #e9ecef;">
                        <span style="color: #667eea; font-size: 1.5rem; width: 30px; text-align: center;">⏱️</span>
                        <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                            <span style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">DURATION</span>
                            <span style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{kwargs.get('duration', '30 minutes')}</span>
                        </div>
                    </div>
                    <div style="background: #f8f9fa; border-radius: 12px; padding: 1.5rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #e9ecef;">
                        <span style="color: #667eea; font-size: 1.5rem; width: 30px; text-align: center;">🎤</span>
                        <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                            <span style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">SPEAKER</span>
                            <span style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{kwargs.get('speaker_name', 'TBD')}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Meeting Link Section -->
            {f'''
            <div style="padding: 0 2rem 2rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="color: #667eea; font-size: 1.2rem;">🔗</span>
                    <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Meeting Link</h3>
                </div>
                <a href="{kwargs.get('meeting_link', '#')}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; border: none; cursor: pointer;">
                    Join Meeting
                </a>
            </div>
            ''' if kwargs.get('meeting_link') else ''}
            
            <!-- Location Section -->
            {f'''
            <div style="padding: 0 2rem 2rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="color: #667eea; font-size: 1.2rem;">📍</span>
                    <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Location</h3>
                </div>
                <p style="color: #2c3e50; font-weight: 500; margin: 0; font-size: 1rem;">{kwargs.get('location', 'TBD')}</p>
            </div>
            ''' if kwargs.get('location') else ''}
            
            <!-- Agenda Section -->
            {f'''
            <div style="padding: 0 2rem 2rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="color: #667eea; font-size: 1.2rem;">📄</span>
                    <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Agenda</h3>
                </div>
                <p style="color: #2c3e50; margin: 0; line-height: 1.6;">{kwargs.get('additional_notes', 'Discussing meeting objectives and key points')}</p>
            </div>
            ''' if kwargs.get('additional_notes') else ''}
            
            <!-- Attendees Section -->
            {f'''
            <div style="padding: 0 2rem 2rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="color: #667eea; font-size: 1.2rem;">👥</span>
                    <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Attendees</h3>
                </div>
                <p style="color: #2c3e50; margin: 0; font-weight: 500;">{attendees if attendees else 'To be confirmed'}</p>
            </div>
            ''' if attendees else ''}
            
            <!-- Action Button -->
            <div style="padding: 2rem; text-align: center; background: #f8f9fa;">
                <button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 1rem 2rem; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer;">
                    Confirm Attendance
                </button>
            </div>
            
            <!-- Footer -->
            <div style="background: #343a40; color: white; padding: 1.5rem 2rem; text-align: center;">
                <p style="margin: 0.25rem 0; font-size: 0.9rem; opacity: 0.9;">Generated by SmartMeetingAI • Professional Meeting Coordination</p>
                <p style="margin: 0.25rem 0; font-size: 0.9rem; opacity: 0.9;">Please respond to confirm your attendance</p>
            </div>
        </div>
        """

# Global instance
template_generator = TemplateGenerator() 