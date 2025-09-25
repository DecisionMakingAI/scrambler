#!/usr/bin/env python
'''
Stream video from the onboard video camera to the web.

Flask is the web server used here.  If is small and light weight, ideal for
this operation.

Flask takes care of generating the comsumers for the video stream. One consumer
is created for each client video stream.  Note: generally only one thread will
be in use, but it is possible to stream to multiple devices.

The application is started via the command:
    python web_stream.py

Accessing video from a browser is accomplished by entering this machines name
or ip address in the command line followed by the port number:

    scrambler.local:8000

or in the case of viewing it locally:

    localhost:8000

Capturing video frames and compressing them is done by the single producer
task, CameraProducer.  The producer communicates directly with the camera class.

The CameraEventMgr class routes compressed video frames between the producer and
the consumers for the clients.

This video streamer is implemented using threads.  The standard cpython
implementation of python only allows one thread to run at a time.  Since
this program is heavily I/O bound this should not be a problem.  The load on
the processor should typically be less than 20%, even smaller on the Jetson
nano if the hardware accelerator can be almost exclusively used.
'''

from importlib import import_module
import os
from flask import Flask, render_template, Response
import threading
from camera_event import *

app = Flask(__name__)

cev = CameraEventMgr()      # Create the event manager
vp = CameraProducer()       # Create the Camera Producer
vp.start(cev.put_frame)     # Start the producer with link for queueing frames

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        frame = cev.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    """
    Start the Flask Web Application.
    While it can be run on any feasible IP, IP = 0.0.0.0 renders the web
    app on the host machine's localhost and is discoverable by other machines
    on the same network.
    """
    app.run(host='0.0.0.0', port=8000, threaded=True)

    """
    After a ^C to terminate the app returns here after shutting down all
    the consumer threads it created.  The producer thread with the camera
    still needs to be properly released. Relying on automatic termination to
    properly clean up the gstreamer, doesn't always work.  If it doesn't get
    shutdown properly, a reboot is required to get it cleaned up.
    """
    vp.stop()               # terminate the video producer
