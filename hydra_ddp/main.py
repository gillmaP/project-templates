"""
Hydra + DDP 템플릿 - 메인 실행 파일
"""
import hydra
from omegaconf import DictConfig, OmegaConf
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
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


def setup_ddp(rank, world_size):
    """DDP 초기화"""
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    
    dist.init_process_group(
        backend='nccl',
        init_method='env://',
        world_size=world_size,
        rank=rank
    )
    torch.cuda.set_device(rank)


def cleanup_ddp():
    """DDP 정리"""
    dist.destroy_process_group()


@hydra.main(config_path="configs", config_name="config", version_base=None)
def main(cfg: DictConfig):
    """
    Hydra 메인 함수
    
    Hydra가 자동으로:
    - configs/ 폴더에서 설정 로드
    - outputs/날짜_시간/ 폴더에 실험 저장
    - .hydra/ 폴더에 사용된 설정 저장
    """
    # 시드 설정
    seed = cfg.get('experiment', {}).get('seed', 42)
    set_seed(seed)
    
    # DDP 설정 (멀티 GPU인 경우)
    if 'RANK' in os.environ:
        rank = int(os.environ['RANK'])
        world_size = int(os.environ['WORLD_SIZE'])
        local_rank = int(os.environ['LOCAL_RANK'])
        setup_ddp(rank, world_size)
        is_main_process = (rank == 0)
    else:
        rank = 0
        world_size = 1
        local_rank = 0
        is_main_process = True
    
    # Hydra 출력 디렉토리 (자동 생성됨)
    output_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
    
    if is_main_process:
        print("=" * 50)
        print("Configuration:")
        print(OmegaConf.to_yaml(cfg))
        print("=" * 50)
        print(f"Output directory: {output_dir}")
    
    try:
        # Trainer 초기화
        trainer = Trainer(
            cfg=cfg,
            rank=rank,
            world_size=world_size,
            local_rank=local_rank,
            is_main_process=is_main_process,
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
        
    finally:
        # DDP 정리
        if world_size > 1:
            cleanup_ddp()


if __name__ == "__main__":
    main()

