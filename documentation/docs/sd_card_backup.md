# Backup the SD Card

Rebuilding the Jetson Nano image is a lengthy process should the SD card get corrupted.
Doing periodic snapshots of the SD card, can give suitable restore points should the inevitable happen.

On the host machine, issue the following command and note the output.
```bash
df -h
```

Insert the SD card and reissue the command:

```bash
df -h
```

Look for what is added to the list and this is location of the SD card. The SD card may contain multiple partitions, so use the base part of the name, i.e., /dev/sdc1, use /dev/sdc.

Go to the directory you wish to save the image into and issue the following command:

```bash
sudo dd bs=4M if=/dev/sdc status=progress | gzip >filename.gz
``` 

Since the SD card is large and the transfer time long, including the status=progress is useful to insure that the operation is working.

# Restore
To restore the SD card image, follow the initial image flashing instructions using etcher.

**Note: these operations take hours to complete given the 128GB size of the SD card.  Further study needs to be done to see how this can be speeded up.**

