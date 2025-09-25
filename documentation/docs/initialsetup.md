## Package Contents
The package contains everything necessary to get the car up and running, except a host computer.
Items in the package are:

* Partially assembled Donkeycar
* LiPo Battery charger (for charging both the 2S motor and 3S processor batteries)
* JST-XH 2S 6" Balance Charging Extension Cable
* JST-XH 3S 6" Balance Charging Extension Cable
* External 5V 5A power supply for operating the Jetson Nano in a stationary position
* USB Card Reader/Writer/OTG Adapter to handle reading and writing the micro SD card
* USB to serial port adapter for configuring the Jetson Nano host port and other RS-232 ports
* USB A to micro B cable
* USB extension cable, 6.5' for extending USB cables
* F710 wireless joystick for car remote control
* Second camera with camera mount (camera with normal lense)
* Assorted spare parts including clip and jumper pins
* Block to raise car off ground for testing
* Assorted shock spacers to adjust the car to sit level
* Small tools, for mounting and unmounting parts on the car

## Inspect Car

* Look car over for damage during shipment.
* Insure power switch on top of the ESC (Electronic Speed Control) of the car chassis is on. It is left on and the side panel switch will be used to enable power to the drive system.
* Insure jumper on top of ESC is set to the LiPo position.

## Car Assembly

The car was partially disassembled for compact packing and part protection so it could be shipped in the original container for the Exceed RC car.
Go to [Final Car Assembly](finalassy/introduction.md) to finish the assembly.

## Charge batteries

The [Charging Batteries](chargingbatteries.md) section illustrates connecting the charger to each of the batteries.
Even though the charger has two ports, it can only charge one battery at a time.
For shipping, the batteries are set to about a 50% charge or less for safety.

## Prepare F710 Joystick

All that needs to be done to ready the joystick is to insert the two AA batteries.
The USB receiver is already plugged in to the processor.
The joystick battery compartment has location to store the USB receiver, should it no longer be needed on the car.

## Login Information

A default user is set up on the Jetson Nano with a user name: *donkey* and password: *donkey*

## Headless Setup of WiFi Connections

When run at a new location, networking parameters will have to be configured.
See the [Headless Setup](headless_setup.md) section to perform this setup.
If an extra display, keyboard and mouse are available, you can go through the normal gui interface to establish WiFi connections instead.

## Set and Query Processor Power Mode

The Jetson Nano has two basic operating power modes.
A 5W mode so that it can run off power from the mini USB connector.
And a 10W mode that enables usage of the full processor performance.
10W mode can be used when power is supplied to the barrel jack on development board.
To enable power from this source, a jumper must be placed on J48.

The processor power levels can then be set and queried with the following commands:

```
    # Set to 10W mode
    sudo nvpmodel -m 0

    # Set to 5W mode
    sudo nvpmodel -m 1

    # Query the power setting
    sudo nvpmodel -q
```

## Setup Donkey Software

The [Install the software](https://docs.donkeycar.com/guide/install_software/) section of the reference guide covers the necessary topics.
Follow the section on "Install Software on Host PC".

The Donkey software has already been installed on the donkey car.
It takes several hours, so you probably don't want to repeat it unless necessary.
There were caveats in the basic install. The [Software Installation](setup_jetson_nano.md) of this document covers this in detail.

TensorRT can be setup on the Jetson Nano as described in the reference document, but has not been done.

Following the Donkeycar setup is a "create your car application" and "calibrate your car".
These operations have been done.  You should follow through these sections to familiarize yourself with the car software.

After all this, you are ready to go out on your own.

## Shock Spacers

The weight of this car is somewhat heavier than the standard car as shipped.
Some spacers for the shocks were 3D printed.  Four 5mm spacers (one to each shock) were added to the rear shocks to get it to sit level.
