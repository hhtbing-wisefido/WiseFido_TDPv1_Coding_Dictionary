"""
项目公共配置模块# 主要路径
DICTIONARY_FILE = PROJECT_ROOT / "coding_dictionary" / "coding_terms.json"
SCHEMA_FILE = PROJECT_ROOT / "schema" / "coding_item.schema.json"
GENERATED_MD_FILE = PROJECT_ROOT / "auto_generated" / "markdown" / "coding_terms.md"
CHANGELOG_FILE = PROJECT_ROOT / "auto_generated" / "changelog.md"
SNAPSHOT_FILE = PROJECT_ROOT / "auto_generated" / ".snapshot.json"
TEMP_DIR = PROJECT_ROOT / "temp"_pycache__ 统一生成到 temp 目录
"""
import sys
from pathlib import Path

# ============================================================
# 路径配置
# ============================================================

# 获取项目根目录（scripts 的父目录）
PROJECT_ROOT = Path(__file__).parent.parent

# 主要文件路径
DICTIONARY_FILE = PROJECT_ROOT / "coding_dictionary" / "coding_terms.json"
SCHEMA_FILE = PROJECT_ROOT / "schema" / "coding_item.schema.json"
GENERATED_MD_FILE = PROJECT_ROOT / "generated" / "markdown" / "coding_terms.md"
CHANGELOG_FILE = PROJECT_ROOT / "generated" / "changelog.md"
SNAPSHOT_FILE = PROJECT_ROOT / "generated" / ".snapshot.json"
TEMP_DIR = PROJECT_ROOT / "temp"

# ============================================================
# 数据验证配置
# ============================================================

# 有效的词条分类
VALID_CATEGORIES = [
    "posture_codes",           # 姿态编码
    "motion_codes",            # 运动编码
    "physiological_codes",     # 生理指标编码
    "disorder_condition_codes",# 疾病状况编码
    "safety_alert_codes",      # 安全警报编码
    "tag"                      # AI 标签
]

# 有效的状态值
VALID_STATUSES = [
    "active",      # 活跃
    "deprecated",  # 已废弃
    "draft"        # 草稿
]

# 必填字段列表
REQUIRED_FIELDS = [
    "id",
    "code",
    "system",
    "display",
    "display_zh",
    "category",
    "status",
    "version"
]

# 版本号正则表达式（语义化版本 X.Y.Z）
VERSION_PATTERN = r'^\d+\.\d+\.\d+$'

# ID 格式说明
ID_FORMAT_EXAMPLES = [
    "snomed:129006008",
    "internal:0001",
    "tdp:tdp://danger_level/emergency"
]

# ============================================================
# 显示配置
# ============================================================

# 错误信息最大显示数量
MAX_ERROR_DISPLAY = 5

# Markdown 描述最大长度
MAX_DESCRIPTION_LENGTH = 100

# ============================================================
# Python 缓存配置
# ============================================================

# 设置 __pycache__ 统一生成到 temp/__pycache__ 目录
# Python 3.8+ 支持 sys.pycache_prefix
if sys.version_info >= (3, 8):
    cache_dir = TEMP_DIR / "__pycache__"
    cache_dir.mkdir(parents=True, exist_ok=True)
    sys.pycache_prefix = str(cache_dir)

