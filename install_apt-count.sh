#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo " please run script as root(sudo)."
    exit
fi

echo "This script will install/update apt-count.  It will also check to"
echo "make sure all dependencies are also install."
echo ""
read -r -p "Do you want to continue? [y/N] " response
if ! [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    exit
fi

packages="python3-paho-mqtt python3-packaging python3-requests-futures"

for package in $packages; do
    dpkg -s "$package" >/dev/null 2>&1 && {
        echo "$package is installed."
    } || {
        apt-get install $package
    }
done

#
# Now that we got here everything is ready for the install
#

py_file="apt-count.py"
if ! [ -f "$py_file" ]; then
    echo "Not in the 'Linux_Server_Updates_Available' directory!"
    exit
fi

cp "$py_file" /usr/local/bin/"$py_file"
echo "Script installed."

ini_file="apt-count-config.ini"
if [ -f /usr/local/etc/"$ini_file" ]; then
    echo "INI file exists, not copied"
else
    cp "$ini_file" /usr/local/etc/"$ini_file"
    echo "INI file installed.  please edit the file with your settings."
fi

echo "Finished install.  You can delete the source file directory."
exit