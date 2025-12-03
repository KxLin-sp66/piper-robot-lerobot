<p align="center">
  <img alt="LeRobot, Hugging Face Robotics Library" src="https://raw.githubusercontent.com/huggingface/lerobot/main/media/lerobot-logo-thumbnail.png" width="100%">
  <br/>
  <br/>
</p>

<div align="center">

[![Tests](https://github.com/huggingface/lerobot/actions/workflows/nightly.yml/badge.svg?branch=main)](https://github.com/huggingface/lerobot/actions/workflows/nightly.yml?query=branch%3Amain)
[![Python versions](https://img.shields.io/pypi/pyversions/lerobot)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/huggingface/lerobot/blob/main/LICENSE)
[![Status](https://img.shields.io/pypi/status/lerobot)](https://pypi.org/project/lerobot/)
[![Version](https://img.shields.io/pypi/v/lerobot)](https://pypi.org/project/lerobot/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1-ff69b4.svg)](https://github.com/huggingface/lerobot/blob/main/CODE_OF_CONDUCT.md)


<!-- [![Coverage](https://codecov.io/gh/huggingface/lerobot/branch/main/graph/badge.svg?token=TODO)](https://codecov.io/gh/huggingface/lerobot) -->



## Installation

LeRobot works with Python 3.10+ and PyTorch 2.2+.First we need to get environment setup.
# LeRobot: State-of-the-art Machine Learning for Real-World Robotics


## Installation

LeRobot works with Python 3.10+ and PyTorch 2.2+. First, set up the environment:

### Install LeRobot
Configure the environment using lerobot
### Install Piper SDK Dependencies
```bash
pip3 install python-can
pip3 install piper_sdk
sudo apt update && sudo apt install can-utils ethtool
```

### Clone Piper SDK Repository
```bash
git clone https://github.com/agilexrobotics/piper_sdk.git
```
### Find and enable a single CAN module
```bash
bash find_all_can_port.sh
bash can_activate.sh can0 1000000
```
## Piper Robot Arm Setup
### Master-Slave Configuration
Runing this，or use the Piper Control Software
1. **Configure Follower Arm**
   ```bash
   python3 -c "from piper_sdk import C_PiperInterface; C_PiperInterface(can_name='can0', judge_flag=True).MasterSlaveConfig(0xFC, 0, 0, 0)"
   ```

2. **Configure Master Arm**
   ```bash
   python3 -c "from piper_sdk import C_PiperInterface; C_PiperInterface(can_name='can0', judge_flag=True).MasterSlaveConfig(0xFA, 0, 0, 0)"
   ```

3. **Power Sequence**
   - Power on follower arm first
   - Wait a few seconds, then power on master arm
   - Wait for synchronization (no additional programs needed)

## Key Modifications
1.New piper follower in Robots  
2.New piper leader in teleoperators  
3.lerobot_record in scripts  
4.lerobot_replay in scripts  

## Teleoperators
```bash
lerobot-teleoperate \
    --robot.type=piper_follower \
    --robot.can_name="can0" \
    --robot.use_leader=true \
    --teleop.type=piper_leader \
    --teleop.can_name="can0" \
    --teleop.use_follower=true \
    --display=true
```





