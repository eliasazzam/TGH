# TGH
import time
import RPi.GPIO as GPIO
import picamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

Motor1A= 16
Motor1B= 18
Motor1E= 22
#motor 1
Motor2A= 36
Motor2B= 38
Motor2E= 40
#motor 2
adcmosi = 19
adcmiso = 21            
adcclk = 23
adccs = 26
#humidity
echo = 13
trig = 11
#ultrasonic sensor
motorq =7
motorb =8
motorc =10
#motor 3
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
#motor 1
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
#motor 2
GPIO.setup(adcmosi, GPIO.OUT)
GPIO.setup(adcmiso, GPIO.IN)
GPIO.setup(adcclk, GPIO.OUT)
GPIO.setup(adccs, GPIO.OUT)
#humidity
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
#ultrasonic sensor
GPIO.setup(motorq,GPIO.OUT)
GPIO.setup(motorb,GPIO.OUT)
GPIO.setup(motorc,GPIO.OUT)
#motor 3
def UltrasonicReading():
    GPIO.output(trig, False)
    time.sleep(0.2)
    GPIO.output(trig, True)
    time.sleep(0.01)
    GPIO.output(trig, False)
    while GPIO.input(echo)==0:
        signalOff=time.time()
    while GPIO.input(echo)==1:
        signalOn=time.time()
        
    timePassed=signalOn-signalOff
    distance=timePassed*17150

    print distance,"cm"
def read (chan):
    if ((chan > 7 ) or (chan < 0 )):
        return -1
    GPIO.output(adccs, True)
    GPIO.output(adcclk, False)
    GPIO.output(adccs, False)

    cout = chan
    cout |= 0x18
    cout <<= 3
    for i in range (5):
        if (cout & 0x80):
            GPIO.output(adcmosi,True)
        else:
            GPIO.output(adcmosi, False)
        cout <<= 1
        GPIO.output(adcclk, True)
        GPIO.output(adcclk, False)
    out = 0
    for i in range (12):
        GPIO.output(adcclk, True)
        GPIO.output(adcclk, False)
        out <<= 1
        if (GPIO.input(adcmiso)):
            out |= 0x1
    GPIO.output(adccs, True)
    out >>= 1
    return out

try:
    camera = picamera.PiCamera()
    time.sleep(0.5)
    start= time.time()
    isStartup = True
    frame = 1
    while True:
        distance = UltrasonicReading()
        if distance < 15:
            camera.capture('Guard'+str(frame)+'.jpg')
            frame = (frame +1)%5
            
                
        if time.time()-start > 20 or isStartup == True:
            start = time.time()
            isStartup = False
            checkMoisture = True
            
        if checkMoisture == True:
            checkMoisture = False
            val =read(0)
            print 'moisture : ',val
            if val>=400:
                print "Going forwards "
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                GPIO.output(Motor1E,GPIO.HIGH)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                GPIO.output(Motor2E,GPIO.HIGH)
                time.sleep(20)
                GPIO.output(Motor1E,GPIO.LOW)
                GPIO.output(Motor2E,GPIO.LOW)
                
            if val<400:
                print "Going backwards"
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                GPIO.output(Motor1E,GPIO.HIGH)

                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                GPIO.output(Motor2E,GPIO.HIGH)
                time.sleep(3)
                GPIO.output(Motor1E,GPIO.LOW)
                GPIO.output(Motor2E,GPIO.LOW)
                
            if val <150:
                print "Water"
                GPIO.output(motorq,GPIO.LOW)
                GPIO.output(motorb,GPIO.HIGH)
                GPIO.output(motorc,GPIO.HIGH)
                time.sleep(4)
                GPIO.output(motorc,GPIO.LOW)

except KeyboardInterrupt:
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    
