import pyotp
import time
import os
from error_handler import printe 

OTP_SECRET_ENV_VAR = ''

logged_in = False

def get_otp_secret():
    OTP_SECRET_ENV_VAR = os.environ('OTP_SECRET')
    if OTP_SECRET_ENV_VAR == None:
        printe('"OTP_SECRET" env var not set')
        quit()

def otp_login(otp_code):
    get_otp_secret()
    
    totp = pyotp.TOTP(OTP_SECRET_ENV_VAR)

    # OTP verified for current time
    totp.verify(otp_code)

