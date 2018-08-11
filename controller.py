import scene
import time
import sys
import tellopy
import motion 
import random

from subprocess import Popen, PIPE

dog = 'woof'

prev_flight_data = None
video_player = None


def handler(event, sender, data, **args):
    global prev_flight_data
    global video_player
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        if prev_flight_data != str(data):
            print(data)
            prev_flight_data = str(data)
    elif event is drone.EVENT_VIDEO_FRAME:
        if video_player is None:
            video_player = Popen(['mplayer', '-fps', '35', '-'], stdin=PIPE)
        try:
            video_player.stdin.write(data)
        except IOError as err:
            print(err)
            video_player = None
    else:
        print('event="%s" data=%s' % (event.getname(), str(data)))


def update(old, new, max_delta=0.3):
    if abs(old - new) <= max_delta:
        res = new
    else:
        res = 0.0
    return res
    
# initialize the drone
drone = tellopy.Tello(random.randint(1000,9000))
drone.connect()

# drone.start_video()
# drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
# drone.subscribe(drone.EVENT_VIDEO_FRAME, handler)

speed = 100
throttle = 0.0
yaw = 0.0
pitch = 0.0
roll = 0.0


class MyScene (scene.Scene):
    # def touch_began(self, touch):
    #    print('touch')
    
    def controller_changed(self, id, key, value):
      print("key: {} -- {}".format(key, value))
      try:
        #help(value)
        # loop with pygame.event.get() is too much tight w/o some sleep
        
        #roll, pitch, yaw = motion.get_attitude()
        roll = 0
        pitch = 0
        yaw = 0
        throttle = 0
        
        if key == 'thumbstick_right' and value:
          roll = value.x
          time.sleep(0.01)
          pitch = value.y
          time.sleep(0.01)
        
        if key == 'thumbstick_left' and value:
          throttle = value.y
          time.sleep(0.01)
          yaw = value.x
          time.sleep(0.01)
        
        
        if key == 'trigger_right' and value:
          roll = value
          yaw = value
        
        if key == 'trigger_left' and value:
          roll = value * -1
          yaw = value * -1
        
        roll = round(roll, 2) 
        pitch = round(pitch, 2)
        yaw = round(yaw, 2)
  
        
        if yaw:
          drone.set_yaw(yaw)
        if pitch:
          drone.set_pitch(pitch)
        if roll:
          drone.set_roll(roll)
        if throttle:
          drone.set_throttle(throttle)
          

      except Exception as e:
          print(e) 

print("starting controll....")
scene.run(MyScene())
drone.quit()
exit(1)
