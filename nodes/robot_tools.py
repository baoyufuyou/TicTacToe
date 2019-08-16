# Echo client program
import socket
import time
import math

HOST = "192.168.1.115" # The UR IP address
PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#f = open ("test.script", "rb")   #Robotiq Gripper

def degrees_to_radians(b,s,e,w1,w2,w3):
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
	
	
activate_gripper() #make sure to activate gripper before using it
pose = degrees_to_radians(-5,-100,-70,-180,12,30)
move_robot_j(pose)
time.sleep(5)
close_gripper()
time.sleep(5)

pose = degrees_to_radians(-25,-120,-70,-200,12,50)
move_robot_j(pose)
time.sleep(5)
open_gripper()
time.sleep(5)

pose = degrees_to_radians(-5,-100,-70,-180,12,30)
move_robot_j(pose)
time.sleep(5)
close_gripper()
time.sleep(5)

pose = degrees_to_radians(-25,-120,-70,-200,12,50)
move_robot_j(pose)
time.sleep(5)
open_gripper()
time.sleep(5)

s.close()



