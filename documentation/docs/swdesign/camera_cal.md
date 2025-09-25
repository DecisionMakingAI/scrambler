## Introduction

The process of calibrating pinhole cameras has bee around for a long.
OpenCV has a set of routines to perform the mathematics for this.
There are several tutorial articals and videos on doing this.
Two very good articles on this are:

* [OpenCV Tutorials](https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html#)
* Satya Mallick's [Camera Calibration using OpenCV](https://www.learnopencv.com/camera-calibration-using-opencv/)
* [Another Python](https://medium.com/analytics-vidhya/camera-calibration-with-opencv-f324679c6eb7)

There are three basic steps to this process:

1. Acquire a set of checkerboard or circle test pattern images from the camera to calibrate.
2. Run the camera calibration program and save coefficients to be used for reconstruction.
3. Develop setup code the properly correct the image.   This code will be inserted in the application that is run when the image is to be corrected.

## Acquiring Calibration Images

Print a copy of the checkerboard and/or circles test images.
These images are downloadable from [Checkerboard](https://docs.opencv.org/2.4/_downloads/pattern.png) and [Circles](https://docs.opencv.org/2.4/_downloads/acircles_pattern.png).
They are also stored in the development directory as *pattern.png* and *acircles_pattern.png*.


