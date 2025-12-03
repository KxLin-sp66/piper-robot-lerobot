import time
# Import piper_sdk module
from piper_sdk import *

if __name__ == "__main__":
    # Instantiate interface, the default parameters of the parameters are as follows
    #   can_name(str): can port name
    #   judge_flag(bool): Whether to enable the can module when creating this instance. 
    #                     If you use an unofficial module, please set it to False
    #   can_auto_init(bool): Whether to automatically initialize to open the can bus when creating this instance. 
    #                        If set to False, please set the can_init parameter to True in the ConnectPort parameter
    #   dh_is_offset([0,1] -> default 0x01): Whether the dh parameter used is the new version of dh or the old version of dh. 
    #                                       The old version is before S-V1.6-3, and the new version is after S-V1.6-3 firmware
    #           0 -> old
    #           1 -> new
    #   start_sdk_joint_limit(bool -> False): Whether to enable SDK joint angle limit, which will limit both feedback and control messages
    #   start_sdk_gripper_limit(bool -> False): Whether to enable SDK gripper position limit, which will limit both feedback and control messages
    #   logger_level(LogLevel -> default LogLevel.WARNING): Set the log level
    #         The following parameters are optional: 
    #               LogLevel.DEBUG
    #               LogLevel.INFO
    #               LogLevel.WARNING
    #               LogLevel.ERROR
    #               LogLevel.CRITICAL
    #               LogLevel.SILENT
    #   log_to_file(bool -> default False): Whether to enable the log writing function, True to enable, default to disable
    #   log_file_path(str -> default False): Set the path to write the log file, the default is the log folder under the sdk path
    piper = C_PiperInterface(can_name="can0",
                                judge_flag=False,
                                can_auto_init=True,
                                dh_is_offset=1,
                                start_sdk_joint_limit=False,
                                start_sdk_gripper_limit=False,
                                logger_level=LogLevel.WARNING,
                                log_to_file=False,
                                log_file_path=None)
    # Enable can send and receive threads
    piper.ConnectPort()
    # Loop and print messages. Note that the first frame of all messages is the default value. For example, the message content of the first frame of the joint angle message defaults to 0
    while True:
        print(piper.GetArmJointMsgs())
        time.sleep(0.05)# 20hz