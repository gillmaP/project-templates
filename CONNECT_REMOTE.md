# 원격 저장소 연결 가이드

## 🔗 원격 저장소 연결 전체 과정

### 1단계: 로컬 Git 저장소 초기화 (이미 했다면 스킵)

```bash
cd /jhbak/project_templates
git init
git add .
git commit -m "Initial commit: 프로젝트 템플릿 저장소"
```

### 2단계: 원격 저장소 준비

#### 옵션 A: 새 저장소 생성 (GitHub)
1. GitHub에 로그인
2. https://github.com/new 접속
3. Repository name: `project-templates` (또는 원하는 이름)
4. Public 또는 Private 선택
5. **"Initialize this repository with a README" 체크 해제** (이미 파일이 있으므로)
6. "Create repository" 클릭

#### 옵션 B: 새 저장소 생성 (GitLab)
1. GitLab에 로그인
2. 새 프로젝트 생성
3. 프로젝트 이름: `project-templates`
4. Visibility 선택
5. "Initialize repository with a README" 체크 해제
6. "Create project" 클릭

#### 옵션 C: 기존 저장소 사용
이미 원격 저장소가 있다면 그 URL을 사용하세요.

### 3단계: 원격 저장소 연결

#### GitHub 사용 시:

```bash
# HTTPS 방식 (권장 - 처음 사용 시)
git remote add origin https://github.com/YOUR_USERNAME/project-templates.git

# 또는 SSH 방식 (SSH 키 설정 후)
git remote add origin git@github.com:YOUR_USERNAME/project-templates.git
```

#### GitLab 사용 시:

```bash
# HTTPS 방식
git remote add origin https://gitlab.com/YOUR_USERNAME/project-templates.git

# 또는 SSH 방식
git remote add origin git@gitlab.com:YOUR_USERNAME/project-templates.git
```

### 4단계: 원격 저장소 확인

```bash
# 연결된 원격 저장소 확인
git remote -v

# 출력 예시:
# origin  https://github.com/YOUR_USERNAME/project-templates.git (fetch)
# origin  https://github.com/YOUR_USERNAME/project-templates.git (push)
```

### 5단계: 브랜치 이름 설정 및 푸시

```bash
# 브랜치 이름을 main으로 설정 (GitHub 기본값)
git branch -M main

# 또는 master 사용 시
# git branch -M master

# 원격 저장소에 푸시
git push -u origin main
```

### 6단계: 인증 (필요 시)

#### Personal Access Token 사용 (HTTPS):
- GitHub: Settings → Developer settings → Personal access tokens → Generate new token
- GitLab: User Settings → Access Tokens → Create personal access token
- 푸시 시 Username과 Token 입력

#### SSH 키 사용 (SSH):
```bash
# SSH 키 생성 (없는 경우)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개키 확인
cat ~/.ssh/id_ed25519.pub

# GitHub/GitLab에 SSH 키 등록
# GitHub: Settings → SSH and GPG keys → New SSH key
# GitLab: User Settings → SSH Keys
```

## 🔄 이미 원격 저장소가 있는 경우

기존 원격 저장소와 연결하려면:

```bash
# 기존 원격 저장소 확인
git remote -v

# 기존 원격 저장소 제거 (필요 시)
git remote remove origin

# 새 원격 저장소 추가
git remote add origin <새_저장소_URL>
```

## ✅ 연결 확인

```bash
# 원격 저장소 정보 확인
git remote show origin

# 원격 브랜치 확인
git branch -r
```

## 🚀 이후 업데이트 방법

템플릿을 수정한 후:

```bash
git add .
git commit -m "Update: 템플릿 개선"
git push
```

## 💡 문제 해결

### "remote origin already exists" 오류
```bash
# 기존 원격 저장소 제거 후 다시 추가
git remote remove origin
git remote add origin <저장소_URL>
```

### "Authentication failed" 오류
- Personal Access Token 사용 확인
- SSH 키 설정 확인
- Git credential helper 설정

### "Permission denied" 오류
- 저장소 접근 권한 확인
- SSH 키가 올바르게 등록되었는지 확인

