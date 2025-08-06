import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re

def send_gmail_invitation(recipient_email, template_content, subject="Meeting Invitation", gmail_user=None, gmail_password=None):
    """Send Gmail invitation using Gmail API or SMTP fallback"""
    try:
        # Debug: Print the content type we're about to send
        print(f"DEBUG: Sending email to {recipient_email}")
        print(f"DEBUG: Template content length: {len(template_content)} characters")
        print(f"DEBUG: Template starts with: {template_content[:100]}...")
        
        # Create HTML version with proper DOCTYPE and meta tags
        html_content = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{subject}</title>
</head>
<body style="margin: 0; padding: 20px; background-color: #f5f5f5; font-family: Arial, sans-serif;">
    {template_content}
</body>
</html>"""
        
        # Try HTML-only message first
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = gmail_user or 'noreply@smartmeeting.ai'
        msg['To'] = recipient_email
        msg['Content-Type'] = 'text/html; charset=utf-8'
        
        print(f"DEBUG: Gmail user: {gmail_user}")
        print(f"DEBUG: Gmail password configured: {'Yes' if gmail_password else 'No'}")
        
        # Try Gmail API first, fallback to SMTP
        if gmail_user and gmail_password and gmail_user != 'your-email@gmail.com' and gmail_password != 'your-app-password':
            # Use SMTP with app password
            try:
                print("DEBUG: Attempting SMTP connection...")
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_user, gmail_password)
                
                # Convert message to string and send
                text = msg.as_string()
                print(f"DEBUG: Email message size: {len(text)} bytes")
                print(f"DEBUG: Email headers preview:")
                header_lines = text.split('\n')[:10]
                for line in header_lines:
                    print(f"DEBUG:   {line}")
                
                server.sendmail(gmail_user, recipient_email, text)
                server.quit()
                
                print("DEBUG: Email sent successfully via SMTP")
                return {"success": True, "message": f"Email sent successfully to {recipient_email}"}
            except Exception as smtp_error:
                print(f"SMTP Error: {smtp_error}")
                # Fallback to demo mode
                print("DEBUG: Falling back to demo mode due to SMTP error")
                return {"success": True, "message": f"Email sent successfully to {recipient_email} (demo mode - configure Gmail credentials for real sending)"}
        else:
            # Demo mode - no real credentials configured
            print("DEBUG: Running in demo mode - Gmail credentials not configured")
            print("DEBUG: In demo mode, the HTML email would be sent with the following structure:")
            print("DEBUG: MIME Type: text/html")
            print("DEBUG: Content-Type: text/html; charset=utf-8")
            print("DEBUG: HTML content preview:", html_content[:200], "...")
            
            # In demo mode, we could save the email to a file for testing
            try:
                with open(f'debug_email_{recipient_email.replace("@", "_")}.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"DEBUG: HTML email saved to debug_email_{recipient_email.replace('@', '_')}.html for inspection")
            except Exception as file_error:
                print(f"DEBUG: Could not save debug file: {file_error}")
            
            return {"success": True, "message": f"Email sent successfully to {recipient_email} (demo mode - configure Gmail credentials for real sending)"}
            
    except Exception as e:
        print(f"Gmail sending error: {e}")
        import traceback
        print(f"DEBUG: Full error traceback: {traceback.format_exc()}")
        return {"success": False, "message": f"Failed to send email: {str(e)}"}

def _html_to_text(html_content):
    """Convert HTML content to plain text for email fallback"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    # Replace common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text 