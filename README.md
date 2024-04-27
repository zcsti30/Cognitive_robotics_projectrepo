# Probarepo
Elkészítettem a pályát a szimulációhoz. Ez itt egy útmutató, hogy hogyan használjátok:

Előkészületek:
1. Clone-ozzátok a repo-t a /catkin_ws/src mappába. Az útvonal fontos!!!

2. Írjátok bele a .bashrc fájlba a Gazebo modellek elérési útját: 

export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/catkin_ws/src/Probarepo/cognitive_homework/gazebo_models/

3. catkin_make parancs a catkin workspace-en belül

Használat:
1. nyissatok két terminált

2. az egyik terminálban indítsátok el a szimulációt:

roslaunch cognitive_homework simulation_line_follow.launch

3. a másik terminálban indítsatok el valamilyen vezérlést:

3.1. pl. vonalkövetés az órai neurális hálóval

rosrun cognitive_homework line_follower_cnn.py

vagy mondjuk
3.2. távirányítóval irányítani a robotot

rosrun teleop_twist_keyboard teleop_twist_keyboard.py
