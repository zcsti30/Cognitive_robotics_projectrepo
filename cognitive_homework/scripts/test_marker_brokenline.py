#!/usr/bin/env python3

import math
import rospy
import numpy
from visualization_msgs.msg import MarkerArray # Library for MarkerArray in Rviz
from visualization_msgs.msg import Marker # Library for Marker in Rviz

rospy.init_node('broken_line_node')    # Init the node with a name

marker_pub = rospy.Publisher('broken_line', MarkerArray, queue_size=100) # We will publish to 'broken_line' topic

rospy.loginfo("broken_line_node Python node has started and publishing data on broken_line topic") # Info message when starting the node 

rate = rospy.Rate(10)        # Set the Hz of the operation of the node 

count = 0                   # Number of markers

markerArray = MarkerArray()

# Make sure that the timer has already been initialized
testTime = 0
while not testTime:
    testTime = rospy.Time.now()

# init delete markerArray and marker
deleteArray = MarkerArray()
deletemarker = Marker()
deletemarker.header.frame_id = "odom"
deletemarker.action = deletemarker.DELETEALL
deletemarker.id = 0
deleteArray.markers.append(deletemarker)

# For testing
increment=0

# Run the node until Ctrl-C is pressed
while not rospy.is_shutdown():  
   # Delete previous markers on the map
   marker_pub.publish(deleteArray)

   # Creating new marker 
   marker = Marker()
   marker.header.frame_id = "odom"
   marker.type = marker.SPHERE
   marker.action = marker.ADD
   marker.header.stamp = rospy.Time.now()
   marker.scale.x = 0.2
   marker.scale.y = 0.2
   marker.scale.z = 0.2
   marker.color.a = 1.0
   marker.color.r = 1.0
   marker.color.g = 0.0
   marker.color.b = 0.0
   marker.pose.orientation.w = 1.0
   # For testing
   increment += 1
   marker.pose.position.x = increment
   marker.pose.position.y = increment
   marker.pose.position.z = 0 

   # Insert new marker
   markerArray.markers.append(marker)
   count += 1

   # Remove oldest marker when reaching timeout
   if(count != 0):    
      currenttime = rospy.Time.now()
      markertime = markerArray.markers[0].header.stamp

      if(currenttime.to_sec() - markertime.to_sec() > 4):
         markerArray.markers.pop(0)
         count -= 1

   # Renumber the marker IDs
   if(count != 0):     
      id = 0
      for m in markerArray.markers:
         m.id = id
         id += 1 

      # Publish the array     
      marker_pub.publish(markerArray)
   
   # Wait until next iteration
   rate.sleep()                