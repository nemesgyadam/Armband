import os
import numpy as np
import roslibpy
clear = lambda: os.system("cls")


from config.armband import *


class Controller:
    def __init__(self, target):
        self.target = target
        if 'ros' in target:
            self.init_ros()
       
        if 'keyboard' in target:
            self.init_keyboard()

    def init_keyboard(self):
        import pyautogui
    
    def init_ros(self):
        from utils.ros import connect, commands

        ros, self.talker, self.ros_commands = connect(target = self.target)
        if self.target =='ros-step':
            self.init_command_buffer()

    def init_command_buffer(self):
        self.command_buffer = np.zeros((3, settings['steps']))
        self.buffer_index = 0
     

    def keyboard_control(self, gas, direction):
        if gas == 0:
            pyautogui.keyUp("up")
        elif gas == 1:
            pyautogui.keyDown("up")
        if direction == 1:
            pyautogui.keyDown("right")
            pyautogui.keyUp("left")
        elif direction == 2:
            pyautogui.keyDown("left")
            pyautogui.keyUp("right")
        else:
            pyautogui.keyUp("right")
            pyautogui.keyUp("left")

    def ros_continous_control(self, gas_continous, direction_continous):
        gas_continous = gas_continous.numpy()
        direction_continous = direction_continous.numpy()[0]
        gas_continous *= 0.4
        gas_continous = np.round(gas_continous, 3)
        direction_continous *= -0.8
        direction_continous = np.round(direction_continous, 3)
        
        if gas_continous < 0.05:
            gas_continuous = 0
        if abs(direction_continous) < 0.05:
            direction_continous = 0
            
        command = roslibpy.Message(
            {"linear": {"x": gas_continous, "y": 0.0, "z": 0.0}, # x előre max 0.4
            "angular": {"x": 0.0, "y": 0.0, "z":direction_continous}  # z irány -0.8 jobbra vége, 0.8 balra vége
            }
            )
        print(command)
        self.talker.publish(command)
     

    def ros_step_control(self, gas, direction):
        self.buffer_index += 1

        if self.buffer_index == -49:
            print('Stand by')
        if self.buffer_index == 0:
            clear()
            print('Recording')
        if self.buffer_index >= 0:
            if gas == 1:
                self.command_buffer[0, self.buffer_index-1] = 1
            if direction == 1:
                self.command_buffer[1, self.buffer_index-1] = 1
            elif direction == 2:
                self.command_buffer[2, self.buffer_index-1] = 1
                
            
            if self.buffer_index == settings['steps']:
                clear()
                print("calculating average")
                gas_summ, right_summ, left_summ = np.count_nonzero(self.command_buffer, axis=1)
                

                print(f"gas: {gas_summ}, left: {left_summ}, right: {right_summ}")
                
                if gas_summ > settings['move_thresholds']['gas']:
                    print("Sending forward to ROS")
                    self.talker.publish(self.ros_commands['forward'])
                elif left_summ > settings['move_thresholds']['left']:
                    print("Sending left to ROS")
                    self.talker.publish(self.ros_commands['left'])
                elif right_summ > settings['move_thresholds']['right']:
                    print("Sending right to ROS")
                    self.talker.publish(self.ros_commands['right'])


                self.init_command_buffer()
                self.buffer_index = -50