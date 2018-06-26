## To start an instance on spot instance

You can create AMIs from any instance.  An Amazon Machine Image [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html). An AMI includes the following:

- A template for the root volume for the instance (for example, an operating system, an application server, and applications)
- Launch permissions that control which AWS accounts can use the AMI to launch instances
- A block device mapping that specifies the volumes to attach to the instance when it's launched

You can create an AMI from any instance that you create. This is how we will manage our EC2 images. We will terminate every instance when it is not in use. 

From now on, we are going to be using [Spot Instances](https://aws.amazon.com/ec2/spot/getting-started/). Spot instances will allow us to use instances at a fraction of the cost. 

## Workflow

1. Click "Spot Request" in the left hand menu and click the blue "Request Spot Instances". Everything is the default setting with the exception of:
  - AMI: group_image_22june2018 - ami-89b157ea
  - Instance type(s): close C3 and choose either the g2.8xlarge (for full analysis) or g2xlarge (for learning and set-up) instance type
  - Security Group: Bitfusion Ubuntu 14 TensorFlow-2017-04-AutogenByAWSMP-2
  - key: versleuteling2
2.  Wait till the instance becomes active. From 1 min to 10 min usually
3.  When instance ready, you can go to "Instances" section, Name your instance, Slack Ciera that you have started using an instance.
4.  Use as normal.
5.  When finished, if you installed new software, make a new AMI and name accordingly. 
6.  Terminate instance when done and Slack Ciera. 




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
