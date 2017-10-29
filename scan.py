# coding=utf-8
import functools

import cv2

import time

COORDS = {'U3': [(3, 385, 234)], 'R8': [[3, 200, 418], (4, 459, 287)], 'L3': [(2, 246, 289)], 'L8': [(1, 526, 270), [2, 505, 227]], 'U2': [(2, 186, 109), (3, 497, 154)], 'F4': [(2, 358, 256), (4, 172, 285)], 'F2': [[2, 461, 148], (4, 241, 141)], 'B4': [(1, 207, 281), [3, 362, 366]], 'R7': [(4, 379, 261)], 'U7': [(2, 292, 210)], 'F3': [(2, 540, 35), (4, 294, 91)], 'R3': [(3, 354, 317)], 'R6': [[3, 253, 357], (4, 535, 270)], 'L2': [(1, 511, 89), [2, 446, 172]], 'R2': [[3, 174, 206], (4, 445, 139)], 'D6': [(4, 421, 397), (1, 341, 453)], 'U1': [(2, 125, 138), (3, 561, 111)], 'L7': [(1, 456, 236)], 'B2': [(1, 295, 114), [3, 448, 205]], 'D9': [(4, 515, 405), (1, 255, 437)], 'F9': [(4, 301, 266)], 'L1': [(1, 441, 59), (2, 323, 239)], 'F8': [[2, 423, 365], (4, 215, 318)], 'F1': [(2, 354, 293)], 'L6': [(1, 615, 231), (2, 363, 300)], 'R1': [[3, 98, 171], (4, 379, 90)], 'B9': [(1, 339, 247)], 'U9': [(2, 456, 122), (3, 244, 124)], 'L4': [(1, 434, 130), [2, 520, 149]], 'L9': [(1, 622, 323), [2, 411, 366]], 'F6': [[2, 514, 197], (4, 289, 175)], 'R9': [[3, 277, 460], (4, 538, 332)], 'U4': [(2, 206, 167), (3, 482, 78)], 'U6': [(2, 366, 103), (3, 291, 184)], 'U8': [(2, 383, 164), (3, 304, 99)], 'R4': [[3, 110, 254], (4, 382, 168)], 'D8': [(4, 441, 442), (1, 328, 383)], 'D7': [(1, 409, 326)], 'D4': [(4, 280, 448), (1, 487, 376)], 'D2': [(4, 276, 385), (1, 517, 443)], 'B7': [(1, 209, 356), [3, 380, 462]], 'B6': [(1, 353, 141), [3, 526, 251]], 'D1': [(4, 210, 418), (1, 573, 406)], 'D3': [(4, 346, 345)], 'B3': [(1, 362, 68), [3, 533, 171]], 'B1': [(3, 460, 309)], 'F7': [(2, 373, 417), (4, 155, 371)], 'B8': [(1, 263, 321), [3, 451, 407]]}


COLORS = {"white": [255, 255, 255], "red": [0, 0, 255], "green": [0, 255, 0], "blue": [255, 0, 0],
          "orange": [0, 140, 255], "yellow": [0, 255, 255]}

SEQ = ["U", "R", "F", "D", "L", "B"]

SIDEMATCH = {"red": "F", "green": "L", "blue": "R", "white": "U", "yellow": "D", "orange": "B"}


def scan():
	frames = [None] * 4

	cv2.namedWindow("preview")
	cv2.namedWindow("preview2")
	cv2.namedWindow("preview3")
	cv2.namedWindow("preview4")

	vc = cv2.VideoCapture(0)
	vc2 = cv2.VideoCapture(1)
	vc3 = cv2.VideoCapture(2)
	vc4 = cv2.VideoCapture(3)

	print("Connection established")

	time.sleep(2)

	print("starting!")
	print(cv2.getBuildInformation())

	cv2.setMouseCallback("preview", functools.partial(clickHandler, index=0, f=frames))
	cv2.setMouseCallback("preview2", functools.partial(clickHandler, index=1, f=frames))
	cv2.setMouseCallback("preview3", functools.partial(clickHandler, index=2, f=frames))
	cv2.setMouseCallback("preview4", functools.partial(clickHandler, index=3, f=frames))

	while True:
		frames[0] = process(vc2.read()[1])   # BDL (lower proximal)
		frames[1] = process(vc4.read()[1])  # LUF (upper proximal)
		frames[2] = process(vc.read()[1])  # BRU (upper distal)
		frames[3] = process(vc3.read()[1])  # FRD (lower distal)

		out = {}

		for i, points in COORDS.items():
			color_list = []

			unreliable = all(point[0] in (2, 3) for point in points)

			for point in points:
				if not point[0] in (2, 3) or unreliable:
					color_list.append(
						get_color(cv2.cvtColor(frames[point[0] - 1], cv2.COLOR_BGR2HSV)[point[2], point[1]]))
			color = resolver(i, color_list)

			for point in points:
				out[i] = color
				if get_color(cv2.cvtColor(frames[point[0] - 1], cv2.COLOR_BGR2HSV)[point[2], point[1]]) == color:
					num = -1
				else:
					num = -1
				if not point[0] in (2, 3) or unreliable:
					cv2.circle(frames[point[0] - 1], (point[1], point[2]), 5, COLORS[color], num)

		cv2.imshow("preview", frames[0])
		cv2.imshow("preview2", frames[1])
		cv2.imshow("preview3", frames[2])
		cv2.imshow("preview4", frames[3])

		key = cv2.waitKey(20)

		if key == 13:  # exit on ENTER
			print(COORDS)
			cv2.waitKey(0)
			cv2.destroyWindow("preview")
			cv2.destroyWindow("preview2")
			cv2.destroyWindow("preview3")
			cv2.destroyWindow("preview4")
			return out


def clickHandler(event, x, y, flags, param, index, f):
	frame = f[index]
	if event == cv2.EVENT_LBUTTONDOWN:
		# print("\nNext")
		# print(x, y)
		# print(frame[y, x])
		# print(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[y, x])
		# cv2.circle(frame, (y, x), 5, [255, 0, 0], -1)
		# print(get_color(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[y, x]))
		# print("[{}, {}, {}], ".format(index + 1, x, y))
		min_dist = float("inf")
		best_coord = None
		best_index = None

		for coord, points in COORDS.items():
			unreliable = all(point[0] in (2, 3) for point in points)
			for i, point in enumerate(points):
				if point[0] != index + 1:
					continue
				if point[0] in (2, 3) and not unreliable:
					continue
				if (point[1] - x) ** 2 + (point[2] - y) ** 2 < min_dist:
					min_dist = (point[1] - x) ** 2 + (point[2] - y) ** 2
					best_coord = coord
					best_index = i

		COORDS[best_coord][best_index] = (index + 1, x, y)
		print(best_coord)


def process(img):
	return img


def get_color(hsv):
	hue = hsv[0]
	sat = hsv[1]
	val = hsv[2]

	if sat < 60:
		return "white"
	if hue < 17.5 or hue > 140:
		if val < 190:
			return "red"
		else:
			return "orange"
	if hue < 50:
		return "yellow"
	if hue < 90:
		return "green"
	if hue < 140:
		return "blue"
	return "white"


def resolver(pos, colors):
	if len(set(colors)) == 1:
		return colors[0]

	if len({"white", "orange"} & set(colors)) == 1:
		if pos[0] in {"U", "L", "B", "R"}:
			return (set(colors) - {"white", "orange"}).pop()
		else:
			return ({"white", "orange"} & set(colors)).pop()

	if set(colors) == {"white", "orange"}:
		return "orange"

	return colors[0]
