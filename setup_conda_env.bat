@echo off
echo 正在创建 AI Hedge Fund conda 环境...
echo.

REM 检查conda是否已安装
echo 检查 conda 安装状态...
conda --version
if %errorlevel% neq 0 (
    echo 错误: conda 命令执行失败。
    echo 请确保 Anaconda 或 Miniconda 已正确安装并添加到 PATH。
    pause
    exit /b 1
) else (
    echo conda 检查通过！
)

echo.
echo 检查 environment.yml 文件是否存在...
if not exist "environment.yml" (
    echo 错误: 未找到 environment.yml 文件。
    pause
    exit /b 1
) else (
    echo environment.yml 文件存在！
)

echo.
echo 使用 environment.yml 创建环境...
conda env create -f environment.yml

if %errorlevel% neq 0 (
    echo.
    echo 错误: 环境创建失败。
    echo 可能的原因:
    echo 1. 环境已存在（尝试运行: conda env remove -n ai-hedge-fund）
    echo 2. 网络连接问题
    echo 3. 依赖包冲突
    pause
    exit /b 1
)

echo.
echo ========================================
echo 环境创建成功！
echo ========================================
echo.
echo 要激活环境，请运行:
echo conda activate ai-hedge-fund
echo.
echo 要停用环境，请运行:
echo conda deactivate
echo.
echo 要删除环境，请运行:
echo conda env remove -n ai-hedge-fund
echo.
pause 