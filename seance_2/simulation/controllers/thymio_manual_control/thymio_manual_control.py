# Copyright 1996-2019 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This controller gives to its node the following behavior:
Listen the keyboard. According to the pressed key, send a
message through an emitter or handle the position of Robot1.
"""
from controller import *

robot = Robot()
timestep = int(robot.getBasicTimeStep())
keyboard = robot.getKeyboard()
keyboard.enable(timestep)

print("Initialization")

#led = robot.getLED('leds.top')
led = robot.getDevice('leds.top') #webots 2021

distanceSensors = []
for i in list(range(0,7)):
  distanceSensors.append(robot.getDevice('prox.horizontal.'+str(i)))
  distanceSensors[i].enable(timestep)

motor_left = robot.getDevice("motor.left");
motor_right = robot.getDevice("motor.right");
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

robot_speed = 0.0
distanceVal = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
state = 0

while (robot.step(timestep) != -1):
  # Read the sensors, like:
  for i in list(range(0,7)):
    distanceVal[i] = distanceSensors[i].getValue()
  #print(distanceVal)
  motor_left.setVelocity(robot_speed)
  motor_right.setVelocity(robot_speed)
  
  # Process sensor data here
  
  # Enter here functions to send actuator commands, like:
  led.set(0x0000ff)
  command = keyboard.getKey()
  #print(command)
  
  if command==keyboard.LEFT:
    print('Left')
    motor_left.setVelocity(0.0) #-robot_speed
    motor_right.setVelocity(robot_speed)
  elif command==keyboard.RIGHT:
    print('right')
    motor_left.setVelocity(robot_speed)
    motor_right.setVelocity(0.0) #-robot_speed
  elif command==keyboard.UP:
    print('up')
    if robot_speed<2:
      robot_speed+=0.2
  elif command==keyboard.DOWN:
    print('down')
    if robot_speed>-2:
      robot_speed-=0.2
        