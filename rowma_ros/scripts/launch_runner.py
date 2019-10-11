#!/usr/bin/env python
import sys
import json
import rospy
import socketio
import requests
import Geohash
import subprocess as sp
import uuid
from rosbridge_library.rosbridge_protocol import RosbridgeProtocol
import signal
import os
import re

rospy.init_node('launch_runner')
client_id_seed = 0
protocol = RosbridgeProtocol(client_id_seed)

sio = socketio.Client()

# Description: Get geohash from IP address
# output: geohash <string> 'xn774h0'
def get_geohash():
    url = "https://freegeoip.app/json/"

    location = json.loads(requests.request("GET", url).text)
    geohash = Geohash.encode(float(location['latitude']), float(location['longitude']))
    precision = 6 # cut to 6 characters
    return geohash[:precision]

# Description: Shape path to roslaunch available command.
# @param: path <string> '/dir/package_name/launch/package.launch'
# output: command <string> 'package_name package.launch'
def path_to_command(path):
    splited_path = path.split('/')
    if (len(splited_path) < 3):
        return
    i = 0
    launch_index = 0
    while (i < len(splited_path)):
        if (splited_path[i] == 'launch'):
            launch_index = i
        i += 1
    return splited_path[launch_index - 1] + ' ' + splited_path[launch_index + 1]

# Description: Get package commands list located at ROS_PACKAGE_PATH environment variable
# output: commands Array<string> ['package_name package.launch']
def list_launch_commands():
    ros_package_path = os.environ['ROS_PACKAGE_PATH']
    paths = ros_package_path.split(':')

    if len(paths) < 1:
        sys.exit('Set ROS_PACKAGE_PATH correctly')

    packages = []
    for path in paths:
        m = re.match(r'^/opt/ros', path)
        if m:
            break
        packages += sp.check_output("find " + path + " | grep \'\\.launch\'", shell=True).decode('utf-8').strip().split('\n')
    commands = []
    for package_path in packages:
        commands.append(path_to_command(package_path))
    return commands

@sio.event(namespace='/conn_device')
def connect():
    print('connection established')
    geohash = get_geohash()
    launch_commands = list_launch_commands()
    id = str(uuid.uuid1())
    msg = {
            'geohash': geohash,
            'uuid': id,
            'launch_commands': launch_commands
            }
    sio.emit('register_geohash', json.dumps(msg), namespace='/conn_device')
    print('Your UUID is: ' + id)

# On reveived a websocket message
@sio.event
def message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})
    message = json.loads(data)
    protocol.incoming(message)

@sio.on('run_launch', namespace='/conn_device')
def on_message(data):
    launch_commands = list_launch_commands()
    print(launch_commands)
    if data.get('command') in launch_commands:
        sp.call("roslaunch " + data.get('command'), shell=True)
        print('run_launch')
        print(data)

def outgoing_func(message):
    msg = json.loads(message)

protocol.outgoing = outgoing_func

@sio.event
def disconnect():
    print('disconnected from server')

def signal_handler(sig, frame):
        sio.disconnect()
        sys.exit(0)

sio.connect('http://18.176.1.219')
signal.signal(signal.SIGINT, signal_handler)
signal.pause()