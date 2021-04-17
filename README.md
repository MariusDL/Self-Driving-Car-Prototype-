## Self-Driving-Car-Prototype
Implementation of a Self Driving Car Prototype with Raspberry Pi and Deep Learning

## Parts used
- SUNFOUNDER Raspberry Pi Robot Car Kit
- Raspberry Pi Camera
- Sony IMX219 Wide Angle camera module
- Raspberry Pi 4 Model B
- Power bank with at least 2A output
- 2 18650 batteries
- Coral USB Accelerator
- Raspberry Pi cooling fan
- PS4 Controller

## Install instructions
1. Follow the instructions in the kit to assemble the Robot car and attach the Raspberry Pi to it
2. Attach the Raspberry Pi Camera along with the wide angle lens module(you can use normal camera, but with wide lens the results are better)
3. I recommend using a cooling fan with the Raspberry Pi because it overheats very quickly because of the high processing demands. 
4. The power bank will power the Raspberry Pi and the 18650 batteries will power the car chassis
5. The Coral USB accelerator is required for the traffic objects detection part. You can eliminate that if you don't want it.
6. I have used a PS4 Controller connected to the Raspberry Pi via bluetooth to drive the car in order to record the data for training.
7. I have created and printed the 3D parts to make the components fit well on the car, but if you can not 3d print you can find alternatives how to fit them

<br>The assembled vehicle<br>
<img src="https://raw.githubusercontent.com/MariusDL/Self-Driving-Car-Prototype-/main/readme%20imges/car.png" alt="app1" border="0" height="400">


## How to use
1. Install the required libraries on the Raspberry Pi: opencv, numpy, keras, edgetpu, PIL, picar, pygame
2. Connect the PS4 controller to the car via Bluetooth
3. Create a road track on the floor using some tape of a different color than the floor 
4. Open the save_training_data.py file, the car will start moving strainght and you have to drive it few laps using the ps4 controller
5. After drving stop the script, and in the same directory with the script will be created a data directory containing images which represent the training data
6. In the name of each image is recorded the corresponding steering angle

<br>Images saved on the Raspberry Pi after driving the car<br>
<img src="https://raw.githubusercontent.com/MariusDL/Self-Driving-Car-Prototype-/main/readme%20imges/Screenshot_2.png" alt="app1" border="0" height="400">
<br>
7. Move the images on a PC to train the model<br>
8. Install the required libraries on PC: pickle, numpy, pandas, tensorflow, sklearn, matplotlib, pil, imgaug, opencv<br>
9. Open the train models.ipynb file with Jupiter Notebook<br>
10. The images should be in a folder called data which should be in the same location with the train models.ipynb file<br>
11. Run all the jupiter notebook components one at a time and wait for the training to finish<br>
12. After training are presented some metrics, if they are not satisfactory you can adjust some of the parameters<br>
13. After running the whole notebook in a folder called model will be a file: model.h5<br>
14. Move this file back on the Raspberry Pi in the models folder on the car<br>
15. Run the drive.py file and the car should drive itself by predicting steering angles with a pretty high level of accuracy
16. In the folder there already exists a model trained that detects traffic objects

<br>The car driving itself<br>
<img src="https://raw.githubusercontent.com/MariusDL/Self-Driving-Car-Prototype-/main/readme%20imges/Screenshot_1.png" alt="app1" border="0" height="400">
<br>

<br>Traffic object detection<br>
<img src="https://raw.githubusercontent.com/MariusDL/Self-Driving-Car-Prototype-/main/readme%20imges/Screenshot_3.png" alt="app1" border="0" height="400">
<br>

