#!/usr/bin/env python

import cv2
import rospy
import argparse
import imutils
import time
import sys
import numpy as np
from collections import deque
from imutils.video import VideoStream
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import socket
import math
from script_TTT import move_bot

square_num = {0:"square1", 1:"square2", 2:"square3", 3:"square4", 4:"square5", 5:"square6", 6:"square7", 7:"square8", 8:"square9"}
robot_position = {
"square1":{
    "base": 0.46,
    "shoulder": -101.61,
    "elbow": -134.98,
    "wrist1": -30.88,
    "wrist2": 92.47,
    "wrist3": 187.86
},
"square2":{
    "base": 17.98,
    "shoulder": -100.34,
    "elbow": -136.54,
    "wrist1": -32.72,
    "wrist2": 89.27,
    "wrist3": 198.16
},
"square3":{
    "base": 31.67,
    "shoulder": -102.46,
    "elbow": -132.36,
    "wrist1": -31.70,
    "wrist2": 91.26,
    "wrist3": 216.00
},
"square4":{
    "base": 1.04,
    "shoulder": -111.87,
    "elbow": -119.31,
    "wrist1": -35.85,
    "wrist2": 88.11,
    "wrist3": 183.71
},
"square5":{
    "base": 13.53,
    "shoulder": -111.35,
    "elbow": -120.23,
    "wrist1": -34.05,
    "wrist2": 88.09,
    "wrist3": 195.78
},
"square6":{
    "base": 25.48,
    "shoulder": -113.11,
    "elbow": -116.71,
    "wrist1": -36.46,
    "wrist2": 85.77,
    "wrist3": 206.48
},
"square7":{
    "base": 0.33,
    "shoulder": -120.27,
    "elbow": -106.33,
    "wrist1": -32.40,
    "wrist2": 87.72,
    "wrist3": 179.40
},
"square8":{
    "base": 11.79,
    "shoulder": -119.05,
    "elbow": -107.67,
    "wrist1": -35.16,
    "wrist2": 86.11,
    "wrist3": 191.70
},
"square9":{
    "base": 21.13,
    "shoulder": -120.87,
    "elbow": 105.63,
    "wrist1": -32.41,
    "wrist2": -87.27,
    "wrist3": 197.81
},
"top":{
    "base": 2.63,
    "shoulder": -84.68,
    "elbow": -92.03,
    "wrist1": -96.84,
    "wrist2": 90.10,
    "wrist3": 184.77
}, #CHANGE all out points
"out1":{
    "base": -33.65,
    "shoulder": -113.77,
    "elbow": -112.07,
    "wrist1": -46.15,
    "wrist2": 90.11,
    "wrist3": 144.32
},
"out2":{
    "base": -20.52,
    "shoulder": -104.95,
    "elbow": -127.42,
    "wrist1": -38.03,
    "wrist2": 91.49,
    "wrist3": 157
},
"out3":{
    "base": -28.88,
    "shoulder": -120.94,
    "elbow": -101.78,
    "wrist1": -46.34,
    "wrist2": 90.87,
    "wrist3": 154.17
},
"out4":{
    "base": -16.34,
    "shoulder": -112.78,
    "elbow": -117.20,
    "wrist1": -36.46,
    "wrist2": 90.88,
    "wrist3": 163.52
}
}



on_board = [0,0,0,0,0,0,0,0,0]
blue_count_list = [0,0,0,0,0,0,0,0,0]
##robot always red##

# 1 = human, blue    2 = robot, red     0 = empty
def has_won(x,y,z,bo):
    if (bo[x] == 1) and (bo[y] == 1) and (bo[z] == 1):
        return 1
#playerwon
    elif (bo[x] == 2) and (bo[y] == 2) and (bo[z] == 2):
        return 2
#compwon
    else:
        return 3 #game not done

def has_won_all(b):
    if (has_won(0,1,2,b)==2) or (has_won(0,4,8,b)==2) or (has_won(0,3,6,b)==2) or (has_won(1,4,7,b)==2) or (has_won(2,5,8,b)==2) or (has_won(2,4,6,b)==2) or (has_won(3,4,5,b)==2) or (has_won(6,7,8,b)==2):
        #comp won
        return 2
    elif (has_won(0,1,2,b)==1) or (has_won(0,4,8,b)==1) or (has_won(0,3,6,b)==1) or (has_won(1,4,7,b)==1) or (has_won(2,5,8,b)==1) or (has_won(2,4,6,b)==1) or (has_won(3,4,5,b)==1) or (has_won(6,7,8,b)==1):
        #player won
        return 1
    else:
        #no one won, game not done
        return 3

def block_player():
    ind = 10
    dup_list = on_board
    for t in range(0,9):
        if dup_list[t] == 0:
            dup_list[t] = 1
            if has_won_all(on_board) == 1:
                #print("This is the winning block for the player", t)
                ind = t
                break
            else:
                dup_list[t] = 0
    return ind

def cpu_winning_move():
    ind = 10
    dup_list2 = on_board
    for t in range(0,9):
        if dup_list2[t] == 0:
            dup_list2[t] = 2
            if has_won_all(on_board) == 2:
                ind = t
                break
            else:
                dup_list2[t] = 0
    return ind

def cpu_piece(on_bo):
	pickup_places_used = {"out1": "empty", "out2": "empty", "out3":"empty", "out4":"empty"}
    if has_won_all(on_board) == 3:
        #print("Looking where to place my piece...\n")
        i = 9
        num = block_player()
        num2 = cpu_winning_move()
        if num2 != 10:
	#cpu can win game on next move
            i = num2
        elif num != 10:
	#cpu can block player on next move
            i = num
        else:
            for l in range(0,9):
                if l in [0,2,6,8]:
                #checks for corner pieces first
                    if on_board[l] == 0:
                    #makes sure space is open
                        i = l
                        break
                    else:
                        continue
            if i not in [0,2,6,8]:
            #checks for center
                if on_board[4] == 0:
                #makes sure space is open
                    i = 4
                elif i not in [0,2,4,6,8]:
                    #checking for sides
                    for l in range(0,9):
                        if l in [1,3,5,7]:
                    #checks for side pieces
                            if on_board[l] == 0:
                                i = l
                                break
        on_bo[i] = 2
        for t in pickup_places_used:
            if pickup_places_used[t] == "empty"
            pickup_place = t
			pickup_places_used[t] = "used"
            break

        #move_bot(pickup_place)
#        access_to_board_pos = square_num[i]
#        move_bot("top")
#        move_bot(access_to_board_pos)

#1 = human, 2 = comp, 0 = empty
def add_player_to_board_list(frame_count, frame_count_checker, on_bo):
	for x in range(0,9):
		if (blue_count_list[x] > 500) and (frame_count == frame_count_checker + 55):
			#print (x)
			on_bo[x] = 1
            frame_count = frame_count_checker
#		elif red_count_list[x] > 500:
#			on_bo[x] = 2
		else:
			on_bo[x] = 0

def detect_player_piece(player_blue_list, image):
	#hardcoats each square place
	square1 = image[524:625, 700:815]
    square2 = image[524:625, 815:920]
    square3 = image[524:625, 920:1005]
    square4 = image[625:725, 700:807]
    square5 = image[625:725, 809:905]
    square6 = image[625:730, 910:1005]
    square7 = image[734:830, 700:792]
    square8 = image[733:830, 796:896]
    square9 = image[740:840, 900:1000]

# bgr values to detect blue
    lower_blue = np.array([200,150,0])
    upper_blue = np.array([255,240,100])
#    lower_red = np.array([130,95,186])
#    upper_red = np.array([160,120,250])

#assigning variable to number of blue pixels in each square
	blue1 = cv2.inRange(square1, lower_blue, upper_blue)
    blue2 = cv2.inRange(square2, lower_blue, upper_blue)
    blue3 = cv2.inRange(square3, lower_blue, upper_blue)
    blue4 = cv2.inRange(square4, lower_blue, upper_blue)
    blue5 = cv2.inRange(square5, lower_blue, upper_blue)
    blue6 = cv2.inRange(square6, lower_blue, upper_blue)
    blue7 = cv2.inRange(square7, lower_blue, upper_blue)
    blue8 = cv2.inRange(square8, lower_blue, upper_blue)
    blue9 = cv2.inRange(square9, lower_blue, upper_blue)

#list of number of blue pixels in each square
    player_blue_list[0] = np.sum(blue1>0)
    player_blue_list[1] = np.sum(blue2>0)
    player_blue_list[2] = np.sum(blue3>0)
    player_blue_list[3] = np.sum(blue4>0)
    player_blue_list[4] = np.sum(blue5>0)
    player_blue_list[5] = np.sum(blue6>0)
    player_blue_list[6] = np.sum(blue7>0)
    player_blue_list[7] = np.sum(blue8>0)
    player_blue_list[8] = np.sum(blue9>0)

class Stream(object):
    def __init__(self):
        self.sub = rospy.Subscriber("/kinect2/hd/image_color", Image, self.sub_callback)
        self.bridge = CvBridge()
        self.image = None
        self.black = None
        self.image_hsv = None
        self.pixel = (20,60,80) # arbitrary default

    def sub_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")

    def example_function(self):
        getImage = 0
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        video_writer = cv2.VideoWriter("/home/sar/catkin_ws/src/skill_assessment/kinect_perception/video.avi", fourcc, 20, (700, 500))
		frame_count = 0
		frame_count_check = 0
        while (not rospy.is_shutdown()) and (getImage == 0):
            frame_count += 1
            frame_cut = self.image[450:900, 640:1079]

           
			detect_player_piece(blue_count_list, self.image)
            add_player_to_board_list(frame_count, frame_count_check, on_board)

        	# cv2.imshow("video", frame_cut)
        	# cv2.waitKey(1)
            if 0 not in on_board: #tie
                break
            else:
        #	player goes first
        #		add_player_to_board_list()
                if has_won_all(on_board) == 1:
        		#player won
                    break
        			#then computer goes
                cpu_piece()
                if has_won_all(on_board) == 2:
        		#comp won
                        break
            while self.image is None:
                rospy.logwarn("Image not being received...")
                rospy.sleep(1)

            cv2.namedWindow('bgr', cv2.WINDOW_NORMAL)
            cv2.resizeWindow("tictactoe_perc", 800, 500)

            #Show RGB images
            # cv2.imshow("bgr", self.image)

            key = cv2.waitKey(1) & 0xFF
            getImage = 0  #

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
	            break

        cv2.destroyAllWindows()


