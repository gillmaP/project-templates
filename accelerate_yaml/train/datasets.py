"""
데이터셋 정의
"""
from torch.utils.data import Dataset
import torch


class YourDataset(Dataset):
    """
    템플릿 데이터셋 - 실제 데이터셋으로 교체하세요
    """
    def __init__(self, data_path, split='train', **kwargs):
        """
        Args:
            data_path: 데이터 경로
            split: 'train', 'val', 'test'
        """
        self.data_path = data_path
        self.split = split
        # 데이터 로드 로직 구현
        self.samples = []  # 실제 데이터 리스트로 교체
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        """
        Returns:
            dict: {
                'image': torch.Tensor,  # (1, D, H, W)
                'label': torch.Tensor   # (1,)
            }
        """
        # 실제 데이터 로드 로직 구현
        sample = self.samples[idx]
        
        return {
            'image': torch.randn(1, 64, 64, 64),  # 예시
            'label': torch.tensor(0)  # 예시
        }

