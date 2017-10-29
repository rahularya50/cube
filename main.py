# coding=utf-8

import scan
import serial_write
import solver

x = scan.scan()

# for i in solver.POS_ORDER:
#    if i not in x and i[1] != "5":
#        x[i] = input("Please enter value of {}:".format(i))

solution = solver.get_solution(solver.gen_data(x))

# print("Solution {}".format(solution))
# input("Proceed?")

serial_write.executeProgram(solution)
