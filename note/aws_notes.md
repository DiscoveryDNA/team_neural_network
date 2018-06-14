## Volumes

After setting up the EC2 image on AWS, you need to attach volume so you have disk space.  The volume size is super flexable, whatever you put on the volume is there and can be attached and detached from any image. Think of as a flash drive.  You pay for the size of the volume as long as it is active. If you only want to pay for the storage you are using, you can take a snapshot, then shut down your volume. You pay for snapshot size. The snapshot can then be restarted on a new volume.

**Steps for attaching volume**

1. Start old snapshot as a new volume
1. Attach volume to instance in gui
2. **ONLY FIRST TIME USING IT**: Create file system on your volume: `sudo mkfs -t ext4 device_name`.  I ran into a bug in which this doesn't work, but this does: `mkfs -t ext4 -L rootfs device_name`
3. `sudo mount device_name mount_point` (example `sudo mount /dev/xvdf data`
4. change permission for directory: `sudo chmod 777 -R mount_point`

**Useful commands**
- `lsblk` - look at your volumes
- `sudo file -s /dev/xvdf` ask if your volume is formatted. If output is data then it is *not* formatted.
- `df` - ask how much space
- `df -Th` 

\* There are ways to assign a volume to an instance and automatically attach at every bootup. But currently not using these, but def useful in future.

**Steps for detaching volume**

1. take snapshot of your volume
2. unmount: `umount -d /dev/sdh`
3. detach volume
4. delete volume

If you change the size of the volume you attach, you have to tell your image to resize the image or it only sees the previous size.

`resize2fs /dev/xvda1`
