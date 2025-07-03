# NOTHING TO SEE HERE

This is an open source multi-function security camera project written in Python for use with Raspberry Pis

This is a lightweight, easy to set up camera server

## Setup

1. Set up Raspberry Pi with camera module (I recommend 3B+)
2. Install the default Raspbian OS onto the rpi
3. Install python 3 when set up
4. Eventually, this will be containerized and simple to set up. For now, you'll have to add this to systemd if you want it to run on startup.
5. Run the program and it should start the camera server using the `cs` bash script. This sources venv for you then runs the server, there may be something missing you'll need to do in the rpi settings to enable the camera

If there's any missing py libraries, create a virtual env using python's `venv` module. Then, source into that venv and run `pip install -r requirements.txt` to install everything needed


## Authentication

This using OTP's as security for logging into the camera. Eventually this may be added on top of a normal login, but for now, I think this is enough since the OTPs are generated via an app on my phone only. Look up how to set up an OTP app, theyre very useful, required for this, and there's some open source ones
