# Template Usage Guide

## 🎯 When to Use Which Template?

### 1. Accelerate + YAML (`accelerate_yaml/`)

**Use Cases:**
- ✅ Fast prototyping needed
- ✅ Simple experiment configurations
- ✅ Personal projects or small teams
- ✅ Code simplicity prioritized

**Example:**
```bash
# Copy template
cp -r project_templates/accelerate_yaml my_new_project
cd my_new_project

# Rename files and variables
# - YourModel → MyModel
# - YourDataset → MyDataset
# - Edit config/default.yaml

# Run
python main.py --mode train
```

### 2. Hydra + DDP (`hydra_ddp/`)

**Use Cases:**
- ✅ Large-scale hyperparameter sweeps needed
- ✅ Experiment reproducibility critical
- ✅ Paper writing and experiment management
- ✅ Team collaboration and experiment sharing

**Example:**
```bash
# Copy template
cp -r project_templates/hydra_ddp my_new_project
cd my_new_project

# Check and modify configs/ folder structure
# Run
python main.py train.learning_rate=1e-5

# Hyperparameter sweep
python main.py -m train.learning_rate=1e-4,1e-5,1e-6
```

### 3. Hybrid (`hybrid/`)

**Use Cases:**
- ✅ Config management important while maintaining code simplicity
- ✅ Experiment tracking + automatic distributed training
- ✅ Production-level projects

**Example:**
```bash
# Copy template
cp -r project_templates/hybrid my_new_project
cd my_new_project

# Run
accelerate launch main.py train.learning_rate=1e-5
```

## 📝 Template Customization Checklist

When starting a new project:

- [ ] Rename folders/files according to project name
- [ ] Change `YourModel` → actual model name
- [ ] Change `YourDataset` → actual dataset name
- [ ] Modify `config/default.yaml` or `configs/` settings
- [ ] Update `models/model.py` to match your architecture
- [ ] Update `train/datasets.py` to match your dataset
- [ ] Update README.md

## 🔄 Template Migration

### Accelerate → Hydra

1. Add `@hydra.main` decorator to `main.py`
2. Change `config/` → `configs/` structure
3. Switch to `DictConfig` usage
4. Add DDP initialization code

### Hydra → Hybrid

1. Add `Accelerator` to `main.py`
2. Remove DDP initialization code (handled by Accelerate)
3. Use `accelerator.prepare()` in `trainer.py`

## 💡 Tips

1. **Template Location**: Templates are stored in `/jhbak/project_templates/`
2. **Version Control**: It's good to manage templates with Git
3. **Sharing**: Include README when sharing templates with team members
4. **Updates**: Reflect improvements back to templates as you use them
