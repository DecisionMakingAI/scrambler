# How to Run or Duplicate the Scrambler Project

This guide outlines every major step needed to reproduce the Scrambler DonkeyCar Capstone setup from fresh Jetson Nano installation to model deployment.

---

## Quick Start

This guide assumes you're using the current Scrambler system setup with:
- Jetson Nano (4GB) running Ubuntu 18.04
- Host PC for training and data management
- Custom PyTorch-based training pipeline
- Optional TensorRT deployment for optimized inference

---

## 1. Hardware Setup

**Required components:**
- 2× Jetson Nano (4 GB)
- CSI Pi Cameras
- Logitech F710 controllers
- 64 GB microSD cards
- RC chassis with ESC and servo
- Power banks

**Setup instructions:**
- Connect the CSI camera securely with the ribbon cable oriented correctly (contacts facing down toward the board)
- Test motor and servo wiring before power-on to avoid startup errors from reversed ESC or servo pins

---

## 2. Host PC Setup

### Installing DonkeyCar

Install DonkeyCar on your host PC following the official installation guide:
[DonkeyCar Installation Guide](https://docs.donkeycar.com/guide/install_software/#step-1-install-software-on-host-pc)

**Important:** Use the **developer installation** method since this project modifies DonkeyCar source code.

```bash
git clone https://github.com/autorope/donkeycar
cd donkeycar
pip install -e .[dev]
```

### Host PC vs Jetson Nano Responsibilities

The Scrambler project splits responsibilities between the host PC and Jetson Nano:

- **Host PC:** Training models, data cleaning, visual inspection of tubs, model conversion
- **Jetson Nano:** Real-time driving, inference, data recording

This separation keeps the Jetson focused on performance-critical tasks and leverages the host PC's superior computational resources for training.

---

## 3. Software Installation on Jetson Nano

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pip python3-venv git

git clone https://github.com/autorope/donkeycar
cd donkeycar

python3 -m venv ~/venvs/dk
source ~/venvs/dk/bin/activate

pip install -e .
pip install tensorflow==2.9.1 opencv-python
```

> **Note:** DonkeyCar version 4.2.1 and OpenCV were confirmed stable on both Nanos.

---

## 4. SSH and VSCode Setup

### Finding Your Jetson IP Address

```bash
hostname -I
# or
ifconfig wlan0
```

### Connecting via SSH

```bash
# Car 1
ssh car1@10.x.x.x
# Password: donkey

# Car 2
ssh car2@10.x.x.x
# Password: 123
```

### SSH Config (Optional)

Create an entry in `~/.ssh/config`:

```
Host car1
    HostName 10.x.x.x
    User car1

Host car2
    HostName 10.x.x.x
    User car2
```

Then connect with: `ssh car1` or `ssh car2`

### VSCode Remote SSH

For development on the Jetson Nano:

- The Jetson runs **Ubuntu 18.04**
- Use **VSCode version 1.85** for remote SSH compatibility with this system
- Later VSCode versions may not support Ubuntu 18.04

---

## 5. How to Run the Car

### Important: Custom runcar.py

**This project uses a custom `runcar.py` instead of the standard `manage.py`.**

The `runcar.py` script handles:
- Camera initialization
- Joystick controller setup
- Model loading (PyTorch or TensorRT)
- Main drive loop

### Basic Commands

```bash
# Manual driving with recording enabled
python runcar.py

# AI mode with recording disabled
python runcar.py --ai
```

### Drive Modes

When AI mode is enabled (`--ai` flag), the car supports three modes that you can cycle through using the **Start button** on the Logitech gamepad:

1. **user mode:** Joystick controls angle and throttle, records data, no model inference
2. **local_angle mode:** Model predicts steering angle, joystick controls throttle
3. **local mode:** Full autopilot (model predicts both angle and throttle), optional throttle multiplier from config

### Configuration Notes

- **Custom config:** This project uses `myconfig.py` instead of the default `config.py`
- **Camera setup:** CSI camera configuration is in `donkeycar/parts/camera.py`
  - Changes to resolution or image flip must be made in that file
  - Recommended: 240×240 at 30 FPS for stable performance

---

## 6. Data Recording and Cleaning

### Recording Data

When you run `python runcar.py` in manual mode, each recording session creates a new `tub_x` folder under the `data/` directory.

```
data/
├── tub_1/
├── tub_2/
└── tub_3/
```

### Data Cleaning Options

#### DonkeyCar UI (Soft Delete)

Recent DonkeyCar versions removed the `tubclean` command-line function. Instead, DonkeyCar uses **soft deletion** in the Donkey UI:

- Deleting records in Donkey UI marks them as deleted but **does not remove image files from disk**
- **Note:** Donkey UI is not fully installed on the Jetson Nano at this time
- **Recommendation:** Install Donkey UI on your host PC for visual inspection of tubs

#### Custom tubclean.py Script (Hard Delete)

This project includes a `tubclean.py` helper script for hard deletion:

**Features:**
- Delete image files and records by index range, single index, or entire tub
- Removes files from disk permanently (unlike Donkey UI soft delete)

**Example usage:**

```bash
# Delete specific frame ranges from tub_1
python tubclean.py --tub data/tub_1 --delete 0-100,401-500
```

**Best practices:**
- Record short, distinct sessions (one behavior per run)
- Avoid long continuous drives as they are harder to clean

---

## 7. Important myconfig.py Settings

### Model and Inference

| Setting | Description |
|---------|-------------|
| `USE_PYTORCH = True` | Must stay true so `runcar.py` loads PyTorch or TensorRT pilots |
| `PYTORCH_MODEL` | Points to the default `.ckpt` model name under `MODELS_PATH` |
| `USE_TENSORRT` | Controls whether `runcar.py` calls the TensorRT pilot loader or PyTorch loader |
| `TENSORRT_MODEL_PATH` | Path to the `.trt` engine on the Jetson |
| `USE_TEMPORAL_MODEL` | Enables frame buffering for temporal models |
| `TEMPORAL_NUM_FRAMES` | Number of frames to buffer (e.g., 3) |

### Joystick

| Setting | Description |
|---------|-------------|
| `JOYSTICK_MAX_THROTTLE = 0.3` | Recommended value (default is 0.5) |

### Legacy Flags

**Note:** Older Keras/TensorFlow training flags in `myconfig.py` are **not used** by the current PyTorch trainer.

---

## 8. Deploying Models to Jetson

### Transfer Model from Host PC

After training on your host PC (see Training.md), transfer the model:

```bash
scp models/mypilot.ckpt car1:~/mycar/models/
```

### Configure Model Path

Edit `myconfig.py` on the Jetson:

```python
PYTORCH_MODEL = "models/mypilot.ckpt"
USE_PYTORCH = True
USE_TENSORRT = False  # Set to True if using TensorRT
```

### Run Inference Mode

```bash
python runcar.py --ai
```

---

## 9. TensorRT Deployment (Optional)

TensorRT provides significant inference speedup on the Jetson Nano (up to 3× faster).

### Jetson Nano Hardware Note

The Jetson Nano supports:
- ✅ **FP16** (half precision)
- ✅ **FP32** (full precision)
- ❌ **INT8** acceleration is **not supported**

### Step 1: Export to ONNX (on Host PC)

```bash
python trt_tools/export_to_onnx.py \
  --model models/mypilot.ckpt \
  --output models/mypilot.onnx
```

### Step 2: Convert ONNX to TensorRT (on Jetson Nano)

Transfer the ONNX file to the Jetson, then:

```bash
# FP16 engine (recommended for speed)
python trt_tools/convert_to_tensorrt.py \
  --onnx models/mypilot.onnx \
  --output models/mypilot.trt \
  --fp16

# FP32 engine (higher precision)
python trt_tools/convert_to_tensorrt.py \
  --onnx models/mypilot.onnx \
  --output models/mypilot.trt \
  --no-fp16
```

### Step 3: Configure and Run

Update `myconfig.py`:

```python
USE_TENSORRT = True
TENSORRT_MODEL_PATH = "models/mypilot.trt"
```

Then run:

```bash
python runcar.py --ai
```

### How TensorRT Integration Works

When `USE_TENSORRT = True`:
1. `runcar.py` checks the config setting
2. Calls `load_tensorrt_pilot(cfg)` instead of the PyTorch loader
3. Constructs a `TensorRTPilot` instance
4. The drive loop calls `pilot.run()` in the same way as the PyTorch pilot

This design keeps the interface consistent regardless of backend.

---

## 10. Common Issues and Solutions

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| **Camera not found** | Incorrect sensor configuration | Set `sensor_id=0` and `sensor_mode=2` in `donkeycar/parts/camera.py` |
| **Wi-Fi unstable** | Dynamic IP assignment | Set a static IP or reconnect after each boot |
| **cv2 import errors** | OpenCV library not linked | `ln -sf /usr/lib/python3.6/dist-packages/cv2.*.so ~/venvs/dk/lib/python3.6/site-packages/` |
| **Low FPS** | Resolution too high | Use 240×240 at 30 FPS |
| **Throttle sensitivity** | Joystick miscalibration | Calibrate F710 triggers and verify mapping |
| **Jetson overheating** | High GPU load during long sessions | Add USB fan or limit GPU frequency to 921MHz |

---

## 11. Behavior Labeling (Optional)

For advanced behavior-based training:

1. Map joystick buttons (A, B, Y) to behavior states
2. Record 2–3 short clips per behavior (turning, braking, straight)
3. Keep clips balanced to avoid overfitting one direction

---

## 12. Acknowledgments

Compiled by **Abe Eldo**, **Kendall Foy**, and **Yu Wang** for the Scrambler Capstone Project.

---

## Additional Resources

- [DonkeyCar Official Documentation](https://docs.donkeycar.com/)
- [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)