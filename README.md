# Linux_Server_Updates_Available
READ file is a work in progress

## What is it?

This project is designed to work with Home Assistant.  It will create a device with a list of sensors using the hostname of each linux server with the number of updates available for it.

![alt text](https://github.com/wayned1014/Linux_Server_Updates_Available/blob/master/images/screen_shot.png)

The reason for this project is because I have many linux server running on ESXi and wanted a central location to see if any of the systems need any updates.  I was hoping Glances had that as a plugin, but it did not(at lease what I could tell).  So i decided since I was in the process of learning Python I figured I would give it a try.  This is my first Python project and I know from past experiences with other languages through the years this is probably not the most efficient code that i wrote.  I will, over time, learn more better coding skills.  I am also open to suggestions on making the code more efficient.

## How to install

+ First, we will need to clone the repository:

```
git clone https://github.com/wayned1014/Linux_Server_Updates_Available.git
```

+ Change to the 'Linux_Server_Updates_Available' directory:

```
cd Linux_Server_Updates_Available
```

+  At this point if this is the initial install, edit the 'apt-count-config.ini' and fill in with the appropriate information.  If this is an update you do not need to edit this file as it will not overwrite your current config file.

+ now just run the install script:

```
sudo ./install_apt-count.sh
```

+ To run the script manually:

```
sudo apt-count.py
```

+ You can use crontab to schedule it to run periodically.  It will need to be added to either the root or system crontab.  I setup the following to execute the script every four hours:

```
10  */4  *  *  *  /usr/bin/python3 /usr/local/bin/apt-count.py > /dev/null 2>&1
```

## Tested with

+ Debian 10 & 11
+ Kubuntu 22.04
