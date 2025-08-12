import RPi.GPIO as GPIO
import time
import serial

# ----- GPIO Setup -----
GPIO.setmode(GPIO.BCM)

SERVO_PIN = 18  # Continuous rotation servo on GPIO 18
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz for continuous servo
pwm.start(0)

# ----- Serial Setup -----
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=2)
time.sleep(2)

# ----- Parameters -----
threshold = 50
motor_running = False

# ----- Servo Control -----
def rotate_continuously():
    pwm.ChangeDutyCycle(10)  # Rotate clockwise
    print("Motor rotating (moisture < 50%)")


def stop_motor():
    pwm.ChangeDutyCycle(7.5)  # Send neutral signal briefly to stop
    time.sleep(0.3)           # Allow motor to settle
    pwm.ChangeDutyCycle(0)    # Cut signal completely to prevent jitter
    print(" Motor stopped cleanly (no jitter)")


# ----- Main Loop -----
try:
    while True:
        if arduino.in_waiting > 0:
            raw = arduino.readline().decode('utf-8').strip()
            print(f"Raw data: {raw}")
            try:
                moisture = float(raw.split(":")[1].strip())
                print(f" Moisture: {moisture:.2f}%")

                if moisture < threshold and not motor_running:
                    rotate_continuously()
                    motor_running = True

                elif moisture >= threshold and motor_running:
                    stop_motor()
                    motor_running = False

                time.sleep(1)

            except (ValueError, IndexError):
                print(f" Invalid moisture data: '{raw}'")

except KeyboardInterrupt:
    print(" Program interrupted.")

finally:
    stop_motor()
    pwm.stop()
    GPIO.cleanup()
    arduino.close()
    print("GPIO and Serial cleaned up.")
