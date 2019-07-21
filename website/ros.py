import rospy
from std_msgs.msg import String
import os
from os.path import expanduser


dir = expanduser("~") + '/Desktop/'
def create_directories():
    global dir
    if not os.path.exists(dir + 'cabinet_db'):
        os.makedirs(dir + 'cabinet_db')
    dir = dir + 'cabinet_db/'




class ROS:
    def __init__(self):
        self.parrot_command_name = rospy.Publisher('web/parrot_command_name', String, queue_size=10)
        self.parrot_command = rospy.Publisher('web/parrot_commands', String, queue_size=10)
        self.parrot_voice_commands = rospy.Publisher('web/parrot_voice_commands', String, queue_size=10)
        self.patient_uid = rospy.Publisher('web/patient_uid', String, queue_size=10)
        self.patient_uid_directories = rospy.Publisher('web/patient_uid/dir', String, queue_size=10)
        self.wheel_status = rospy.Publisher('web/something', String, queue_size= 10)
        rospy.init_node('web_logger', anonymous=False)
        create_directories()
