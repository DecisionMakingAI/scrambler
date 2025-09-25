## Hotspot

Explored hotspot creation as a means to setup WiFi access to a local host in environments that it is difficult to connect to the local network system.
[This](https://medium.com/@jones.0bj3/wireless-networking-for-the-jetson-nano-and-rpi-504868dd1b3a) article discusses setting up a hotspot between the Jetson nano and a linux laptop.

## Jetson Nano as the Hotspot

I ran a little experiment to see how feasable this is.

* Plugged a spare Edimax WiFi module into the host.
* Issued the command to see if it is discovered:

```bash
    nmcli d
    # output shows the device is disconnected
```

* Connect USB cable between host and nano.
* Login to the nano from the host on this port.

```bash
    screen /dev/ttyACM0 115200

    # Login to nano
```

* Issue the following commands to setup the hotspot

```bash
    # Shutdown current network connection
    sudo nmcli c down <current-connected-SSID>

    # Create a hotspot named 'scrambler'
    sudo nmcli -a dev wifi hotspot ifname wlan0 ssid scrambler

    # see if the device is connected as a hotspot
    nmcli c

    # Setup priority for auto-connect
    # (needs priorities set for other networks as well)
    # Did not actually test this out
    sudo nmcli c midufy scrambler connection.autoconnect-priority <int>
```

* From the host, connect to the hotspot

```bash
    # find the SSID
    nmcli d wifi list

    # connect to the network
    sudo nmcli -a d wifi connect scrambler

    # See which IP addresses it gave us
    route -n

    # remote login to the nano
    ssh donkey@10.42.0.1
```

It seems like there are a few other parameters that should be set up, but it does work.

## Local Host as the Hotspot

If the local host is equiped with the extra WiFi adapter and it is the hotspot, then we can use it to manage the traffic and perhaps set up the passthrough to the web, all without burdoning the Jetson Nano which is really intended for other tasks.

Using the grahical interface on the host is the easiest way to setup the interface.
[This](https://vitux.com/make-your-ubuntu-pc-a-wireless-access-point/) site describes the process for doing this on Ubuntu 18.04.

```text
    settings->wifi
    select the network device (may have to connect to a network first)
    menu bar->Turn On Wi-Fi Hotspot...
    remember password
```

When this is up and running you can just connect to it from the nano as before.

This also routes the nano out to the web as necessary.
