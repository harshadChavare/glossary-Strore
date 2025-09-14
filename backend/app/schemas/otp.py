from pydantic import BaseModel

class OTPRequest(BaseModel):
    pass

class OTPVerify(BaseModel):
    otp_code: str
