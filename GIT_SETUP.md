# Git 저장소 설정 가이드

## 📚 .gitkeep이란?

`.gitkeep`은 **빈 폴더를 Git에 추적하기 위한 관례적인 파일**입니다.

### 왜 필요한가?

Git은 파일만 추적하고, **빈 폴더는 추적하지 않습니다**. 하지만 프로젝트 구조상 빈 폴더가 필요할 때가 있습니다.

예를 들어:
```
project/
├── logs/          # 빈 폴더 (나중에 로그 저장)
├── checkpoints/   # 빈 폴더 (나중에 모델 저장)
└── outputs/       # 빈 폴더 (나중에 결과 저장)
```

이런 폴더들을 Git에 포함시키려면 `.gitkeep` 파일을 넣어야 합니다.

### 사용 방법

```bash
# 빈 폴더에 .gitkeep 파일 생성
touch logs/.gitkeep
touch checkpoints/.gitkeep
```

Git은 이 파일을 추적하므로, 폴더도 함께 추적됩니다.

### 주의사항

- `.gitkeep`은 Git의 공식 기능이 아닙니다
- 단지 관례적으로 사용되는 파일명입니다
- 다른 이름(`.gitignore`, `.placeholder` 등)을 사용해도 됩니다
- 파일 내용은 비어있어도, 주석을 넣어도 상관없습니다

## 🚀 Git 저장소 설정하기

### 1단계: Git 저장소 초기화

```bash
cd /jhbak/project_templates
git init
```

### 2단계: .gitignore 확인

`.gitignore` 파일이 이미 생성되어 있습니다. 필요에 따라 수정하세요.

### 3단계: 파일 추가 및 커밋

```bash
# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: 프로젝트 템플릿 저장소"

# 상태 확인
git status
```

### 4단계: GitHub/GitLab에 원격 저장소 연결

#### GitHub 사용 시:

1. GitHub에서 새 저장소 생성 (예: `project-templates`)
2. 원격 저장소 추가:

```bash
# HTTPS 방식
git remote add origin https://github.com/yourusername/project-templates.git

# 또는 SSH 방식
git remote add origin git@github.com:yourusername/project-templates.git
```

3. 브랜치 이름 설정 (필요시):

```bash
git branch -M main  # 또는 master
```

4. 푸시:

```bash
git push -u origin main
```

#### GitLab 사용 시:

```bash
git remote add origin https://gitlab.com/yourusername/project-templates.git
git push -u origin main
```

### 5단계: 인증 설정 (필요시)

#### SSH 키 사용 (권장):

```bash
# SSH 키 생성 (없는 경우)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개키 복사
cat ~/.ssh/id_ed25519.pub

# GitHub/GitLab에 SSH 키 등록
```

#### Personal Access Token 사용:

GitHub/GitLab에서 Personal Access Token을 생성하고 사용합니다.

## 📝 일반적인 Git 워크플로우

### 템플릿 업데이트 후:

```bash
# 변경사항 확인
git status

# 변경된 파일 추가
git add .

# 커밋
git commit -m "Update: 템플릿 개선사항 추가"

# 푸시
git push
```

### 새 템플릿 추가 후:

```bash
git add new_template/
git commit -m "Add: 새로운 템플릿 추가"
git push
```

## 🔍 유용한 Git 명령어

```bash
# 원격 저장소 확인
git remote -v

# 브랜치 확인
git branch

# 커밋 히스토리 확인
git log --oneline

# 변경사항 확인
git diff

# 원격 저장소와 동기화
git pull origin main
```

## 💡 팁

1. **README.md 작성**: 각 템플릿의 README를 잘 작성하면 나중에 이해하기 쉬움
2. **태그 사용**: 버전별로 태그를 달아두면 좋음
   ```bash
   git tag -a v1.0 -m "Initial templates"
   git push origin v1.0
   ```
3. **브랜치 전략**: 여러 템플릿을 병렬로 개발할 때 브랜치 사용
4. **.gitkeep 제거**: 나중에 폴더에 실제 파일이 생기면 .gitkeep은 제거해도 됨

