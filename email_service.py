import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import Config
import os
import time

def send_assessment_email(to_email, client_name, pdf_path):
    """Send body composition assessment report via email"""
    
    # Email configuration
    from_email = Config.MAIL_USERNAME
    password = Config.MAIL_PASSWORD
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Your Body Composition Assessment Report - PowerFuel'
    
    # Email body
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2C3E50; border-bottom: 3px solid #3498DB; padding-bottom: 10px;">
                    Body Composition Assessment Report
                </h2>
                
                <p>Dear {client_name},</p>
                
                <p>Thank you for participating in our body composition assessment event!</p>
                
                <p>Please find your detailed body composition report attached to this email. 
                This comprehensive assessment includes:</p>
                
                <ul style="background-color: #ECF0F1; padding: 20px; border-radius: 5px;">
                    <li>Personal measurements and body composition metrics</li>
                    <li>BMI and metabolic indicators</li>
                    <li>Subcutaneous fat and muscle mass distribution</li>
                    <li>Additional calculated metrics for performance optimization</li>
                </ul>
                
                <p style="background-color: #FFF9E6; padding: 15px; border-left: 4px solid #F39C12; margin: 20px 0;">
                    <strong>For Marathon Runners & Athletes:</strong><br>
                    Your body composition plays a crucial role in your performance. Use this report to 
                    track your progress and make informed decisions about your training and nutrition.
                </p>
                
                <p>If you have any questions about your results or would like personalized nutrition 
                and training recommendations, please don't hesitate to reach out to us.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ECF0F1;">
                    <p style="margin-bottom: 5px;"><strong>Best regards,</strong></p>
                    <p style="margin: 0; color: #3498DB; font-size: 18px; font-weight: bold;">
                        PowerFuel - The Nutrition Hub
                    </p>
                    <p style="margin: 5px 0; font-size: 12px; color: #7F8C8D;">
                        Email: {from_email}
                    </p>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background-color: #F8F9FA; 
                           border-radius: 5px; font-size: 11px; color: #7F8C8D;">
                    <p style="margin: 0;"><em>This email and its attachments contain confidential 
                    health information. If you received this email in error, please notify us immediately 
                    and delete it.</em></p>
                </div>
            </div>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    # Attach PDF
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                     filename=os.path.basename(pdf_path))
            msg.attach(pdf_attachment)
    
    # Send email
    try:
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_email}")
        
        # Clean up temporary PDF file
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                print(f"Cleaned up temporary file: {pdf_path}")
        except Exception as cleanup_error:
            print(f"Warning: Could not clean up temporary file: {cleanup_error}")
        
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise e
