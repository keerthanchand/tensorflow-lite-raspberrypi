import time
import RPi.GPIO as GPIO
from time import sleep
import subprocess
import smbus
from datetime import datetime
dis = [0,0,0]


GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)
GPIO.setup(04, GPIO.OUT)
pwm=GPIO.PWM(04, 50)


def get_distance():
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 25  
    GPIO_ECHO    = 8   
    x=17               
    y=18               
    z=0
    a=[]
    sv = 5            

    GPIO.setup(x,GPIO.OUT)
    GPIO.setup(y,GPIO.OUT)
    GPIO.output(x,0)
    GPIO.output(y,0)

    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  
    GPIO.setup(GPIO_ECHO,GPIO.IN)      
    val2 = []
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)

    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
    elapsed = stop-start
    distance =int( elapsed * 34300 / 2)
    a.append(distance)

    if distance>=200:
        GPIO.output(x,1)
        GPIO.output(y,0)

    if distance<=100:
        GPIO.output(y,1)
        GPIO.output(x,0)
    z=z+1
    if z>19:
        z=0

    return distance
while (True):

    pwm.start(0)
    sleep(0.7)

    pwm.ChangeDutyCycle(1)
    sleep(0.7)
    dis[2] =  get_distance()

    pwm.ChangeDutyCycle(6)
    sleep(0.7)
    dis[1]= get_distance()

    pwm.ChangeDutyCycle(11)
    sleep(0.7)
    dis[0] = get_distance()

    

    print (dis)
    text = ["left", "forward", "right"]
    x = dis.index(max(dis))
    speak = "go "+text[x]
    exitCode = subprocess.call(["espeak","-ven+f3","-a200",speak])
    sleep(4)


pwm.stop()
GPIO.cleanup()

