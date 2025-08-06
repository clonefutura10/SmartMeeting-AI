from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import datetime
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration and database
from config import config
from db import init_db, get_db

# Import utility functions
from utils.validation import validate_email, validate_phone
from utils.template_generator import template_generator
from utils.email_service import send_gmail_invitation
from utils.whatsapp_service import send_whatsapp_message
from utils.supabase_service import supabase_service

app = Flask(__name__, template_folder='../frontend/templates', static_folder='static')

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'production')
app.config.from_object(config[config_name])

# Template Configuration
DEFAULT_TEMPLATE_TYPE = app.config['DEFAULT_TEMPLATE_TYPE']

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = init_db(app)

# Initialize models with database instance
from utils.models import init_models
User, Template, Distribution = init_models(db)

# Initialize Supabase service and demo data
with app.app_context():
    try:
        # Initialize demo contacts
        db.initialize_demo_contacts()
        print("Supabase connection and demo data initialized successfully!")
        
        # Create a demo user if none exists
        demo_user_data = db.get_user_by_email('demo@example.com')
        if not demo_user_data:
            demo_user = db.create_user(
                username='demo_user',
                email='demo@example.com',
                password_hash=generate_password_hash('demo123')
            )
            print("Demo user created: demo@example.com / demo123")
            
    except Exception as e:
        print(f"Database initialization warning: {e}")

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Routes
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return app.send_static_file('favicon.ico')

@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon_precomposed():
    return app.send_static_file('favicon.ico')

@app.route('/')
@login_required
def dashboard():
    # Get statistics
    stats = {
        'templates_generated': Template.query().filter_by(user_id=current_user.id).count(),
        'invitations_sent': Distribution.query().filter_by(user_id=current_user.id, status='sent').count(),
        'total_recipients': 0,  # Will calculate from distributions
        'calendar_events': Distribution.query().filter_by(user_id=current_user.id, method='calendar').count(),
        'success_rate': 94.2,  # Mock data
        'recent_activity': []
    }
    
    # Calculate total recipients
    distributions = Distribution.query().filter_by(user_id=current_user.id).all()
    for dist in distributions:
        if dist.recipients:
            recipients_list = json.loads(dist.recipients) if isinstance(dist.recipients, str) else dist.recipients
            stats['total_recipients'] += len(recipients_list)
    
    # Get recent distributions
    recent_distributions = Distribution.query().filter_by(user_id=current_user.id).all()
    
    # Sort by created_at, handling both string and datetime objects
    def get_sort_key(dist):
        timestamp = dist.created_at
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                # Convert to naive datetime for comparison
                return dt.replace(tzinfo=None) if dt.tzinfo else dt
            except:
                return datetime.min
        # Ensure datetime is naive for comparison
        if timestamp and hasattr(timestamp, 'tzinfo') and timestamp.tzinfo:
            return timestamp.replace(tzinfo=None)
        return timestamp or datetime.min
    
    recent_distributions.sort(key=get_sort_key, reverse=True)
    recent_distributions = recent_distributions[:5]
    
    for dist in recent_distributions:
        # Get template data from Supabase
        template_data = db.get_template(dist.template_id)
        template_title = template_data.get('title', 'Unknown Template') if template_data else 'Unknown Template'
        
        # Parse timestamp if it's a string
        timestamp = dist.created_at
        if isinstance(timestamp, str):
            try:
                # Try to parse ISO format timestamp
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                # Convert to naive datetime
                timestamp = timestamp.replace(tzinfo=None) if timestamp.tzinfo else timestamp
            except:
                try:
                    # Fallback to dateutil parser if available
                    from dateutil import parser as date_parser
                    timestamp = date_parser.parse(timestamp)
                    # Convert to naive datetime
                    timestamp = timestamp.replace(tzinfo=None) if timestamp.tzinfo else timestamp
                except:
                    timestamp = datetime.utcnow()
        elif not timestamp:
            timestamp = datetime.utcnow()
        else:
            # Ensure existing datetime is naive
            timestamp = timestamp.replace(tzinfo=None) if hasattr(timestamp, 'tzinfo') and timestamp.tzinfo else timestamp
        
        stats['recent_activity'].append({
            'id': dist.id,
            'type': 'invitation_sent',
            'title': template_title,
            'description': f'Sent via {dist.method}',
            'timestamp': timestamp,
            'status': dist.status
        })
    
    return render_template('dashboard.html', stats=stats)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        if action == 'login':
            # Bypass authentication - allow any login
            email = data.get('email', 'demo@example.com')
            password = data.get('password', 'demo123')
            
            # Check if user exists, if not create one
            user = User.get_by_email(email)
            if not user:
                user_data = db.create_user(
                    username=email.split('@')[0],
                    email=email,
                    password_hash=generate_password_hash(password)
                )
                user = User(
                    id=user_data['id'],
                    username=user_data['name'],
                    email=user_data['email'],
                    password_hash='demo_password_hash'  # Simplified for demo
                )
            else:
                # For existing users, create User object from contact data
                user = User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    password_hash='demo_password_hash'  # Simplified for demo
                )
            
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        
        elif action == 'register':
            email = data.get('email', 'demo@example.com')
            username = data.get('username', 'demo_user')
            password = data.get('password', 'demo123')
            
            # Check if user exists, if not create one
            user = User.get_by_email(email)
            if not user:
                user_data = db.create_user(
                    username=email.split('@')[0],
                    email=email,
                    password_hash=generate_password_hash(password)
                )
                user = User(
                    id=user_data['id'],
                    username=user_data['name'],
                    email=user_data['email'],
                    password_hash='demo_password_hash'  # Simplified for demo
                )
            else:
                # For existing users, create User object from contact data
                user = User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    password_hash='demo_password_hash'  # Simplified for demo
                )
            
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
    
    return render_template('auth.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

@app.route('/template-generator')
@login_required
def template_generator_page():
    return render_template('template_generator.html')

@app.route('/api/templates/generate', methods=['POST'])
@login_required
def generate_template():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log
        
        # Validate required fields
        required_fields = ['meetingTopic', 'speakerName', 'date', 'time', 'templateType']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        print(f"Template type: {data['templateType']}")  # Debug log
        
        # Generate template using predefined templates
        template_data = template_generator.generate_template(
            template_type=data['templateType'],
            meeting_topic=data['meetingTopic'],
            speaker_name=data['speakerName'],
            meeting_date=data['date'],
            meeting_time=data['time'],
            duration=data.get('duration', '30 minutes'),
            meeting_link=data.get('meetingLink', ''),
            location=data.get('location', ''),
            attendees=data.get('attendees', ''),
            additional_notes=data.get('additionalNotes', ''),
            priority=data.get('priority', 'Medium')
        )
        
        print(f"Template data generated: {template_data['title']}")  # Debug log
        
        # Save template to database using Supabase
        template_data_to_save = {
            'user_id': current_user.id,
            'title': template_data['title'],
            'content': template_data['content'],
            'meeting_topic': template_data['meeting_topic'],
            'speaker_name': template_data['speaker_name'],
            'meeting_date': data['date'],
            'meeting_time': data['time'],
            'duration': template_data['duration'],
            'meeting_link': template_data['meeting_link'],
            'location': template_data['location'],
            'attendees': json.dumps(template_data['attendees']) if isinstance(template_data['attendees'], list) else template_data['attendees'],
            'additional_notes': template_data['additional_notes'],
            'meeting_type': template_data['meeting_type'],
            'priority': template_data['priority']
        }
        
        saved_template = db.create_template(**template_data_to_save)
        
        print(f"Template saved with ID: {saved_template['id']}")  # Debug log
        
        return jsonify({
            'success': True,
            'template': template_data['content'],
            'template_id': saved_template['id'],
            'message': 'Template generated successfully using professional templates'
        })
        
    except Exception as e:
        print(f"Error in template generation: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates/available', methods=['GET'])
@login_required
def get_available_templates():
    """Get list of available template types"""
    try:
        templates = template_generator.get_available_templates()
        return jsonify({
            'success': True,
            'templates': templates
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/distribution')
@login_required
def distribution():
    templates = Template.query().filter_by(user_id=current_user.id).all()
    return render_template('distribution.html', templates=templates)

@app.route('/api/distribution/gmail', methods=['POST'])
@login_required
def send_gmail():
    try:
        data = request.get_json()
        recipient_emails = data.get('recipientEmails', [])
        recipient_email = data.get('recipientEmail')  # Backward compatibility
        template_id = data.get('templateId')
        subject = data.get('subject', 'Meeting Invitation')
        
        # Handle both single email and multiple emails
        if recipient_email and not recipient_emails:
            recipient_emails = [recipient_email]
        
        if not recipient_emails or not template_id:
            return jsonify({'error': 'Recipient email(s) and template ID are required'}), 400
        
        # Validate all emails
        invalid_emails = [email for email in recipient_emails if not validate_email(email)]
        if invalid_emails:
            return jsonify({'error': f'Invalid email format(s): {", ".join(invalid_emails)}'}), 400
        
        template_data = db.get_template(template_id)
        if not template_data or template_data.get('user_id') != current_user.id:
            return jsonify({'error': 'Template not found'}), 404
        
        # Send emails to all recipients
        results = []
        successful_sends = 0
        
        for email in recipient_emails:
            # Customize subject with meeting topic if available
            meeting_topic = template_data.get('meeting_topic', '')
            custom_subject = f"{subject}: {meeting_topic}" if meeting_topic else subject
            
            result = send_gmail_invitation(
                email, 
                template_data['content'], 
                custom_subject,
                app.config.get('GMAIL_USER'),
                app.config.get('GMAIL_PASSWORD')
            )
            results.append({
                'email': email,
                'success': result['success'],
                'message': result['message']
            })
            
            if result['success']:
                successful_sends += 1
        
        # Save distribution record using Supabase
        recipients_json = json.dumps([{'email': email} for email in recipient_emails])
        db.create_distribution(
            user_id=current_user.id,
            template_id=template_id,
            method='gmail',
            recipients=recipient_emails,  # Pass as list
            status='sent' if successful_sends > 0 else 'failed',
            sent_at=datetime.utcnow().isoformat(),
            formatted_recipients=recipients_json  # Store formatted recipients
        )
        
        # Return summary
        if successful_sends == len(recipient_emails):
            return jsonify({
                'success': True,
                'message': f'Successfully sent {successful_sends} invitation(s)',
                'details': results
            })
        elif successful_sends > 0:
            return jsonify({
                'success': True,
                'message': f'Partially successful: {successful_sends}/{len(recipient_emails)} sent',
                'details': results
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send any invitations',
                'details': results
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/distribution/whatsapp', methods=['POST'])
@login_required
def send_whatsapp():
    try:
        data = request.get_json()
        phone_number = data.get('phoneNumber')
        template_id = data.get('templateId')
        
        if not phone_number or not template_id:
            return jsonify({'error': 'Phone number and template ID are required'}), 400
        
        if not validate_phone(phone_number):
            return jsonify({'error': 'Invalid phone number format'}), 400
        
        template_data = db.get_template(template_id)
        if not template_data or template_data.get('user_id') != current_user.id:
            return jsonify({'error': 'Template not found'}), 404
        
        # Send WhatsApp message
        result = send_whatsapp_message(phone_number, template_data['content'])
        
        # Save distribution record using Supabase
        recipients_json = json.dumps([{'phone': phone_number}])
        db.create_distribution(
            user_id=current_user.id,
            template_id=template_id,
            method='whatsapp',
            recipients=[phone_number],  # Pass as list
            status='sent' if result['success'] else 'failed',
            sent_at=datetime.utcnow().isoformat(),
            formatted_recipients=recipients_json  # Store formatted recipients
        )
        
        return jsonify({
            'success': result['success'],
            'message': result['message']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/templates/<template_id>/download')
@login_required
def download_template(template_id):
    """Download template as HTML file"""
    try:
        template_data = db.get_template(template_id)
        if not template_data or template_data.get('user_id') != current_user.id:
            return jsonify({'error': 'Template not found'}), 404
        
        # Create HTML content with proper styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{template_data['title']}</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    line-height: 1.6; 
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 30px; 
                    text-align: center;
                }}
                .content {{ 
                    padding: 30px; 
                }}
                .footer {{ 
                    margin-top: 20px; 
                    text-align: center; 
                    color: #666; 
                    font-size: 14px; 
                    padding: 20px;
                    background: #f8f9fa;
                }}
                .meeting-details {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .meeting-details h3 {{
                    color: #667eea;
                    margin-top: 0;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                td {{
                    padding: 8px 0;
                }}
                td:first-child {{
                    font-weight: bold;
                    color: #555;
                    width: 30%;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                {template_data['content']}
                <div class="footer">
                    <p>Generated by SmartMeetingAI</p>
                    <p>Date: {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create response with HTML file
        from io import BytesIO
        response = send_file(
            BytesIO(html_content.encode('utf-8')),
            mimetype='text/html',
            as_attachment=True,
            download_name=f"{template_data['title'].replace(' ', '_')}_meeting_invitation.html"
        )
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# New API endpoints for Module 1 database integration

@app.route('/api/meetings', methods=['GET'])
@login_required
def get_meetings():
    """Get all meetings from database"""
    try:
        meetings = supabase_service.get_meetings()
        return jsonify({
            'success': True,
            'meetings': meetings
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meetings/<meeting_id>', methods=['GET'])
@login_required
def get_meeting(meeting_id):
    """Get specific meeting with attendees"""
    try:
        meeting = supabase_service.get_meeting_with_attendees(meeting_id)
        if not meeting:
            return jsonify({'error': 'Meeting not found'}), 404
        
        return jsonify({
            'success': True,
            'meeting': meeting
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meetings/upcoming', methods=['GET'])
@login_required
def get_upcoming_meetings():
    """Get upcoming meetings"""
    try:
        meetings = supabase_service.get_upcoming_meetings()
        return jsonify({
            'success': True,
            'meetings': meetings
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts', methods=['GET'])
@login_required
def get_contacts():
    """Get all contacts from database"""
    try:
        member_type = request.args.get('member_type')  # 'internal' or 'external'
        contacts = supabase_service.get_contacts(member_type)
        return jsonify({
            'success': True,
            'contacts': contacts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/internal', methods=['GET'])
@login_required
def get_internal_members():
    """Get internal members only"""
    try:
        contacts = supabase_service.get_internal_members()
        return jsonify({
            'success': True,
            'contacts': contacts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/external', methods=['GET'])
@login_required
def get_external_contacts():
    """Get external contacts only"""
    try:
        contacts = supabase_service.get_external_contacts()
        return jsonify({
            'success': True,
            'contacts': contacts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts', methods=['POST'])
@login_required
def add_contact():
    """Add a new contact"""
    try:
        data = request.get_json()
        required_fields = ['email', 'name', 'member_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        contact = supabase_service.add_contact(
            email=data['email'],
            name=data['name'],
            member_type=data['member_type'],
            organization_id=data.get('organization_id')
        )
        
        if contact:
            return jsonify({
                'success': True,
                'contact': contact,
                'message': 'Contact added successfully'
            })
        else:
            return jsonify({'error': 'Failed to add contact'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/organizations', methods=['GET'])
@login_required
def get_organizations():
    """Get all organizations"""
    try:
        organizations = supabase_service.get_organizations()
        return jsonify({
            'success': True,
            'organizations': organizations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'module': 'SmartMeetingAI Flask'
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001) 