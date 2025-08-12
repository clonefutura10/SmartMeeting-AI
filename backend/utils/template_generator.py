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
        """Create a modern, professional template matching the image design"""
        
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
        
        # Format date and time
        meeting_date = kwargs.get('meeting_date', 'TBD')
        meeting_time = kwargs.get('meeting_time', 'TBD')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Meeting Invitation</title>
        </head>
        <body style="margin: 0; padding: 20px; background-color: #F5F5DC; font-family: Arial, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
                <tr>
                    <td style="background: #F5F5DC; border-radius: 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        
                        <!-- Header Section -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="background: #F5F5DC; padding: 3rem 2rem; text-align: center;">
                                    <!-- Logo Section -->
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td style="text-align: center; padding-bottom: 2rem;">
                                                <table cellpadding="0" cellspacing="0" style="margin: 0 auto;">
                                                    <tr>
                                                        <td style="text-align: center; padding-right: 2rem;">
                                                            <!-- SKILL Logo -->
                                                            <div style="font-size: 2.5rem; font-weight: 700; color: #90EE90; position: relative; display: inline-block;">
                                                                SKILL
                                                                <span style="position: absolute; top: 0; right: -15px; width: 12px; height: 12px; background: #FF6B6B; border-radius: 50%;"></span>
                                                            </div>
                                                            <div style="font-size: 0.9rem; color: #6c757d; font-weight: 500; margin-top: 0.5rem;">भारत ASSOCIATION</div>
                                                        </td>
                                                        <td style="width: 2px; background: #6c757d; opacity: 0.3; padding: 0 1rem;"></td>
                                                        <td style="text-align: center; padding-left: 2rem;">
                                                            <!-- Elite Principals Club Logo -->
                                                            <div style="width: 120px; height: 120px; background: #000; border-radius: 50%; display: inline-block; vertical-align: middle; line-height: 120px; color: white;">
                                                                <div style="font-size: 0.8rem; font-weight: 700; text-align: center; line-height: 1.2; padding: 1rem;">
                                                                    ELITE PRINCIPALS CLUB
                                                                    <div style="font-size: 0.6rem; opacity: 0.8; margin-top: 0.25rem;">World's Biggest Influencers Network</div>
                                                                </div>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Main Title Section -->
                                    <div style="margin-bottom: 2rem;">
                                        <h1 style="font-size: 2.5rem; font-weight: 700; color: #000; margin: 0 0 0.5rem 0; text-transform: uppercase;">ELITE PRINCIPALS CLUB</h1>
                                        <div style="font-size: 1.2rem; color: #000; font-style: italic; margin-bottom: 1rem;">Presents</div>
                                        <div style="font-size: 3.5rem; font-weight: 700; color: #000; margin: 0 0 1rem 0;">
                                            <span style="color: #8B4513; font-size: 2.5rem;">🧠</span>
                                            <span>{kwargs.get('meeting_topic', 'Think Tank Meet')}</span>
                                        </div>
                                        <div style="font-size: 1.3rem; color: #000; font-weight: 500; margin: 0;">Where Ideas for Meaningful Education Begin</div>
                                    </div>
                                    
                                    <!-- Event Description -->
                                    <div style="margin-bottom: 2rem;">
                                        <p style="font-size: 1.1rem; color: #6c757d; margin: 0; line-height: 1.6;">Join us for an inspiring virtual gathering of thought leaders, educators, and changemakers!</p>
                                    </div>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Date & Time Section -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 2rem; background: #F5F5DC;">
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td style="text-align: center;">
                                                <table cellpadding="0" cellspacing="0" style="margin: 0 auto;">
                                                    <tr>
                                                        <td style="text-align: center; padding-right: 2rem;">
                                                            <span style="color: #6c757d; font-size: 1.2rem;">📅</span>
                                                            <span style="font-size: 1.5rem; font-weight: 700; color: #000;">{meeting_date.upper() if meeting_date != 'TBD' else 'TBD'}</span>
                                                        </td>
                                                        <td style="width: 2px; background: #6c757d; opacity: 0.3; padding: 0 1rem;"></td>
                                                        <td style="text-align: center; padding-left: 2rem;">
                                                            <span style="color: #6c757d; font-size: 1.2rem;">⏰</span>
                                                            <span style="font-size: 1.5rem; font-weight: 700; color: #000;">{meeting_time.upper() if meeting_time != 'TBD' else 'TBD'}</span>
                                                            <span style="font-size: 1.2rem; font-weight: 700; color: #000;">SHARP</span>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Meeting Details -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 2rem;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                                        <span style="color: #667eea; font-size: 1.2rem;">📋</span>
                                        <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Meeting Details</h3>
                                    </div>
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                                                                         <td style="padding: 0.5rem;">
                                                 <table width="100%" cellpadding="0" cellspacing="0" style="background: #F5F5DC; border-radius: 12px; border: 1px solid #e9ecef;">
                                                     <tr>
                                                         <td style="padding: 1.5rem; text-align: center;">
                                                             <span style="color: #667eea; font-size: 1.5rem;">📅</span>
                                                             <div style="margin-top: 0.5rem;">
                                                                 <div style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">DATE</div>
                                                                 <div style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{meeting_date}</div>
                                                             </div>
                                                         </td>
                                                     </tr>
                                                 </table>
                                             </td>
                                                                                         <td style="padding: 0.5rem;">
                                                 <table width="100%" cellpadding="0" cellspacing="0" style="background: #F5F5DC; border-radius: 12px; border: 1px solid #e9ecef;">
                                                     <tr>
                                                         <td style="padding: 1.5rem; text-align: center;">
                                                             <span style="color: #667eea; font-size: 1.5rem;">🕐</span>
                                                             <div style="margin-top: 0.5rem;">
                                                                 <div style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">TIME</div>
                                                                 <div style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{meeting_time}</div>
                                                             </div>
                                                         </td>
                                                     </tr>
                                                 </table>
                                             </td>
                                        </tr>
                                        <tr>
                                                                                         <td style="padding: 0.5rem;">
                                                 <table width="100%" cellpadding="0" cellspacing="0" style="background: #F5F5DC; border-radius: 12px; border: 1px solid #e9ecef;">
                                                     <tr>
                                                         <td style="padding: 1.5rem; text-align: center;">
                                                             <span style="color: #667eea; font-size: 1.5rem;">⏱️</span>
                                                             <div style="margin-top: 0.5rem;">
                                                                 <div style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">DURATION</div>
                                                                 <div style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{kwargs.get('duration', '30 minutes')}</div>
                                                             </div>
                                                         </td>
                                                     </tr>
                                                 </table>
                                             </td>
                                                                                         <td style="padding: 0.5rem;">
                                                 <table width="100%" cellpadding="0" cellspacing="0" style="background: #F5F5DC; border-radius: 12px; border: 1px solid #e9ecef;">
                                                     <tr>
                                                         <td style="padding: 1.5rem; text-align: center;">
                                                             <span style="color: #667eea; font-size: 1.5rem;">🎤</span>
                                                             <div style="margin-top: 0.5rem;">
                                                                 <div style="font-size: 0.75rem; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">SPEAKER</div>
                                                                 <div style="font-size: 1rem; color: #2c3e50; font-weight: 600;">{kwargs.get('speaker_name', 'TBD')}</div>
                                                             </div>
                                                         </td>
                                                     </tr>
                                                 </table>
                                             </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Meeting Link Section -->
                        {f'''
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 0 2rem 2rem;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                                        <span style="color: #667eea; font-size: 1.2rem;">🔗</span>
                                        <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Meeting Link</h3>
                                    </div>
                                    <a href="{kwargs.get('meeting_link', '#')}" style="display: inline-block; background: #007bff; color: white; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; margin-right: 1rem;">
                                        <span style="margin-right: 0.5rem;">📹</span>ZOOM
                                    </a>
                                    <a href="{kwargs.get('meeting_link', '#')}" style="display: inline-block; background: #17a2b8; color: white; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600;">
                                        Join us
                                    </a>
                                </td>
                            </tr>
                        </table>
                        ''' if kwargs.get('meeting_link') else ''}
                        
                        <!-- Location Section -->
                        {f'''
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 0 2rem 2rem;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                                        <span style="color: #667eea; font-size: 1.2rem;">📍</span>
                                        <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Location</h3>
                                    </div>
                                    <p style="color: #2c3e50; font-weight: 500; margin: 0; font-size: 1rem;">{kwargs.get('location', 'TBD')}</p>
                                </td>
                            </tr>
                        </table>
                        ''' if kwargs.get('location') else ''}
                        
                        <!-- Agenda Section -->
                        {f'''
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 0 2rem 2rem;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                                        <span style="color: #667eea; font-size: 1.2rem;">📄</span>
                                        <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Agenda</h3>
                                    </div>
                                    <p style="color: #2c3e50; margin: 0; line-height: 1.6;">{kwargs.get('additional_notes', 'Discussing meeting objectives and key points')}</p>
                                </td>
                            </tr>
                        </table>
                        ''' if kwargs.get('additional_notes') else ''}
                        
                        <!-- Attendees Section -->
                        {f'''
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 0 2rem 2rem;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                                        <span style="color: #667eea; font-size: 1.2rem;">👥</span>
                                        <h3 style="color: #2c3e50; font-weight: 600; margin: 0; font-size: 1.1rem;">Attendees</h3>
                                    </div>
                                    <p style="color: #2c3e50; margin: 0; font-weight: 500;">{attendees if attendees else 'To be confirmed'}</p>
                                </td>
                            </tr>
                        </table>
                        ''' if attendees else ''}
                        
                        <!-- Slogan Section -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 2rem; text-align: center; background: #6c757d;">
                                    <div style="font-size: 1.5rem; font-weight: 700; color: white; text-transform: uppercase; margin-bottom: 0.5rem;">PURPOSEFUL CONVERSATIONS.</div>
                                    <div style="font-size: 1.5rem; font-weight: 700; color: white; text-transform: uppercase;">COLLECTIVE GROWTH.</div>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Footer -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                                                 <td style="background: #F5F5DC; color: #6c757d; padding: 1.5rem 2rem; text-align: center;">
                                    <table cellpadding="0" cellspacing="0" style="margin: 0 auto;">
                                        <tr>
                                            <td style="text-align: center; padding-right: 1rem;">
                                                <span style="color: #6c757d; font-size: 1rem;">📞</span>
                                                <span style="font-size: 0.9rem;">+918879188188</span>
                                            </td>
                                            <td style="width: 2px; height: 20px; background: #6c757d; opacity: 0.3; padding: 0 0.5rem;"></td>
                                            <td style="text-align: center; padding-left: 1rem;">
                                                <span style="color: #6c757d; font-size: 1rem;">✉️</span>
                                                <span style="font-size: 0.9rem;">Info@skillba.org</span>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

# Global instance
template_generator = TemplateGenerator() 