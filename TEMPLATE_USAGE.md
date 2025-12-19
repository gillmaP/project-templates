# 템플릿 사용 가이드

## 🎯 언제 어떤 템플릿을 사용할까?

### 1. Accelerate + YAML (`accelerate_yaml/`)

**사용 시나리오:**
- ✅ 빠른 프로토타이핑이 필요할 때
- ✅ 단순한 실험 설정
- ✅ 개인 프로젝트 또는 소규모 팀
- ✅ 코드 단순성을 우선시할 때

**예시:**
```bash
# 템플릿 복사
cp -r project_templates/accelerate_yaml my_new_project
cd my_new_project

# 파일명 및 변수명 수정
# - YourModel → MyModel
# - YourDataset → MyDataset
# - config/default.yaml 수정

# 실행
python main.py --mode train
```

### 2. Hydra + DDP (`hydra_ddp/`)

**사용 시나리오:**
- ✅ 대규모 하이퍼파라미터 스윕 필요
- ✅ 실험 재현성이 중요할 때
- ✅ 논문 작성 및 실험 관리
- ✅ 팀 협업 및 실험 공유

**예시:**
```bash
# 템플릿 복사
cp -r project_templates/hydra_ddp my_new_project
cd my_new_project

# configs/ 폴더 구조 확인 및 수정
# 실행
python main.py train.learning_rate=1e-5

# 하이퍼파라미터 스윕
python main.py -m train.learning_rate=1e-4,1e-5,1e-6
```

### 3. Hybrid (`hybrid/`)

**사용 시나리오:**
- ✅ 설정 관리가 중요하면서도 코드 단순성 유지
- ✅ 실험 추적 + 자동 분산 학습
- ✅ 프로덕션 레벨 프로젝트

**예시:**
```bash
# 템플릿 복사
cp -r project_templates/hybrid my_new_project
cd my_new_project

# 실행
accelerate launch main.py train.learning_rate=1e-5
```

## 📝 템플릿 커스터마이징 체크리스트

새 프로젝트를 시작할 때:

- [ ] 프로젝트 이름에 맞게 폴더/파일명 변경
- [ ] `YourModel` → 실제 모델 이름으로 변경
- [ ] `YourDataset` → 실제 데이터셋 이름으로 변경
- [ ] `config/default.yaml` 또는 `configs/` 설정 수정
- [ ] 모델 아키텍처에 맞게 `models/model.py` 수정
- [ ] 데이터셋에 맞게 `train/datasets.py` 수정
- [ ] README.md 업데이트

## 🔄 템플릿 간 전환

### Accelerate → Hydra로 전환

1. `main.py`에 `@hydra.main` 데코레이터 추가
2. `config/` → `configs/` 구조로 변경
3. `DictConfig` 사용으로 변경
4. DDP 초기화 코드 추가

### Hydra → Hybrid로 전환

1. `main.py`에 `Accelerator` 추가
2. DDP 초기화 코드 제거 (Accelerate가 처리)
3. `trainer.py`에서 `accelerator.prepare()` 사용

## 💡 팁

1. **템플릿 저장 위치**: `/jhbak/project_templates/`에 저장되어 있음
2. **버전 관리**: 템플릿도 Git으로 관리하면 좋음
3. **공유**: 팀원들과 템플릿 공유 시 README 포함
4. **업데이트**: 사용하면서 개선사항을 템플릿에 반영

## 📚 참고 자료

- [Accelerate 문서](https://huggingface.co/docs/accelerate/)
- [Hydra 문서](https://hydra.cc/)
- [PyTorch DDP](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)

