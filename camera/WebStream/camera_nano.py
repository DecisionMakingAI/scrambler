import os
import cv2


class Camera():
    """
    Jetson Nano CSI camera interface
    """

    def __init__(self, width=640, height=360, fps=10, quality=80):
        self.width = width
        self.height = height
        self.fps = fps
        self.quality = quality
        camera = cv2.VideoCapture(self.gstr(), cv2.CAP_GSTREAMER)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        self.cap = camera

    def get_frame(self):
        if self.cap.isOpened():
            _, img = self.cap.read()  # read current frame

            # encode as a jpeg image and return it
            return cv2.imencode('.jpg', img, \
                    [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])[1].tobytes()

    def start(self):
        if not self.cap.isOpened():
            self.cap.open(gstr(), cv2.CAP_GSTREAMER)

    def stop(self):
        if hasattr(self, 'cap'):
            self.cap.release()

    def gstr(self):
        return "nvarguscamerasrc "\
               "! video/x-raw(memory:NVMM), width=1280, height=720, "\
                    "format=(string)NV12, framerate=60/1 "\
               "! nvvidconv flip-method=2 ! videorate "\
               "! video/x-raw, width=%d, height=%d, "\
                    "framerate=(fraction)%d/1, format=(string)BGRx "\
               "! videoconvert ! video/x-raw, format=(string)BGR "\
               "! appsink wait-on-eos=false max-buffers=1 drop=True"\
                % (self.width, self.height, self.fps)
