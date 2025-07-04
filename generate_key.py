import pyotp
import os
import qrterm
from cryptography.fernet import Fernet

secret_key = pyotp.random_base32()

print('Key to use for authenticator app is:', secret_key, '\n\n It is saved in the "otp_key" file. Do not share this with anyone.\n\n')

email_account = input('Please enter your email account, use the same email in your authenticator app: ')

uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=email_account, issuer_name='NothingToSeeHere')

with open('.otp_key', 'w') as f:
    f.write(uri)

qrterm.draw(uri)
