import subprocess
import signal
from subprocess import check_output
from subprocess import Popen
import time
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import threading
import glob, os
from ffprobe import FFProbe

tests = 0
testPassed = 0
testFailed = 0
def printFail(text):
	global testFailed
	global tests
	tests = tests + 1
	testFailed = testFailed + 1
	print("FAIL: {0}".format(text))

def printPass(text):
	global testPassed
	global tests
	tests = tests + 1
	testPassed = testPassed + 1
	print("PASS: {0}".format(text))

def checkFileExists():
	os.chdir(".")
	for file in glob.glob("*.avi"):
		return (file,True)

def deleteFile(fileName):
	os.chdir(".")
	os.remove(fileName)

def getLength(filename):
	duration = float(FFProbe(filename).video[0].duration)
	return duration

def openDriverSender():
	p = Popen(['rosrun', "camera_driver","camera_driver_sender"])
	return p
	#p.terminate()

def openDriverReceiver():
	p = Popen(["rosrun", "camera_driver","camera_driver_receiver"])
	return p


def testRecorder(seconds):
	cameraProcess = openDriverSender() #start camera
	receiverProcess = openDriverReceiver() #start recorder
	time.sleep(seconds) #wait for 5 seconds
	receiverProcess.terminate() #stop recorder
	cameraProcess.terminate() #stop camara
	name = checkFileExists()[0]
	exists = checkFileExists()[1]
	if exists is True:
		printPass("File exits") #check if file exists
		videoLength = getLength(name)
		if  videoLength > 0:
			printPass("Video length is {0} seconds > 0".format(videoLength)) #check if video length is bigger than 0
			deleteFile(name)
		else:
			printFail("Video length is 0") #check if video length is bigger than 0
	else:
		printFail("FAIL: File doesn't exists")

def imageReceiver(data):
	bridge = CvBridge()
	try:
		cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
		if cv_image is not None:
			printPass("Image is ok")
		else:
			printFail("Image is not ok")
	except CvBridgeError, e:
		print e

def testStream():
	#listen for pictures
	#check if images are received
	rospy.spin()

def startTestStream(seconds):
	cameraProcess = openDriverSender() #start camera
	rospy.init_node('driver_tester', anonymous=True)
	rospy.Subscriber("driverChannel",Image,imageReceiver)
	t1 = threading.Thread(target=testStream)
	t1.start()
	time.sleep(seconds)
	t1._Thread__stop()
	cameraProcess.terminate()


if __name__ == "__main__":

	print("Starting tests")
	print("Starting roscore")
	
	p = Popen(['roscore'])
	time.sleep(3)
	print("Roscore started")
	seconds = 5
	print("Running first test for {0} seconds".format(seconds))
	testRecorder(seconds)
	print("Tests: {0}, Passed: {1}, Failed: {2}".format(tests,testPassed,testFailed))
	tests = 0
	testPassed = 0
	testFailed = 0
	seconds = 600
	print("Running second test for {0} seconds".format(seconds))
	testRecorder(seconds)
	print("Tests: {0}, Passed: {1}, Failed: {2}".format(tests,testPassed,testFailed))
	

	tests = 0
	testPassed = 0
	testFailed = 0
	seconds = 15
	print("Running third test for {0} seconds".format(seconds))
	startTestStream(seconds)
	print("Tests: {0}, Passed: {1}, Failed: {2}".format(tests,testPassed,testFailed))
	
	print("All tests ran")
	p.terminate()
	

	