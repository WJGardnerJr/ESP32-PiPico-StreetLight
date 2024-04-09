# ESP32-PiPico-StreetLight

This project marks the development of an embedded platform for the ESP32S3 CAM and Pi Pico, whereby
both devices function together to control and operate a "Smart Street Light." This is, of course, meant to be implemented on a breadboard, and is more of an educational exercise than an actualized implementation--but it is scalable.

The ESP32S3 CAM used here is a Freenove variant; info is available at https://github.com/Freenove/Freenove_ESP32_S3_WROOM_Board/tree/main. This is essentially an ESP32 CAM with all goodies incorporated, and it possesses a built-in SD card reader, camera header, and all normal GPIO broken-out. Problematically, not all GPIO is always accessible. It runs C++.

The Raspberry Pi Pico is a well-known microcontroller; it is used here to drive this project, running all sensors and sending the main UART commands to the ESP32S3 CAM. It runs MicroPython.

Why the difference in programming languages? Ease of use.

---

## Operational Guide

The basic operational principle is as follows: the Pi Pico uses the HC-SR04 sensors to determine the direction and speed of an object. This is reported in mph, and displayed on an attached ssd1306 OLED display. Six LEDs are connected to the Pi Pico, each a trio of red, yellow, and green, representative of danger, warning, and all-clear lights at the "next city block."

The Pi Pico records the speed of an object passing between the sensors, which are a fixed 17.5 cm apart. If the speed exceeds a threshold (in this case, the threshold is very low for demonstrative purposes only), a UART command is sent via RS-232 to the ESP32S3 CAM. The ESP32S3 CAM and Pi Pico have their UARTs wired in a null-modem configuration.

A key-word, "trigger\n" is read, and prompts the ESP32S3 CAM to take a photo. The ESP32S3 CAM then uploads said photo to a Firebase storage location, which can be viewed via an app.

## Design and Implementation Photo
![IMG_5636](https://github.com/WJGardnerJr/ESP32-PiPico-StreetLight/assets/135628958/060c208b-dd18-4a6a-9e73-0c01aaead33f)

## BOM
| Part  | Quantity  |
| :--- | :---: |
| Freenove ESP32S3 CAM  | `1` |
| Raspberry Pi Pico  | `1` |
| Solderless Breadboards (or protoboards)  | `3.5`[^1] |
| 330 Ω / 470 Ω Resistors| `6` |
| TTL Logic Level Converter  | `1` [^2]|
| LEDs (Any color will do, but it's really your choice.)  | `8`[^3] |
| Various Cables/DuPont Wires| As needed |

[^1]: Use a small protobard/breadboard for the ESP32. Unfortunately, the Freenove variant is NOT a normal width; some pins are inaccessible by design.

[^2]: Needed if you're using the Pico to drive the HC-SR04s, as those use 5V signaling and the Pico can only accept 3.3V signals.

[^3]: Two LEDs are used for operation success/failure on the ESP32. This allows for headless operation and determination if the photos have uploaded as intended.
