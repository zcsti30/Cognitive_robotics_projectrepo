[//]: # (Image References)

[image1]: ./assets/emelkedo_oldalrol.JPG "emelkedo_oldalrol"
[image2]: ./assets/emelkedo_terben.JPG "emelkedo_terben"
[image3]: ./assets/gazebo_teljes_palya.JPG "gazebo_teljes_palya"
[image4]: ./assets/ut.JPG "ut"
[image5]: ./assets/szakadas_detektalas.JPG "szakadas_detektalas"
[image6]: ./assets/mappastruktura.png "mappastruktura"
[image7]: ./assets/hiba.png "hiba"

# Kognitív robotika házi feladat
## Vonalkövetés turtlebottal és neurális hálóval, szakadások detektálása (3. feladat) szimuláció


Készítette: Csóti Zoltán, Endrődi Áron Péter, Eszter Ákos Endre, Havriló Balázs

videó link: https://www.youtube.com/watch?v=iF7i6ESd8c0

# Tartalomjegyzék:
- [Kognitív robotika házi feladat](#kognitív-robotika-házi-feladat)
  - [Vonalkövetés turtlebottal és neurális hálóval, szakadások detektálása (3. feladat) szimuláció](#vonalkövetés-turtlebottal-és-neurális-hálóval-szakadások-detektálása-3-feladat-szimuláció)
- [Tartalomjegyzék:](#tartalomjegyzék)
- [Telepítés:](#telepítés)
- [Használat:](#használat)
- [Fejlesztési lépések:](#fejlesztési-lépések)
  - [Pályakészítés (Csóti Zoltán)](#pályakészítés-csóti-zoltán)
  - [A szakadás detektálása (Csóti Zoltán és Havriló Balázs)](#a-szakadás-detektálása-csóti-zoltán-és-havriló-balázs)
  - [Neurális háló (Endrődi Áron Péter és Eszter Ákos Endre)](#neurális-háló-endrődi-áron-péter-és-eszter-ákos-endre)

# Telepítés:
1. A projekt használata előtt telepíteni kell a szükséges csomagokat:
- turtlebot3 (wiki: http://wiki.ros.org/turtlebot3, http://wiki.ros.org/turtlebot3_msgs, http://wiki.ros.org/turtlebot3_simulations): a repository-kat érdemes a /catkin_ws/src mappába klónozni.
```console
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs
git clone https://github.com/MOGI-ROS/turtlebot3
```
- hector trajectory server (wiki: http://wiki.ros.org/hector_trajectory_server)
```console
sudo apt install ros-noetic-hector-trajectory-server
```
- amcl (wiki: http://wiki.ros.org/amcl)
```console
sudo apt install ros-noetic-amcl
``` 
- compressed_image_transport (wiki: http://wiki.ros.org/compressed_image_transport)
```console
sudo apt install ros-noetic-compressed-image-transport
``` 

- teleop_twist_keyboard (wiki: http://wiki.ros.org/teleop_twist_keyboard)
```console
sudo apt install ros-noetic-teleop-twist-keyboard
``` 

- opencv-python (wiki: https://pypi.org/project/opencv-python/ https://opencv.org/)
```console
pip install opencv-python
``` 
- tensorflow 2.9.2 (wiki: https://www.tensorflow.org/versions/r2.9/api_docs/python/tf)
```console
pip install tensorflow==2.9.2
``` 

2. Klónozni a projekt repository-t a /catkin_ws/src mappába. Az útvonal fontos!
```console
git clone https://github.com/zcsti30/Cognitive_robotics_projectrepo
```

3. Beleírni a .bashrc fájlba a Gazebo modellek elérési útját: 
```console
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/catkin_ws/src/Cognitive_robotics_projectrepo/cognitive_homework/gazebo_models/
```

4. Fordítani a catkin workspace-t.
```console
catkin_make
```

# Használat:

1. Célszerű nyitni 3 terminált.

2. Az egyik terminálban el kell indítani a szimulációt:

```console
roslaunch cognitive_homework simulation_line_follow.launch
```

3. A második terminálban el kell indítani az Rviz-ben való rajzolást:

```console
rosrun cognitive_homework mark_brokenline.py
```

4. A harmadik terminálban el kell indítani a vonalkövetést:

```console
rosrun cognitive_homework line_follower_cnn.py
```

# Fejlesztési lépések:
A teljes feladatot felosztottuk a csapaton belül, ismertetjük a különálló fejlesztési lépéseket.

## Pályakészítés (Csóti Zoltán)
A Turtlebot3 csomagjait használtuk, így a robotot nem kellett megtervezni. Azonban a feladat megvalósítása igényelt egy saját pályát. Első lépésként megterveztem az utat Blenderben. Egy fekete téglatest elem közepét fehér színre színeztem (a követendő vonalat reprezentálva), majd egy Bezier-görbe mentén végigpásztáztam a testet.

![][image4]

A következő lépés a szakadások megtervezése. Mivel a Gazeboban szimuláció közben nem lehet átszínezni az elemeket, ezért fekete színű emelkedőket terveztem, amelyeket szimuláció közben a megfelelő helyre mozgatva eltakarható a vonal. Mivel a testnek el kell takarnia az út középvonalát, ezért annak az út felett kell elhelyezkednie egy emelkedőként. A Turtlebot nehezen képes nem sík terepen való közlekedésre, így gondosan megtervezett alacsony szögű, lankás emelkedőket hoztam létre Bezier-görbékkel. A következő képeken oldalról és féloldalasan látható az emelkedő modellje.

![][image1]![][image2]

A Blender modellek elkészítése után exportáltam őket Collada fájlként, majd Gazebo modelleket készítettem belőlük. Mindkét elemet Kinematic tulajdonságúra állítottam, hogy ne hassanak rájuk külső hatások (pl. gravítáció). Végül a modellekből felépítettem egy Gazebo világot, amelyben a szimuláció zajlik.

![][image3]

A világ az úttestet tartalmazza, illetve 3 példányt az említett emelkedőkből. A robot később töltődik be, alapvetően nem része az általam készített mytrack.world fájlnak. A világot előre berendeztem a feladatnak megfelelően: az első körben 2 emelkedő takarja el a vonalat. Szimuláció közben az emelkedők oldalra húzással egyszerűen átrendezhetőek, hogy a második körben például az eddig kimaradt emelkedő is szerepet játsszon. 

Fontos beállítás volt az ütközési paraméterek (collision) testreszabása, amely egy bitmaszkkal történik. Tesztelés során kiderült, hogy a Turtlebot-nak a viszonylag enyhe lejtők is nagy kihívást jelentenek, továbbá a lejtőn való áthaladás során kiszámíthatatlanná vált a robot mozgása és több alkalalommal lement a pályáról. Ebből az okból kikapcsoltam az ütközést az emelkedő és a robot között, így a robot már nem lép interakcióba az emelkedővel - az emelkedő már csak egy vizuális elemként funkcionál a vonal eltakarása érdekében. Továbbá kikapcsoltam az ütközést az emelkedő és az úttest között is a szimuláció gyorsítása érdekében: az átlapolódások miatt felesleges ütközéseket számított a program. A kikapcsolás után a Real Time Factor átlagosan 0,16 értékről 0,76-ra emelkedett.

## A szakadás detektálása (Csóti Zoltán és Havriló Balázs)

A feladatunk kiírásában az is szerepelt, hogy a vonalkövető robot  szakadásokat is detektáljon. Ezt a feladatot a broken_line_node node végzi majd el, amit a mark_brokenline.py nevezetű python script irányít. Az Rviz konfigurációjában létre kellett hoznunk egy MarkerArray kijelzőt, amely a megfelelő topic-on kapja az információt az elkészített node-tól. Térjünk rá a kódra:

A megvalósításhoz először is importálnunk kell számos libraryt. A [Marker](http://wiki.ros.org/rviz/DisplayTypes/Marker) és a MarkerArray könyvtárakat az Rviz-ben való kijelzéshez, illetve a az [Odometry](http://wiki.ros.org/navigation/Tutorials/RobotSetup/Odom) és a Twist könyvtárakat ahhoz, hogy a robot pontos pozícióját, illetve sebességét tudjuk. Ezeket később fel fogjuk használni a folyamat során.

Először is inicializáljuk a node-ot. Ezután létrehozzuk a marker_pub-ot, ami majd tartalmazni fogja a közölni kívánt szükséges adatokat a kijelzéshez. Ezt fogja a node publisholni a broken_line topic-ra az Rviz számára. Fontos megemlíteni, hogy a queue_size paramétert érdemes 1 értéken hagyni kijelzés típusú alkalmazások esetén, ugyanis ebben az esetben nem gond, hogy ha adatot veszítünk, viszont fontos, hogy mindig a legfrissebb adattal dolgozzunk. Érdemes elhelyezni egy loginfo parancsot a kódban, így tudni fogjuk, hogy fut már a node.

Praktikus a node operációs frekvenciáját összhangban  megválasztani a funkciójával. Esetünkben a megjelenítéshez 50 Hz elég, ezt a rospy.Rate()-tel állíthatjuk be Hz-ben.
A count változó a markerek számát fogja számon tartani.
A kódban az is beállítható, hogy hány másodperc után törölje a program a régi markereket. A feladat például a második körben elvárja, hogy egy pontban cseréljük le a szakadást sima vonalra, illetve tegyünk szakadást máshova. Ahhoz, hogy ezt megfelelően illusztálni tudjuk, meg kell győződnünk arről, hogy az első kör által detektált adatok nem folynak át a második körbe. A node-unk a régi markereit a beállított idő elteltével törli, így ez nem fog problémát jelenteni.

Ahhoz, hogy ezt a metódust használni tudjuk, meg kell győződnünk arról, hogy az időzítés megfelelően elindult a futtatás során. Ebből az okból a program elején egy while ciklussal bizonyosodunk meg arról, hogy az időzítés inicializálódott, vagyis a rospy.Time.now() nem nulla értéket ad. Erre azért van szükség, mert a timer néha későn inicializálódik, ezért az első pár futásnál nem lenne értéke.

Minden iterációban töröljük az összes kijelzett markert, majd összeállítjuk az akkor kijelezni kívánt markerek új listáját, majd végül azt közöljük az Rviz-zel. Ehhez használjuk a deletemarker és deleteArray változókat.

Az odom_data fogja tárolni a robot helyzetét egy annak megfelelően felépített globális változóban.
Ahhoz, hogy mindig az aktuális adatokat meg tudjuk kapni, fell kell iratkozni a megfelelő topic-ra és szükségünk van egy callback függvényre. Ez fogja majd lekérni a pozíció adatokat és frissíteni a változó értékét. Ugyanezt a műveletet elvégezzük a sebességekre is.

A pozicionális adatokra azért van szükség, mert azok alapján tudjuk majd kijelezni a szakadás helyét, míg a sebességadatok arra engednek következtetni, hogy az adott pontban szakadás van-e vagy sem.

A node futását egy végtelen ciklussal biztosítjuk, amit jelen esetben Ctrl-C billentyűkombinációval tudunk leállítani Iterációnként egy pontot vizsgálunk, amit egy markerként kezelünk. Az ehhez a markerhez tartozó fontosabb paramétereket itt állítjuk be.
Kiválaszotttuk a frame-et, amelyhez a markereket rendeltük.
Ezután megadjuk, hogy a marker maga hogy nézzen ki. Esetünkben ez egy piros gömb lesz a vizsgált pont pozíciójában. A képen látható egy példa, ahol egy szakadás hosszát rengeteg marker egymás melletti elhelyezésével jelöli a program.

![][image5]

Ha a neurális háló szakadást érzékel, akkor az x irányú lineáris sebességet 0.22 egységre állítja. Ha ez az adott iterációban megvalósul, akkor mivel szakadásunk van, az elkészített markert hozzáfűzzük az előzetesen létrehozott marker tömbhöz. Ezt a tömböt használjuk arra, hogy a kijelezni kívánt markereket átadjuk az Rviz-nek. A régi markerek eltávolítását időbélyegek összehasonlításával végeztük el.

Ezek után érdemes a markerek ID-ját újraírni, hogy elkerüljünk különféle csúszásokat, ugyanis a hozzáfőzött új marker id-ja is mindig 0, illetve, ha eltávolítjuk az utolsó lejárt markert, az is mindig a legkisebb id-val rendelkezik. Ha minden iterációban újrarendezzük az id-kat, akkor az iterációk között tudunk még kommunikálni, és mindig kézben tudjuk tartani ezeket az értékeket.

Az iteráció végén publish paranccsal küldi ki a node az adatokat. Ezután már csak egy sleep parancs fordul le, ami a node operációs frekvenciáját hivatott megtartani.

## Neurális háló (Endrődi Áron Péter és Eszter Ákos Endre)
A feladatunkban használt neurális háló az órai neurális hálós megoldást veszi alapul. Tehát egy klasszifikáló neurális hálót készítettünk a vonalkövetés és szakadás detektálás feladat elvégzésére. Ez azt jelentette, hogy az órán használt „forward”, „left”, „right”, „nothing” classok-hoz hozzáadtunk egy „tear”class-t, illetve a finomabb kormányzás és ezáltal a nagyobb kanyarsebesség elérése érdekében „light left” és „light right” class-ok is implementálásra kerültek. A „save_training_images.py”, a „train_network.py” és a „line_follower_cnn.py” kódokon változtattunk a fentebb említett módon. 
Mivel a projekt felépítése mappaszerkezet szempontjából azonos a „turtlebot3_mogi” ROS package-hez, a „save_training_images.py” fileban csak a 
```python
path = rospack.get_path('turtlebot3_mogi ')
```
sort kellett megváltoztatni a következőre:
```python
path = rospack.get_path('cognitive_homework')
```

Így már a szimuláció elindítása és egy távirányító bekapcsolása után a
```console
rosrun cognitive_homework save_training_images.py
```
parancsot futtatva a robotot tudjuk vezetni a pályán és tanító képeket is tudunk készíteni az ’s’ vagy space gombok lenyomásával. 

Ezek után a készített tanító képeket a ROS package-ünk „training_images” mappájának megfelelő almappáiba rendezve, majd pedig lefuttatva a tanító algoritmust elkészült a már szakadást és éles, illetve finom kanyarokat detektáló neurális hálónk.
A tanítóképek mappastruktúrájában a class-ok elnevezése a következő:

![][image6]

A tanító algoritmus train_network.py kódjában a fő változtatás a képeket felcímkéző for ciklusban történt. Itt kellett újabb „elif” ágakat implementálni, amik az új class-okat valósították meg. Az ábrán látható kódrészletből kiderül, milyen „prediction” értékhez milyen class tartozik. Ez fontos, amikor parancssorban vizsgáljuk például debug céljából, hogy például egy szakadáshoz érkezve azt a neurális hálónk helyesen detektálja-e.

```python
for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data  list
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (image_size, image_size))
    image = img_to_array(image)
    data.append(image)
    # extract the class label from the image path and update the
    # labels list
    label = imagePath.split(os.path.sep)[-2]
    print("Image: %s, Label: %s" % (imagePath, label))
    if label == 'forward':
        label = 0
    elif label == 'right':
        label = 1
    elif label == 'lright':
        label = 2
    elif label == 'left':
        label = 3
    elif label == 'lleft':
        label = 4
    elif label == 'tear':
        label = 5
    else:
        label = 6
    labels.append(label)
```

Emellett, mivel a class-ok száma változott és a class-ok darabszáma több függvénynél is paraméterként átadásra kerül, néhány helyen ezt is át kellet írni. A tanító és validációs adatok szétválasztásánál, illetve magánál a neurális hálót felépítő függvénynél 4-ről 7-re változott ez a paraméter.

```python
trainY = to_categorical(trainY, num_classes=7)
testY = to_categorical(testY, num_classes=7)

model = build_LeNet(width=image_size, height=image_size, depth=3, classes=7)
```
A tanítást a következő paranccsal tudjuk lefuttatni:
```console
python3 train_network.py 
```
Mivel egy ilyen hálónak működése nehezen jósolható, a tanító adatokat javítani és kiegészíteni kellett több alkalommal is. Ezt folytatva addig, amíg kellően jó eredményt nem kaptunk, amit a következő grafikon szemléltet. Láthatóan a tanító adatokon az accuracy 1-hez, míg a loss 0-hoz tart és a validációs adatok kellően jól konvergálnak tanító adatok eredményeihez.

![][image7]

Ezek után az utolsó lépés a „line_follower_cnn.py” kód átalakítása volt. Természetesen itt is a 
```python
path = rospack.get_path('turtlebot3_mogi ')
```
sort meg kellett változtatni a következőre:
```python
path = rospack.get_path('cognitive_homework')
```
, hogy mindent a mi ROS package-ünkben keressen a program.
Emellett a „def processImage(self, img):”-en  belüli if-else ágban egészítettük ki plusz class-okkal a kódot. Az alábbi kódból láthatóak továbbá a beállított transzlációs és rotációs sebességértékek:

```python
        if prediction == 0: # Forward
            self.cmd_vel.angular.z = 0
            self.cmd_vel.linear.x = 0.4
        elif prediction == 1: # right
            self.cmd_vel.angular.z = -0.8
            self.cmd_vel.linear.x = 0.2
        elif prediction == 2: # lright
            self.cmd_vel.angular.z = -0.3
            self.cmd_vel.linear.x = 0.3
        elif prediction == 3: # left
            self.cmd_vel.angular.z = 0.8
            self.cmd_vel.linear.x = 0.2
        elif prediction == 4: # lleft
            self.cmd_vel.angular.z = 0.3
            self.cmd_vel.linear.x = 0.3
        elif prediction == 5: #tear
            self.cmd_vel.angular.z= 0.0 
            self.cmd_vel.linear.x = 0.22
        else: # Nothing
            self.cmd_vel.angular.z = 0.1
            self.cmd_vel.linear.x = 0.0
```
Ezzel megvalósítottuk az átalakított neurális hálóval való vonalkövetést. 