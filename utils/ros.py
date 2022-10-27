import roslibpy
import math
# platypous wifi: s4vqjc5n3cgx
# 192.168.1.200
#10.8.8.187
# irob
# bark
frame_id = "base_link"
        
commands = {
    "forward": roslibpy.Message(
        {
            "header": {"frame_id": frame_id},
            "pose": {
                "position": {"x": 1.0, "y": 0.0,  "z": 0.0},
                "orientation": {"x": 0.0, "y": 0.0, "w": 1.0, "z": 0.0},
            },
        }
    ),
    "right": roslibpy.Message(
        {
           "header": {"frame_id": frame_id},
            "pose": {
                "position": {"x": 0.0, "y": 0.0,  "z": 0.0},
                "orientation": {"x": 0.0, "y": 0.0, "w": math.cos(math.pi/4), "z": math.sin(-(math.pi/4))},
            },
        }
    ),
    "left": roslibpy.Message(
        {
           "header": {"frame_id": frame_id},
            "pose": {
                "position": {"x": 0.0, "y": 0.0,  "z": 0.0},
                "orientation": {"x": 0.0, "y": 0.0, "w": math.cos(math.pi/4), "z": math.sin(math.pi/4)},
            },
        }
    ),
}
def connect(host="10.8.8.187", port=9090, target = 'ros-step'):
    """
    Connect to ROS
    and subsribe to the required topics
    """
    if target == 'ros-step':
        topic="/mobile_controller/set_target"
        msg_type = 'geometry_msgs/PoseStamped'
    if target == 'ros-continous':
        topic = '/cmd_vel/nav'
        msg_type = 'geometry_msgs/Twist'
        
    ros = roslibpy.Ros(host=host, port=port)
    ros.run()

    if ros.is_connected:
        print("Connected to ROS")
    talker = roslibpy.Topic(ros, topic, msg_type)
    return ros, talker, commands
