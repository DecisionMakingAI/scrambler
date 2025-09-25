If an extra display, keyboard and mouse are available, you can go through the no
rmal gui interface to establish the necessary WiFi connections to get the car up and running.
For situations where this is not available, a headless setup procedure can be used.
It requires a terminal emulator on the host and a USB cable connected between the host and the micro USB port on the Jetson Nano.


# Host Setup

There are many serial terminals available and almost any will do.
The example here will use *screen* on a linux machine.
If you are on a windows machine, *puTTY* is a good emulator to use.

If not already installed on the host, it can be simply done via:

```
    sudo apt-get update
    sudo apt-get install screen
```

To discover which port the USB cable is plugged into, open a terminal window and type the following command:

```
    dmesg --follow
```

Connect the USB cable between the Jetson Nano and the host, and observe the output of dmesg.
Somewhere in the spew of information, some TTY port information will show up.
Typically, the port will show up as *ttyACM0*.

Exit out of the *dmesg* command.

Start up the terminal emulator with the command:

```
    sudo screen /dev/ttyACM0 115200
```

You are now ready to log into the port.

# Configuring WiFi Parameters

In configuring a WiFi setting, there are three types of variables of interest:

| Variable 	| Values 	|
|--------------------------	|---------------------------	|
| <SavedWiFiConnections\> 	| list of saved connections 	|
| <WiFiSSID\> 	| available networks 	|
| <WiFiInterface\> 	| device interfaces 	|

This information can all be queried through the following commands

```
    # Get a list of saved connections (<SavedWiFiConnections>)
    nmcli c

    # Get a list of available networks (<WiFiSSID>)
    nmcli d wifi list

    # optionally to get a fresh list
    nmcli d wifi list rescan

    # To get the list of interfaces (<WiFiInterface>):
    # Typically the value of interest is: wlan0
    ifconfig -a
```

In the commands below, substitute the environment values for <SavedWiFiConnections\>, <WiFiSSID\>, and <WiFiInterface\>. Note that the shorthand arguments 'c' and 'd' stand for 'connection' and 'device' respectively.

```
    # disconnect from a network
    sudo nmcli c down <SavedWiFiConnection>

    # connect to a saved network
    sudo nmcli c up <SavedWiFiConnection>

    # If password is not automatically recognized issue this command
    sudo nmcli -a c up <SavedWiFiConnection>
```

To connect to a new network, issue the following command.
The -a stands for 'ask' for the password.
The connection should be saved and will reconnect automatically the next time the processor is booted.

```
    sudo nmcli -a d wifi connect <WiFiSSID>
```

To forget a connection:

```
    sudo nmcli c delete <SavedWiFiConnection>
```

# Changing Current Time Zone if Necessary

```
    sudo dpkg-reconfigure tzdata
```

When the menu comes up select the appropriate country, e.g., America.
Then select from a list of cities in your time zone.

