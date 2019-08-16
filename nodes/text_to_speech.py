#import pyttsx
#import time

#engine = pyttsx.init()
#engine.setProperty('rate', 120)
#engine.setProperty('volume', 1)

##voices = engine.getProperty('voices')

##for voice in voices:
##	print("Voice:")
##	print(" - ID: %s" % voice.id)
##	print(" - Name: %s" % voice.name)
##	print(" - Languages: %s" % voice.languages)
##	print(" - Gender: %s" % voice.gender)
##	print(" - Age: %s" % voice.age)
##	engine.say("hello!")
##	engine.runAndWait()

#def talk(words):
#	engine.startLoop(False)
#	engine.say(words)
#	engine.iterate()
#	while engine.isBusy():
#		time.sleep(0.1)
#	engine.endLoop()
#	engine.runAndWait()

##text_to_speech("want to play again?")


##engine.runAndWait()
##engine.say("Let's play tic tac toe!")
##engine.runAndWait()

#import os
#import datetime

#def talk(text):
#      return os.system("espeak  -s 155 -a 200 "+text+" " )

#m = datetime.datetime.now().strftime("%I %M %S")
##talk("'Sir the time is"+str(int(m[0:2]))+" "+str(int(m[3:5]))+" : ' ")
#talk("'Let's play tic tac toe'")


from subprocess import call

def talk(words):
	call(["espeak","-s140 -ven+18 -z", words])
