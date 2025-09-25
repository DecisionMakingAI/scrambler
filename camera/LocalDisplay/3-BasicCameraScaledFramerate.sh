gst-launch-1.0 nvarguscamerasrc \
	! 'video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, \
	    format=(string)NV12' \
    ! nvvidconv flip-method=2 ! videorate \
    ! 'video/x-raw, width=(int)640, height=(int)480, \
	    format=(string)NV12, framerate=(fraction)5/1' \
	! videoconvert \
	! xvimagesink -e

