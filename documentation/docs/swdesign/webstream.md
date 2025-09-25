## Introduction

In order to get resonable video over the to the remote host display, the video stream needs to be compressed then transmitted.
The host needs to have something running to receive and display this.

A common approach to this is to use the web browser.
Jupyter notebooks does this as well as the donkeycar software.

To start with, I went looking for a simple app to test this out and see what limitations there are.
[Using Jetson for Video Streaming](https://maker.pro/nvidia-jetson/tutorial/streaming-real-time-video-from-rpi-camera-to-browser-on-jetson-nano-with-flask) discusses video streaming for the Jetson Nano.
This program runs, but does not stream uniformly as the video is not sent out smoothly.

[Video Streaming with Flask](https://blog.miguelgrinberg.com/post/video-streaming-with-flask) gives a more general discussion of the video streaming process.
It was not set up for the nano and suffers many of the same problems.

[Flask Video Streaming Revisited](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited) is upgraded from the previous article and addresses more improvements and robustness issues.
This program has been modified to run on the nano and the details are discussed below.

Naturally, not being an expert on any of these tools, a little study was needed to sort this code out.
Flask is the framework used to accomplish this.  There is a good tutorial on the from [freecodecamp](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/).

In viewing this tutorial, one of the first things discovered is that they use python decorators. The [Decorators in Python](https://www.datacamp.com/community/tutorials/decorators-python) web page covers this in detail.

Threading is central to running this web app, a tutorial on [threading](https://realpython.com/intro-to-python-threading/) was consulted.

After all is said and done, these example apps did not handle shutting down the Jetson CSI Camera very well.
If this is not cleanly done, you are forced to do a reboot to fix the problem.
In addition, what appeared to be the best written program, turned out to be very difficult to follow and I couldn't figure out where to insert the necessary code to insure the camera would shutdown correctly.
After about so much time, it was time to consider writing the necessary code from scratch.


## Video Streaming App

To run the app, from the host:
```bash
    ssh donkey@scrambler.local

    # After logging in...
    pip install flask       # if not already installed

    cd ~/projects/camera/WebStream
    python web_stream.py
```

One the host, open a blank web page in your chrome browser and enter:

```bash
    scrambler.local:8000
```

or if the car is connected to a display you can issue the browser command:

```bash
    localhost:8000
```

Note: you may have to substute the IP address for scrambler.local.

You should see the camera output on the display.

This program also supports streaming to multiple devices, but performance may get sluggish rather quickly.

