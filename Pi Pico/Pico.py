from machine import UART, Pin, I2C
import utime
import ssd1306

# Initialize UART for ESP32 Cam
uart0 = UART(0, baudrate=115200)
uart0.init(baudrate=115200, tx=Pin(0), rx=Pin(1))

# Initialize HC-SR04 sensors
trigger1 = Pin(3, Pin.OUT)
echo1 = Pin(2, Pin.IN)
trigger2 = Pin(10, Pin.OUT)
echo2 = Pin(11, Pin.IN)

#LEDs
greenL = Pin(20, Pin.OUT)
yellowL = Pin(19, Pin.OUT)
redL = Pin(18, Pin.OUT)
greenR = Pin(16, Pin.OUT)
yellowR = Pin(22, Pin.OUT)
redR = Pin(21, Pin.OUT)

# Initialize I2C for SSD1306 OLED display
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

sensor_distance = 17.5  # in centimeters

def get_distance(trigger, echo):
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    time_passed = signalon - signaloff
    distance = (time_passed * 0.0343) / 2  # in centimeters
    return distance

def display_speed_direction(speed_m_s, direction):
    greenL.low()
    yellowL.low()
    redL.low()
    greenR.low()
    yellowR.low()
    redR.low()
    speed_mph = speed_m_s * 2.237
    if speed_mph < 1:
        if direction is "L->R":
            greenL.high()
        else:
            greenR.high()
    elif 2 <= speed_mph <= 2.5:
        if direction is "L->R":
            yellowL.high()
        else:
            yellowR.high()
    else:
        if direction is "L->R":
            redL.high()
        else:
            redR.high()
        uart0.write("trigger\n")
        print("Sending command to ESP32!\n")
    display.fill(0)  # Clear the display
    display.text('Speed: {:.2f} mph'.format(speed_mph), 0, 0)
    display.text(f"Direction: {direction}", 0, 10)
    display.show()

def main():
    try:
        while True:
            detectionL = detectionR = False
            start_timeL = start_timeR = 0
            print("Waiting for object detection...")
            
            while not (detectionL and detectionR):
                if not detectionL and get_distance(trigger1, echo1) <= 10:
                    start_timeL = utime.ticks_ms()
                    print("Object detected at sensor 1")
                    detectionL = True

                if not detectionR and get_distance(trigger2, echo2) <= 10:
                    start_timeR = utime.ticks_ms()
                    print("Object detected at sensor 2")
                    detectionR = True

            # Calculate the direction and speed of movement
            if detectionL and detectionR:
                time_difference = abs(start_timeR - start_timeL) / 1000  # Ensure no negative time
                if time_difference > 0:
                    speed_cm_s = sensor_distance / time_difference
                    speed_m_s = speed_cm_s / 100  # Convert cm/s to m/s
                    direction = "L->R" if start_timeL < start_timeR else "R->L"
                    print(f"Object moving {direction}")
                    display_speed_direction(speed_m_s, direction)
                else:
                    print("No movement detected or too fast to calculate")
            else:
                print("Object detected only at one sensor")

    except Exception as e:
        print("Error:", e)
        
if __name__ == "__main__":
    utime.sleep(1.5)
    main()

