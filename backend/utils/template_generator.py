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
        """Create a modern, card-based template"""
        
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
        <div class="modern-meeting-card">
            <!-- Header Section -->
            <div class="meeting-header">
                <div class="header-content">
                    <div class="calendar-icon">
                        <i class="fas fa-calendar"></i>
                        <span class="date-number">{current_date}</span>
                    </div>
                    <div class="header-text">
                        <h1 class="meeting-title">Meeting Invitation</h1>
                        <p class="meeting-subtitle">SmartMeetingAI • Professional Meeting Coordination</p>
                    </div>
                    <div class="meeting-type-badge">
                        {meeting_type_label}
                    </div>
                </div>
            </div>
            
            <!-- Meeting Overview -->
            <div class="meeting-overview">
                <h2 class="meeting-topic">{kwargs.get('meeting_topic', 'Meeting')}</h2>
                <div class="priority-badge" style="background-color: {priority_color}">
                    {priority.upper()} PRIORITY
                </div>
            </div>
            
            <!-- Meeting Details Grid -->
            <div class="meeting-details-section">
                <div class="section-header">
                    <i class="fas fa-clipboard-list"></i>
                    <h3>Meeting Details</h3>
                </div>
                <div class="details-grid">
                    <div class="detail-card">
                        <i class="fas fa-calendar-alt"></i>
                        <div class="detail-content">
                            <span class="detail-label">DATE</span>
                            <span class="detail-value">{kwargs.get('meeting_date', 'TBD')}</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <i class="fas fa-clock"></i>
                        <div class="detail-content">
                            <span class="detail-label">TIME</span>
                            <span class="detail-value">{kwargs.get('meeting_time', 'TBD')}</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <i class="fas fa-stopwatch"></i>
                        <div class="detail-content">
                            <span class="detail-label">DURATION</span>
                            <span class="detail-value">{kwargs.get('duration', '30 minutes')}</span>
                        </div>
                    </div>
                    <div class="detail-card">
                        <i class="fas fa-microphone"></i>
                        <div class="detail-content">
                            <span class="detail-label">SPEAKER</span>
                            <span class="detail-value">{kwargs.get('speaker_name', 'TBD')}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Meeting Link Section -->
            {f'''
            <div class="meeting-link-section">
                <div class="section-header">
                    <i class="fas fa-link"></i>
                    <h3>Meeting Link</h3>
                </div>
                <a href="{kwargs.get('meeting_link', '#')}" class="join-meeting-btn" target="_blank">
                    Join Meeting
                </a>
            </div>
            ''' if kwargs.get('meeting_link') else ''}
            
            <!-- Location Section -->
            {f'''
            <div class="location-section">
                <div class="section-header">
                    <i class="fas fa-map-marker-alt"></i>
                    <h3>Location</h3>
                </div>
                <p class="location-text">{kwargs.get('location', 'TBD')}</p>
            </div>
            ''' if kwargs.get('location') else ''}
            
            <!-- Agenda Section -->
            {f'''
            <div class="agenda-section">
                <div class="section-header">
                    <i class="fas fa-file-alt"></i>
                    <h3>Agenda</h3>
                </div>
                <p class="agenda-text">{kwargs.get('additional_notes', 'Discussing meeting objectives and key points')}</p>
            </div>
            ''' if kwargs.get('additional_notes') else ''}
            
            <!-- Attendees Section -->
            {f'''
            <div class="attendees-section">
                <div class="section-header">
                    <i class="fas fa-users"></i>
                    <h3>Attendees</h3>
                </div>
                <p class="attendees-text">{attendees if attendees else 'To be confirmed'}</p>
            </div>
            ''' if attendees else ''}
            
            <!-- Action Button -->
            <div class="action-section">
                <button class="confirm-attendance-btn">
                    Confirm Attendance
                </button>
            </div>
            
            <!-- Footer -->
            <div class="meeting-footer">
                <p>Generated by SmartMeetingAI • Professional Meeting Coordination</p>
                <p>Please respond to confirm your attendance</p>
            </div>
        </div>
        """

# Global instance
template_generator = TemplateGenerator() 