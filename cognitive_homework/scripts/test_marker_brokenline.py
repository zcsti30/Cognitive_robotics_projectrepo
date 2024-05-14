#!/usr/bin/env python3

import math
import rospy
import numpy
from visualization_msgs.msg import MarkerArray # Library for MarkerArray in Rviz
from visualization_msgs.msg import Marker # Library for Marker in Rviz

rospy.init_node('broken_line_node')    # Init the node with a name

marker_pub = rospy.Publisher('broken_line', MarkerArray, queue_size=100) # We will publish to 'broken_line' topic

rospy.loginfo("broken_line_node Python node has started and publishing data on broken_line") # Info message when starting the node 

rate = rospy.Rate(1)        # Set the Hz of the operation of the node 

count = 0
MARKERS_MAX = 100
markerArray = MarkerArray()

# Make sure that the timer has already been initialized
testTime = 0
while not testTime:
    testTime = rospy.Time.now()

# For testing
increment=0

# Run the node until Ctrl-C is pressed
while not rospy.is_shutdown():  
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

   # Remove oldest marker when reaching the maximum number of markers
   if(count > MARKERS_MAX-1):
       markerArray.markers.pop(0)
       count -= 1

   # Insert new marker
   markerArray.markers.append(marker)
   count += 1

   # Remove oldest marker when reaching timeout
   currenttime = rospy.Time.now()
   markertime = markerArray.markers[0].header.stamp
   ## testing begin
   difftime = currenttime.to_sec() - markertime.to_sec()
   print(difftime)
   ## testing end
   if(currenttime.to_sec() - markertime.to_sec() > 7):
       markerArray.markers.pop(0)
       count -= 1

   # Renumber the marker IDs
   id = 0
   for m in markerArray.markers:
       m.id = id
       id += 1 

   
   
   ## testing
   for m in markerArray.markers:
       print(m.id)

   # Publish the array     
   marker_pub.publish(markerArray)
   
   # Testing
   print(count)
    # Wait until next iteration
   rate.sleep()                