def _ypo():
	pickup_places_used = {"out1": "used", "out2": "empty", "out3":"empty", "out4":"empty"}
	for t in pickup_places_used:
#		print("this is in the loop, {}".format(t))
		if pickup_places_used[t] == "empty":
#			print("this is the pickup place for the degrees to radians function," + t)
			pickup_places_used[t] = "used"
			print(t)
			return t
for x in range(4):
	_ypo()

