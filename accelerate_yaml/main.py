"""
Accelerate + YAML 템플릿 - 메인 실행 파일
"""
import yaml
import argparse
from train.trainer import Trainer

import os
import random
import numpy as np
import torch


def load_config(config_path=""):
    """YAML 설정 파일 로드"""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Training script")
    parser.add_argument("-m", "--mode", type=str, default="train", 
                       choices=["train", "inference"])
    parser.add_argument("-c", "--checkpoint", type=str, default=None,
                       help="Checkpoint path for inference")
    parser.add_argument("-d", "--config", type=str, default="./config/default.yaml",
                       help="Path to config YAML file")
    args = parser.parse_args()

    # 설정 로드
    config = load_config(args.config)
    set_seed(seed=config.get('experiment', {}).get('seed', 42))
    
    # Trainer 초기화
    if args.mode != 'train':
        assert args.checkpoint is not None, "Checkpoint required for inference"
        trainer = Trainer(config, mode='inference')
    else:
        trainer = Trainer(config, mode='train')
    
    # 체크포인트 로드 (있는 경우)
    if args.checkpoint:
        trainer.load(args.checkpoint)

    # 실행
    if args.mode == "train":
        trainer.train()
    elif args.mode == "inference":
        trainer.inference()
    else:
        exit()

