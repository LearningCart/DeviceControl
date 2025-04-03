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
    This file a main entry point of the system.
    It initialized the system and implements core logic for menu navigation
    and device control.

Supported Platforms:
    - MicroPython v1.24.1 on 2024-11-29; 
    - Board: Raspberry Pi Pico with RP2040

Usage:
    Upload all project files (Python code and json configuration files)
    to micro python board.
    See README.md -> "Upload files to board" section.

-------------------------------------------------------------------------------
"""
"""
-------------------------------------------------------------------------------
 Modules
-------------------------------------------------------------------------------
"""
import gc
import utime

from math import ceil

from machine import Pin

# Rotary encoder APIs
import rotary

# Custom Character APIs
import display

# Import device control
import devicectrl

# Import device json configuration module
import deviceconfig

# Project configuration is the only module where everything is taken directly.,
from proj_defines import *;

"""
-------------------------------------------------------------------------------
 Global variables 
-------------------------------------------------------------------------------
"""
# Menu Navigation., 
CurrentPage = 0;
TotalPages  = 0;

# OSI (On Screen Index)
# It indicate cursor position on the "screen"., 
# Since it is 16xN display, OSI will be in range 0 to (I2C_DISPLAY_NUM_ROWS - 1)
OnScreenIndex = 0;


"""
-------------------------------------------------------------------------------
 Functions 
-------------------------------------------------------------------------------
"""

"""
This function initialize complete system.

Args:
    
Returns:
        None

Raises:

Notes:
    - Order of initialization is important!
"""

def init_system():
    global CurrentPage;
    global TotalPages;
    # Initialize display first., (error message are routed to display).
    display.init();

    # Load device configuration, <name : gpio> pair and last status.,
    # Other sub-systems depends on this module., hence,
    # just after display, we are initializing device configuration.,
    deviceconfig.init();

    # Setup GPIO
    devicectrl.init();

    # Initialize rotary encoder
    rotary.init(deviceconfig.get_total_devices());

    # Set page details for device list navigation.,
    CurrentPage = 0;

    total_devices = deviceconfig.get_total_devices();

    if(0 == I2C_DISPLAY_NUM_ROWS):
        print("Invalid number of rows..,");
        error_state("Div by 0");

    TotalPages  = ceil(total_devices / I2C_DISPLAY_NUM_ROWS);
    # End-of-Function


"""
This function draws the requested page on display.

Args:
    
Returns:
        None

Raises:

Notes:
    - It limits the number of characters of devce name to
      total columns on screen - reserved space for ON/OFF and cursor.,
    - It doesn't handle "cursor" draw as it is not it's core task.,
"""

# Menu navigation and control logic
def draw_page(page):
    global TotalPages;
   
    devicestatus = deviceconfig.get_device_status();

    if (page < 0 or page >= TotalPages):
        print("Invliad page number {0}".format(page));
        error_state("Page No.");
    
    # If last page., total to print = Total Devices % I2C_DISPLAY_NUM_ROWS
    if ((TotalPages - 1) == page and 0 != (deviceconfig.get_total_devices() % I2C_DISPLAY_NUM_ROWS)):
        # This is the last page., and it doesn't have enough devices to fill all the rows., 
        num_devices_to_show = deviceconfig.get_total_devices() % I2C_DISPLAY_NUM_ROWS;
    else:
        # draw full page as its not the last page.,
        num_devices_to_show = I2C_DISPLAY_NUM_ROWS;
 
    device_id = page * I2C_DISPLAY_NUM_ROWS; # Device start.,
    
    # Clear screen., 
    display.clear();

    # Display device list
    for i in range(num_devices_to_show):
        DeviceName = deviceconfig.get_device_name(device_id);
        
        display.show_string(1, i, DeviceName[:I2C_DISPLAY_NUM_COLS - 1 - ONOFF_INDICATOR_NUMCHAR]);

        # Show device status icon too., (on/off)
        if devicestatus[str(device_id)] == 1:
            display.show_on_off_charset( 14, i, True);
        else:
            display.show_on_off_charset( 14, i, False);
        
        device_id = device_id + 1;

    gc.collect();
    pass;
    # End-of-Function



"""
This function handles "UP" event received from rotary encoder
It takes care of requesting appropriate page draw if "Up" event is received
on first element on screen.
Args:
    
Returns:
        None

Raises:

Notes:
    - Up event will receive deviceid as 'previous' element we need to navigate to..,

"""


def handler_up_event(deviceid):
    global OnScreenIndex;
    global CurrentPage;
    global TotalPages;

    # If user pressed up on first element on screen.,
    if(0 == OnScreenIndex):
        
        # if we are on first device and this is first page.,
        if(0 == CurrentPage):
            # Set current page to last page
            CurrentPage = TotalPages  - 1;
        else:
            # Set current page to previous page., 
            CurrentPage = CurrentPage - 1;
        
        # Draw new page
        draw_page(CurrentPage);
        
        #Set On Screen Index to last item.,
        total_devices = deviceconfig.get_total_devices();
        
        # Select last element of the current page
        # if there are not enough devices and
        # we are on the last page.
        if (0 != total_devices % I2C_DISPLAY_NUM_ROWS and (TotalPages  - 1) == CurrentPage):
            OnScreenIndex = (total_devices % I2C_DISPLAY_NUM_ROWS) - 1;
        else:
            OnScreenIndex = I2C_DISPLAY_NUM_ROWS - 1;
        
        display.show_cursor(0, OnScreenIndex);

    # else of if(0 == OnScreenIndex):
    else:
        # This is not first element on screen., so we don't need to go to previous page.,
        # Just move the cursor up., 
        display.hide_cursor(0, OnScreenIndex);
        
        OnScreenIndex = OnScreenIndex - 1;
        
        display.show_cursor(0, OnScreenIndex);
    gc.collect();
    pass;
    # End-of-Function


"""
This function handles "DOWN" event received from rotary encoder
It takes care of requesting appropriate page draw if "Down" event is received
on last element on screen.
Args:
    
Returns:
        None

Raises:

Notes:
    - Up event will receive deviceid as 'next' element we need to navigate to.,

"""

def handler_down_event(deviceid):
    global OnScreenIndex;
    global CurrentPage;
    global TotalPages;

    # If user pressed down on last page or last element., 
    if ((I2C_DISPLAY_NUM_ROWS - 1) == OnScreenIndex) or (0 == deviceid):
        
        # if we are on last device or this is last page.,
        # We were on last already and pressing down, rotary encoder sent first device.,
        if(0 == deviceid or (TotalPages -1) == CurrentPage):
            # Set current page to last page
            CurrentPage = 0;
        else:
            # Set current page to previous page., 
            CurrentPage = CurrentPage + 1;
        
        # Draw new page
        draw_page(CurrentPage);
        
        #Set On Screen Index to last item.,
        total_devices = deviceconfig.get_total_devices();
        
        # Select first element of the current page
        OnScreenIndex = 0;
        
        display.show_cursor(0, OnScreenIndex);

    # else of if(0 == OnScreenIndex):
    else:
        # Tis is not first element on screen., so we don't need to go to previous page.,
        # Just move the cursor up., 
        display.hide_cursor(0, OnScreenIndex);
        
        OnScreenIndex = OnScreenIndex + 1;
        
        display.show_cursor(0, OnScreenIndex);

    gc.collect();
    pass;
    # End-of-Function


"""
This function handles "Button Press"/"Clicked" event received from rotary encoder
It takes care of changing state of GPIO pin and showing respective ON/OFF icon
for given device.
Args:
    
Returns:
        None

Raises:

Notes:
    - Up event will receive deviceid as 'current' element that was clicked

"""



def handler_clicked_event(deviceid):
    global OnScreenIndex;
    global DeviceIndex;

    devicestatus = deviceconfig.get_device_status();

    # Toggle device status and reflect it in icon too., (on/off)
    if devicestatus[str(deviceid)] == 1:
        # It is ON., so turn it off
        devicectrl.set_device_onoff(deviceid, False);
        display.show_on_off_charset( 14, OnScreenIndex, False);
    else:
        # It is OFF., so turn it on
        devicectrl.set_device_onoff(deviceid, True);
        display.show_on_off_charset( 14, OnScreenIndex, True);
    pass;
    # End-of-Function


# Keeping this dictionary of event and handler close to main event handler.,
# Event handler table
eventhanders = {
        ROTARY_UP:          handler_up_event,
        ROTARY_DOWN:        handler_down_event,
        ROTARY_BTN_PRESSED: handler_clicked_event
    };


"""
Main entry point of system.
"""

if __name__ == "__main__": 
    init_system();

    # Draw the first page on the screen.,
    draw_page(0);
    # Show cursor
    display.show_cursor(0, OnScreenIndex);

    while True:
        [event, deviceId] = rotary.getUserInput();

        if (None == event):
            utime.sleep_ms(10); # If user entered nothing, try after 10 ms.,
            continue;

        # User event occured.
        # Just re-assuaring event is correct
        if( event not in [ROTARY_UP, ROTARY_DOWN, ROTARY_BTN_PRESSED]):
            # Something is wrong in rotary encoder driver.,
            utime.sleep_ms(10);
            continue;
        
        # Call the event handler., 
        eventhanders[event](deviceId);

        # Retry after 5 ms.,
        utime.sleep_ms(5);

# End-of-File
