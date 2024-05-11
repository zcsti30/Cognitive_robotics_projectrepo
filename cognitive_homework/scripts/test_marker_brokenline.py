#!/usr/bin/env python3

import math
import rospy
import numpy
#from std_msgs.msg import Int32  # Message type used in the node
from visualization_msgs.msg import MarkerArray # Library for MarkerArray in Rviz
from visualization_msgs.msg import Marker # Library for Marker in Rviz

rospy.init_node('broken_line_node')    # Init the node with a name

marker_pub = rospy.Publisher('broken_line', MarkerArray, queue_size=100) # We will publish to 'broken_line' topic

rospy.loginfo("broken_line_node Python node has started and publishing data on broken_line") # Info message when starting the node 

rate = rospy.Rate(2)        # set the Hz of the operation of the node 

count = 0
MARKERS_MAX = 5
markerArray = MarkerArray()

# Run the node until Ctrl-C is pressed
while not rospy.is_shutdown():  
   marker = Marker()
   marker.header.frame_id = "odom"
   marker.type = marker.SPHERE
   marker.action = marker.ADD
   marker.scale.x = 0.2
   marker.scale.y = 0.2
   marker.scale.z = 0.2
   marker.color.a = 1.0
   marker.color.r = 1.0
   marker.color.g = 0.0
   marker.color.b = 0.0
   marker.pose.orientation.w = 1.0
   marker.pose.position.x = count
   marker.pose.position.y = count
   marker.pose.position.z = 0 

   # We add the new marker to the MarkerArray, removing the oldest
   # marker from it when necessary
   if(count > MARKERS_MAX-1):
       markerArray.markers.pop(0)

   markerArray.markers.append(marker)

   # Renumber the marker IDs
   id = 0
   for m in markerArray.markers:
       m.id = id
       id += 1

   # Publish the array     
   marker_pub.publish(markerArray)

   count += 1
    
    # Wait until next iteration
   rate.sleep()                