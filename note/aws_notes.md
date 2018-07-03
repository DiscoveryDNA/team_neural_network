## To start an instance on spot instance

You can create AMIs from any instance.  An Amazon Machine Image [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html). An AMI includes the following:

- A template for the root volume for the instance (for example, an operating system, an application server, and applications)
- Launch permissions that control which AWS accounts can use the AMI to launch instances
- A block device mapping that specifies the volumes to attach to the instance when it's launched

You can create an AMI from any instance that you create. This is how we will manage our EC2 images. We will terminate every instance when it is not in use. 

From now on, we are going to be using [Spot Instances](https://aws.amazon.com/ec2/spot/getting-started/). Spot instances will allow us to use instances at a fraction of the cost. 

## Workflow
0. Make sure you are in "US West Oregon". This is the closest regions that allows P2 and P3 spot instances.
1. Click "Spot Request" in the left hand menu and click the blue "Request Spot Instances". Everything is the default setting with the exception of:
  - AMI: deep_learning_AWS_ubuntuV9_28June2018
  - Instance type(s): close C3 and choose p2.xlarge
  - Security Group: deep_learning_security
  - key: oregon_group_key.pem
2.  Wait till the instance becomes active. From 1 min to 3 min usually
3.  When instance ready, you can go to "Instances" section, Name your instance, Slack Ciera that you have started using an instance.
4.  Copy the instance's public dns.
5.  `cd` to the your key directory.
6.  Use this command to access the instance: `ssh -L localhost:8888:localhost:8888 -i <your .pem filename> ubuntu@<your instance DNS>`. (**Note: This command is not the same as the one mentioned on the ec2 instance connecting page. For Jupyter Notebook to configure correctly, you need to use this command.**)
7.  The Amazon Deep Learning AMI uses Anaconda virtual environments to host and manage many different deep learning frameworks at the same time. Hence, you need to choose which deep learning framework you want to use at the beginning of each session:
  - For *TensorFlow(+Keras2) with Python3 (CUDA 9.0 and Intel MKL-DNN)*, use the command (type it anywhere in the terminal): `source activate tensorflow_p36`. This will take about 2 minutes to run.
  - For any other framework, follow the instruction detailed in the terminal window at the beginning of each session.
8.  To access the Jupyter Notebook, use the command: `jupyter notebook`.
9.  Look for the sentence 'Copy/paste this URL into your browser when you connect for the first time, to login with a token:' in the terminal window. Copy the URL after this sentence **verbatim** into the browser (i.e. do not change `localhost` to anything else).
10.  By this point, you should be able to access the jupyter notebook in the browser.
11.  A quick way to test GPU is running: open the notebook 'tutorials/ensorFlow/3_mnist_from_scratch.ipynb', and run cells. Then in another terminal window connected to the EC2 instance run the command: `nvidia-smi -l 1`. This will update every second and you should see GPUs running in real time. Use this command to monitor your GPU usage while running tensorflow.  
12.  When finished, if you installed new software, make a new AMI and name accordingly. 
13.  Terminate instance when done and Slack Ciera. 

**Useful Commands**

 - Use the `screen` program to monitor the GPU usage while the jupyter notebook is running:
  - The `screen` program let you open multiple windows that work seperately at the same time on the Ubuntu virtual machine.
  - Type `screen` and press `enter` to initiate the `screen` program.
  - Type `control-A` then `C` to open a new window where you can run the GPU monitor.
  - To switch between the window of jupyter notebook and the GPU monitor, use either `control-A` then `P` (move to the previous window) or `control-A` then `N` (move to the next window).
 - `nvidia-smi -l 1` - monitor and view GPU usage every second
 - `lspci | grep -i nvidia` - ask which NVIDIA controller you are using
 - To check if tensorflow is working (in jupyter notebook):
 ```
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```

## Useful tips for Using Keras with GPU

- For some neural networks, there are layers specifically designed for GPU acceleration. For example, for LSTM layer, there are two different options in Keras: `LSTM` and `CuDNNLSTM`. `LSTM` should only be used with CPU, using it with GPU would be > 2 times slower than CPU. Instead, you should use `CuDNNLSTM` with GPU. `CuDNNLSTM` achieves the same result as `LSTM` but is tailored for GPU. Using it can easily achieve a > 10 times speed boost when comparing with using CPU.
- For rnn networks, you should always use the ‘CuDNN’ version of layers in order for GPU acceleration to work properly.
- At current stage, the GPU shouldn’t take more than 1 minute to run 1 epoch for our data. If it takes much longer than that (e.g. > 2 minutes), it is a sign that GPU is not fully utilized.


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
2. unmount: `sudo umount -d /dev/xvdf`
3. detach volume
4. delete volume

If you change the size of the volume you attach, you have to tell your image to resize the image or it only sees the previous size.

`resize2fs /dev/xvda1`


