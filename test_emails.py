import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import random

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "yassinebenayed100@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

if not SENDER_PASSWORD:
    raise RuntimeError("SENDER_PASSWORD environment variable is required.")

# File paths
CSV_FILE = '/Users/yassinebenayed/Desktop/cleaning/Export_cleaned.csv'
CV_FILE = '/Users/yassinebenayed/Desktop/cleaning/Yassine Ben Ayed 2026 .pdf'

# Test email
TEST_EMAIL = "elfaidighassen@gmail.com"

# Cover letter template (will be personalized with company name)
COVER_LETTER_TEMPLATE = """Dear {company_name} Team,

I hope this email finds you well. I am Yassine Ben Ayed, a Software Engineering student based in Sfax, Tunisia, and I am reaching out to express my strong interest in joining your team.

I am passionate about DevOps, SRE, Platform Engineering, and cloud infrastructure. Through my projects, I have focused on creating systems that reflect real production scenarios with attention to reliability and security. I have developed strong problem-solving skills in troubleshooting, debugging, and understanding how different components of a system interact together.

I am particularly interested in DevOps, Site Reliability Engineering (SRE), Platform Engineering, and cloud-related roles, with a focus on automation, CI/CD pipelines, infrastructure as code, and improving system reliability. Even though I may not have seen a specific job posting, I believe my skills and enthusiasm could be valuable to your organization, and I would be grateful for any opportunity to contribute and grow with your team.

Despite this being my first professional experience, I take my learning seriously and always aim to deeply understand what I build, compare different approaches, and learn the reasoning behind technical decisions. What drives me is my genuine passion for building and maintaining systems, and working with different tools and environments to solve real problems.

I would be delighted to discuss how I can contribute to {company_name}. Please find my CV attached for your consideration.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
Yassine Ben Ayed"""

EMAIL_SUBJECT = "Spontaneous Application - DevOps/SRE/Platform Engineering/Cloud - Yassine Ben Ayed"

def send_email(recipient_email, company_name):
    """Send email to a single recipient"""
    try:
        # Personalize cover letter with company name
        cover_letter = COVER_LETTER_TEMPLATE.format(company_name=company_name)
        
        # Create message
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = EMAIL_SUBJECT
        
        # Add body
        message.attach(MIMEText(cover_letter, "plain"))
        
        # Attach CV if it exists
        if os.path.exists(CV_FILE):
            with open(CV_FILE, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= Yassine Ben Ayed 2026 .pdf")
            message.attach(part)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        
        print(f"✓ Test email sent to {recipient_email} with company: {company_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to send test email: {str(e)}")
        return False

def main():
    """Main function to send test emails with random company names"""
    
    # List of random company names for testing
    random_companies = [
        "Tech Innovations Inc",
        "Cloud Solutions Ltd",
        "DevOps Masters",
        "Infrastructure Pro",
        "Platform Systems Corp",
        "Reliability Engineering Co",
        "Automation Experts",
        "Cloud Native Systems",
        "SRE Specialists",
        "Digital Infrastructure"
    ]
    
    print(f"🧪 Running TEST mode - sending to: {TEST_EMAIL}\n")
    
    # Send 3 test emails with random company names
    for i in range(3):
        company = random.choice(random_companies)
        print(f"Test {i+1}/3:")
        send_email(TEST_EMAIL, company)
        print()
        
        # Delay between emails
        import time
        time.sleep(2)
    
    print("✓ Test completed! Check your email at elfaidighassen@gmail.com")

if __name__ == "__main__":
    main()
