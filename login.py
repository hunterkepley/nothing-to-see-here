import os
import re
import pyotp
from datetime import datetime
from error_handler import printe

# TODO: LOG OUT AFTER X MINUTES!!! OR X MINUTES WITH NO REQUESTS FROM SAME USER, SOMETHING SAFE

def login(code, ip):
    f = open('.otp_key')
    if f == None:
        printe('OTP Key not generated, please run "generate_key.sh"')

    otp = pyotp.parse_uri(f.read())

    print('\n!!!\nVerifying OTP user passed in at ', datetime.now(), '\n!!!\n')

    code_numbers = re.compile(r'\d+(?:\.\d+)?')
    if not isinstance(code, str): 
        print('\n!!!\nDenied user\n!!!\n')
        os.environ['LOGGED_IN'] = 'f'
        return

    code_regex = code_numbers.findall(code)
    
    if len(code_regex) == 0:
        return

    code = code_regex[0]

    logged_in = otp.verify(code)

    # TODO: Log info about user! Maybe send email/text warning! Or show on site itself!
    if logged_in:
        os.environ['LOGGED_IN'] = 't'
        os.environ['CLIENT_IP'] = ip
        print('\n!!!\nLogged user in!\n!!!\n')
        print('\n!!!\nLogged in user IP address:',ip,'\n!!!\n')
    else:
        os.environ['LOGGED_IN'] = 'f'
        print('\n!!!\nDenied user\n!!!\n')

