# Echo client program
import socket
import time
import math


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

def import_gripper_commands(f):
	
	l = f.read(1024)
	while (l):
		s.send(l)
		l = f.read(1024)

def activate_gripper():
	f = open ("test.script", "rb")
	import_gripper_commands(f)
	s.send("rq_activate_and_wait()" + "\n")
	s.send("end" + "\n")
	f.close()

def open_gripper():
	f = open ("test.script", "rb")
	import_gripper_commands(f)
	s.send("rq_open()" + "\n")
	s.send("end" + "\n")
	f.close()
	
	
def close_gripper():
	f = open ("test.script", "rb")
	import_gripper_commands(f)
	s.send("rq_close()" + "\n")
	s.send("end" + "\n")
	f.close()
	
def deactivate_gripper():
	s.send("end" + "\n")
	
def get_points(num_for_square):
	square_num = str(num_for_square)
	base = robot_position[square_num]["base"]
	shoulder = robot_position[square_num]["shoulder"]
	elbow = robot_position[square_num]["elbow"]
	wrist1 = robot_position[square_num]["wrist1"]
	wrist2 = robot_position[square_num]["wrist2"]
	wrist3 = robot_position[square_num]["wrist3"]
	parts_list = [base, shoulder, elbow, wrist1, wrist2, wrist3]
	return parts_list
		

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
#open_gripper()
#time.sleep(5)

#s.close()

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
activate_gripper()
move_robot_j(degrees_to_radians("top")) #go up each time to avoid bumping into anything
open_gripper()
move_robot_j(degrees_to_radians(select_pickup_places(pickup_places_dict))) #move to pickup spot that hasnt been used
close_gripper()
move_robot_j(degrees_to_radians("top"))
pose = degrees_to_radians(index_to_square_num[index])
move_robot_j(pose)
open_gripper()
s.close()


