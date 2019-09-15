################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, time
import thread
import csv
import matplotlib.pyplot as plt
import numpy as np
from model import *

sys.path.insert(0,"C:\\Users\\chinc\\Desktop\\Project_Fingering\\LeapDeveloperKit_3.2.1_win\\LeapDeveloperKit_3.2.1+45911_win\\LeapSDK\\lib")
sys.path.insert(0,"C:\\Users\\chinc\\Desktop\\Project_Fingering\\LeapDeveloperKit_3.2.1_win\\LeapDeveloperKit_3.2.1+45911_win\\LeapSDK\\lib\\x64")
import Leap

file_name='a0000.csv'
data = []

plt.ion()

# count = 0

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def __init__(self):
        Leap.Listener.__init__(self)
        self.count = 0
        self.thumbm = get_weights('thumb.h5')
        self.fingerm = get_weights('finger.h5')
        self.number = [0,0,0,0,0,0]

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        stuff = None
        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Get fingers
            data.append([])
            count = 0
            stuff = []
            for finger in hand.fingers:
                count+=1
                stuff.append([])
                if True:
                    for b in range(0, 3):
                        bone1 = finger.bone(b)
                        bone2 = finger.bone(b+1)
                        data[-1].append(bone1.direction.x*bone2.direction.x+bone1.direction.y*bone2.direction.y+bone1.direction.z*bone2.direction.z)
                        stuff[-1].append(bone1.direction.x*bone2.direction.x+bone1.direction.y*bone2.direction.y+bone1.direction.z*bone2.direction.z)
        if stuff!=None and stuff!=[]:
            n = 0
            a=''
            trial = np.array([stuff[0]])
            # print trial
            # print self.thumbm
            out = actual_outputs(self.thumbm,trial)
            if trial[0][1]<0.93:
                a += '0'
            else:
                a += '1'
                n+=1
            for i in range(4):
                trial = np.array([stuff[i+1]])
                out = actual_outputs(self.fingerm, trial)
                if trial[0][1]<0.93:
                    a+='0'
                else:
                    a+='1'
                    n+=1
            self.number[n]+=1
            # print a
        if not frame.hands.is_empty:
            pass
    def get_number(self):
        return np.argmax(np.array(self.number))

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

def count(t):
    print 'ready'
    time.sleep(1)
    print 'start'
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    start = time.time()
    while time.time()-start<t:
        pass
    n = listener.get_number()
    print n
    controller.remove_listener(listener)


if __name__ == "__main__":
    while True:
        count(1)
