"""
Accelerate + YAML 템플릿 - Trainer 클래스
"""
import os
from pathlib import Path
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import ReduceLROnPlateau
from accelerate import Accelerator
from accelerate.utils import DistributedDataParallelKwargs
from tqdm.auto import tqdm

from .datasets import YourDataset
from models.model import YourModel
from utils.train_util import calculate_metrics


class Trainer:
    def __init__(
        self,
        cfg,
        mode='train',
        fp16=True,
        split_batches=True,
    ):
        """
        Args:
            cfg: 설정 딕셔너리 (YAML에서 로드)
            mode: 'train' or 'inference'
            fp16: Mixed precision 사용 여부
            split_batches: 배치를 프로세스 간 분할 여부
        """
        # Accelerator 초기화
        self.accelerator = Accelerator(
            kwargs_handlers=[
                DistributedDataParallelKwargs(find_unused_parameters=True)
            ],
            split_batches=split_batches,
            mixed_precision='fp16' if fp16 else 'no',
            log_with="tensorboard",
            project_dir=cfg.get('experiment', {}).get('log_dir', './logs')
        )
        
        self.cfg = cfg
        cfg_flattened = self._flatten_dict(cfg)
        self.accelerator.init_trackers(
            cfg.get('experiment', {}).get('run_name', 'default'),
            config=cfg_flattened
        )
        
        # 모델 초기화
        self.model = YourModel(**cfg.get('model', {}))
        if self.accelerator.is_main_process:
            print(f"Model initialized: {self.model.__class__.__name__}")
        
        # 옵티마이저 및 스케줄러
        self.opt = optim.Adam(
            self.model.parameters(),
            lr=cfg.get('train', {}).get('learning_rate', 1e-4)
        )
        self.scheduler = ReduceLROnPlateau(
            self.opt, mode='min', factor=0.8, patience=5, verbose=True
        )
        self.criterion = nn.CrossEntropyLoss()
        
        # 결과 저장 폴더
        self.results_folder = Path(
            os.path.join(
                cfg.get('experiment', {}).get('log_dir', './logs'),
                cfg.get('experiment', {}).get('run_name', 'default')
            )
        )
        self.results_folder.mkdir(existok=True, parents=True)
        
        # 학습 설정
        self.step = 0
        self.best_loss = float('inf')
        self.train_num_steps = cfg.get('train', {}).get('steps', 2000)
        self.gradient_accumulate_every = cfg.get('train', {}).get(
            'gradient_accumulation_steps', 1
        )
        self.save_checkpoint_every = cfg.get('train', {}).get(
            'save_checkpoint_every', 2
        )
        
        # 데이터셋 및 데이터로더 (학습 모드일 때만)
        if mode == 'train':
            train_dataset = YourDataset(**cfg.get('data', {}), split='train')
            val_dataset = YourDataset(**cfg.get('data', {}), split='val')
            
            train_dl = DataLoader(
                train_dataset,
                batch_size=cfg.get('train', {}).get('batch_size', 64),
                shuffle=True,
                num_workers=cfg.get('data', {}).get('num_workers', 4)
            )
            val_dl = DataLoader(
                val_dataset,
                batch_size=cfg.get('train', {}).get('valid_batch_size', 64),
                shuffle=False,
                num_workers=cfg.get('data', {}).get('num_workers', 4)
            )
            
            # Accelerator로 준비
            self.model, self.opt, train_dl, val_dl = self.accelerator.prepare(
                self.model, self.opt, train_dl, val_dl
            )
            self.train_dl = train_dl
            self.val_dl = val_dl
            self.train_iterator = iter(train_dl)
    
    @property
    def device(self):
        return self.accelerator.device
    
    def _flatten_dict(self, d, parent_key='', sep='/'):
        """중첩 딕셔너리를 평탄화 (TensorBoard 로깅용)"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, (int, float, str, bool)):
                items.append((new_key, v))
        return dict(items)
    
    def save(self, milestone):
        """체크포인트 저장"""
        if not self.accelerator.is_main_process:
            return
        
        data = {
            'step': self.step,
            'model': self.accelerator.get_state_dict(self.model),
            'opt': self.opt.state_dict(),
            'best_loss': self.best_loss
        }
        torch.save(data, str(self.results_folder / f'model-{milestone}.pt'))
        self.accelerator.print(f"Checkpoint saved: model-{milestone}.pt")
    
    def load(self, checkpoint_path):
        """체크포인트 로드"""
        checkpoint_path = Path(checkpoint_path)
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
        
        data = torch.load(checkpoint_path, map_location=self.device)
        model_state_dict = data['model']
        
        # DDP 모델인 경우 처리
        model = self.model
        if hasattr(model, 'module'):  # DDP로 감싸진 경우
            from collections import OrderedDict
            new_state_dict = OrderedDict()
            for key, value in model_state_dict.items():
                new_key = f"module.{key}" if not key.startswith("module.") else key
                new_state_dict[new_key] = value
            model_state_dict = new_state_dict
        
        model.load_state_dict(model_state_dict)
        self.step = data.get('step', 0)
        self.best_loss = data.get('best_loss', float('inf'))
        self.accelerator.print(f"Checkpoint loaded from {checkpoint_path}")
    
    def train(self):
        """학습 루프"""
        acc = self.accelerator
        model = self.model
        opt = self.opt
        grad_acc = self.gradient_accumulate_every
        
        loss_meter = 0.0
        seen_steps = 0
        pbar = tqdm(
            initial=self.step,
            total=self.train_num_steps,
            disable=not acc.is_main_process
        )
        
        while self.step < self.train_num_steps:
            tot_loss = 0.0
            
            # Gradient accumulation
            for _ in range(grad_acc):
                try:
                    batch = next(self.train_iterator)
                except StopIteration:
                    self.train_iterator = iter(self.train_dl)
                    batch = next(self.train_iterator)
                
                # Forward pass
                images = batch['image'].to(self.device)
                labels = batch['label'].to(self.device)
                
                outputs = model(images)
                loss = self.criterion(outputs, labels)
                
                loss_meter += loss.item()
                tot_loss += loss / grad_acc
                seen_steps += 1
            
            # Backward pass
            acc.backward(tot_loss)
            acc.clip_grad_norm_(model.parameters(), 1.0)
            acc.wait_for_everyone()
            opt.step()
            opt.zero_grad()
            self.step += 1
            
            # 로깅 및 평가
            if self.step % 100 == 0:  # 매 100 스텝마다
                avg_loss = loss_meter / seen_steps if seen_steps > 0 else 0
                if acc.is_main_process:
                    acc.log({
                        "Loss/train": avg_loss,
                        "lr": opt.param_groups[0]["lr"]
                    }, step=self.step)
                loss_meter = 0.0
                seen_steps = 0
            
            # 주기적 평가 및 저장
            if self.step % (self.save_checkpoint_every * 100) == 0:
                val_loss = self.evaluate()
                if val_loss < self.best_loss:
                    self.best_loss = val_loss
                    self.save("best_loss")
            
            pbar.set_description(f"Loss {loss_meter / seen_steps:.4f}" if seen_steps > 0 else "Training")
            pbar.update(1)
        
        acc.print("Training complete!")
    
    @torch.no_grad()
    def evaluate(self):
        """검증"""
        acc = self.accelerator
        model = self.model.eval()
        
        sum_loss = 0.0
        n_samples = 0
        
        for batch in self.val_dl:
            images = batch['image'].to(self.device)
            labels = batch['label'].to(self.device)
            
            outputs = model(images)
            loss = self.criterion(outputs, labels)
            
            sum_loss += loss.item() * len(labels)
            n_samples += len(labels)
        
        # DDP에서 모든 프로세스 값 집계
        sum_loss = acc.gather_for_metrics(
            torch.tensor(sum_loss, device=self.device)
        ).sum()
        n_samples = acc.gather_for_metrics(
            torch.tensor(n_samples, device=self.device)
        ).sum()
        
        avg_loss = (sum_loss / n_samples).item()
        
        if acc.is_main_process:
            self.scheduler.step(avg_loss)
            acc.log({"Loss/val": avg_loss}, step=self.step)
        
        model.train()
        return avg_loss
    
    @torch.no_grad()
    def inference(self):
        """추론"""
        # 추론 로직 구현
        pass

