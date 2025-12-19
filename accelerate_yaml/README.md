# Accelerate + YAML Template

A simple project structure using HuggingFace Accelerate and YAML configuration files.

## 📋 Structure

```
project/
├── main.py                 # Main execution file
├── config/
│   └── default.yaml        # YAML configuration file
├── train/
│   ├── trainer.py          # Trainer class
│   └── datasets.py         # Dataset definitions
├── models/
│   ├── __init__.py
│   └── model.py            # Model architecture
└── utils/
    └── train_util.py       # Utility functions
```

## 🎯 Features

- **Simplicity**: Start with minimal code
- **Automation**: Accelerate handles DDP and Mixed Precision automatically
- **Flexibility**: Easy switching between single/multi GPU

## 🚀 Usage

### Single GPU
```bash
python main.py --mode train --config config/default.yaml
```

### Multi GPU (Automatic)
```bash
accelerate launch main.py --mode train
# or
torchrun --nproc_per_node=4 main.py --mode train
```

## 📝 Key Code Patterns

### Trainer Initialization
```python
from accelerate import Accelerator

accelerator = Accelerator(
    mixed_precision='fp16',
    log_with="tensorboard",
    project_dir=cfg['experiment']['log_dir']
)
model, optimizer = accelerator.prepare(model, optimizer)
```

### Configuration Loading
```python
import yaml

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
```

### Main Process Check
```python
if accelerator.is_main_process:
    # Logging, saving, etc. - only run on main process
    accelerator.log({"loss": loss}, step=step)
```

## ⚙️ Configuration File Example

```yaml
train:
  batch_size: 64
  learning_rate: 1.0e-4
  steps: 2000

model:
  name: "MyModel"

experiment:
  log_dir: "./logs"
  run_name: "experiment_1"
```

## ✅ Pros

- Simple and easy to understand code
- Accelerate automatically handles distributed training
- Easy debugging (same code works on single GPU)
- Fast prototyping

## ❌ Cons

- Basic configuration management (manual)
- Difficult experiment tracking
- Inconvenient hyperparameter sweeps
