import time
import serial
import RPi.GPIO as GPIO

# GPIO setup
pump_pin = 18  # use the GPIO pin you connected the relay to
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.output(pump_pin, GPIO.LOW)  # make sure pump is OFF initially

# Moisture threshold
threshold = 50
pump_on = False

# Serial setup (adjust port as needed)
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=2)
time.sleep(2)  # allow time for Arduino to reset

try:
    while True:
        if arduino.in_waiting > 0:
            raw = arduino.readline().decode('utf-8').strip()
            try:
                moisture = float(raw)
                print(f"Moisture: {moisture:.2f}%")

                if moisture < threshold and not pump_on:
                    print("Pump ON")
                    GPIO.output(pump_pin, GPIO.HIGH)
                    pump_on = True
                    time.sleep(5)  # run motor for 5 seconds
                    print("Pump OFF")
                    GPIO.output(pump_pin, GPIO.LOW)
                    pump_on = False

                time.sleep(2)

            except ValueError:
                print(f"Invalid data from Arduino: {raw}")

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    GPIO.output(pump_pin, GPIO.LOW)
    GPIO.cleanup()
    arduino.close()
    print("GPIO and serial connection cleaned up.")
