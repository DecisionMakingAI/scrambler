# Model Training Guide

<video width="640" height="360" controls>
  <source src="/assets/videos/demo.mp4" type="video/mp4">
  Your browser doesn't support the video tag.
</video>

## Overview

This guide explains how to **train**, **evaluate**, **visualize**, and **deploy** deep learning models for the Scrambler autonomous car platform.

The supervised learning pipeline uses **PyTorch Lightning** for robust training, **DonkeyCar** for data collection, and supports **ONNX → TensorRT** conversion for fast, optimized inference on the Jetson Nano.

**Important:** All training and data cleaning should be performed on the **host PC** to keep the Jetson Nano focused on driving and inference.

---

## Training Pipeline Structure

The training workflow is composed of interconnected modules:

```
train_pytorch.py (entry point)
└── torch_train.py (coordinates training)
    ├── torch_utils.py (model registry)
    │   └── ResNet18.py (model definition)
    └── torch_data.py (data loading)
```

### File Responsibilities

| File | Purpose |
|------|---------|
| `myconfig.py` | Defines hyperparameters and environment settings (batch size, epochs, learning rate, etc.) |
| `torch_data.py` | Loads and preprocesses Tub data into PyTorch datasets |
| `ResNet18.py` | Defines the ResNet18 CNN model used for steering/throttle prediction |
| `torch_utils.py` | Instantiates models by type and handles checkpoint loading |
| `torch_train.py` | Coordinates training using PyTorch Lightning |
| `train_pytorch.py` | Command-line entry point for running training |
| `runcar.py` | Executes real-time inference on the Jetson Nano (autopilot) |

---

## PyTorch File Structure Deep Dive

Understanding the `donkeycar/parts/pytorch/` folder structure is essential for extending the system:

### torch_train.py

- Wraps the training loop using PyTorch Lightning
- Sets up checkpoints, early stopping, and the trainer entry point
- Called by `train_pytorch.py` to execute training

### torch_utils.py

- Holds the **model registry** and helper functions
- Provides `register_pytorch_model()` and `get_model_by_type()` for model lookup by string name (e.g., "resnet18", "resnet18_temporal")
- Contains helpers to load checkpoints for inference and optional quantization utilities

### torch_data.py

- Defines `TorchTubDataset`, `TemporalTubDataset`, and `TorchTubDataModule`
- Handles loading tub records and building train/validation splits
- Automatically skips bad or missing images

### Model Implementations

- Individual models like `ResNet18` and `ResNet18Temporal` live in **separate files** in the same folder
- Each model is a `LightningModule` that defines:
  - Network architecture
  - Loss function
  - Optimizer configuration
  - `run()` method for inference in `runcar.py`

### Extending with New Models

To add new models to the system:

1. **Create a new `LightningModule` file** in `donkeycar/parts/pytorch/`
2. Define the network architecture, loss function, and optimizer
3. Implement the `run()` method for inference that accepts camera images
4. **Create a small factory function** that instantiates your model
5. **Register it** with `register_pytorch_model()` so both `train_pytorch.py` and `runcar.py` can request it by type name

Example registration:

```python
from donkeycar.parts.pytorch.torch_utils import register_pytorch_model
from donkeycar.parts.pytorch.my_new_model import MyNewModel

def create_my_model(cfg):
    return MyNewModel(
        learning_rate=cfg.PYTORCH_LEARNING_RATE,
        weight_decay=cfg.PYTORCH_WEIGHT_DECAY
    )

register_pytorch_model('my_model', create_my_model)
```

### Inference Notes

- Images are normalized in the same way during training and inference
- The `run()` method converts camera images to tensors
- Returns steering and throttle in range `[-1, 1]` for direct use in `runcar.py`

---

## Configuration (myconfig.py)

All hyperparameters and options are centralized in `myconfig.py`.

### Training Parameters

| Setting | Description |
|---------|-------------|
| `MAX_EPOCHS` | Maximum number of training epochs (e.g., 30) |
| `BATCH_SIZE` | Effective batch size in the data module (e.g., 64) |
| `PYTORCH_LEARNING_RATE` | Learning rate for Adam optimizer (e.g., 1e-4) |
| `PYTORCH_WEIGHT_DECAY` | Weight decay for regularization (e.g., 1e-5) |
| `DEFAULT_MODEL_TYPE` | Default model architecture (e.g., 'resnet18') |
| `PRINT_MODEL_SUMMARY` | Whether to print model architecture |

### Legacy Flags

**Note:** Older Keras/TensorFlow training flags in `myconfig.py` are **not used** by the current PyTorch trainer.

> **Tip:** Start with smaller epoch counts and lower learning rates when training on limited datasets, then scale once the model converges smoothly.

---

## Training the Model

### PyTorch Only

**Important:** This project disables TensorFlow training and uses **PyTorch only**. All training is performed using the `train_pytorch.py` script located in the driving directory.

### Training Commands

| Use Case | Command |
|----------|---------|
| **Single tub** | `python train_pytorch.py --model=models/mypilot.ckpt --tub=data/tub_1` |
| **Multiple tubs** | `python train_pytorch.py --model=models/mypilot.ckpt --tub=data/tub_1,data/tub_2` |
| **Temporal model (3 frames)** | `python train_pytorch.py --model=models/pilot_temporal.ckpt --temporal --num-frames=3` |
| **Explicit ResNet18** | `python train_pytorch.py --model=models/mypilot.ckpt --type=resnet18` |

### Supported Model Types

The PyTorch model registry currently includes:

- **resnet18:** Single frame steering + throttle regression
- **resnet18_temporal:** Multi-frame temporal model for sequential processing

### Behavioral Models Warning

**Behavioral model support is disabled in the current PyTorch stack.**

Setting `TRAIN_BEHAVIORS = True` will raise a runtime error in PyTorch utilities and the data loader.

If you need behavioral models in the future:
- Significant additional work is required
- Start from the official DonkeyCar behavioral model documentation: [DonkeyCar Behavioral Models](https://docs.donkeycar.com/guide/deep_learning/train_autopilot/)

---

## Inside the Training Script (torch_train.py)

The `torch_train.py` script handles model training, checkpointing, and diagnostics with the following flow:

### 1. Model Initialization

Uses `get_model_by_type()` to load the correct architecture. Resumes from checkpoint if one exists.

### 2. Data Loading

Loads DonkeyCar tub data via `TorchTubDataModule`, splitting into training/validation sets.

### 3. Training Configuration

Uses PyTorch Lightning's `Trainer` with automatic GPU detection.

### 4. Callbacks

- **ModelCheckpoint:** Saves the best model based on validation loss
- **EarlyStopping:** Stops training if validation loss stops improving

### 5. Logging (Optional)

Optionally logs metrics to TensorBoard:

```bash
tensorboard --logdir tb_logs
```

### 6. Diagnostics

After training, the script can save metrics to CSV and generate loss curves for performance tracking.

---

## Deploying the Model

### Option 1: PyTorch Checkpoint (Direct)

1. Transfer the `.ckpt` file to the Jetson:

```bash
scp models/mypilot.ckpt car1:~/mycar/models/
```

2. Configure `myconfig.py` on the Jetson:

```python
USE_PYTORCH = True
PYTORCH_MODEL = "models/mypilot.ckpt"
USE_TENSORRT = False
```

3. Run inference:

```bash
python runcar.py --ai
```

### Option 2: ONNX → TensorRT (Optimized)

For better performance on the Jetson Nano:

#### Step 1: Export to ONNX (on Host PC)

```bash
python trt_tools/export_to_onnx.py \
  --model models/mypilot.ckpt \
  --output models/mypilot.onnx
```

The `export_to_onnx.py` script:
- Takes a PyTorch `.ckpt` checkpoint
- Exports it to ONNX format for cross-platform compatibility

#### Step 2: Convert ONNX to TensorRT (on Jetson Nano)

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

The `convert_to_tensorrt.py` script:
- Converts the ONNX model to a `.trt` engine
- Optimizes specifically for the Jetson Nano GPU

**Jetson Nano Hardware Note:**
-  Supports **FP16** and **FP32** in TensorRT
-  **INT8** acceleration is **not supported**

#### Step 3: Configure and Run

Update `myconfig.py` on the Jetson:

```python
USE_TENSORRT = True
TENSORRT_MODEL_PATH = "models/mypilot.trt"
```

Then run:

```bash
python runcar.py --ai
```

> **Performance Note:** TensorRT models achieve up to **3× faster** inference on the Jetson Nano compared to PyTorch.

---

## Example Training Workflow

Here's a complete workflow from data collection to deployment:

### 1. Collect Data on Jetson

```bash
# SSH into Jetson
ssh car1

# Record training data
python runcar.py
# Drive manually, data saves to data/tub_1, data/tub_2, etc.
```

### 2. Transfer Data to Host PC

```bash
# On host PC
rsync -avz car1:~/mycar/data/ ./data/
```

### 3. Clean Data (Optional)

```bash
# Remove bad frames
python tubclean.py --tub data/tub_1 --delete 0-50,200-250
```

### 4. Train on Host PC

```bash
# Single tub
python train_pytorch.py --model=models/mypilot.ckpt --tub=data/tub_1

# Multiple tubs for better generalization
python train_pytorch.py --model=models/mypilot.ckpt --tub=data/tub_1,data/tub_2,data/tub_3
```

### 5. Deploy to Jetson

```bash
# Transfer model
scp models/mypilot.ckpt car1:~/mycar/models/

# Optional: Convert to TensorRT for speed
python trt_tools/export_to_onnx.py --model models/mypilot.ckpt --output models/mypilot.onnx
scp models/mypilot.onnx car1:~/mycar/models/

# On Jetson
ssh car1
python trt_tools/convert_to_tensorrt.py --onnx models/mypilot.onnx --output models/mypilot.trt --fp16
```

### 6. Test Inference

```bash
# On Jetson
python runcar.py --ai
# Use Start button to cycle through drive modes
```

---

## Troubleshooting

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| **CUDA not available** | Missing Jetson drivers | Reinstall JetPack with PyTorch support |
| **FileNotFoundError: tub** | Dataset path incorrect | Check `--tub` path matches your data location |
| **Model fails to load** | Checkpoint file missing or corrupted | Ensure `.ckpt` file exists and is complete |
| **Model overfits** | Small dataset or high learning rate | Collect more diverse data or reduce `PYTORCH_LEARNING_RATE` |
| **Training hangs** | Empty or corrupted tub folders | Delete empty tubs or run `tubclean.py` |
| **Low validation accuracy** | Insufficient training data | Collect more laps with varied lighting and positions |
| **TensorRT conversion fails** | ONNX export issue | Verify ONNX file is valid before converting |

---

## Best Practices

### Data Collection

- Record short, distinct sessions (one behavior per run)
- Avoid long continuous drives as they are harder to clean
- Collect data in various lighting conditions and track positions
- Keep clips balanced to avoid overfitting to one direction

### Training

- Start with smaller epoch counts (10-15) and increase if underfitting
- Use lower learning rates (1e-4 to 1e-5) for stability
- Monitor validation loss to detect overfitting early
- Save checkpoints frequently in case training is interrupted

### Deployment

- Test with PyTorch models first before converting to TensorRT
- Use FP16 TensorRT engines for best speed/accuracy balance
- Always validate models in controlled environments before racing

---

## Additional Resources

- [DonkeyCar Official Documentation](https://docs.donkeycar.com/)
- [PyTorch Lightning Documentation](https://lightning.ai/docs/pytorch/stable/)
- [TensorRT Documentation](https://docs.nvidia.com/deeplearning/tensorrt/)
- [DonkeyCar Behavioral Models Guide](https://docs.donkeycar.com/guide/deep_learning/train_autopilot/)