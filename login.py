import os

password_env_var_name = 'BASE64_ENCODED_PASSWORD_TO_CAM'
username_env_var_name = 'USERNAME_TO_CAM'

# TODO: LOG OUT AFTER X MINUTES!!! OR X MINUTES WITH NO REQUESTS FROM SAME USER, SOMETHING SAFE
logged_in = False

def login(username, password):
    base64_encoded_password = os.environ[password_env_var_name]
    correct_username = os.environ[username_env_var_name] 
    
