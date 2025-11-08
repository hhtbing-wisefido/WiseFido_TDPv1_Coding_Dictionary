"""
项目公共配置模块
自动配置 __pycache__ 统一生成到 temp 目录
"""
import sys
from pathlib import Path

# 设置 __pycache__ 统一生成到 temp/__pycache__ 目录
# Python 3.8+ 支持 sys.pycache_prefix
if sys.version_info >= (3, 8):
    # 获取项目根目录（scripts 的父目录）
    project_root = Path(__file__).parent.parent
    cache_dir = project_root / "temp" / "__pycache__"
    cache_dir.mkdir(parents=True, exist_ok=True)
    sys.pycache_prefix = str(cache_dir)
