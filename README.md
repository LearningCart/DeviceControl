# Raspberry Pi Pico Device Control

This project is based on the Raspberry Pi Pico using MicroPython, with an LCD display, rotary encoder, 
It includes fixed and configurable GPIO assignments, external hardware, and software library details.

---
## GPIO Allocation
## 📌 Fixed GPIO Pin Allocation

| GPIO | Function                 |
|------|--------------------------|
| 0    | SDA for LCD display      |
| 1    | SCL for LCD display      |
| 13   | Rotary encoder switch    |
| 14   | Rotary encoder data      |
| 15   | Rotary encoder clock     |

---

## 🔧 Configurable GPIO Pins

| GPIO | Function         |
|------|------------------|
| 28   | First Device     |
| 27   | Second Device    |
| 26   | Third Device     |
| 22   | Fourth Device    |
| 21   | Fifth Device     |
| 20   | Sixth Device     |

---

## 🧾 Bill of Materials

1. Raspberry Pi Pico flashed with MicroPython  
2. 16x2 LCD with PCF8574 I2C LCD backpack  
3. Rotary encoder  
4. Breadboard  
5. Jumper wires  
6. Number of LEDs and current-limiting resistors  
   - *Alternatively*, opto-coupler isolated relays can be used  

---

## 📚 External Software Libraries

This project uses the I2C LCD control library:

🔗 [RPI-PICO-I2C-LCD by T-622](https://github.com/T-622/RPI-PICO-I2C-LCD)  
- Import the following files:
  - `lcd_api.py`
  - `pico_i2c_lcd.py`

---
## ▶️ Usage

1. **Connect components** as per the pin allocation
2. **Flash your Raspberry Pi Pico** with the latest version of MicroPython.
3. **Upload the necessary files**:
   - `main.py`, devices.json, devicestatus.json, etc., 
   - `lcd_api.py`
   - `pico_i2c_lcd.py`
4. **Power up the Pico** and the display will show device control options.
5. Use the **rotary encoder** to scroll and select which device to control.

### Follow how_to_upload.md to upload all the project files to the board

Feel free to fork, modify, or expand this project to fit your use case!
