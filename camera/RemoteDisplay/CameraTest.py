import os
import cv2
 
# Work around DISPLAY issues
disp = os.environ["DISPLAY"]
os.environ["DISPLAY"] = ':0'

# Set video size information
width = 640
height = 480
fps = 10

# Create a VideoCapture object
gst_str = ('nvarguscamerasrc ! '
    'video/x-raw(memory:NVMM), '
    'width=(int)1280, height=(int)720, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=2 ! '
    'video/x-raw, '
    'width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'appsink' % (fps, width, height))

cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Put back the display environment
os.environ["DISPLAY"] = disp
 
winName = "CameraWin"
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
cv2.resizeWindow(winName, width, height)
cv2.setWindowTitle(winName, "Preview")
 
while(True):
  ret, frame = cap.read()
 
  if ret == True: 
     
    # Display the resulting frame    
    cv2.imshow(winName, frame)
 
    # Press q on keyboard exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
      break
    if cv2.getWindowProperty(winName, 0) < 0: #see if user closed the window
        break
 
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()

