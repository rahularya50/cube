# coding=utf-8
import functools
import time

import cv2

from params import COORDS, COLORS


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
		frames[0] = process(vc2.read()[1])  # BDL (lower proximal)
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
	if event == cv2.EVENT_LBUTTONDOWN:
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
