FROM balenalib/rpi-raspbian

RUN apt update && apt install -f -y --no-install-recommends python3 gnupg git cmake gcc g++ python3-pip python3-venv libcap-dev pkg-config libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libavfilter-dev libswresample-dev libswscale-dev python3-picamera2

COPY requirements.txt .

RUN python3 -m venv --system-site-packages env
RUN /bin/bash -c "source /env/bin/activate"
RUN env/bin/python3 -m pip install --upgrade pip
RUN env/bin/python3 -m pip install -r requirements.txt

COPY * /app/

RUN touch /etc/udev/rules.d/99-camera.rules

RUN echo "SUBSYSTEM==\"vchiq\",MODE=\"0666\"" > /etc/udev/rules.d/99-camera.rules

CMD ["env/bin/python3", "/app/main.py"]

