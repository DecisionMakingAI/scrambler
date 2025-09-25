## Introduction

The linux image for the jetson nano already comes with the gstreamer installed.
There are no python interfaces included with this, except for opencv which has added a camera interface.
This if fine if you are only interested in grabbing baseband images to further process.
If you would like to take an image and compress it with the gstreamer inside of an application, you are out of luck.
The purpose of this exercise is to set up an environment to use the gstreamer inside a python program.

## Gstreamer Installation

To start with a new virtual environment was created:

```bash
    cpvirtualenv car gst
```

Note: if things go awry we can use 'rmvirtualenv' to clean up this mess.


Nvidia's [Accelerated Gstreamer Guide](https://developer.download.nvidia.com/embedded/L4T/r32_Release_v1.0/Docs/Accelerated_GStreamer_User_Guide.pdf?a6ZBlTHvmSASDPBwP2Epy7E4PlLILaxFACnTF_4Ant4USFNnxb4fWqszUEfHsJ2pvaXL82-alqH5O3Kr5wHeduD6fxqbde-hC9vN3RzX06VTbDfCvkNZoIaEs-eu9KXkb88pDTaq4apeeG9kSFHPxjGh4NUic19CiWaj6E9BbeId3oC1FPg) is followed here to insure the necessary gstreamer environment for the Jetson Nano is installed.

Installation follows these steps:
```bash
sudo add-apt-repository universe
sudo add-apt-repository multiverse
sudo apt-get update
sudo apt-get install gstreamer1.0-tools gstreamer1.0-alsa \
 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
 gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
 gstreamer1.0-libav
sudo apt-get install libgstreamer1.0-dev \
 libgstreamer-plugins-base1.0-dev \
 libgstreamer-plugins-good1.0-dev \
 libgstreamer-plugins-bad1.0-dev
```

To check the installation of GStreamer issue the following command:

```bash
    gst-inspect-1.0 --version
```

It should cleanly return some version information.

In following the "[How to install Gstreamer Python Bindings](http://lifestyletransfer.com/how-to-install-gstreamer-python-bindings/)" discovered that the API Check produced errors, so we need to build from source.
This failed also, as it couldn't resolve PyGObject module.

However, the following commands were issued which seem to have installed sufficient tools to run:

```bash
sudo apt-get install python3-gi python-gst-1.0 
sudo apt-get install libgirepository1.0-dev
sudo apt-get install libcairo2-dev gir1.2-gstreamer-1.0

pip install --upgrade wheel pip setuptools

pip install pycairo
pip install PyGObject`
```

Run the following test script to check installation:

```bash
python -c "import gi; gi.require_version('Gst', '1.0'); \
gi.require_version('GstApp', '1.0'); \
gi.require_version('GstVideo', '1.0'); \
gi.require_version('GstBase', '1.0')"
```

