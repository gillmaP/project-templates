#!/bin/bash
# Git 저장소 설정 스크립트

echo "🚀 Git 저장소 설정을 시작합니다..."

# Git 저장소 초기화
if [ ! -d .git ]; then
    git init
    echo "✅ Git 저장소 초기화 완료"
else
    echo "ℹ️  이미 Git 저장소가 존재합니다"
fi

# .gitignore 확인
if [ ! -f .gitignore ]; then
    echo "⚠️  .gitignore 파일이 없습니다. 생성해주세요."
else
    echo "✅ .gitignore 파일 확인됨"
fi

# 파일 추가
echo ""
echo "📝 파일 추가 중..."
git add .

# 상태 확인
echo ""
echo "📊 현재 상태:"
git status

echo ""
echo "✅ 준비 완료!"
echo ""
echo "다음 단계:"
echo "1. git commit -m 'Initial commit: 프로젝트 템플릿 저장소'"
echo "2. GitHub/GitLab에서 새 저장소 생성"
echo "3. git remote add origin <저장소_URL>"
echo "4. git push -u origin main"
echo ""
echo "자세한 내용은 GIT_SETUP.md를 참고하세요."

