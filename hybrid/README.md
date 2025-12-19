# Hybrid Template (Accelerate + Hydra)

A hybrid template combining Accelerate's automatic distributed training with Hydra's powerful configuration management.

## 📋 Structure

```
project/
├── main.py                 # Hydra + Accelerate
├── configs/
│   ├── config.yaml
│   ├── model/
│   ├── data/
│   └── train/
├── train/
│   └── trainer.py          # Uses Accelerate
├── models/
└── utils/
```

## 🎯 Features

- **Hydra**: Powerful configuration management, experiment tracking
- **Accelerate**: Automatic distributed training, code simplicity
- **Best of Both Worlds**: Combines advantages of both approaches

## 🚀 Usage

### Single GPU
```bash
python main.py
```

### Multi GPU
```bash
accelerate launch main.py
# or
torchrun --nproc_per_node=4 main.py
```

### Configuration Override
```bash
python main.py train.learning_rate=1e-5
```

## 📝 Key Code Patterns

### Hydra + Accelerate Combination
```python
from accelerate import Accelerator
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="configs", config_name="config")
def main(cfg: DictConfig):
    # Configuration management with Hydra
    accelerator = Accelerator(
        mixed_precision=cfg.train.mixed_precision,
        log_with="tensorboard",
        project_dir=cfg.experiment.log_dir
    )
    # Automatic distributed training with Accelerate
    model, opt = accelerator.prepare(model, optimizer)
```

## ✅ Pros

- Hydra's configuration management + Accelerate's automation
- Experiment tracking + code simplicity
- Hyperparameter sweeps + automatic multi-GPU support

## 📊 Comparison

| Feature | Accelerate Only | Hydra Only | Hybrid |
|---------|----------------|------------|--------|
| Config Management | Basic | Powerful | Powerful |
| Distributed Training | Automatic | Manual | Automatic |
| Experiment Tracking | Manual | Automatic | Automatic |
| Code Simplicity | High | Medium | High |
