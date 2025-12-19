# Hybrid 템플릿 (Accelerate + Hydra)

Accelerate의 분산 학습 자동화와 Hydra의 강력한 설정 관리를 결합한 하이브리드 템플릿입니다.

## 📋 구조

```
project/
├── main.py                 # Hydra + Accelerate
├── configs/
│   ├── config.yaml
│   ├── model/
│   ├── data/
│   └── train/
├── train/
│   └── trainer.py          # Accelerate 사용
├── models/
└── utils/
```

## 🎯 특징

- **Hydra**: 강력한 설정 관리, 실험 추적
- **Accelerate**: 분산 학습 자동화, 코드 단순성
- **최고의 조합**: 두 방식의 장점 결합

## 🚀 실행 방법

### 단일 GPU
```bash
python main.py
```

### 멀티 GPU
```bash
accelerate launch main.py
# 또는
torchrun --nproc_per_node=4 main.py
```

### 설정 오버라이드
```bash
python main.py train.learning_rate=1e-5
```

## 📝 주요 코드 패턴

### Hydra + Accelerate 결합
```python
from accelerate import Accelerator
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="configs", config_name="config")
def main(cfg: DictConfig):
    # Hydra로 설정 관리
    accelerator = Accelerator(
        mixed_precision=cfg.train.mixed_precision,
        log_with="tensorboard",
        project_dir=cfg.experiment.log_dir
    )
    # Accelerate로 분산 학습 자동화
    model, opt = accelerator.prepare(model, optimizer)
```

## ✅ 장점

- Hydra의 설정 관리 + Accelerate의 자동화
- 실험 추적 + 코드 단순성
- 하이퍼파라미터 스윕 + 멀티 GPU 자동 지원

## 📊 비교

| 기능 | Accelerate만 | Hydra만 | Hybrid |
|-----|------------|---------|--------|
| 설정 관리 | 기본 | 강력 | 강력 |
| 분산 학습 | 자동 | 수동 | 자동 |
| 실험 추적 | 수동 | 자동 | 자동 |
| 코드 단순성 | 높음 | 중간 | 높음 |

