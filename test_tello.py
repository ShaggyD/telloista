"""
tellopy sample using joystick and video palyer

 - you can use PS3/PS4/XONE joystick to controll DJI Tello with tellopy module
 - you must install mplayer to replay the video
 - Xbox One Controllers were only tested on Mac OS with the 360Controller Driver.
    get it here -> https://github.com/360Controller/360Controller'''
"""

import time
import sys
import tellopy

from subprocess import Popen, PIPE


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


def main():

    # Try to identify the joystick (Which is not going to be used by us)
    buttons = None
    '''
    try:
        js = pygame.joystick.Joystick(0)
        js.init()
        js_name = js.get_name()
        print('Joystick name: ' + js_name)
        if js_name in ('Wireless Controller', 'Sony Computer Entertainment Wireless Controller'):
            buttons = JoystickPS4
        elif js_name in ('PLAYSTATION(R)3 Controller', 'Sony PLAYSTATION(R)3 Controller'):
            buttons = JoystickPS3
        elif js_name == 'Xbox One Wired Controller':
            buttons = JoystickXONE
    except pygame.error:
        pass

    if buttons is None:
        print('no supported joystick found')
        return

    '''

    # initialize the drone
    drone = tellopy.Tello()
    drone.connect()

    # drone.start_video()
    drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
    # drone.subscribe(drone.EVENT_VIDEO_FRAME, handler)

    speed = 100
    throttle = 0.0
    yaw = 0.0
    pitch = 0.0
    roll = 0.0

    # Manage the drone with the access
    try:
        while 1:
            # loop with pygame.event.get() is too much tight w/o some sleep
            time.sleep(0.01)
            raise

            # Define a Deadzone
            # if -buttons.DEADZONE <= e.value and e.value <= buttons.DEADZONE:
            #     e.value = 0.0

            if e.axis == buttons.LEFT_Y:
                throttle = update(
                    throttle, e.value * buttons.LEFT_Y_REVERSE)
                drone.set_throttle(throttle)

            if e.axis == buttons.LEFT_X:
                yaw = update(yaw, e.value * buttons.LEFT_X_REVERSE)
                drone.set_yaw(yaw)

            if e.axis == buttons.RIGHT_Y:
                pitch = update(pitch, e.value *
                                buttons.RIGHT_Y_REVERSE)
                drone.set_pitch(pitch)

            if e.axis == buttons.RIGHT_X:
                roll = update(roll, e.value * buttons.RIGHT_X_REVERSE)
                drone.set_roll(roll)


    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)

    drone.quit()
    exit(1)


if __name__ == '__main__':
    main()
