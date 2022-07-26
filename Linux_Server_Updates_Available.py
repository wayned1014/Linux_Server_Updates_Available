#!/usr/bin/env python3
#coding=utf-8

import apt
import os
import sys
import signal
import paho.mqtt.client as mqtt

# from datetime import timedelta
# import datetime as dt
# import apt_pkg
# import subprocess
# from re import findall

# This information need to be filled in
#
broker_url = "0.0.0.0"          # MQTT server IP
broker_port = 1883              # MQTT server port
broker_username = "username"    # MQTT Username
broker_password = "password"    # MQTT Password

# Set deviceName to the hostname
deviceName = os.uname()[1]

client = mqtt.Client()
client.username_pw_set(broker_username, broker_password)

class ProgramKilled(Exception):
    pass

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

    pkgs = get_update_packages_count()
    print('%d updates' % pkgs)


    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    client.connect(broker_url, broker_port)

    client.publish(
        topic="homeassistant/sensor/Linux_Updates_Available/"+ deviceName +"/config", 
        payload='''{ 
            "name": "'''+ deviceName +'''", 
            "json_attributes_topic": "homeassistant/sensor/Linux_Updates_Available/state", 
            "entity_category": "diagnostic",
            "enabled_by_default": true,
            "state_topic": "homeassistant/sensor/Linux_Updates_Available/state", 
            "state_class": "measurement", 
            "unique_id": "linux_updates_available_'''+ deviceName +'''", 
            "value_template": "{{ value_json.'''+ deviceName +''' }}", 
            "device":{
                "identifiers":["Linux_Updates"], 
                "manufacturer":"WLD", 
                "model":"Debian", 
                "name":"Updates Available" 
                } 
            }''', 
        qos=1, retain=True)

    client.publish(
        topic="homeassistant/sensor/Linux_Updates_Available/state", 
        payload='{ "'+ deviceName +'": '+ str(pkgs) +' }', 
        qos=1, retain=True)

