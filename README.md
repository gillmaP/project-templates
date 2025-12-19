# Project Templates Repository

A collection of deep learning project structure templates for rapid prototyping and production use.

## 📁 Available Templates

### 1. `accelerate_yaml/` - Accelerate + YAML Approach
- **Features**: Simple and fast prototyping
- **Pros**: Simple code, automatic multi-GPU support, easy debugging
- **Cons**: Basic configuration management, manual experiment tracking
- **Use Cases**: Initial experiments, prototypes, small-scale projects

### 2. `hydra_ddp/` - Hydra + DDP Approach
- **Features**: Powerful configuration management and experiment tracking
- **Pros**: Hierarchical configs, automatic experiment saving, hyperparameter sweeps
- **Cons**: Steeper learning curve, manual DDP management required
- **Use Cases**: Large-scale experiments, paper writing, team collaboration

### 3. `hybrid/` - Accelerate + Hydra Hybrid
- **Features**: Best of both worlds
- **Pros**: Hydra config management + Accelerate automatic distributed training
- **Use Cases**: When experiment management is important while maintaining code simplicity

## 🚀 Quick Start

1. Copy the desired template folder to your new project
2. Rename files/variables according to your project name
3. Customize model architecture and dataset to fit your needs

## 📝 Template Structure

Each template folder includes:
- `main.py`: Main execution file
- `train/trainer.py`: Trainer class
- `config/` or `configs/`: Configuration files
- `models/`: Model definitions
- `train/datasets.py`: Dataset classes
- `utils/`: Utility functions
- `README.md`: Template-specific detailed documentation

## 💡 Template Selection Guide

| Project Characteristics | Recommended Template |
|------------------------|---------------------|
| Fast prototyping | `accelerate_yaml` |
| Simple experiments | `accelerate_yaml` |
| Large-scale hyperparameter sweeps | `hydra_ddp` |
| Reproducibility critical | `hydra_ddp` |
| Config management + code simplicity | `hybrid` |

## 📚 Resources

- [Accelerate Documentation](https://huggingface.co/docs/accelerate/)
- [Hydra Documentation](https://hydra.cc/)
- [PyTorch DDP Tutorial](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
