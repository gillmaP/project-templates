"""
학습 관련 유틸리티 함수
"""
from sklearn.metrics import accuracy_score, f1_score, classification_report
import torch
import random
import numpy as np
import os


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


def calculate_metrics(y_true, y_pred, target_names=None):
    """
    평가지표 계산
    
    Args:
        y_true: 실제 레이블
        y_pred: 예측 레이블
        target_names: 클래스 이름 리스트
    
    Returns:
        dict: accuracy, macro_f1, weighted_f1, report
    """
    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    weighted_f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    report = classification_report(
        y_true, y_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0
    )
    
    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "report": report
    }

