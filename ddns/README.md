DDNS
=================
This project will allow you to remote connect from an external network using an authorized ssh key pair; we will create an ssh connection from a remote (client) computer to a host (server).

SSH Server Set-up
-----------------
Install the SSH server:

    sudo apt-get install openssh-server
    
Disable SSH password login by changing line (51) on the server from:

    #PasswordAuthentication yes
    
to:

    PasswordAuthentication no 
    
Next, generate the public and private keys:

    ssh-keygen -t rsa

You'll be asked to enter a passphrase. *Use a good, secure passphrase.*

    Enter passphrase (empty for no passphrase): [Type a passphrase]
    Enter same passphrase again: [Type passphrase again]
    
    Your identification has been saved in /home/you/.ssh/id_rsa.
    Your public key has been saved in /home/you/.ssh/id_rsa.pub.
    The key fingerprint is:
    01:0f:f4:3b:ca:85:d6:17:a1:7d:f0:68:9d:f0:a2:db
    
Lastly, add your new key to the ssh-agent and create a file for authorized keys:

    ssh-add ~/.ssh/id_rsa
    touch ~/.ssh/authorized_keys
    
The authorized keys file is where we will store approved .pub keys from other computers that we will allow to connect.

SSH Client Set-up
--------------------
Install the SSH client:

    sudo apt-get install openssh-client
    
Generate public and private keys as shown in the previous section. Now copy the contents of the file `~/.ssh/id_rsa.pub` from the client into the file `~/.ssh/authorized_keys` on the server.

Great, at this stage we should be able to remotely connect between the two computers on an internal network. To do this first find the IP of the server:

    ifconfig | grep 'inet addr'
    # look for the line along the lines of:
    # 192.168.X.XXX

Now from the client run:

    ssh <hostuser>@<host_ip_address>
    # E.g. 
    # ssh jeff@192.168.2.25
    
And voila you're in and should see the command prompt of the server. Next we are going to expand the capability to allow us to ssh in from external networks.

Router
--------------------
At a very high level the flow to remote connect from an external IP looks like:

    External client -> Router External -> Router Internal -> Server

We are required to adjust some settings our our router to map our servers internal port 22 to the clients external port 22. We must do:

1. DHCP Reservation: to reserve an internal IP address. When we connect to our router we are given an internal IP address at random between 0-255. A DHCP reservation will set asside a certain address that only we can access.

2. PortForwarding: We need to tell the router to map requests coming in on a given external port to an internal ip and port. This is why a DHCP reservation is essential.

DHCP Reservation
--------------------
Its in your router settings somewhere and is intuitive. Select any IP for your server (reserved usually based on its mac address). 

PortForwarding
--------------------
This is also intuitive after you dig up the setting in your router. You map the external request coming in on port 22 to the internal IP that you set in the last section on port 22. 

Wrapping up
--------------------
All that's left to do is test it out! You can get the servers external IP by looking online or just use this handy little line:

    wget http://smart-ip.net/myip -O - -q ; echo

and at last from the client run:
  
    ssh <hostuser>@<external_host_ip_address>
    
I bet you're wondering what that script is in here for? Well, every now and then your external IP might change in which case if you are looking to ssh in remotely you will have no idea what the external IP address is of the server. What the script is intended to do is simply print the external IP to a file in a Dropbox client (which is set to automatically update) so that you can check this file before you try and ssh into the server. 

Run this on a cronjob set to some sort of time interval you're comfortable with. As an example I use every 6 hours.
