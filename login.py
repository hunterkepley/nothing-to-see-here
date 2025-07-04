import os
import pyotp
import time
from error_handler import printe

# TODO: LOG OUT AFTER X MINUTES!!! OR X MINUTES WITH NO REQUESTS FROM SAME USER, SOMETHING SAFE
logged_in = False

def login(code):
    f = open('.otp_key')
    if f == None:
        printe('OTP Key not generated, please run "generate_key.sh"')

    otp = pyotp.parse_uri(f.read())

    print('\n!!!\nVerifying OTP user passed in at ', time.now(), '\n!!!\n')

    logged_in = otp.verify(code)

