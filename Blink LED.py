# coding: utf-8
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
GPIO_TRIGECHO = 12
GPIO_LED = 17

# Initialize GPIO
GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)  # Trigger/echo pin as output
GPIO.setup(GPIO_LED, GPIO.OUT)       # LED pin as output

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGECHO, False)

def measure():
    # This function measures a distance
    # Pulse the trigger/echo line to initiate a measurement
    GPIO.output(GPIO_TRIGECHO, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGECHO, False)
    # Ensure start time is set in case of very quick return
    start = time.time() 
    # Set line to input to check for start of echo response
    GPIO.setup(GPIO_TRIGECHO, GPIO.IN)
    while GPIO.input(GPIO_TRIGECHO) == 0:
        start = time.time()
    # Wait for end of echo response
    while GPIO.input(GPIO_TRIGECHO) == 1:
        stop = time.time()
    GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
    GPIO.output(GPIO_TRIGECHO, False)
    elapsed = stop - start
    distance = (elapsed * 34300) / 2.0
    time.sleep(0.1)
    return distance

try:
    while True:
        distance = measure()
        print("Distance: %.1f cm" % distance)
        
        # LED control based on distance
        if distance < 18:
            for i in range(0,5):
                GPIO.output(GPIO_LED, GPIO.HIGH)
                time.sleep(0.2) #wait 0.2 second before next measurement 
                GPIO.output(GPIO_LED, GPIO.LOW)
                time.sleep(0.2)
        elif 18 <= distance < 25:
            GPIO.output(GPIO_LED, GPIO.LOW)
            time.sleep(1)
            GPIO.output(GPIO_LED, GPIO.HIGH)
            time.sleep(1)
        elif 25 <= distance <= 30:
            GPIO.output(GPIO_LED, GPIO.LOW)
            time.sleep(2)
            GPIO.output(GPIO_LED, GPIO.HIGH)
            time.sleep(2)
        else:
            GPIO.output(GPIO_LED, GPIO.LOW)
            time.sleep(1) #wait 1 second before next measurement 

except KeyboardInterrupt:
    print("Stop")
    GPIO.cleanup()
