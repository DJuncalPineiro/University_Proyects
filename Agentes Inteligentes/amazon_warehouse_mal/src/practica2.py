#!/usr/bin/env python
from amazon_warehouse.src.utils import obstacles
import rospy
from utils import navigation
from geometry_msgs.msg import Pose2D, Twist, Point, Quaternion
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan

class Practica1:

    def __init__(self):
        self.nav = navigation.Navigation()
        self.execTest0()
        #self.execTest1()

    def execAstar(self,requests):
        print("A STAR ")

    # TESTS 

    def execTest0(self):
        print("TEST WAREHOUSE0")
        
        self.nav.move(1)
        self.nav.rotateLeft()
        self.nav.move(1)
        self.nav.rotateRight()
        self.nav.move(2)
        self.nav.rotateLeft()
        self.nav.move(1)
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.rotateLeft()
        self.nav.move(3)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.move(4)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.rotateLeft()
        self.nav.move(3)
        self.nav.rotateRight()
        self.nav.move(2)
        self.nav.rotateLeft()
        self.nav.move(4)
        self.nav.rotateLeft()
        self.nav.move(1)
        self.nav.rotateLeft() 









    def execTest1(self):
        print("TEST WAREHOUSE1")
        
        # First pallet
        self.nav.move(3)
        self.nav.rotateLeft()
        self.nav.move(2)
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.upLift()
        self.nav.move(2)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.move(7)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.move(2)
        self.nav.downLift()
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.move(2)
        self.nav.rotateRight()

        # Second pallet       
        self.nav.move(5)
        self.nav.rotateLeft()
        self.nav.move(3)
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.upLift()
        self.nav.move(3)
        self.nav.rotateRight()
        self.nav.move(6)
        self.nav.downLift()
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.move(11)

        # Init position
        self.nav.rotateLeft()
        self.nav.rotateLeft()

class Estado:

    def __init__(self):
        x = 0
        y = 0
        orientation = 1
        pallet = False
        robot_state = [[x, y], orientation, pallet]
        map_dimensions = [7,9]
        obst = [[4,3], [5,3], [6,3], [2,6], [3,6]]

        rospy.init_node('Practica 2', anonymous= True)
        self.pub_vel = rospy.Publisher('/amazon_warehouse_robot/cmd_vel', Twist, queue_size=10)
        self.pub_grabber = rospy.Publisher('/amazon_warehouse_robot/joint_cmd', Float32, queue_size=10)
        rospy.Subscriber('/amazon_warehouse_robot/laser/scan', LaserScan,self.LaserCb)

    def LaserCb(self, msg):
        global front_dist
        front_dist = msg.ranges[len(msg)//2]
    
    def forward_posible(self):
        if front_dist < 0.5:
            return False
        else:
            return True



if __name__ == '__main__':
    try:
        p = Practica1()
    except (RuntimeError, TypeError, NameError) as err:
        rospy.loginfo("Practica2 terminated: ", err)