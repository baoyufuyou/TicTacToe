# Echo client program

### look at test script thing
import socket
import time
import math


robot_position = {
"square1":{
	"base": 50.95,
	"shoulder": -108.82,
	"elbow": -122,
	"wrist1": -40.78,
	"wrist2": 95.82,
	"wrist3": 228.28
},
"square2":{
	"base": 61.53,
	"shoulder": -120.25,
	"elbow": -103.61,
	"wrist1": -45.53,
	"wrist2": 93.78,
	"wrist3": 243.12
},
"square3":{
	"base": 67.02,
	"shoulder": -134.11,
	"elbow": -77.76,
	"wrist1": -58.38,
	"wrist2": 91.65,
	"wrist3": 248.05
},
"square4":{
	"base": 42.1,
	"shoulder": -118.68,
	"elbow": -106.23,
	"wrist1": -44.34,
	"wrist2": 93.29,
	"wrist3": 225.68
},
"square5":{
	"base": 50.68,
	"shoulder": -127.48,
	"elbow": -90.8,
	"wrist1": -49.87,
	"wrist2": 95.84,
	"wrist3": 233.38
},
"square6":{
	"base": 58.41,
	"shoulder": -141.35,
	"elbow": -64.5,
	"wrist1": -61.58,
	"wrist2": 93.27,
	"wrist3": 242.5
},
"square7":{
	"base": 34.49,
	"shoulder": -129.56,
	"elbow": -86.59,
	"wrist1": -52.11,
	"wrist2": 95.19,
	"wrist3": 216.63
},
"square8":{
	"base": 43,
	"shoulder": -140.01,
	"elbow": -66.75,
	"wrist1": -61.97,
	"wrist2": 96.03,
	"wrist3": 224.19
},
"square9":{
	"base": 50.26,
	"shoulder": -151.63,
	"elbow": -44.94,
	"wrist1": -68.52,
	"wrist2": 95.87,
	"wrist3": 232.87
},
"top":{
	"base": 85.55,
	"shoulder": -82.85,
	"elbow": -107.1,
	"wrist1": -71.3,
	"wrist2": 93.65,
	"wrist3": 270.02
},

"out1":{
	"base": 85.76,
	"shoulder": -108.66,
	"elbow": -123.61,
	"wrist1": -36.65,
	"wrist2": 94.04,
	"wrist3": 267.67
},
"out2":{
	"base": 71.25,
	"shoulder": -102.37,
	"elbow": -132.02,
	"wrist1": -36.68,
	"wrist2": 94.02,
	"wrist3": 253.59
},
"out3":{
	"base": 72.77,
	"shoulder": -112.58,
	"elbow": -117.32,
	"wrist1": -38.45,
	"wrist2": 95.45,
	"wrist3": 254.78
},
"out4":{
	"base": 84.82,
	"shoulder": -97.30,
	"elbow": -139.65,
	"wrist1": -32.66,
	"wrist2": 95.42,
	"wrist3": 266.29
},
}



HOST = "192.168.1.115" # The UR IP address
PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#f = open ("test.script", "rb")   #Robotiq Gripper

def degrees_to_radians(square_num):
	b = robot_position[str(square_num)]["base"]
	s = robot_position[str(square_num)]["shoulder"]
	e = robot_position[str(square_num)]["elbow"]
	w1 = robot_position[str(square_num)]["wrist1"]
	w2 = robot_position[str(square_num)]["wrist2"]
	w3 = robot_position[str(square_num)]["wrist3"]
	base = b/180.0* math.pi
	shoulder = s/180.0* math.pi
	elbow = e/180.0* math.pi
	wrist1 = w1/180.0* math.pi
	wrist2 = w2/180.0* math.pi
	wrist3 = w3/180.0* math.pi
	return "[" + str(base) + "," + str(shoulder) + "," + str(elbow) + "," + str(wrist1) + "," + str(wrist2) + "," + str(wrist3) + "]"
	
def move_robot_j(pose):
	s.send("movej(" + pose + ", a=0.2, v=0.2)" + "\n")

#def import_gripper_commands(f):
#	
#	l = f.read(1024)
#	while (l):
#		s.send(l)
#		l = f.read(1024)

#def activate_gripper():
#	f = open ("home/sar/catkin_ws/src/skill_assessment/kinect_perception/nodes/test.script", "rb")
#	import_gripper_commands(f)
#	s.send("rq_activate_and_wait()" + "\n")
#	s.send("end" + "\n")
#	f.close()

#def open_gripper():
#	f = open ("home/sar/catkin_ws/src/skill_assessment/kinect_perception/nodes/test.script", "rb")
#	import_gripper_commands(f)
#	s.send("rq_open()" + "\n")
#	s.send("end" + "\n")
#	f.close()
#	
#	
#def close_gripper():
#	f = open ("home/sar/catkin_ws/src/skill_assessment/kinect_perception/nodes/test.script", "rb")
#	import_gripper_commands(f)
#	s.send("rq_close()" + "\n")
#	s.send("end" + "\n")
#	f.close()
#	
#def deactivate_gripper():
#	s.send("end" + "\n")
#	
#def get_points(num_for_square):
#	square_num = str(num_for_square)
#	base = robot_position[square_num]["base"]
#	shoulder = robot_position[square_num]["shoulder"]
#	elbow = robot_position[square_num]["elbow"]
#	wrist1 = robot_position[square_num]["wrist1"]
#	wrist2 = robot_position[square_num]["wrist2"]
#	wrist3 = robot_position[square_num]["wrist3"]
#	parts_list = [base, shoulder, elbow, wrist1, wrist2, wrist3]
#	return parts_list
		

#activate_gripper() #make sure to activate gripper before using it
#pose = degrees_to_radians(-5,-100,-70,-180,12,30)
#move_robot_j(pose)
#time.sleep(5)
#close_gripper()
#time.sleep(5)

#pose = degrees_to_radians(-25,-120,-70,-200,12,50)
#move_robot_j(pose)
#time.sleep(5)
#open_gripper()
#time.sleep(5)

#pose = degrees_to_radians(-5,-100,-70,-180,12,30)
#move_robot_j(pose)
#time.sleep(5)
#close_gripper()
#time.sleep(5)

#pose = degrees_to_radians(-25,-120,-70,-200,12,50)
#move_robot_j(pose)
#time.sleep(5)
##open_gripper()
##time.sleep(5)

##s.close()

##activate_gripper()
##print("gripper activated")
#move_robot_j(degrees_to_radians("top"))
#print("moved to top")
#time.sleep(6)
##open_gripper()
##print("gripper opened")
##time.sleep(5)
#move_robot_j(degrees_to_radians("square5"))
#print("moved to get block")
#time.sleep(6)
##open_gripper()
##time.sleep(4)
##close_gripper()
##print("gripper closed")
##time.sleep(5)
##move_robot_j(degrees_to_radians("top"))
##time.sleep(6)
##move_robot_j(degrees_to_radians("square3"))
##time.sleep(6)
##open_gripper()
##time.sleep(5)
#activate_gripper()
move_robot_j(degrees_to_radians("top")) #go up each time to avoid bumping into anything
time.sleep(5)
#open_gripper()
#time.sleep(2)
pickup_place = "out1"
move_robot_j(degrees_to_radians(pickup_place)) #move to pickup spot that hasnt been used
time.sleep(5)
#close_gripper()
#time.sleep(2)
#move_robot_j(degrees_to_radians("top"))
#time.sleep(5)
#pose = degrees_to_radians("square1") #move to selected square
#move_robot_j(pose)
#time.sleep(5)
#open_gripper()
#time.sleep(2)

s.close()


