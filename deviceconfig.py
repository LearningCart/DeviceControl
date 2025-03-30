"""
------------------------------------------------------------------------------
Relay Control Board - A menu based relay control board that can replaces
                      large number of switches with 16x2 LCD and a rotary encoder.
                      It also remembers the state of each device to ensure
                      that it starts with same satate when power is restored.
------------------------------------------------------------------------------

Author: Jatin Gandhi (https://github.com/LearningCart)
Created: 2025-03-29
Updated: 2025-03-30
Version: v1.0
License: MIT (see LICENSE file for details)

Description:
    This file contains core logic to parse the json configuration files
    and provide necessary interfaces to access the loaded configuration
    data.

Supported Platforms:
    - MicroPython v1.24.1 on 2024-11-29; 
    - Board: Raspberry Pi Pico with RP2040

Usage:

-------------------------------------------------------------------------------
"""
"""
-------------------------------------------------------------------------------
 Modules
-------------------------------------------------------------------------------
"""
import gc
import ujson
import utime

# Import all constants and defines.,
from proj_defines import *
# Import error state
from display import error_state


"""
-------------------------------------------------------------------------------
 Global variables 
-------------------------------------------------------------------------------
"""
# Dictionary to store the json file data for devices.json
deviceinfo   = None;
# Dictionary to store the json file data for devicestate.json
devicestatus = None;

# Total devices connected to the system.
total_devices = 0;

"""
-------------------------------------------------------------------------------
 Functions 
-------------------------------------------------------------------------------
"""

"""
This function loads the devices.json and devicestate.json files.,

Args:
    
Returns:
        None

Raises:

Notes:
    - This function assumes devices.json and devicestate.json files
    - to be present in the root directory of the micropyton board.
"""
def load_device_config():
    global deviceinfo;
    global devicestatus;
    global total_devices;
    
    # Re-initialize the global variables, just be on safe side., 
    deviceinfo    = None;
    devicestatus  = None;
    total_devices = 0;
    
    # Load device name(to be shown on display.,) and mapped GPIO
    with open(deviceinfo_cfgfile, "rb") as f:
        deviceinfo = ujson.load(f);

    # Load last know status, so that it persist the power cycle.,
    # if we call save_device_state() on each GPIO write., 
    with open (devicestatus_cfgfile, "rb") as f:
        devicestatus = ujson.load(f);

    if(numdevices not in deviceinfo.keys() and numdevices not in devicestatus.keys()):
        print("Key (numdevices) not found");
        error_state( "\'no tag : 1\'");

    # numdevices of each configuration file "MUST" match., 
    if(deviceinfo[numdevices] != devicestatus[numdevices]):
        errmsg = "Invalid configuration., please check {0}, {1} ->> numdevices".format(deviceinfo_cfgfile, devicestatus_cfgfile);
        print(errmsg);
        error_state( "tag 1 mismatch");
    else:
        # Value of both numdevice tags identical.,
        # Configuration is accurate.,
        # set total_devices to value.,
        total_devices = int(deviceinfo[numdevices]);

    gc.collect();
    utime.sleep_ms(50);
    pass; # End-of-Function

"""
This function returns deviceinfo (Device ID, Device name and
corresponding GPIO pin assigned to this device.

Args:
    None

Returns:
    dictionary: deviceinfo device information dictioonary.

Raises:
    

Example:
    True

Notes:
    - This function assumes load_device_config() is successful.
    deviceinfo dictionary structure contains multiple device ID entries:
    Structue:
    Device Id : [<"Device Name String">,  <GPIO Pin>].
    e.g.,
    0 : ["First Device",  28],
    Hence, devices[deviceid][0] will give device name (< (16  - Reserved) characters)
    and    devices[deviceid][1] will give device GPIO pin.,
"""

def get_device_info():
    global deviceinfo;
    return deviceinfo;
    # End-of-Function


"""
This function returns devicestatus (Device ID, status ) of the device.

Args:
    None

Returns:
    dictionary: devicestatus device information dictioonary.

Raises:
    

Example:

Notes:
    - This function assumes load_device_config() is successful.
"""
def get_device_status():
    global devicestatus;
    return devicestatus;
    # End-of-Function

"""
This function returns total number of devices found in numdevices tag.

Args:
    None

Returns:
    integer: total numbner of devices connected to the controller.,

Raises:
    

Example:


Notes:
    - This function assumes load_device_config() is successful.
"""
def get_total_devices():
    global total_devices;
    return total_devices;
    # End-of-Function

"""
This function returns name of device for 'deviceid'.

Args:
    integer: deviceid out of 0 -> total device - 1

Returns:
    integer: total numbner of devices connected to the controller.,

Raises:
    

Example:


Notes:
    - This function assumes load_device_config() is successful.
"""
# Device ID should range from 0 to total_devices - 1
def get_device_name(deviceid):
    global deviceinfo;

    if( deviceid < 0 or deviceid >= total_devices):
        # Return empty string :(.., Silent failure :(..,
        # Should we call display.error_state() here?
        return ""; 
    else:
        # Each element at deviceinfo[deviceid] is a list of device name and gpio pin
        # Structue: device : [Device Name, GPIO pin], 
        # hence deviceinof[deviceid][0] will give device name
        return deviceinfo[deviceid][0];
    # End-of-Function


"""
This function is the entry function of this module.
It loads the devices.json and devicestate.json configurations.

Args:
    None

Returns:
    None

Raises:
    

Example:


Notes:
    - This function calls load_device_config().
"""
def init():
    load_device_config();

# End-of-File
