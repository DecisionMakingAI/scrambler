gst-launch-1.0 nvarguscamerasrc ! \
	'video/x-raw(memory:NVMM), width=(int)640, height=(int)480, \
	format=(string)NV12, framerate=(fraction)20/1' ! \
	nvvidconv flip-method=2 ! \
	xvimagesink -e

