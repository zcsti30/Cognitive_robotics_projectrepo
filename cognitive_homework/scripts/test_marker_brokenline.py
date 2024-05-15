#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import MarkerArray # Library for MarkerArray in Rviz
from visualization_msgs.msg import Marker # Library for Marker in Rviz
from nav_msgs.msg import Odometry

rospy.init_node('broken_line_node')    # Init the node with a name

marker_pub = rospy.Publisher('broken_line', MarkerArray, queue_size=100) # We will publish to 'broken_line' topic

rospy.loginfo("broken_line_node Python node has started and publishing data on broken_line topic") # Info message when starting the node 

rate = rospy.Rate(10)        # Set the Hz of the operation of the node 

count = 0                    # Count the number of markers

memorytime = 15              # Markers will be deleted after this time [sec]

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

# We store the latest odometry data in this variable
odom_data = Odometry()

# Callback function and subscribe for current odometry data
def odom_callback(msg):
    global odom_data
    odom_data = msg
    
rospy.Subscriber("/odom", Odometry, odom_callback, queue_size=1)

# Run the node until Ctrl-C is pressed
while not rospy.is_shutdown():  
   # Delete previous markers on the map
   marker_pub.publish(deleteArray)

   # Create new marker 
   marker = Marker()
   marker.header.frame_id = "odom"
   marker.type = marker.SPHERE
   marker.action = marker.ADD
   marker.header.stamp = rospy.Time.now()
   marker.scale.x = 0.05
   marker.scale.y = 0.05
   marker.scale.z = 0.05
   marker.color.a = 1.0
   marker.color.r = 1.0
   marker.color.g = 0.0
   marker.color.b = 0.0
   marker.pose.orientation.w = 1.0
   marker.pose.position.x = odom_data.pose.pose.position.x
   marker.pose.position.y = odom_data.pose.pose.position.y
   marker.pose.position.z = 0 

   # Insert new marker
   if(marker.pose.position.x != 0):
         markerArray.markers.append(marker)
         count += 1

   # Remove oldest marker when reaching timeout
   if(count != 0):    
      currenttime = rospy.Time.now()
      markertime = markerArray.markers[0].header.stamp

      if(currenttime.to_sec() - markertime.to_sec() > memorytime):
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