# Screws

The 3D printed parts and electronics will be held together by screws.
Self threading screws are the most desireable since they take the least post printing effort for mounting.
For the small screws here, sheet metal screws usually work well, however, screws designed for threading plastic have some advantages.
Plastic thread forming screws have sharply angled threads that require less driving force and are less likely to crack the plastic.

There many vendors for screws on the web.
Only a few have a good selection of screws designed for plastic.
McMaster-Carr, has a wide selection and good shipping times.
The only down side is that they tend to be expensive.
Most of their smaller screws come with torx heads.
Torx allows you to apply extra force with less slippage or damage to the recess than the most common philips head.
Again, the downside to this, is that not everyone has access to small torx screw drivers.
Nonetheless, this is the chosen screw for putting this robot together.

# Circuit Board Mounting Requirements

Each circuit board or piece of hardware has different sized mounting holes.
Some consolidation of sizes could take place, but for the initial pass, appropriate sized scres were used for each.

The following lists the measurements component.

| Item 	| Hole Size 	| Length 	|
|--------------	|-----------	|--------	|
| Camera 	| 2.1mm 	| 5mm 	|
| Volt Meter 	| 2.0mm 	| 4mm 	|
| Servo Contoller | 2.6mm 	| 5mm 	|
| Regulator 	| 3.1mm 	| 4mm 	|
| Jetson Nano 	| 2.7mm 	| 8mm 	|

To minimize the screw varieties, the selected screws with their parameters are outlined below:

| Item 	| Screw<br>(mm) 	| Drive Size 	| Head Size<br>dia / ht (mm) 	| Drill Size<br>(mm) 	| Bit to Clean<br>Printed Hole 	|
|:-------------------:	|:-------------:	|:----------:	|:--------------------------:	|:------------------:	|:----------------------------:	|
| Camera<br>Voltmeter 	| M2 x 5<br>self tapping 	| T6 	| 3.35 / 1.6 	| \#52 - 1.6129 	| 1/16" 	|
| Servo Controller<br>Jetson Nano<br>Regulator 	| M2.5 x 8<br>self tapping 	| T8 	| 4.25 / 1.9 	| \#45 - 2.0808 	| 5/64" 	|
| Roll Bar 	| M3 x 16<br>self tapping 	| T10 	| 5.15 / 2.3 	| \#41 - 2.4384 	| 3/32" 	|
| Board Sandwich 	| M3 x 24 	| T10 	| 5.15 / 2.3 	| 3.0 	| 1/8" 	|

Even tough the 3D printer has parameters to control the amount of horizontal expansion, when printing small holes, there is always some extra expansion or imperfections, so using a drill bit to clean out a printed hole makes inserting screws much easier.
SAE bits are more common, so the above right table column lists the bit to use for cleaingn out the printed holes.

# 3D Printed Sandwich Mounting

Three layers of printed materials form a sandwich that is mounted to the chassis.
The center layer is the base layer from which the other components are mounted.

Below this layer are the two side panels.
These panels are bolted to the base with M3x24mm screws with nyloc nuts.
Bolts and nuts are used here so that we don't rely on integrety of the Z-axis filament strength to hold things together.

Above the center layer is mounted the processor and camera mount board.
This layer encloses the processor battery.
To make battery access easy, this layer is held in place by bent spring clips that are used in several places on the car.

# Mounting to the Chassis

There are four mounting points where the car top (which is removed) is attached.The sandwich mounts to these points with the same bent spring clips.

# Mounting the Camera

A useful feature might be to have a pan and tilt camera on the car.
The full implementation of this will take place later, but there is sufficient room to mount the Adafruit Pan/Tilt mechanism.
The camera mount location is based on this mechanism's requirements.
A 3D print of a fixed camera will use these mounting points.

