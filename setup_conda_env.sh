#!/bin/bash

echo "正在创建 AI Hedge Fund conda 环境..."
echo

# 检查conda是否已安装
if ! command -v conda &> /dev/null; then
    echo "错误: 未找到 conda。请先安装 Anaconda 或 Miniconda。"
    exit 1
fi

echo "使用 environment.yml 创建环境..."
conda env create -f environment.yml

if [ $? -ne 0 ]; then
    echo "错误: 环境创建失败。"
    exit 1
fi

echo
echo "环境创建成功！"
echo
echo "要激活环境，请运行:"
echo "conda activate ai-hedge-fund"
echo
echo "要停用环境，请运行:"
echo "conda deactivate" 