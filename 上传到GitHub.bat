@echo off
chcp 65001 >nul
echo ================================================
echo 🚀 发货助手 - 上传到GitHub自动构建APK
echo ================================================
echo.

echo 📋 使用说明：
echo 1. 这将帮您把项目上传到GitHub
echo 2. GitHub会自动构建APK文件
echo 3. 您可以在GitHub Actions页面下载APK
echo.

echo ⚠️  前提条件：
echo - 已安装Git（https://git-scm.com/）
echo - 有GitHub账号
echo - 需要创建新的GitHub仓库
echo.

set /p confirm="确认继续？(y/n): "
if /i not "%confirm%"=="y" (
    echo 已取消操作
    pause
    exit /b
)

echo.
echo 🔧 初始化Git仓库...
git init

echo.
echo 📁 添加所有文件...
git add .

echo.
echo 💾 提交代码...
git commit -m "发货助手Android版 - 初始提交"

echo.
echo 📝 请按以下步骤操作：
echo.
echo 1. 打开 https://github.com/new
echo 2. 创建新仓库，名称建议：shipping-app
echo 3. 不要添加README、.gitignore或LICENSE
echo 4. 创建后复制仓库URL（类似：https://github.com/你的用户名/shipping-app.git）
echo.

set /p repo_url="请输入您的GitHub仓库URL: "

if "%repo_url%"=="" (
    echo ❌ 未输入仓库URL，操作终止
    pause
    exit /b
)

echo.
echo 🔗 添加远程仓库...
git remote add origin %repo_url%

echo.
echo 📤 推送到GitHub...
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo ✅ 上传成功！
    echo ================================================
    echo.
    echo 📱 接下来的步骤：
    echo 1. 打开您的GitHub仓库页面
    echo 2. 点击"Actions"标签页
    echo 3. 等待构建完成（约10-20分钟）
    echo 4. 构建完成后点击下载APK文件
    echo.
    echo 🔗 GitHub仓库：%repo_url%
    echo 🔗 Actions页面：%repo_url%/actions
    echo.
) else (
    echo.
    echo ================================================
    echo ❌ 上传失败！
    echo ================================================
    echo.
    echo 💡 可能的解决方案：
    echo 1. 检查网络连接
    echo 2. 确认GitHub仓库URL正确
    echo 3. 确认有权限推送到该仓库
    echo 4. 检查Git是否正确安装
    echo.
)

pause
