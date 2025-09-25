"""
Flask takes care of generating the comsumers for the video stream. One consumer
is created for each client video stream.  Note: generally only one thread will
typically be in use, but it is nice to have extras available.

Capturing video frames and compressing them will be done by a single producer
task.  The producer task is coded in here and connectes to the specified
camera.

The pipeline class in here takes care of routing video frames produced to each
client.
"""

import threading
from camera_nano import Camera

class CameraProducer():
    """
    Captures video frame and passes it to the event manager.
    """
    def __init__(self):
        self.cam = Camera()

    def start(self, vput):
        if not hasattr(self, 'thread') or not self.thread.isAlive():
            self.thread = threading.Thread(target=self.run, args=(vput,))
        self.running = True
        self.thread.start() # start the thread (calls 'run')

    def run(self, vput):
        """ Thread to continuously get and send video frames """
        while self.running is True:
            frame = self.cam.get_frame()
            vput(frame)     # queue up the frame

        self.cam.stop()     # insure gstreamer pipeline is properly shutdown

    def stop(self):
        """ Signal capture thread to terminate """
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()  # wait for thread to finish

class CameraEventMgr:
    """
    Class with single element pipeline between producer and multiple consumers.
    """
    def __init__(self):
        self.frame = None
        self.lock = threading.Condition()

    """
    Send video frames to the client.  Each client running as a separate
    thread will call this when it is ready for a frame.
    """
    def get_frame(self):
        self.lock.acquire()     # acquire the lock
        self.lock.wait()        # wait (releases lock while waiting) for frame
        frame = self.frame      # get the new frame
        self.lock.release()     # release the lock
        return frame

    """
    Queues up video frame to be sent to each client.
    If the clients are slow to react, any previous frames will be dropped.
    """
    def put_frame(self, frame):
        self.lock.acquire()     # grab the thread lock
        self.frame = frame      # set up the next frame
        self.lock.notifyAll()   # notify clients that new frame is available
        self.lock.release()     # release the thread lock
