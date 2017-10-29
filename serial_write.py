# coding=utf-8

import serial
import time

ser = serial.Serial('COM3', 19200)

time.sleep(2)


def executeProgram(program):
    # input("Please confirm sequence start \n")
    # print(program)
    for move in program:
        ser.write(bytes(move, "utf-8"))
