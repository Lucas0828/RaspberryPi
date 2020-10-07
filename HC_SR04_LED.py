import RPi.GPIO as GPIO
import time
import sys
import signal


TRIG = 24 
ECHO = 23 
RED = 20
BLUE = 21
buzzer = 26


MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1)

def signal_handler(signal, frame):
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def distanceInCm(duration):
    return (duration/2)/29.1

def main():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(TRIG, GPIO.OUT) 
    GPIO.setup(ECHO, GPIO.IN) 
    GPIO.setup(RED,GPIO.OUT)
    GPIO.setup(BLUE,GPIO.OUT)

    GPIO.output(TRIG, False)
    time.sleep(1)
    

    while True:
        fail = False
        time.sleep(0.1)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        timeout = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                fail = True
                break    
        if fail:
            continue
        
        timeout = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
                fail = True
                break
      
        if fail:
            continue

        pulse_duration = (pulse_end - pulse_start) * 1000000

        distance = distanceInCm(pulse_duration)
        distance = round(distance, 2)
        
        if distance <=10:
            GPIO.output(RED, GPIO.HIGH)
            if distance <=5:
                GPIO.output(buzzer, GPIO.HIGH)
            else:
                GPIO.output(buzzer, GPIO.LOW)
        else :
            GPIO.output(RED, GPIO.LOW)

        if distance > 10:
            GPIO.output(BLUE, GPIO.HIGH)
        else:
            GPIO.output(BLUE, GPIO.LOW)

    GPIO.cleanup()



if __name__ == '__main__':
    main()