#!/bin/bash

# 指定 Conda 環境的名稱
CONDA_ENV="skyline"

# 指定 Conda 環境的 Python 解析器路徑
PYTHON="/home/aclab/miniconda3/envs/skyline/bin/python"

# 定義要執行的 Python 檔案清單
FILES=(
    "dis-EPSU-WSnew.py"
    "dis-EPSU-psnew.py"
    "dis-EPSU-dimnew.py"
    "dis-EPSU-radiusnew.py"
)

# 迭代運行 Python 檔案
for file in "${FILES[@]}"; do
    echo "執行 ${file}"
    ${PYTHON} ${file}
done
