#!/usr/bin/python
import subprocess
import signal
from subprocess import check_output
from subprocess import Popen
import rospy
from std_msgs.msg import String
import threading
import sys
import glob, os
import time
firstFilterCount = 0
secondFilterCount = 0
thirdFilterCount = 0
totalFirstFilterCount = 0
totalSecondFilterCount = 0
totalThirdFilterCount = 0
tests = 0
testPassed = 0
testFailed = 0
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def printFail(text):
	global testFailed
	global tests
	tests = tests + 1
	testFailed = testFailed + 1
	print(bcolors.FAIL+"FAIL: {0}".format(text)+bcolors.ENDC)

def printPass(text):
	global testPassed
	global tests
	tests = tests + 1
	testPassed = testPassed + 1
	print(bcolors.OKGREEN+"PASS: {0}".format(text)+bcolors.ENDC)
#This is the callback for the ros message. Each channel subscribed should have another callback.
def callbackFirst(data):
	global firstFilterCount
	global totalFirstFilterCount
	firstFilterCount = firstFilterCount + 1
	totalFirstFilterCount = totalFirstFilterCount + 1
	print("Received message from first filter: "+str(data.data))

def callbackSecond(data):
	global secondFilterCount
	global totalSecondFilterCount
	secondFilterCount = secondFilterCount + 1
	totalSecondFilterCount = totalSecondFilterCount + 1
	print("Received message from second filter: "+str(data.data))

def callbackThird(data):
	global thirdFilterCount
	global totalThirdFilterCount
	thirdFilterCount = thirdFilterCount + 1
	totalThirdFilterCount = totalThirdFilterCount + 1
	print("Received message from third filter: "+str(data.data))

def listener():
	#Subsribing to all the incoming channels
    rospy.Subscriber("FirstTaskFilter_Channel", String, callbackFirst)
    print("subscribed to FirstTaskFilter_Channel")

    rospy.Subscriber("SecondTaskFilter_Channel", String, callbackSecond)
    print("subscribed to SecondTaskFilter_Channel")

    rospy.Subscriber("collision_channel", String, callbackThird)
    print("subscribed to collision_channel")

	#Add subscription to new channel
	#rospy.Subscriber("SecondTaskFilter_Channel", String, callbackSecond)
	#print("subscribed to SecondTaskFilter_Channel")
    rospy.spin()

def talker():
	global testPassed
	global tests
	global testFailed
	global firstFilterCount
	global secondFilterCount
	global thirdFilterCount
	pub = rospy.Publisher('PythonTests', String, queue_size=10)
	rate = rospy.Rate(1) # 10hz
	print("Starting test 1")
	rate.sleep()
	pub.publish("201") 	#Starting filter 1
	time.sleep(5)		#Letting it run for 5 seconds
	pub.publish("211")	#Stopping filter 1
	rate.sleep()
	print("Received " + str(firstFilterCount) +" messages from the first filter")
	print("Received " + str(secondFilterCount) +" messages from the second filter")
	print("Received " + str(thirdFilterCount) +" messages from the third filter")
	if firstFilterCount > 50 and secondFilterCount < 5 and thirdFilterCount < 5:
		printPass("First Test")
	else:
		printFail("First Test")
	print("End test 1")
	

	thirdFilterCount = 0
	firstFilterCount = 0
	secondFilterCount = 0
	print("Waiting 3 seconds between tests...")
	time.sleep(3)
	print("Starting test 2")
	pub.publish("202") 	#Starting filter 2
	time.sleep(5)		#Letting it run for 5 seconds
	pub.publish("212")	#Stopping filter 2
	print("Received " + str(firstFilterCount) +" messages from the first filter")
	print("Received " + str(secondFilterCount) +" messages from the second filter")
	print("Received " + str(thirdFilterCount) +" messages from the third filter")
	if firstFilterCount < 5 and secondFilterCount > 50 and thirdFilterCount < 5:
		printPass("Second Test")
	else:
		printFail("Second Test")
	print("End test 2")

	firstFilterCount = 0
	secondFilterCount = 0
	thirdFilterCount = 0
	print("Waiting 3 seconds between tests...")
	time.sleep(3)
	print("Starting test 3")
	pub.publish("201") 	#Starting filter 1
	pub.publish("202") 	#Starting filter 2
	pub.publish("203") 	#Starting filter 3
	time.sleep(5)		#Letting it run for 5 seconds
	pub.publish("211")	#Stopping filter 1
	pub.publish("212")	#Stopping filter 2
	pub.publish("213")	#Stopping filter 3
	print("Received " + str(firstFilterCount) +" messages from the first filter")
	print("Received " + str(secondFilterCount) +" messages from the second filter")
	print("Received " + str(thirdFilterCount) +" messages from the third filter")
	if firstFilterCount > 50 and secondFilterCount > 50 and thirdFilterCount > 50:
		printPass("Third Test")
	else:
		printFail("Third Test")
	print("End test 3")
	
	thirdFilterCount = 0
	firstFilterCount = 0
	secondFilterCount = 0
	print("Waiting 3 seconds between tests...")
	time.sleep(3)
	print("Starting test 4")
	pub.publish("204") 	#Starting filter 4 (not implemented, shouldn't do anything)
	rate.sleep()
	print("Received " + str(firstFilterCount) +" messages from the first filter")
	print("Received " + str(secondFilterCount) +" messages from the second filter")
	print("Received " + str(thirdFilterCount) +" messages from the third filter")
	if firstFilterCount < 5 and secondFilterCount < 5 and thirdFilterCount < 5:
		printPass("Fourth Test")
	else:
		printFail("Fourth Test")
	print("End test 4")


	thirdFilterCount = 0
	firstFilterCount = 0
	secondFilterCount = 0
	print("Waiting 3 seconds between tests...")
	time.sleep(3)
	print("Starting test 5")
	pub.publish("201") 	#Starting filter 1
	time.sleep(5)		#Letting it run for 5 seconds
	pub.publish("201")	#Starting filter 1 again (should't make any problem)
	time.sleep(1)
	pub.publish("201")	#Starting filter 1 again (should't make any problem)
	#time.sleep()
	pub.publish("201")	#Starting filter 1 again (should't make any problem)
	time.sleep(2)
	pub.publish("201")	#Starting filter 1 again (should't make any problem)
	time.sleep(1)
	pub.publish("211")	#Stopping filter 1 once. Should stop the system entirely
	print("Received " + str(firstFilterCount) +" messages from the first filter")
	print("Received " + str(secondFilterCount) +" messages from the second filter")
	print("Received " + str(thirdFilterCount) +" messages from the third filter")
	if firstFilterCount > 50 and secondFilterCount < 5 and thirdFilterCount < 5:
		printPass("Fifth Test")
	else:
		printFail("Fifth Test")
	print("End test 5")


	thirdFilterCount = 0
	firstFilterCount = 0
	secondFilterCount = 0
	print("Waiting 3 seconds between tests...")
	time.sleep(3)
	print("Starting test 6")
	pub.publish("202") 	#Starting filter 2
	time.sleep(5)		#Letting it run for 5 seconds
	pub.publish("212")	#Stopping filter 2
	time.sleep(1)	
	pub.publish("212")	#Stopping filter 2 again (shouldn't make any problem)
	time.sleep(1)	
	pub.publish("212")	#Stopping filter 2 again (shouldn't make any problem)
	time.sleep(1)	
	pub.publish("212")	#Stopping filter 2 again (shouldn't make any problem)
	time.sleep(1)	
	pub.publish("212")	#Stopping filter 2 again (shouldn't make any problem)
	print("Received " + str(firstFilterCount) +" messages from the first filter")
	print("Received " + str(secondFilterCount) +" messages from the second filter")
	print("Received " + str(thirdFilterCount) +" messages from the third filter")
	if firstFilterCount < 5 and secondFilterCount > 50 and thirdFilterCount < 5:
		printPass("Sixth Test")
	else:
		printFail("Sixth Test")
	print("End test 6")

	#Add pretty prints "starting test 7".. "ending test 7" and test numbers.
	#Don't forget to add the code in the main.cpp in the server (203 to start, 213 to stop)
	#Gery's manual explains it pretty good. Drive -> documents for AGANA
	#pub.publish(203) to start your filter
	#time.sleep(seconds) let it play some time
	#pub.publish(213) stop the filter
	print("In total received " + str(totalFirstFilterCount) +" messages from the first filter")
	print("In total received " + str(totalSecondFilterCount) +" messages from the second filter")
	print("In total received " + str(totalThirdFilterCount) +" messages from the third filter")
	#print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC
	print("Tests: {0},".format(tests)+bcolors.OKGREEN+" Passed: {0}".format(testPassed)+bcolors.ENDC+","+bcolors.FAIL+" Failed: {0}".format(testFailed)+bcolors.ENDC)
	t1._Thread__stop()


t1 = threading.Thread(target=listener)
t2 = threading.Thread(target=talker)
if __name__ == '__main__':
    try:
    	print("Starting roscore")
    	roscoreProcess = Popen(['roscore'])
    	time.sleep(3)
    	print("Starting the camera")
    	driverProcess = Popen(['rosrun', "camera_driver","camera_driver_sender"])
    	time.sleep(1)
    	os.chdir("/home/jdorfsman/git/IPU_ROS/src")
    	print("Starting the server")
    	hc_visionProcess = Popen(['rosrun', "hc_vision","hc_vision_src"])
    	time.sleep(3)
    	print("Starting the tests")
    	rospy.init_node('python_testing')
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Terminating the processes")
        roscoreProcess.terminate()
        hc_visionProcess.terminate()
        driverProcess.terminate()
    except rospy.ROSInterruptException:
        pass
