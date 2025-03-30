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
    This file contains rotray encoder reading functionality.
    NOTE: There is a tight logical coupling between menu navigation logic and
    value returned by getUserInput().


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
import utime
from machine import Pin

from proj_defines import *

from deviceconfig import get_total_devices;

from display import error_state;


"""
-------------------------------------------------------------------------------
 Global variables 
-------------------------------------------------------------------------------
"""
DATA_PIN   = Pin(ROTARY_ENCODER_DATA_PIN,   Pin.IN, Pin.PULL_UP);
CLOCK_PIN  = Pin(ROTARY_ENCODER_CLOCK_PIN,  Pin.IN, Pin.PULL_UP);
SWITCH_PIN = Pin(ROTARY_ENCODER_SWITCH_PIN, Pin.IN, Pin.PULL_UP);

value         = 0;
previousValue = 1;

"""
-------------------------------------------------------------------------------
 Functions 
-------------------------------------------------------------------------------
"""
"""
This function initialize rotary encoder 'total' elements.,

Args:
    
Returns:
        None

Raises:

Notes:

"""
def init(total : int):
    global TOTAL_DEVICES;
    if (total > 0):
        TOTAL_DEVICES = get_total_devices();
    else:
        TOTAL_DEVICES = 1;
        print("Error: Invalid arguments");
        error_state("Total <= 0");

"""
This function initialize rotary encoder 'total' elements.,

Args:
        None
Returns:
        [retval, value]: retval is the event (UP/DOWN/BUTTON PRESSED) event
                         value is the count mainted in the range of
                         0 to total - 1.

Raises:

Notes:
    - 'value' returned is tightly coupuled with menu navigation logic.
"""
def getUserInput():
    global value;
    global previousValue;
    global TOTAL_DEVICES;
    
    retval = None;

    if previousValue != CLOCK_PIN.value():
        if CLOCK_PIN.value() == 0:
            if DATA_PIN.value() == 0:
                value = (value - 1) % TOTAL_DEVICES;
                # Need to swap Up and Down based on rotary encoder's location/orientation in system.
                retval = ROTARY_UP;
            else:
                value = (value + 1) % TOTAL_DEVICES;
                # Need to swap Up and Down based on rotary encoder's location/orientation.
                retval = ROTARY_DOWN;

        previousValue = CLOCK_PIN.value()

         
    if SWITCH_PIN.value() == 0:       
        retval = ROTARY_BTN_PRESSED;
        utime.sleep(1)
    
    return [retval, value];

# End-of-File