from utils.ros import connect, commands
import roslibpy

ros, talker = connect(topic = '/cmd_vel/nav')
print("sending:")
print(commands["forward"])
import time
#time.sleep(3)
continous = roslibpy.Message(
        {"linear": {"x": 0.1, "y": 0.0, "z": 0.0}, # x előre max 0.4
         "angular": {"x": 0.0, "y": 0.0, "z":0.0}  # z irány -0.8 jobbra vége, 0.8 balra vége
        })
for i in range(100):
    print("sending:")
    talker.publish(continous)
    time.sleep(0.5)
time.sleep(3)
#talker.publish(commands['forward'])
