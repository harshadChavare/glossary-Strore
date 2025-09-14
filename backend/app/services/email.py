import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.otp import OTP
from ..models.user import User
from ..core.config import settings

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp_email(user_email: str, otp_code: str) -> bool:
    if not settings.SMTP_SERVER or not settings.SMTP_USERNAME:
        print(f"[OTP] Email not configured. OTP for {user_email}: {otp_code}")
        return True
    
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = settings.EMAIL_FROM
        message["To"] = user_email
        message["Subject"] = "Your OTP for Purchase Verification"
        
        body = f"""
        Dear Customer,
        
        Your OTP for purchase verification is: {otp_code}
        
        This OTP will expire in 5 minutes.
        
        If you did not request this, please ignore this email.
        
        Thank you!
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # Create SMTP session
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        
        # Send email
        server.sendmail(settings.EMAIL_FROM, user_email, message.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        print(f"[OTP] Fallback - OTP for {user_email}: {otp_code}")
        return True

def create_otp_record(db: Session, user_id: int, otp_code: str) -> OTP:
    # Delete existing OTPs for this user
    db.query(OTP).filter(OTP.user_id == user_id, OTP.used == False).delete()
    
    # Create new OTP
    otp_record = OTP(
        user_id=user_id,
        otp_code=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
        attempts=0,
        used=False
    )
    
    db.add(otp_record)
    db.commit()
    db.refresh(otp_record)
    
    return otp_record
