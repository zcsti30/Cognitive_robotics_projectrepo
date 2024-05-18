[//]: # (Image References)

[image1]: ./assets/emelkedo_oldalrol.JPG "emelkedo_oldalrol"
[image2]: ./assets/emelkedo_terben.JPG "emelkedo_terben"
[image3]: ./assets/gazebo_teljes_palya.JPG "gazebo_teljes_palya"
[image4]: ./assets/ut.JPG "ut"

# Kognitív robotika házi feladat
## Vonalkövetés turtlebottal és neurális hálóval, szakadások detektálása (3. feladat) szimuláció


Készítette: Csóti Zoltán, Endrődi Áron Péter, Eszter Ákos Endre, Havriló Balázs

videó link: ...

# Tartalomjegyzék:
1. [Telepítés](#Telepítés) 
2. [Használat](#Használat)
3. [Fejlesztési lépések](#fejlesztési-lépések)
    3.1. [Pályakészítés:](#pályakészítés-csóti-zoltán)
    3.2. ...



# Telepítés:
1. A projekt használata előtt telepíteni kell a szükséges csomagokat:
- turtlebot3 (wiki: http://wiki.ros.org/turtlebot3, http://wiki.ros.org/turtlebot3_msgs, http://wiki.ros.org/turtlebot3_simulations): a repository-kat érdemes a /catkin_ws/src mappába klónozni.
```console
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs
git clone https://github.com/MOGI-ROS/turtlebot3
```
- ...
- ...

2. Klónozni a projekt repository-t a /catkin_ws/src mappába. Az útvonal fontos!
```console
git clone https://github.com/zcsti30/Cognitive_robotics_projectrepo
```

3. Beleírni a .bashrc fájlba a Gazebo modellek elérési útját: 

export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/catkin_ws/src/Cognitive_robotics_projectrepo/cognitive_homework/gazebo_models/

4. catkin_make parancs kiadása a catkin workspace-en belül.

# Használat:

1. Célszerű nyitni 3 terminált.

2. Az egyik terminálban el kell indítani a szimulációt:

roslaunch cognitive_homework simulation_line_follow.launch

3. A második terminálban el kell indítani az Rviz-ben való rajzolást:

rosrun cognitive_homework mark_brokenline.py

4. A harmadik terminálban el kell indítani a vonalkövetést:

rosrun cognitive_homework line_follower_cnn.py

# Fejlesztési lépések:
A teljes feladatot felosztottuk a csapaton belül, ismertetjük a különálló fejlesztési lépéseket.

## Pályakészítés: (Csóti Zoltán)
A Turtlebot3 csomagjait használtuk, így a robotot nem kellett megtervezni. Azonban a feladat megvalósítása igényelt egy saját pályát. Első lépésként megterveztem az utat Blenderben. Egy fekete tégletest elem közepét fehér színre színeztem (a követendő vonalat reprezentálva), majd egy Bezier-görbe mentén végigpásztáztam a testet.

![][image4]

A következő lépés a szakadások megtervezése. Mivel a Gazeboban szimuláció közben nem lehet átszínezni az elemeket, ezért fekete színű emelkedőket terveztem, amelyeket szimuláció közben a megfelelő helyre mozgatva eltakarható a vonal. Mivel a testnek el kell takarnia az út középvonalát, ezért annak az út felett kell elhelyezkednie egy emelkedőként. A Turtlebot nehezen képes nem sík terepen való közlekedésre, így gondosan megtervezett alacsony szögű, lankás emelkedőket hoztam létre Bezier-görbékkel. A következő képeken oldalról és féloldalasan látható az emelkedő modellje.

![][image1]![][image2]

A Blender modellek elkészítése után exportáltam őket Collada fájlként, majd Gazebo modelleket készítettem belőlük. Mindkét elemet Kinematic tulajdonságúra állítottam, hogy ne hassanak rájuk külső hatások (pl. gravítáció). Végül a modellekből felépítettem egy Gazebo világot, amelyben a szimuláció zajlik.

![][image3]

A világ az úttestet tartalmazza, illetve 3 példányt az említett emelkedőkből. A robot később töltődik be, alapvetően nem része az általam készített mytrack.world fájlnak. A világot előre berendeztem a feladatnak megfelelően: az első körben 2 emelkedő takarja el a vonalat. Szimuláció közben az emelkedők oldalra húzással egyszerűen átrendezhetőek, hogy a második körben például az eddig kimaradt emelkedő is szerepet játsszon. 

Fontos beállítás volt az ütközési paraméterek (collision) testreszabása, amely egy bitmaszkkal történik. Tesztelés során kiderült, hogy a Turtlebot-nak a viszonylag enyhe lejtők is nagy kihívást jelentenek, továbbá a lejtőn való áthaladás során kiszámíthatatlanná vált a robot mozgása és több alkalalommal lement a pályáról. Ebből az okból kikapcsoltam az ütközést az emelkedő és a robot között, így a robot már nem lép interakcióba az emelkedővel - az emelkedő már csak egy vizuális elemként funkcionál a vonal eltakarása érdekében. Továbbá kikapcsoltam az ütközést az emelkedő és az úttest között is a szimuláció gyorsítása érdekében: az átlapolódások miatt felesleges ütközéseket számított a program. A kikapcsolás után a Real Time Factor átlagosan 0,16 értékről 0,76-ra emelkedett.