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


if command -v pip3 > /dev/null; then
  pip3_installed=0
else
  pip3_installed=1
fi

Package=paho
python3 -c "import sys, pkgutil; sys.exit(0 if pkgutil.find_loader('$Package') else 1)"
pm_installed=$?

if [ $pm_installed -eq 1 ]
then
    echo "Missing paho.mqtt"
fi

if [ $pip3_installed -eq 1 ]
then
    echo "Missing pip3"
fi

if [ $pm_installed -eq 1 ] || [ $pip3_installed -eq 1 ]
then
    echo "Exiting..."
    exit
fi

#
# Now that we got here everything is ready for the install
#

py_file="apt-count.py"
if ! [ -f "$py_file"]; then
    echo "Not in the proper directory!"
    exit
fi

cp "$py_file" /usr/local/bin/"$py_file"
echo "Script installed."

ini_file="apt-count-config.ini"
if [ -f "$ini_file"]; then
    echo "INI file exists, not copied"
else
    cp "$ini_file" /usr/local/etc/"$ini_file"
    echo "INI file installed.  please edit the file with your settings."
fi

echo "Finished install.  You can delete the source file directory."
exit