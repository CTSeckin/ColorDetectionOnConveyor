import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 20
ECHO = 16
s2 = 27
s3 = 22
signal = 25
NUM_CYCLES = 10
Motor1A = 18 #motorileripini
Motor1E = 21 #enable pin
coil_A_1_pin = 4 # pink
coil_A_2_pin = 17 # orange
coil_B_1_pin = 23 # blue
coil_B_2_pin = 24 # yellow
 
# adjust if different
StepCount = 8
Seq = range(0, StepCount) #28BYJ-38 icin degerler
global pulse_end, pulse_start, distance

Seq[0] = [1,0,0,0] 
Seq[1] = [1,1,0,0]
Seq[2] = [0,1,0,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,0,1,0]
Seq[5] = [0,0,1,1]
Seq[6] = [0,0,0,1]
Seq[7] = [1,0,0,1]
 

 
 
def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  GPIO.setup(coil_A_1_pin, GPIO.OUT)
  GPIO.setup(coil_A_2_pin, GPIO.OUT)
  GPIO.setup(coil_B_1_pin, GPIO.OUT)
  GPIO.setup(coil_B_2_pin, GPIO.OUT)
  GPIO.setup(Motor1A,GPIO.OUT)
  GPIO.setup(Motor1E,GPIO.OUT)
  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)
  print("\n")
  

def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
 
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


def loop():
  temp = 1
  while(1):  
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(0.1)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   
   
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.1)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    

    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.1)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    GPIO.output(TRIG,GPIO.LOW)
    time.sleep(0.00001)
    GPIO.output(TRIG,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG,GPIO.LOW)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance,2)
    
    if distance < 8:
        GPIO.output(Motor1E,GPIO.LOW)
        x=0
        if x==0:
          if red>14000 and blue<17000 and green<17000:
            print("yesil")
            temp=1
            delay = 1
            steps = 170
            forward(int(delay) / 1000.0, int(steps))
            time.sleep(1)
            steps = 170
            GPIO.output(Motor1E,GPIO.HIGH)
            time.sleep(3)
            backwards(int(delay) / 1000.0, int(steps))
          
          elif red>12000 and blue>12000 and green<17000:
            print("mavi")
            temp=1
            delay = 1
            steps = 340
            forward(int(delay) / 1000.0, int(steps))
            time.sleep(1)
            GPIO.output(Motor1E,GPIO.HIGH)
            time.sleep(3)
            steps = 340
            backwards(int(delay) / 1000.0, int(steps))
          elif red>22000 and blue<25000 and green<24000:
            print("kirmizi")
            temp=1
            delay = 1
            steps = 512
            forward(int(delay) / 1000.0, int(steps))
            time.sleep(1)
            GPIO.output(Motor1E,GPIO.HIGH)
            time.sleep(3)
          elif red<12000 and blue<12000 and green<12000 and temp==1:
            print("lutfen kutu koyunuz")
            temp=0


def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    delay=0
    steps=0
    setup()
    setStep(coil_A_1_pin,coil_A_2_pin,coil_B_1_pin,coil_B_2_pin)
    forward(delay, steps)
    backwards(delay, steps)
    try:
        loop()

    except KeyboardInterrupt:
        endprogram()
