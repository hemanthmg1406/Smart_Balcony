import RPi.GPIO as GPIO
import time

# Define the GPIO pin connected to the servo's signal wire
# IMPORTANT: Change this to the actual GPIO pin number you used (e.g., 18, 12, 13)
# This refers to the BCM pin numbering.
SERVO_PIN = 18

# Set up GPIO mode
GPIO.setmode(GPIO.BCM) # Use Broadcom SOC channel numbers (GPIO numbers)

# Set the GPIO pin as an output
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM (Pulse Width Modulation) on the servo pin
# A common PWM frequency for servos is 50 Hz
pwm = GPIO.PWM(SERVO_PIN, 50)

# Start PWM with a duty cycle of 0 (servo motor off/no movement)
pwm.start(0)

# Function to set servo angle
def set_angle(angle):
    # Calculate duty cycle: (angle / 18) + 2
    # This formula roughly maps 0-180 degrees to 2-12% duty cycle for many servos.
    # You might need to fine-tune these values (e.g., 2 to 12 or 0.5ms to 2.5ms pulse width)
    # depending on your specific servo.
    duty_cycle = (angle / 18) + 2
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5) # Give the servo time to move

try:
    print("Moving servo to 0 degrees...")
    set_angle(0)
    time.sleep(1) # Wait for a second

    print("Moving servo to 90 degrees...")
    set_angle(90)
    time.sleep(1)

    print("Moving servo to 180 degrees...")
    set_angle(180)
    time.sleep(1)

    print("Returning servo to 90 degrees...")
    set_angle(90)
    time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    # Stop PWM and clean up GPIO pins
    pwm.stop()
    GPIO.cleanup() # This resets all GPIO pins to their default state
    print("GPIO cleaned up.")
