import logging
import time

from lerobot.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError
from ..teleoperator import Teleoperator
from .config_piper_leader import PiperLeaderConfig
from piper_sdk import *
from typing import Any


logger = logging.getLogger(__name__)

class PiperLeader(Teleoperator):
    config_class = PiperLeaderConfig
    name = "piper_leader"

    def __init__(self, config: PiperLeaderConfig):
        super().__init__(config)
        self.config = config
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
    def action_features(self) -> dict[str, type]:
        return {f"joint_{i}.pos": float for i in range(1,8)}
    
    @property
    def feedback_features(self) -> dict[str, type]:
        return {}
    
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
    
    @property
    def is_connected(self) -> bool:
        return self.piper.get_connect_status()
    
    
    def connect(self,calibrate: bool = True) -> None:
        if self.config.use_follower is True and self.piper.get_connect_status:
            pass
        else:
            if self.is_connected:
                raise DeviceAlreadyConnectedError(f"{self} already connected")
            self.piper.ConnectPort()
            if not self.piper.get_connect_status():
                raise ValueError(f"Piper can not connect!")
        self.configure()
        logger.info(f"{self} connected")
    
    def get_state(self) -> dict[str, Any]:
        joint_status = self.piper.GetArmJointCtrl()
        gripper_status = self.piper.GetArmGripperCtrl()
        joint_state = joint_status.joint_ctrl
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
                "joint_7.pos": gripper_status.gripper_ctrl.grippers_angle,
            }
        )

        return obs_dict

    def get_action(self) -> dict[str, float]:
        start = time.perf_counter()
        action = self.get_state()
        # get_state() already returns keys with .pos suffix, so just convert values to float
        action = {key: float(val) for key, val in action.items()}
        dt_ms = (time.perf_counter() - start) * 1e3
        logger.debug(f"{self} read action: {dt_ms:.1f}ms")
        return action
    
    def send_feedback(self, feedback: dict[str, float]) -> None:
        # TODO(rcadene, aliberts): Implement force feedback
        raise NotImplementedError

    def disconnect(self) -> None:
        # When use_follower=True, the leader may not be fully connected, so we allow graceful disconnect
        if not self.config.use_follower and not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")
        # Only disconnect port if it's actually connected
        if self.piper.get_connect_status():
            self.piper.DisconnectPort()
        logger.info(f"{self} disconnected.")

    