#!/usr/bin/env python3

import rospy
import numpy
#from std_msgs.msg import Int32  # Message type used in the node
from visualization_msgs.msg import Marker # Library for Marker in Rviz

rospy.init_node('broken_line_pub')    # Init the node with name "publisher"

marker_pub = rospy.Publisher('broken_line', Marker, queue_size=2) # We will publish to 'broken_line' topic

rospy.loginfo("broken_line_pub Python node has started and publishing data on broken_line")

rate = rospy.Rate(2)            # set the Hz

#count = Int32()                 # Count is now a ROS Int32 type variable that is ready to be published

#count.data = 0                  # Initializing count


########################### Marker code ####################################
marker = Marker()

marker.header.frame_id = "odom"
marker.header.stamp = rospy.Time.now()

# set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
marker.type = 2
marker.id = 0

# Set the scale of the marker
marker.scale.x = 1.0
marker.scale.y = 1.0
marker.scale.z = 1.0

# Set the color
marker.color.r = 1.0
marker.color.g = 0.0
marker.color.b = 0.0
marker.color.a = 1.0

# Set the pose of the marker
marker.pose.position.x = 0
marker.pose.position.y = 0
marker.pose.position.z = 0
marker.pose.orientation.x = 0.0
marker.pose.orientation.y = 0.0
marker.pose.orientation.z = 0.0
marker.pose.orientation.w = 1.0



while not rospy.is_shutdown():  # Run the node until Ctrl-C is pressed

    marker.header.stamp = rospy.Time.now()
    marker.pose.position.x = 1
    marker.pose.position.y = 1
    

    #marker_pub.publish(count)          # Publishing data on topic "publisher_topic"
    marker_pub.publish(marker)
    #count.data += 1
        
    rate.sleep()                # Wait until next iteration