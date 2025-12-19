# Hydra + DDP 템플릿

Hydra를 사용한 강력한 설정 관리와 PyTorch DDP를 직접 관리하는 템플릿입니다.

## 📋 구조

```
project/
├── main.py                 # Hydra 데코레이터 사용
├── configs/
│   ├── config.yaml        # 메인 설정
│   ├── model/
│   │   └── cnn.yaml       # 모델별 설정
│   ├── data/
│   │   └── dataset.yaml    # 데이터셋 설정
│   └── train/
│       └── default.yaml    # 학습 설정
├── train/
│   ├── trainer.py
│   └── datasets.py
├── models/
│   └── model.py
└── utils/
    └── train_util.py
```

## 🎯 특징

- **계층적 설정**: 모듈별 설정 분리
- **자동 실험 저장**: 모든 실험 설정 자동 저장
- **하이퍼파라미터 스윕**: Multi-run으로 자동 스윕
- **타입 안전성**: OmegaConf로 타입 체크

## 🚀 실행 방법

### 기본 실행
```bash
python main.py
```

### 설정 오버라이드
```bash
python main.py train.learning_rate=1e-5 model.embed_dim=512
```

### 하이퍼파라미터 스윕
```bash
python main.py -m train.learning_rate=1e-4,1e-5,1e-6
```

### 멀티 GPU
```bash
torchrun --nproc_per_node=4 main.py
```

## 📝 주요 코드 패턴

### Hydra 메인 함수
```python
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="configs", config_name="config", version_base=None)
def main(cfg: DictConfig):
    # cfg는 DictConfig 객체
    lr = cfg.train.learning_rate
    model = YourModel(**cfg.model)
```

### DDP 초기화
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

### 실험 저장 경로
```python
# Hydra가 자동으로 outputs/날짜_시간/ 폴더 생성
output_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
```

## ⚙️ 설정 파일 구조

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

## ✅ 장점

- 강력한 설정 관리 (계층적, 모듈화)
- 자동 실험 추적 (모든 설정 저장)
- 하이퍼파라미터 스윕 쉬움
- 타입 안전성

## ❌ 단점

- 학습 곡선 높음 (Hydra 학습 필요)
- DDP 직접 관리 필요
- 코드 복잡도 증가
- 디버깅 어려움

