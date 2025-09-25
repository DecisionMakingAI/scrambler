gst-launch-1.0 videotestsrc pattern=smpte ! \
	'video/x-raw, width=(int)640, height=(int)480, \
	framerate=(fraction)20/1' ! \
	xvimagesink -e

