from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig, make_cameras_from_configs
from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots import Robot, RobotConfig
from lerobot.cameras.configs import ColorMode, Cv2Rotation


@RobotConfig.register_subclass("piper_follower")
@dataclass
class PiperFollowerConfig(RobotConfig):
    can_name: str
    use_leader: bool = True
    max_relative_target: float = None
    cameras: dict[str, CameraConfig] = field(
        default_factory=lambda:{
            "base_camera":OpenCVCameraConfig(
                index_or_path=2,
                fps=30,
                width=640,
                height=480,
                color_mode=ColorMode.RGB
            ),
            "wrist_camera": OpenCVCameraConfig(
                index_or_path=0,
                fps=30,
                width=640,
                height=480,
                color_mode=ColorMode.RGB
            ),
        }
    )
    disable_torque_on_disconnect: bool = True

    # `max_relative_target` limits the magnitude of the relative positional target vector for safety purposes.
    # Set this to a positive scalar to have the same value for all motors, or a dictionary that maps motor
    # names to the max_relative_target value for that motor.
    max_relative_target: float | dict[str, float] | None = None
    # Set to `True` for backward compatibility with previous policies/dataset
    use_degrees: bool = False