# Hydra + DDP Template

A template with powerful configuration management using Hydra and manual PyTorch DDP management.

## 📋 Structure

```
project/
├── main.py                 # Uses Hydra decorator
├── configs/
│   ├── config.yaml        # Main configuration
│   ├── model/
│   │   └── cnn.yaml       # Model-specific configs
│   ├── data/
│   │   └── dataset.yaml   # Dataset configuration
│   └── train/
│       └── default.yaml   # Training configuration
├── train/
│   ├── trainer.py
│   └── datasets.py
├── models/
│   └── model.py
└── utils/
    └── train_util.py
```

## 🎯 Features

- **Hierarchical Configuration**: Modular configuration separation
- **Automatic Experiment Saving**: All experiment configs automatically saved
- **Hyperparameter Sweeps**: Automatic sweeps with multi-run
- **Type Safety**: Type checking with OmegaConf

## 🚀 Usage

### Basic Execution
```bash
python main.py
```

### Configuration Override
```bash
python main.py train.learning_rate=1e-5 model.embed_dim=512
```

### Hyperparameter Sweep
```bash
python main.py -m train.learning_rate=1e-4,1e-5,1e-6
```

### Multi GPU
```bash
torchrun --nproc_per_node=4 main.py
```

## 📝 Key Code Patterns

### Hydra Main Function
```python
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="configs", config_name="config", version_base=None)
def main(cfg: DictConfig):
    # cfg is a DictConfig object
    lr = cfg.train.learning_rate
    model = YourModel(**cfg.model)
```

### DDP Initialization
```python
import torch.distributed as dist

def setup_ddp(rank, world_size):
    dist.init_process_group(
        backend='nccl',
        init_method='env://',
        world_size=world_size,
        rank=rank
    )
    torch.cuda.set_device(rank)
```

### Experiment Output Directory
```python
# Hydra automatically creates outputs/date_time/ folder
output_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
```

## ⚙️ Configuration File Structure

### configs/config.yaml
```yaml
defaults:
  - model: cnn
  - data: dataset
  - train: default

experiment:
  name: my_experiment
  seed: 42
```

### configs/train/default.yaml
```yaml
batch_size: 64
learning_rate: 1.0e-4
steps: 2000
```

## ✅ Pros

- Powerful configuration management (hierarchical, modular)
- Automatic experiment tracking (all configs saved)
- Easy hyperparameter sweeps
- Type safety

## ❌ Cons

- Steep learning curve (need to learn Hydra)
- Manual DDP management required
- Increased code complexity
- Difficult debugging
