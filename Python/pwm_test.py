import RPi.GPIO as IO

IO.setwarnings(False)

IO.setmode(IO.BOARD)

IO.setup(7, IO.OUT)

p1 = IO.PWM(7, 100)

p1.start(0)

while 1:
    p1.ChangeDutyCycle(100)
