import cv2
import math
import main
import constant as ct

def find_point(pose, p):
	for point in pose:
		try:
			body_part = point.body_parts[p]
			return (int(body_part.x * ct.width + 0.5), int(body_part.y * ct.height + 0.5))
		except:
			return (0,0)
	return (0,0)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def human_counter(humans, image):
	no_people = len(humans)
	# print("Total no. of People : ", no_people)
	cv2.putText(image,
			"People: %d" % (no_people),
			(10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 1,
			(255, 255, 0), 2)
	return no_people