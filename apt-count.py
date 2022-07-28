#!/usr/bin/env python3
#coding=utf-8

import configparser
import apt
import os
import sys
import signal
import paho.mqtt.client as mqtt
import time
import configparser

# This is the default infomation.  Then we will read the config file
# for the current information
#

parser = configparser.ConfigParser()

ini_file_name = "/usr/local/etc/apt-count-config.ini"

flag = os.path.isfile(ini_file_name)

if not flag:
    exit("Config file "+ ini_file_name + " missing.\nPlease fix and try again. Exiting.")

parser.read(ini_file_name)

# Set deviceName to the hostname
deviceName = os.uname()[1]

class ProgramKilled(Exception):
    pass

def get_config(config, section, name):
    if config.has_option(section,name):
        return config.get(section,name)
    else:
        exit("Missing "+ name + ".\nPlease try again. Exiting.")

def signal_handler(signum, frame):
    raise ProgramKilled

def get_update_packages_count():
    
    # Return the number of updates available

    try:
        cache = apt.Cache(apt.progress.base.OpProgress())
    except SystemError as e:
        sys.stderr.write("Error: Opening the cache (%s)" % e)
        sys.exit(-1)

    try:
        cache.update()
    except SystemError as e:
        sys.stderr.write("Error: Marking the update (%s)" % e)
        sys.exit(-1)

    cache.open(None)
    cache.upgrade()

    update_count = len(cache.get_changes())
    return update_count

if __name__ == '__main__':

    # First we will check that we are running the script as root
    #
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

    broker_url = get_config(parser, "settings", "broker_url")
    broker_port = int(get_config(parser, "settings", "broker_port"))
    broker_username = get_config(parser, "settings", "broker_username")
    broker_password = get_config(parser, "settings", "broker_password")

    client = mqtt.Client()
    client.username_pw_set(broker_username, broker_password)

    pkgs = get_update_packages_count()
    print('%d updates' % pkgs)


    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    client.connect(broker_url, broker_port)

    client.publish(
        topic="homeassistant/sensor/Linux_Updates_Available/"+ deviceName +"/config", 
        payload='''{ 
            "name": "'''+ deviceName +'''", 
            "json_attributes_topic": "homeassistant/sensor/Linux_Updates_Available/'''+ deviceName +'''/state", 
            "entity_category": "diagnostic",
            "enabled_by_default": true,
            "state_topic": "homeassistant/sensor/Linux_Updates_Available/'''+ deviceName +'''/state", 
            "state_class": "measurement", 
            "unique_id": "linux_updates_available_'''+ deviceName +'''", 
            "value_template": "{{ value_json.updates_available_'''+ deviceName +''' }}", 
            "device":{
                "identifiers":["Linux_Updates"], 
                "manufacturer":"WLD", 
                "model":"Debian", 
                "name":"Updates Available" 
                } 
            }''', 
        qos=1, retain=True)
    
    time.sleep(6)

    client.publish(
        topic="homeassistant/sensor/Linux_Updates_Available/updates_available_"+ deviceName +"/state", 
        payload='{ "'+ deviceName +'": '+ str(pkgs) +' }', 
        qos=1, retain=True)
