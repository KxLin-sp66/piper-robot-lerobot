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

</div>

# LeRobot: State-of-the-art Machine Learning for Real-World Robotics

This repository is a modified version of LeRobot with support for **Piper Robot Arm** teleoperation and control.

## 📋 Requirements

- Python 3.10+
- PyTorch 2.2+
- Ubuntu (recommended for CAN bus support)

## 🚀 Installation

### 1. Install LeRobot

Follow the standard LeRobot installation process to configure the environment.

### 2. Install Piper SDK Dependencies

```bash
pip3 install python-can
pip3 install piper_sdk
sudo apt update && sudo apt install can-utils ethtool
```

### 3. Clone Piper SDK Repository

```bash
git clone https://github.com/agilexrobotics/piper_sdk.git
```

### 4. Setup CAN Interface

Find and enable your CAN module:

```bash
bash find_all_can_port.sh
bash can_activate.sh can0 1000000
```

## 🤖 Piper Robot Arm Setup

### Master-Slave Configuration

You can configure the arms using the commands below or use the Piper Control Software.

#### 1. Configure Follower Arm

```bash
python3 -c "from piper_sdk import C_PiperInterface; C_PiperInterface(can_name='can0', judge_flag=True).MasterSlaveConfig(0xFC, 0, 0, 0)"
```

#### 2. Configure Master Arm

```bash
python3 -c "from piper_sdk import C_PiperInterface; C_PiperInterface(can_name='can0', judge_flag=True).MasterSlaveConfig(0xFA, 0, 0, 0)"
```

#### 3. Power Sequence

1. Power on the **follower arm** first
2. Wait a few seconds
3. Power on the **master arm**
4. Wait for automatic synchronization (no additional programs needed)

## 🎯 Usage

### Teleoperation

Run the teleoperation system with the following command:

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

## 🔧 Key Modifications

This fork includes the following modifications to support Piper Robot Arm:

1. **New Piper Follower** - Added in `src/lerobot/robots/piper_follower/`
2. **New Piper Leader** - Added in `src/lerobot/teleoperators/piper_leader/`
3. **Updated Recording Script** - Modified `lerobot_record` in `scripts/`
4. **Updated Replay Script** - Modified `lerobot_replay` in `scripts/`

## 📚 Additional Resources

- [Original LeRobot Repository](https://github.com/huggingface/lerobot)
- [Piper SDK Repository](https://github.com/agilexrobotics/piper_sdk)
- [LeRobot Documentation](https://huggingface.co/docs/lerobot)

## 📄 License

This project inherits the Apache 2.0 license from the original LeRobot project.





