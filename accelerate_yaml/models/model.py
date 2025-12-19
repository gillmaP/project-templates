"""
모델 아키텍처 정의
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class YourModel(nn.Module):
    """
    템플릿 모델 - 실제 모델로 교체하세요
    """
    def __init__(self, embed_dim=256, num_classes=3, **kwargs):
        super().__init__()
        # 모델 레이어 정의
        self.conv1 = nn.Conv3d(1, 64, 3, padding=1)
        self.pool = nn.AdaptiveAvgPool3d(1)
        self.fc = nn.Linear(64, num_classes)
    
    def forward(self, x):
        """
        Args:
            x: (B, 1, D, H, W) 형태의 입력
        Returns:
            logits: (B, num_classes) 형태의 출력
        """
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

