# use command before import sudo apt install python3-gpiozero 
from gpiozero import Motor
def move(forward, motor):
    if forward==True:
        motor.forward()
    else:
        motor.backward()
def stop(motor):
    motor.stop()