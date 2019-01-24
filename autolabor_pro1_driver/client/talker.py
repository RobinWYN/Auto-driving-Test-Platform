#!/usr/bin/env python

import rospy
import socket
import os
import time
import json

from std_msgs.msg import String
from nav_msgs.msg import Odometry

try:
    MASTER_IP = os.environ['SEND_IP'].strip('\r')
    MASTER_PORT = os.environ['SEND_PORT'].strip('\r')
except:
    print "please set the IP and PORT for master node!!"

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((MASTER_IP,int(MASTER_PORT)))

def callback(data):

    send_data = {}
    # print(type(data.pose))
    send_data['position'] = str(data.pose).encode('utf8')
        
    send_data['twist'] = str(data.twist).encode('utf8')
    send_data['car_number'] = 1
    send_data['timestamp'] = time.time()
    send_data['pkg_seqnum'] = data.header.seq
    
    s.send(json.dumps(send_data,encoding = 'utf-8'))
        
    print send_data['timestamp']
       
def listener():
    rospy.init_node('listener1',anonymous=True)

    rospy.Subscriber("wheel_odom",Odometry,callback)
    
    rospy.sleep(2)
    
    rospy.spin()
        
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
