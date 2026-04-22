import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "yassinebenayed100@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

if not SENDER_PASSWORD:
    raise RuntimeError("SENDER_PASSWORD environment variable is required.")

# File paths
CSV_FILE = '/Users/yassinebenayed/Desktop/cleaning/Export_cleaned_remaining.csv'
CV_FILE = '/Users/yassinebenayed/Desktop/cleaning/Yassine Ben Ayed 2026 .pdf'  # Adjust path to your CV

# Cover letter template (will be personalized with company name)
COVER_LETTER_TEMPLATE = """Dear {company_name} Team,

I hope this email finds you well. I am Yassine Ben Ayed, a Software Engineering student based in Sfax, Tunisia, and I am reaching out to express my strong interest in joining your team for an internship opportunity.

I am passionate about DevOps, SRE, Platform Engineering, and cloud infrastructure. Through my projects, I have focused on creating systems that reflect real production scenarios with attention to reliability and security. I have developed strong problem-solving skills in troubleshooting, debugging, and understanding how different components of a system interact together.

I am particularly interested in DevOps, Site Reliability Engineering (SRE), Platform Engineering, and cloud-related internship roles, with a focus on automation, CI/CD pipelines, infrastructure as code, and improving system reliability. Even though I may not have seen a specific internship posting, I believe my skills and enthusiasm could be valuable to your organization, and I would be grateful for any opportunity to contribute and grow with your team.

Despite this being my first professional experience, I take my learning seriously and always aim to deeply understand what I build, compare different approaches, and learn the reasoning behind technical decisions. What drives me is my genuine passion for building and maintaining systems, and working with different tools and environments to solve real problems.

I would be delighted to discuss how I can contribute to {company_name}. Please find my CV attached for your consideration.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
Yassine Ben Ayed"""

EMAIL_SUBJECT = "Internship Application - DevOps/SRE/Platform Engineering/Cloud - Yassine Ben Ayed"

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
            part.add_header("Content-Disposition", f"attachment; filename= CV.pdf")
            message.attach(part)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        
        print(f"✓ Email sent to {company_name} ({recipient_email})")
        return True
    except Exception as e:
        print(f"✗ Failed to send to {company_name} ({recipient_email}): {str(e)}")
        return False

def main():
    """Main function to send emails to all companies"""
    
    # Read the CSV
    df = pd.read_csv(CSV_FILE, sep=';')
    
    print(f"Starting email campaign...")
    print(f"Total recipients: {len(df)}\n")
    
    # Filter out empty emails
    df_valid = df[df['Email entreprise'].notna() & (df['Email entreprise'].astype(str).str.strip() != '')]
    
    print(f"Valid email addresses: {len(df_valid)}\n")
    
    sent_count = 0
    failed_count = 0
    
    # Send emails
    for idx, row in df_valid.iterrows():
        email = row['Email entreprise'].strip()
        company = row["Nom de l'entreprise"]
        
        if send_email(email, company):
            sent_count += 1
        else:
            failed_count += 1
        
        # Small delay to avoid rate limiting
        import time
        time.sleep(2)
    
    print(f"\n--- Campaign Summary ---")
    print(f"Successfully sent: {sent_count}")
    print(f"Failed: {failed_count}")
    print(f"Total attempted: {sent_count + failed_count}")

if __name__ == "__main__":
    main()
