# Setup Script for Stock Data Downloader
# Run this script to initialize your GitHub repository

Write-Host "🚀 Stock Data Downloader - GitHub Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first:" -ForegroundColor Red
    Write-Host "   https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📋 Prerequisites:" -ForegroundColor Yellow
Write-Host "   1. Create a new repository on GitHub" -ForegroundColor White
Write-Host "   2. Copy the repository URL (e.g., https://github.com/username/repo.git)" -ForegroundColor White
Write-Host ""

# Ask for repository URL
$repoUrl = Read-Host "Enter your GitHub repository URL"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "❌ Repository URL is required!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Initializing Git repository..." -ForegroundColor Cyan

# Initialize git if not already initialized
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git repository already exists" -ForegroundColor Yellow
}

# Add remote
try {
    git remote remove origin 2>$null
} catch {}

git remote add origin $repoUrl
Write-Host "✅ Remote 'origin' added" -ForegroundColor Green

# Create main branch
git branch -M main

# Add all files
Write-Host ""
Write-Host "📦 Adding files to Git..." -ForegroundColor Cyan
git add .
Write-Host "✅ Files added" -ForegroundColor Green

# Create initial commit
Write-Host ""
Write-Host "💾 Creating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit: Stock data downloader with GitHub Actions"
Write-Host "✅ Initial commit created" -ForegroundColor Green

# Push to GitHub
Write-Host ""
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "   (You may need to authenticate)" -ForegroundColor Yellow

try {
    git push -u origin main
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to push to GitHub" -ForegroundColor Red
    Write-Host "   Please check your credentials and repository URL" -ForegroundColor Yellow
    Write-Host "   You can manually push using: git push -u origin main" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Go to your GitHub repository" -ForegroundColor White
Write-Host "   2. Navigate to Settings → Actions → General" -ForegroundColor White
Write-Host "   3. Under 'Workflow permissions', select 'Read and write permissions'" -ForegroundColor White
Write-Host "   4. Click 'Save'" -ForegroundColor White
Write-Host ""
Write-Host "   The workflow will run automatically every 2 days at 2:00 AM UTC" -ForegroundColor White
Write-Host "   You can also trigger it manually from the Actions tab" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Repository: $repoUrl" -ForegroundColor Cyan
