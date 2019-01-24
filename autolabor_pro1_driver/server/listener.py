#!/usr/bin/env python
import rospy
import os 
import socket
import json
import yaml
from std_msgs.msg import String

pub = rospy.Publisher('CarLocation', String, queue_size=10)
rospy.init_node('server', anonymous=True)
        
def server():
    MASTER_IP = os.environ['ROS_IP']
    MASTER_PORT = os.environ['ROS_PORT']

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.bind((MASTER_IP,int(MASTER_PORT)))
    s.listen(5)
    print("server waiting!!")
    while True:
        connection,address = s.accept()
        while True:
            buf = connection.recv(1024)
            if buf:
                try:
                    data = json.loads(buf,encoding = 'utf-8')
                    pose_data = yaml.load(data['position'])
                    twist_data = yaml.load(data['twist'])
                    print(data['car_number']) 
                    print(pose_data['pose'])
                    car_location = {}
                    car_location['car_number'] = data['car_number']
                    car_location['position'] = pose_data['pose']['position']
                    pub.publish(json.dumps(car_location,encoding = 'utf8'))
                except:
                    pass
    

if __name__ == '__main__':
    server()
