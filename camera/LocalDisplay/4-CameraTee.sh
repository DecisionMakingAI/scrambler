#!/bin/bash
# Uses GSTREAMER to capture video from the camera, send it down two different
# paths to the display.  In future, would add separate process in one path.

gst-launch-1.0 nvarguscamerasrc \
    ! 'video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, \
        format=(string)NV12, framerate=(fraction)30/1' \
    ! nvvidconv flip-method=2 \
    ! 'video/x-raw(memory:NVMM), width=(int)320, height=(int)240, \
       format=(string)NV12' \
    ! videoconvert \
    ! tee name=t ! queue ! nv3dsink -e t. ! queue ! nv3dsink -e

