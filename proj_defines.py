"""
------------------------------------------------------------------------------
Relay Control Board - A menu based relay control board that can replaces
                      large number of switches with 16x2 LCD and a rotary encoder.
                      It also remembers the state of each device to ensure
                      that it starts with same satate when power is restored.
------------------------------------------------------------------------------

Author: Jatin Gandhi (https://github.com/LearningCart)
Created: 2025-03-29
Updated: 2025-03-29
Version: v1.0
License: MIT (see LICENSE file for details)

Description:
    This file contains all the constants and configuration variables. 

Supported Platforms:
    - MicroPython v1.24.1 on 2024-11-29; 
    - Board: Raspberry Pi Pico with RP2040

Usage:

-------------------------------------------------------------------------------
"""
"""
-------------------------------------------------------------------------------
 Constants and configurations
-------------------------------------------------------------------------------
"""
# Project wide contants/defines.,
# A place holder for all the constants and defines.,

# LCD display address and configurations
I2C_ADDR             = 39
I2C_DISPLAY_NUM_ROWS = 2
I2C_DISPLAY_NUM_COLS = 16

# I2C channel ID
I2C_CHANNEL_ID = 0

# I2C GPIO pins
I2C_LCD_SDA_PIN = 0
I2C_LCD_SCL_PIN = 1

#I2C bus frequency., <= 400 KHz
I2C_BUS_FREQUENCY = 400000

# GPIO pins used for rotary encoder
ROTARY_ENCODER_SWITCH_PIN = 13
ROTARY_ENCODER_DATA_PIN   = 14
ROTARY_ENCODER_CLOCK_PIN  = 15

# Roatry encoder event ID
ROTARY_UP           = 10;
ROTARY_DOWN         = ROTARY_UP + 1;
ROTARY_BTN_PRESSED  = ROTARY_UP + 2;

# Custom cursor character ID
CURSOR_CHARSET_ID = 7;

# Total number of characters used for ON/OFF special symbol
# Must be reflected in define_customcharacters()-> onchars, offchars,
# Last custom char at CURSOR_CHARSET_ID 7 is set for cursor.,
# hence, it must be less that that., 
ONOFF_INDICATOR_NUMCHAR = 2


# NOTE: Isolating device status and configuration file as configuration is
#       constant however device status keeps changing.,
#       Isolation will help in future design to minimize impact of
#       frequent write to flash., (each device GPIO state toggles cause one full write).

# Device configuration file
# device id : [<Device Name>, <GPIO Pin Number>]
# devices[deivceid][0] is name on screen
# devices[deivceid][1] is GPIO Number
# DO NOT OVERWRITE THIS FILE IN CODE., NO ujson.dump/ujson.dumps please.,
deviceinfo_cfgfile  = "devices.json";

# Last selected device status ON/OFF.,
# <<<  NOTE >>> 
# This file is constantly updated to reflect the device GPIO state.,
# This allow us to restore the On/Off after power cycle/power loss., 
# TODO: It wears out flash quicker. We need to find more optimal solution,
#       Or change this mechanism to use internal/external EEPROM in future.,
devicestatus_cfgfile = "devicestate.json";

# Total number of devices controlled by the system.,
# This is a tag and it must be present in devices.json and devicestate.json files., 
numdevices = "numdevices"

# End-of-File