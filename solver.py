# coding=utf-8
import urllib.request

POS_ORDER = ["U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9",
             "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
             "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
             "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
             "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9",
             "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"]

CENTERS = {'blue': 'u', 'green': 'd', 'red': 'r', 'white': 'f', 'yellow': 'b', 'orange': 'l'}


def get_solution(data):
    print(data)
    return urllib.request.urlopen("http://127.0.0.1:9001/?{}".format(data)).read()[14:-18].decode("utf-8").split()


def gen_data(facelets, centers=CENTERS):
    out = []
    for pos in POS_ORDER:
        out += centers[facelets[pos]] if pos[1] != "5" else pos[0].lower()
    return "".join(out)
