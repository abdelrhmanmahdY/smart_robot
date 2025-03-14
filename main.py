from config import *
from motor import *
from time import sleep
motor1=Motor(forward=motor1_en4, backward=motor1_en3)
while True:
    move( True, motor1)
    sleep(5)
    move(motor=motor1, forward= True)
    sleep(5)
    stop(motor=motor1)
    