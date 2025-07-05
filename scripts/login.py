import hashlib
from urllib.parse import unquote
import os
import re
import pyotp
from datetime import datetime
from scripts.error_handler import printe

# TODO: LOG OUT AFTER X MINUTES!!! OR X MINUTES WITH NO REQUESTS FROM SAME USER, SOMETHING SAFE

def login(request_body, ip):
    f = open('.user_otp_pairs')
    if f == None:
        printe('OTP Key not generated, please run "generate_key.sh"')

    otp_file_contents = f.read()

    # Set OTP code, username, and password from payload request body
    code = '' 
    username = ''
    password = ''

    split_body = request_body.split('&')
    for key_value in split_body:
        key_value = key_value.split('=')
        if 'username' in key_value[0]:
            username = key_value[1]
        elif 'password' in key_value[0]:
            password = key_value[1]
        elif 'OTP' in key_value[0]:
            code = key_value[1]

    # Set URI for OTP so it can authenticate, based on the username entered
    uri = ''
    pairs = otp_file_contents.split('\n')
    for pair in pairs:
        pair_split = pair.split(' : ')
        if pair_split[0] == username:
            uri = pair_split[1]

    if uri == '':
        printe('User not found locally, please run `create_user.sh` then `generate_otp_key.sh`')
        exit()

    otp = pyotp.parse_uri(uri)

    # Verify username + password exists in "database"
    if not verify_user(username, password):
        printe('User entered wrong username/password. Denied')
        return

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


def verify_user(username, password) -> bool:
    password_hash = hashlib.sha256(unquote(password).encode('utf-8')).hexdigest()
    with open('.users') as f:
        users = f.read()
        for user in users.split('\n'):
            if len(user) < 2:
                continue
            user_split = user.split(',')
            if user_split[0][0] == '[':
                user_split[0] = user_split[0][1:]
            if user_split[1][len(user_split[1])-1] == ']':
                user_split[1] = user_split[1][:len(user_split[1])-1]
            if user_split[0] == username:
                # Username found, check password
                if user_split[1] == password_hash:
                    print('User entered correct username+password. Checking OTP')
                    return True
        f.close()
    return False 

