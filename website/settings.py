# defaults
# integer field (minutes)
DEFAULT_GAME_DURATION = 1
DEFAULT_WHEEL_DURATION = 1
DEFAULT_PARROT_DURATION = 1

NOT_STARTED_STAGE  = "NS"
GAME_STAGE = "G"
WHEEL_STAGE = "W"
PARROT_STAGE = "P"
DONE_STAGE = "D"

NEXT_STAGE = {NOT_STARTED_STAGE: GAME_STAGE, GAME_STAGE: WHEEL_STAGE, WHEEL_STAGE: PARROT_STAGE, PARROT_STAGE: DONE_STAGE, DONE_STAGE: DONE_STAGE}

from website.ros import ROS
ros = ROS()