# Accelerate + YAML 템플릿

HuggingFace Accelerate와 YAML 설정 파일을 사용하는 단순한 프로젝트 구조입니다.

## 📋 구조

```
project/
├── main.py                 # 메인 실행 파일
├── config/
│   └── default.yaml        # YAML 설정 파일
├── train/
│   ├── trainer.py          # Trainer 클래스
│   └── datasets.py         # 데이터셋 정의
├── models/
│   ├── __init__.py
│   └── model.py            # 모델 아키텍처
└── utils/
    └── train_util.py       # 유틸리티 함수
```

## 🎯 특징

- **단순성**: 최소한의 코드로 시작
- **자동화**: Accelerate가 DDP, Mixed Precision 자동 처리
- **유연성**: 단일/멀티 GPU 전환 쉬움

## 🚀 실행 방법

### 단일 GPU
```bash
python main.py --mode train --config config/default.yaml
```

### 멀티 GPU (자동)
```bash
accelerate launch main.py --mode train
# 또는
torchrun --nproc_per_node=4 main.py --mode train
```

## 📝 주요 코드 패턴

### Trainer 초기화
```python
from accelerate import Accelerator

accelerator = Accelerator(
    mixed_precision='fp16',
    log_with="tensorboard",
    project_dir=cfg['experiment']['log_dir']
)
model, optimizer = accelerator.prepare(model, optimizer)
```

### 설정 로드
```python
import yaml

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
```

### 메인 프로세스 체크
```python
if accelerator.is_main_process:
    # 로깅, 저장 등 메인 프로세스에서만 실행
    accelerator.log({"loss": loss}, step=step)
```

## ⚙️ 설정 파일 예시

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

## ✅ 장점

- 코드가 단순하고 이해하기 쉬움
- Accelerate가 분산 학습 자동 처리
- 디버깅이 쉬움 (단일 GPU에서도 동일 코드)
- 빠른 프로토타이핑 가능

## ❌ 단점

- 설정 관리가 기본적 (수동)
- 실험 추적이 어려움
- 하이퍼파라미터 스윕이 불편

