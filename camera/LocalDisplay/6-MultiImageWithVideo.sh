WIDTH=320
HEIGHT=240
CAPS="video/x-raw, width=$WIDTH, height=$HEIGHT"

gst-launch-1.0 \
    nvcompositor name=comp \
        sink_0::xpos=0 sink_0::ypos=0 \
        sink_0::width=$WIDTH sink_0::height=$HEIGHT \
        sink_1::xpos=$WIDTH sink_1::ypos=0 \
        sink_1::width=$WIDTH sink_1::height=$HEIGHT \
        sink_2::xpos=0 sink_2::ypos=$HEIGHT \
        sink_2::width=$WIDTH sink_2::height=$HEIGHT \
        sink_3::xpos=$WIDTH sink_3::ypos=$HEIGHT \
        sink_3::width=$WIDTH sink_3::height=$HEIGHT \
    ! nvoverlaysink \
        videotestsrc is-live=true pattern=smpte ! $CAPS ! comp. \
        videotestsrc is-live=true pattern=ball ! $CAPS ! comp. \
        videotestsrc is-live=true pattern=zone-plate kx2=20 ky2=20 kt=1 ! $CAPS ! comp. \
        nvarguscamerasrc \
            ! 'video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, \
                format=(string)NV12, framerate=(fraction)30/1' \
            ! nvvidconv flip-method=2 ! $CAPS ! videoconvert ! queue ! comp.
