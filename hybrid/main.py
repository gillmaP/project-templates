"""
Hybrid 템플릿 - Accelerate + Hydra 결합
"""
import hydra
from omegaconf import DictConfig, OmegaConf
from accelerate import Accelerator
from accelerate.utils import DistributedDataParallelKwargs
import torch
import os
import random
import numpy as np

from train.trainer import Trainer


def set_seed(seed=42):
    """재현성을 위한 시드 고정"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


@hydra.main(config_path="configs", config_name="config", version_base=None)
def main(cfg: DictConfig):
    """
    Hydra + Accelerate 하이브리드 메인 함수
    
    - Hydra: 설정 관리 및 실험 추적
    - Accelerate: 분산 학습 자동화
    """
    # 시드 설정
    seed = cfg.experiment.get('seed', 42)
    set_seed(seed)
    
    # Hydra 출력 디렉토리
    output_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
    
    # Accelerate 초기화 (Hydra 설정 사용)
    accelerator = Accelerator(
        kwargs_handlers=[
            DistributedDataParallelKwargs(find_unused_parameters=True)
        ],
        mixed_precision=cfg.train.get('mixed_precision', 'fp16'),
        log_with="tensorboard",
        project_dir=cfg.experiment.get('log_dir', './logs')
    )
    
    if accelerator.is_main_process:
        print("=" * 50)
        print("Configuration:")
        print(OmegaConf.to_yaml(cfg))
        print("=" * 50)
        print(f"Output directory: {output_dir}")
        print(f"Number of processes: {accelerator.num_processes}")
    
    # Trainer 초기화 (Accelerate 전달)
    trainer = Trainer(
        cfg=cfg,
        accelerator=accelerator,
        output_dir=output_dir
    )
    
    # 모드에 따라 실행
    mode = cfg.get('mode', 'train')
    if mode == 'train':
        trainer.train()
    elif mode == 'inference':
        checkpoint = cfg.get('checkpoint', None)
        if checkpoint:
            trainer.load(checkpoint)
        trainer.inference()
    
    accelerator.end_training()

