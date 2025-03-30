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
    This file contains display related functions such as
    draw cursor, draw string, draw ON/OFF state icon special characters.
    Due to tight coupling, it also implements critical error handler., 

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
# Custom characters for ON/OFF device status and cursor related APIs
import gc;
import utime;

from machine import Pin
from machine import I2C

from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

from proj_defines import *

"""
-------------------------------------------------------------------------------
 Global variables 
-------------------------------------------------------------------------------
"""
i2c = I2C(I2C_CHANNEL_ID, sda = Pin(I2C_LCD_SDA_PIN), scl = Pin(I2C_LCD_SCL_PIN), freq = I2C_BUS_FREQUENCY)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_DISPLAY_NUM_ROWS, I2C_DISPLAY_NUM_COLS)

"""
-------------------------------------------------------------------------------
 Functions 
-------------------------------------------------------------------------------
"""

"""
This function turns off the display

Args:
    
Returns:
        None

Raises:

Notes:
"""
def turn_off_display():
    lcd.hal_backlight_off();
    # End-of-Function

"""
This function turns on the display

Args:
    
Returns:
        None

Raises:

Notes:
"""
def turn_on_display():
    lcd.hal_backlight_on();
    # End-of-Function


"""
This function shows greeting message during power on after
initialization.

Args:
    
Returns:
        None

Raises:

Notes:
"""
def greeting():
    lcd.clear();
    lcd.move_to(2,0);
    lcd.putstr("Relay Control");
    lcd.move_to(5,1);
    lcd.putstr("Board");
    utime.sleep(2);
    lcd.clear();
    # End-of-Function


"""
This function shows greetings message and
calls function to loads to custom characters

Args:
    
Returns:
        None

Raises:

Notes:
"""
def init():
    greeting();
    # Load custom characters in LCD CGRAM
    define_customcharacters();
    # End-of-Function


"""
This function shows custom character for On or Off.

Args:
    int: x column
    int: y row
    bool: show_on - flag to decide if we need to show ON custom character
                    or OFF custom character.
Returns:
        None

Raises:

Notes:
"""
# Custom characters APIs: 
def show_on_off_charset(x, y, show_on = False):
    if (x >= I2C_DISPLAY_NUM_COLS or y >= I2C_DISPLAY_NUM_ROWS):
        error_state("Arguments");
        print("Invalid arguments");
        return;

    if (show_on == True):
        startindex = 0;
    else:
        startindex = 2;
    
    for a in range(2):
        lcd.move_to (a + x, y);
        lcd.putchar(chr(a + startindex));
    # End-of-Function


"""
This function defines the custom character for On or Off and cursor.
We can simply show any characters to show ON or OFF and even cursor,
but having custom characters for ON, OFF and cursor gives us ability
to customize.

Args:

Returns:
        None

Raises:

Notes:
"""
# Modifying total number of characters to represent ONOFF_INDICATOR_NUMCHAR
def define_customcharacters():
    # ON custom character set
    onchars =  [ bytearray([  0x07,  0x08,  0x13,  0x17,  0x17,  0x13,  0x08,  0x07]),
                 bytearray([  0x1C,  0x02,  0x19,  0x1D,  0x1D,  0x19,  0x02,  0x1C])
                ];
    # OFF custom character set
    offchars = [ bytearray([  0x07,  0x08,  0x10,  0x10,  0x10,  0x10,  0x08,  0x07]),
                 bytearray([  0x1C,  0x02,  0x01,  0x01,  0x01,  0x01,  0x02,  0x1C])
                ];
   
    # Cursor custom character set
    cursor = bytearray([  0x18,  0x0C,  0x06,  0x1F,  0x1F,  0x06,  0x0C,  0x18]);

    # Set all custom characters.,
    custom_char_id = 0;

    for a in onchars:
        lcd.custom_char(custom_char_id, a);
        custom_char_id = custom_char_id + 1;
        
    for b in offchars:
        lcd.custom_char(custom_char_id, b);
        custom_char_id = custom_char_id + 1;
            
    # CURSOR_CHARSET_ID must not collide with above., custome chars.,
    # Setting last custom character as a cursor., 
    lcd.custom_char(CURSOR_CHARSET_ID, cursor);
    # End-of-Function

"""
This function shows the custom cursor at given row and column

Args:
    x: int Column
    y: int Row

Returns:
        None

Raises:

Notes:
"""
def show_cursor(x, y):
    if (x >= I2C_DISPLAY_NUM_COLS or y >= I2C_DISPLAY_NUM_ROWS):
        error_state(lcd, "Arguments");
        print("Invalid arguments");
        return;
    # Show cursor at given XY, User is smart., 
    lcd.move_to(x,y);
    lcd.putchar(chr(CURSOR_CHARSET_ID));
    gc.collect();
    # End-of-Function

"""
This function hides the custom cursor at given row and column

Args:
    x: int Column
    y: int Row

Returns:
        None

Raises:

Notes:
"""
def hide_cursor(x, y):
    if (x >= I2C_DISPLAY_NUM_COLS or y >= I2C_DISPLAY_NUM_ROWS):
        error_state(lcd, "Arguments");
        print("Invalid arguments");
        return;
    # Show cursor at given XY, User is smart., 
    lcd.move_to(x,y);
    lcd.putchar(' ');
    gc.collect();
    # End-of-Function


"""
Wrapper  to clear the screen.,

Args:

Returns:
        None

Raises:

Notes:
"""
def clear():
    lcd.clear();
    # End-of-Function


"""
Move cursor to given row and column.,

Args:
    x: int column to move to.,
    y: int row to move to.,

Returns:
        None

Raises:

Notes:
"""
def moveto(x, y):
    lcd.move_to(x, y);
    # End-of-Function


"""
Show the string at given row and column.,

Args:
    x: int column to show given sring
    y: int row to show given string.,
    string: str String to be shown.,

Returns:
        None

Raises:

Notes:
"""
def show_string(x, y, string):
    if (x < I2C_DISPLAY_NUM_COLS and y < I2C_DISPLAY_NUM_ROWS and None != string):
        lcd.move_to(x, y);
        lcd.putstr(string);
    # End-of-Function


############ Error handling function ########
# To avoid circular dependencies, it is kept inside display module.

"""
This function shows error message on display.
It is used for critical error., 

Args:
    msg: string to show
Returns:
        None

Raises:

Notes:
It shows the messge and turns backlight on and off for error
"""
def error_state(msg):
    msg = msg[:I2C_DISPLAY_NUM_COLS-4]; # Restrict to display length., 
    print("Unrecoverable error occured");
    lcd.move_to(0,0)
    lcd.putstr("ERR:");
    lcd.putstr(msg);
    while True:
        lcd.hal_backlight_off();
        utime.sleep(1);
        lcd.hal_backlight_on();
        utime.sleep(1);
        gc.collect();
    # End-of-Function

# End-of-File