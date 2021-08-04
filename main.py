import argparse
import time
import cv2
import numpy as np
import sys
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from datetime import datetime
import os
import worker as w
import math
from telebot import Bot
import algorithm
import constant as ct
from imutils.video import VideoStream
from sort import Sort
import random

'''
Note:
cmd: python main.py --camera rtmp://192.168.100.240:1935/camera/531f18a283754033820eb3b3e359d2f2 --model mobilenet_thin
'''

fps_time = 0
bot = Bot()
worker = w.Worker(bot.send,10)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Pose Estimation realtime')
	parser.add_argument('--camera', type=str, default=0)
	parser.add_argument('--resize', type=str, default='432x368',
						help='432x368 or 656x368 or 1312x736 ')
	parser.add_argument('--resize-out-ratio', type=float, default=4.0,
						help='if provided, resize heatmaps before they are post-processed. default=1.0')

	parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
	parser.add_argument('--show-process', type=bool, default=False,
						help='for debug purpose, if enabled, speed for inference is dropped.')
	parser.add_argument('--save', type=bool, default=False,
						help='save video')
	args = parser.parse_args()

	w, h = model_wh(args.resize)
	if w > 0 and h > 0:
		e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
	else:
		e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
	cam = VideoStream(args.camera).start()

	tracker = Sort()
	tracked = []

	check = 0
	flag = args.save
	if flag:
		out = cv2.VideoWriter('out.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (image.shape[1],image.shape[0]))
	notify = False
	n = 1
	while True:
		pose_list = []
		image = cam.read()
		poses = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
		image = TfPoseEstimator.draw_humans(image, poses, imgcopy=False)
		ct.height,ct.width = image.shape[0],image.shape[1]

		if len(poses) > 0:
			for pose in poses:
				# cổ
				x1, y1 = algorithm.find_point([pose], 1)
				# cổ tay trái
				x2, y2 = algorithm.find_point([pose], 7)
				# cổ tay phải
				x3, y3 = algorithm.find_point([pose], 4)
				# hông
				x4, y4 = algorithm.find_point([pose], 8)
				d = algorithm.distance(x2, y2, x3, y3)

				lx, ly = [], []
				for i in range(0,17):
					x, y = algorithm.find_point([pose], i)
					if x > 0 and y > 0:
						lx.append(x)
						ly.append(y)

				xmax = max(lx)
				xmin = min(lx)
				ymax = max(ly)
				ymin = min(ly)

				if (y2 < y1 and y3 < y1) and (x3 < x2) and (150 < d < 600):
					dets = [xmin,ymin,xmax,ymax]
					pose_list.append(dets)
					trackers = tracker.update(np.array(pose_list))
					for d in trackers:
						d = d.astype(np.int32)
						id = int(d[4])
						if id in tracked:
							if n % 50 == 0:
								notify = True
							n += 1
							cv2.rectangle(image,(xmin - 50, ymin - 50), (xmax + 50, ymax + 50),(0,0,255),3)
							cv2.putText(image, 'ID : %s' % id,
								(d[0] + 200, d[1] - 100),
								cv2.FONT_HERSHEY_SIMPLEX, 1,
								(255, 0, 0), 2)
							cv2.putText(image,
								"HELP ME",
								(d[0] - 100, d[1] - 100),
								cv2.FONT_HERSHEY_SIMPLEX, 1,
								(0, 0, 255), 2)
						else: tracked.append(id)
		if notify:
			c = check
			counter = len(tracked)
			check = counter
			if counter > c:
				msg = "Cảnh báo kêu cứu!!!!" "\nSố người: " + str(counter) + "\nThời gian phát tín hiệu: " + str(datetime.now())
				l = [msg, image]
				worker.add_job(l)
				notify = False
		cv2.putText(image,
					"FPS: %f" % (1.0 / (time.time() - fps_time)),
					(10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
					(0, 255, 0), 2)
		
		# cv2.imshow('tf-pose-estimation result', cv2.resize(image,(1920,1080)))
		cv2.imshow('tf-pose-estimation result', cv2.resize(image,(1000,800)))
		fps_time = time.time()
		if cv2.waitKey(1) == 27:
			break
		if flag:
			out.write(image)
	if flag:
		out.release()
	cam.stop()
	cv2.destroyAllWindows()
worker.wait_and_stop()