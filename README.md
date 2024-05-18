# Cognitive_robotics_projectrepo
Kész a repo és át lett nevezve.

Előkészületek:

1. Clone-ozzátok a repo-t a /catkin_ws/src mappába. Az útvonal fontos!!!

2. Írjátok bele a .bashrc fájlba a Gazebo modellek elérési útját: 

export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/catkin_ws/src/Cognitive_robotics_projectrepo/cognitive_homework/gazebo_models/

3. catkin_make parancs a catkin workspace-en belül

Használat:

1. nyissatok 3 terminált

2. az egyik terminálban indítsátok el a szimulációt:

roslaunch cognitive_homework simulation_line_follow.launch

3. a második terminálban indítsátok el az Rviv-ben való rajzolást

rosrun cognitive_homework mark_brokenline.py

4. a harmadik terminálban indítsátok el a vonalkövetést:

rosrun cognitive_homework line_follower_cnn.py

