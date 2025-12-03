import logging
import time
from lerobot.robots import Robot, RobotConfig
from lerobot.cameras.utils import make_cameras_from_configs
from functools import cached_property
from typing import Any
from .config_piper_follower import PiperFollowerConfig
from piper_sdk import *
from lerobot.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError
from ..utils import ensure_safe_goal_position


logger = logging.getLogger(__name__)

class PiperFollower(Robot):

    config_class = PiperFollowerConfig
    name = "piper_follower"

    def __init__(self, config: PiperFollowerConfig):
        super().__init__(config)
        self.config = config
        self.cameras = make_cameras_from_configs(config.cameras)
        self.piper = C_PiperInterface(can_name=config.can_name,
                                judge_flag=False,
                                can_auto_init=True,
                                dh_is_offset=1,
                                start_sdk_joint_limit=False,
                                start_sdk_gripper_limit=False,
                                logger_level=LogLevel.WARNING,
                                log_to_file=False,
                                log_file_path=None)
        



    @property
    def _motors_ft(self) -> dict[str, type]:
        return {f"joint_{i}.pos": float for i in range(1,8)}
    
    @property
    def _cameras_ft(self) -> dict[str, tuple]:
        return {cam:(self.cameras[cam].height, self.cameras[cam].width, 3)for cam in self.cameras}
    
    @cached_property
    def observation_features(self) -> dict[str, type | tuple]:
        return {**self._motors_ft, **self._cameras_ft}
    
    @cached_property
    def action_features(self) -> dict[str, type]:
        return self._motors_ft
    
    @property
    def is_connected(self) -> bool:
        return self.piper.get_connect_status() and all(cam.is_connected for cam in self.cameras.values())
    
    @property
    def is_calibrated(self) -> bool:
        return True
        # This function is only for decorative documentation purposes
    
    def calibrate(self) -> None:
        pass
        # You should perform the calibration on the host computer.

    def configure(self) -> None:
        pass
        # No need do this in piper robots, this function is only for decorative documentation purposes
    
    def connect(self,calibrate: bool = True) -> None:
        if self.is_connected:
            raise DeviceAlreadyConnectedError(f"{self} already connected")
        self.piper.ConnectPort()
        if not self.config.use_leader:
            self.piper.MotionCtrl_2(0x01, 0x01, 100, 0x00)
            self.piper.EnableArm()
            print("Connected and enabled Piper follower arm.")
        if not self.piper.get_connect_status():
            raise ValueError(f"Piper can not connect!")
        for cam in self.cameras.values():
            cam.connect()
        self.configure()
        logger.info(f"{self} connected")

    def get_state(self) -> dict[str, Any]:
        joint_status = self.piper.GetArmJointMsgs()
        gripper_status = self.piper.GetArmGripperMsgs()
        joint_state = joint_status.joint_state
        obs_dict = {
            "joint_1.pos": joint_state.joint_1,
            "joint_2.pos": joint_state.joint_2,
            "joint_3.pos": joint_state.joint_3,
            "joint_4.pos": joint_state.joint_4,
            "joint_5.pos": joint_state.joint_5,
            "joint_6.pos": joint_state.joint_6,
        }
        obs_dict.update(
            {
                "joint_7.pos": gripper_status.gripper_state.grippers_angle,
            }
        )

        return obs_dict

    def get_observation(self) -> dict[str, Any]:
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")
        start = time.perf_counter()
        obs_dict = self.get_state()
        for cam_key, cam in self.cameras.items():
            start = time.perf_counter()
            obs_dict[cam_key] = cam.async_read()
            dt_ms = (time.perf_counter() - start) * 1e3
            logger.debug(f"{self} read {cam_key}: {dt_ms:.1f}ms")
        return obs_dict

            
    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        if self.config.use_leader:
            return self.get_state()
        else:
            if not self.is_connected:
                raise DeviceNotConnectedError(f"{self} is not connected.")
            goal_pos = {key.removesuffix(".pos"): val for key, val in action.items() if key.endswith(".pos")}     
            print(goal_pos)   
            if self.config.max_relative_target is not None:
                ValueError("Now we do not have this function!")
            # 预先转为整数
            joints = [int(round(goal_pos[f'joint_{i}'])) for i in range(1, 7)]
            gripper_pos = int(round(goal_pos['joint_7']))  # 如果 gripper 也要求整数
            self.piper.MotionCtrl_2(0x01, 0x01, 100, 0x00)
            self.piper.JointCtrl(*joints)
            self.piper.GripperCtrl(gripper_pos, 1000, 0x01, 0)
            return {0}

            
    def disconnect(self):
        # When use_leader=True, the follower may not be fully connected, so we allow graceful disconnect
        if not self.config.use_leader and not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")
        if not self.config.use_leader:
            end_1=2165
            end_2=-298
            end_3=1482
            end_4=1870
            end_5=18963
            end_6=2286
            self.piper.MotionCtrl_2(0x01, 0x01, 20, 0x00)
            self.piper.JointCtrl(end_1,end_2,end_3,end_4,end_5,end_6)
            time.sleep(10.0)
            self.piper.DisableArm()
        # Only disconnect port if it's actually connected
        if self.piper.get_connect_status():
            self.piper.DisconnectPort()
        for cam in self.cameras.values():
            if cam.is_connected:
                cam.disconnect()
        logger.info(f"{self} disconnected")
    






