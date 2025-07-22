import getpass
import hashlib

print('Your username must contain only letters and numbers.\n')

while True:
    username = input('Enter username for new account: ')
    if username.isalnum():
        break
    else:
        print('\nYour username contains invalid characters. Please try again, using only letters and numbers.\n')

print('\nYour password will never be stored or sent as plaintext. After this script finishes, the plaintext will no longer be in memory either\n')

password = getpass.getpass('Enter your password: ')

print('\nPlease set up your OTP using `generate_otp_key.sh`. It will be tied to your account\n')

password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

with open('.users', 'a') as f:
    f.write('['+username+','+password_hash+']\n')
    f.close()
