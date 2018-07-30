# Using AWS in the DiscoveryDNA Neural Network Team

The Amazon Web Services (AWS) is a cloud computing service.  It essentially allows you to create and use any size computer you can imagine.  We in the Neural Network team use it to utilize GPU power when running Tensor Flow and have a central location for our large datasets. 

## Important Vocabulary 

- **EC2**: Stands for Elastic Cloud Commputing.  An EC2 instance is essentially a computer you start in the cloud.  You pay for the size and time you use the machine. Therefore it is essential that you only use the size you need for the time you need it. It is possible to accidently spend a lot of money very fast. Ciera does not like wasting money and will get mad.
- **Volume**: Disk space for your machine.  Think of as a flash drive or hard drive. Volumes are also created as the root drive for your EC2 instance.  These root drives are started and terminated with the EC2.
- **AMIs**:  An Amazon Machine Image [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html). You can create AMIs from any instance. An AMI is essentially the directions for building your EC2. An AMI includes the following:
  - A template for the root volume for the instance (for example, an operating system, an application server, and applications)
  - Launch permissions that control which AWS accounts can use the AMI to launch instances
  - A block device mapping that specifies the volumes to attach to the instance when it's launched
- **Spot Instance**: This is the service we use to start our EC2 images. [Spot Instances](https://aws.amazon.com/ec2/spot/getting-started/) allow us to use instances at a fraction of the cost because we are using "left over" AWS resources that are not in use by other people/busineses. 

## Starting EC2 image and connecting to Jupyter notebook
0. Make sure you are in "US West Oregon". This is the closest regions that allows P2 and P3 spot instances, which are used to provide GPU utilzation when running Tensor Flow. 
1. Click "Spot Request" in the left hand menu and click the blue "Request Spot Instances". Everything is the default setting with the exception of:
  - **AMI**: deep_learning_AWS_ubuntuV9_18July2018
  - **Instance type(s)**: close C3 and choose instance type: 
    -  t2.nano or t2.micro for basic tasks (small data cleaning jobs, folder organization, installing, documentation)
    -  t2.xlarge for formatting large datasets
    -  p2.xlarge for running tensorflow
  - **Availability Zone**:  us-west-2a (so you can use volumes)
  - **Security Group**: deep_learning_security 
  - **key**: oregon_group_key.pem
2.  Wait till the instance becomes active. From 1 min to 3 min usually.
3.  When instance ready, you can go to "Instances" section, Name your instance, and Slack Ciera that you have started using an instance.
4.  Copy the instance's public dns.
5.  `cd` to the your key directory.
6.  Use this command to access the instance: `ssh -L localhost:8888:localhost:8888 -i <your .pem filename> ubuntu@<your instance DNS>`. (**Note: This command is not the same as the one mentioned on the ec2 instance connecting page. For Jupyter Notebook to configure correctly, you need to use this command.**)
7.  The Amazon Deep Learning AMI uses Anaconda virtual environments to host and manage many different deep learning frameworks at the same time. Hence, you need to choose which deep learning framework you want to use at the beginning of each session:
  - For *TensorFlow(+Keras2) with Python3 (CUDA 9.0 and Intel MKL-DNN)*, use the command (type it anywhere in the terminal): `source activate tensorflow_p36`. This will take about 2 minutes to run.
  - For any other framework, follow the instruction detailed in the terminal window at the beginning of each session.
8.  To access the Jupyter Notebook, use the command: `jupyter notebook`. [Click here](#notes-on-terminating-the-jupyter-notebook-session) for important information about terminating the Jupyter Notebook session.
9.  Look for the sentence 'Copy/paste this URL into your browser when you connect for the first time, to login with a token:' in the terminal window. Copy the URL after this sentence **verbatim** into the browser (i.e. do not change `localhost` to anything else).
10.  By this point, you should be able to access the jupyter notebook in the browser.
11.  When finished, if you installed new software, make a new AMI and name accordingly. 
12.  We will terminate every instance when it is not in use, with the exception of t2.nano and t2.micro, which you can leave open for up to a week. 
12.  Terminate instance when done and Slack Ciera. 

## Notes on terminating the jupyter notebook session

It is crucial that you terminate the Jupyter Notebook session in the correct way. Otherwise, you would not be able to log back into the Jupyter Notebook (in the normal way) again. To terminate a Jupyter Notebook session, always press `Ctrl-c` then `y` in the terminal. Just clicking the `Logout` button on the webpage does not help.

If you did not close a session in the way mentioned above, and you cannot log back into the Jupyter Notebook again, use the following steps to close the notebook:

1. Issue `jupyter notebook list` in the terminal. It would list all currently running Jupyter Notebook sessions.
2. See if it lists the URL corresponding to port 8888. If there is such a URL, issue `jupyter notebook stop 8888`.
3. Issue `jupyter notebook list` again. The returned list should be empty now.
4. Log back into the Jupyter Notebook normally by issuing `jupyter notebook` and copying the URL prompted.

## Volumes

After setting up the EC2 image on AWS, you need to attach volume so you have disk space.  The volume size is super flexable, whatever you put on the volume can be attached and detached from any EC2 image. Think of volumes like flash drives.  You pay for the size of the volume for as long as it exists. If you only want to pay for the storage you are using, you can take a snapshot, then shut down your volume. You pay for snapshot size, but for less of a cost. The snapshot can then be restarted on a new volume of any size larger than the original snapshot. 

**Steps for attaching volume**

0. Start Volume. 
  A. Create a new volume and specify size (its easier to make a smaller volume bigger than decreasing volume, so pick minimum size until you know exactly what you will need. 
  B. Start a volume from a snapshot.
  C. Select an existing volume.
1. Attach volume to instance in gui by clicking on volume and selecting attach, choose the running EC2 instance you want to attach to. If you do not see your EC2 instance, this may because the instance and the volumes were started in different regions. 
2. **ONLY FIRST TIME USING IT**: Create file system on your volume: `sudo mkfs -t ext4 device_name`.  I ran into a bug in which this doesn't work, but this does: `mkfs -t ext4 -L rootfs <device_name>`
3. Mount the volume from within the instance using `sudo mount device_name mount_point` (example `sudo mount /dev/xvdf data`) 
  - use `lsblk` to see device name
4. change permission for directory: `sudo chmod 777 -R mount_point` to gain access 

**Steps for detaching volume**

You need to properly detach volume to avoid corruption of volume.

1. In EC2 instance terminal unmoun using: `sudo umount -d /dev/xvdf`
2. Detach volume (from AWS GUI Volumes section)
3. If you are unable to detach volume, take a snap shot of the volume and force detach or terminate instance. This way you have a backup of the volume you can restart if your volume is broken.  Likely the volume is fine though. It's analogous to properly detaching a flash drive from your computer vs just pulling it out.

**Steps for desizing volume**

AWS does not allow us to create a new volume with a smaller size from a snapshot. It would return an error message `“The size of a volume can only be increased, not decreased.” `

To desize a volume properly:

1. Create a new volume.
2. Attach both old and new volume to a same machine.
3. Move the data from the old volume to the new volume.
4. Delete the old volume.

**Useful commands**
- `lsblk` - look at your volumes
- `sudo file -s /dev/xvdf` ask if your volume is formatted. If output is data then it is *not* formatted.
- `df` - ask how much space
- `df -Th` 
- To copy files from your computer to the volume, use the following command: `sudo scp -r -i <your security key .pem file> <data folder address on your computer> ubuntu@instance_public_ip:folder_address_to_store_data_on_the_instance`.
- If you change the size of the volume you attach, you have to tell your image to resize the image or it only sees the previous size.
`resize2fs /dev/xvda1`

\* There are ways to assign a volume to an instance and automatically attach at every bootup. But currently not using these, but def useful in future.

## Workflow for doing neural network training

### Useful tips for using Keras with GPU

- For some neural networks, there are layers specifically designed for GPU acceleration. For example, for LSTM layer, there are two different options in Keras: `LSTM` and `CuDNNLSTM`. `LSTM` should only be used with CPU, using it with GPU would be > 2 times slower than CPU. Instead, you should use `CuDNNLSTM` with GPU. `CuDNNLSTM` achieves the same result as `LSTM` but is tailored for GPU. Using it can easily achieve a > 10 times speed boost when comparing with using CPU.
- For rnn networks, you should always use the ‘CuDNN’ version of layers in order for GPU acceleration to work properly.
- At current stage, the GPU shouldn’t take more than 1 minute to run 1 epoch for our data. If it takes much longer than that (e.g. > 2 minutes), it is a sign that GPU is not fully utilized.
- A quick way to test GPU is running: open the notebook 'tutorials/ensorFlow/3_mnist_from_scratch.ipynb', and run cells. Then in another terminal window connected to the EC2 instance run the command: `nvidia-smi -l 1`. This will update every second and you should see GPUs running in real time. Use this command to monitor your GPU usage while running tensorflow.  

## Useful Commands

 - Use the `screen` program to monitor the GPU usage while the jupyter notebook is running:
    1. The `screen` program let you open multiple windows that work seperately at the same time on the Ubuntu virtual machine.
    2. Type `screen` and press `enter` to initiate the `screen` program.
    3. Type `control-A` then `C` to open a new window where you can run the GPU monitor.
    4. To switch between the window of jupyter notebook and the GPU monitor, use either `control-A` then `P` (move to the previous window) or `control-A` then `N` (move to the next window).
 - `nvidia-smi -l 1` - monitor and view GPU usage every second
 - `lspci | grep -i nvidia` - ask which NVIDIA controller you are using
 - To check if tensorflow is working (in jupyter notebook):
 
 ```
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```

