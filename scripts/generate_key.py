import pyotp
import os
import qrterm
from cryptography.fernet import Fernet

users_body = []
with open('.users', 'r') as f:
    users_body = f.read().split('\n')

if len(users_body) == 0:
    print('Please create an account before generating an OTP by running `create_account.sh`')
    quit()

users = {}

chosen_username = input('Please type the username of the account you wish to associate with this TOTP key: ')

for user in users_body:
    user_split = user.split(',')
    # TODO: Make username only alphanumeric!

    if len(user_split) <= 1:
        continue

    username = user_split[0][1:]
    password = user_split[1][:len(user_split[1])-1]
    users[username] = password

if chosen_username not in users:
    print('\nUser does not exist. Please run `create_account.sh` to create one before running this script')
    quit()

secret_key = pyotp.random_base32()

print('Key to use for authenticator app is:', secret_key, '\nIt is saved in the ".otp_key" file. Do not share this with anyone.\n\n')

email_account = input('Please enter your email account, use the same email in your authenticator app: ')

uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=email_account, issuer_name='NothingToSeeHere')

with open('.otp_key', 'a') as f:
    f.write(uri)

with open('.user_otp_pairs', 'a') as f:
    f.write(chosen_username + ' : ' + uri)

qrterm.draw(uri)
