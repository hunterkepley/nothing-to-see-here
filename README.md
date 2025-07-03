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

*IMPORTANT*: Use `python -m venv --system-site-packages env` to set up the virtual environment. This uses the picamera+libcamera libraries directly from Raspbian bundled together. If you try to install `picamera2` from pip, you won't be able to install libcamera, you need the system packages.

In the case of this project, the `cs` bash script is set up to source into the env for you when it runs. You may want to install packages or edit this project, source into the virtual env before doing so. You may need to edit the `cs` bash script to match your virtual env name if it is not `env`


## Authentication

This using OTP's as security for logging into the camera. Eventually this may be added on top of a normal login, but for now, I think this is enough since the OTPs are generated via an app on my phone only. Look up how to set up an OTP app, theyre very useful, required for this, and there's some open source ones
