# NOTHING TO SEE HERE

This is an open source multi-function security camera project written in Python for use with Raspberry Pis

This is a lightweight, easy to set up camera server

## Setup

1. Set up Raspberry Pi with camera module (I recommend 3B+)
2. Install the default Raspbian OS onto the rpi
3. Run `setup.sh` - Soon, this will be containerized and simple to set up, but forr now, if you want this to run when the raspberry pi starts up, you'll have to add this to systemd.
4. Run the `cs.sh` bash script. This sources venv for you then runs the server, there may be something missing you'll need to do in the rpi settings to enable the camera

If there's any missing py libraries, create a virtual env using python's `venv` module. Then, source into that venv and run `pip install -r requirements.txt` to install everything needed

*IMPORTANT*: Use `python -m venv --system-site-packages env` to set up the virtual environment. This uses the picamera+libcamera libraries directly from Raspbian bundled together. If you try to install `picamera2` from pip, you won't be able to install libcamera, you need the system packages.

In the case of this project, the `cs.sh` script is set up to source into the env for you when it runs. You may want to install packages or edit this project, source into the virtual env before doing so. You may need to edit the `cs.sh` script to match your virtual env name if it is not `env`


## Authentication

Create a new account using `create_account.sh`

After making an account, you'll need to set up OTP:

OTP is used to authenticate and get past the login webpage. To generate a base32 key, please run the `generate_key.sh` script 

This will save the key in a file named `.otp_key`. A QR code will be spat out in your terminal (so feel free to use SSH for this whole setup!), you can scan it and use Google Authenticator (or presumably, any OTP auth app with QR code support). FreeOTP is a good option.

You will use this OTP to log into the main login page

## Logging

Logs will be stored in `logs.txt`. The logs contain every login attempt, as well as different actions the server chose. Use these logs to see if anyone tried to send a POST request for example :) Easy peace-of-mind

