"""
------------------------------------------------------------------------------
Relay Control Board - A menu based relay control board that can replaces
                      large of switches with 16x2 LCD and a rotary encoder.
                      It also remembers the state of each device to ensure
                      that it starts with same satate when power is restored.
------------------------------------------------------------------------------

Author: Jatin Gandhi (https://github.com/LearningCart)
Created: 2025-03-29
Updated: 2025-03-29
Version: v1.0
License: MIT (see LICENSE file for details)

Description:
    This file contains core logic to control the GPIO pins of corresponding
    devices.
    During initialization, it configures pins defined for each devices,
    fetch the last saved state and set the initial values.

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

import gc;
import utime
import ujson

from machine import Pin

from display import lcd
from display import error_state

# Import all constants and defines.,
from proj_defines import *

# Import device config., 
import deviceconfig

"""
-------------------------------------------------------------------------------
 Global variables 
-------------------------------------------------------------------------------
"""
# GPIO pins already used to connect peripheral.,
# It can not be allocated to device relay.
# fuction config_gpio() checks during device GPIO configuration.
allocated_pins = [I2C_LCD_SDA_PIN,
                  I2C_LCD_SCL_PIN,
                  ROTARY_ENCODER_CLOCK_PIN,
                  ROTARY_ENCODER_DATA_PIN,
                  ROTARY_ENCODER_SWITCH_PIN];

# Pin informaton structure.,
devicepins = [];

"""
-------------------------------------------------------------------------------
 Functions 
-------------------------------------------------------------------------------
"""

"""
This function initialize thee device GPIO pins and sets them to thier initial
values before power off.,
It creates "Pin" object and stores them in the list devicepins.
They are 'index bound' with device ID.

Args:
    
Returns:
        None

Raises:
        TODO: Add exception handling in next versoin.

Notes:
    - This function assumes deviceconfig.init() is successful and all the
    - device configuration is readily available. 
    - to be present in the root directory of the micropyton board.
    - FIXME:
      Known bug: Sometimes, deviceconfig module doesn't load the devicestate.json
      correctly.,
      It shows all off devices as 0, however for some device that was on (1) before
      power failure, it shows 0!!.
      Upon checking the devicestate.json file, it shows correctly but when same file
      is loaded (even in REPL), it shows incorrect state just like deviceconfig module.
"""
def init():
    global allocated_pins;
    global devicepins;
    global devicestatus;
    
    # Get the device inforamation dictionary pre-parsed from devices.json file.
    deviceinfo   = deviceconfig.get_device_info();

    # Get device status dictionary pre-parsed from devicestate.json file.
    devicestatus = deviceconfig.get_device_status();
    if (None == deviceinfo or None == devicestatus):
        print("Please configure the device first, deviceconfig.init() first");
        error_state("Not Conf..,");
        
    if(len(deviceinfo) <= 0 or len(devicestatus) <= 0):
        print("Please load configuration first., ");
        error_state( "Config Err");

    if(numdevices not in deviceinfo.keys()):
        print("Key (numdevices) not found");
        error_state( numdevices);
    
    devices = deviceinfo[numdevices];

    devicepins.clear();

    for i in range(devices):
        gpio = deviceinfo[i][1];
        # Check if GPIO for relay/device is already in use by us., 
        if gpio in allocated_pins:
            print("Config error, GPIO pin already assigned");
            error_state( "GPIO Re-used");
        else:
            pin = Pin(gpio, Pin.OUT);

            devicepins.append(pin);

            if devicestatus[str(i)] == 1:
                pin.value(1);
            else:
                pin.value(0);

    gc.collect();
    # End-of-Function        

"""
This function turns on/off specifc device.,
It also sets the device status in deviceconfig.devicestatus dictionary
and saves the json file.

It is not 'flash' friendly way to update each and every device state
change to devicestate.json, but it is easy to implement at the moment
compared to stroring it in 'sliding' files and keeping a track on last
status file used., (Kind of like wear leveling., )., Keeping track of
number of writes to devicestate1.json and if it exceed some pre-defined
threshold, use devicestate2.json and update config file extension to 2.,
this can go on and on for devicestate<n>.json. where n is upper bound to
flash size of the Raspberry Pi Pico.

Or some other better ways., 

Args:
    int: deviceid for the device to be turned on/off.
         this device id is converted to string so that it can be used
         as a 'key' for devicestate dictionary.
    bool: state
          state = False -> Turn off the device.,
          state = True -> Turn on the device.

Returns:
    None

Raises:
    

Example:


Notes:
     - This function calls save_device_state() and machine.Pin::value to
       turn the device on or off;
"""
def set_device_onoff(deviceid, state = False):
    global devicestatus;
    global devicepins;

    if ( deviceid >= devicestatus[numdevices] ):
        print("Invalid device id");
        error_state( "Device ID");
    else:
        devicepins[deviceid].value(int(state == True));
        devicestatus[str(deviceid)] = int((state == True));
        save_device_state(); # Save device status.
    # End-of-Function

"""
This function saves the device status in devicestate.json
configuration file.

Args:
    None

Returns:
    None

Raises:
    

Example:


Notes:
    - This function is vital to ensure state is preserved across
      power failures.
"""
def save_device_state():
    global devicestatus;
    with open (devicestatus_cfgfile, "wb") as f:
        ujson.dump(devicestatus, f);

    # End-of-Function
# End-of-File
