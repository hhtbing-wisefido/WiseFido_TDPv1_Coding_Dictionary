"""
JSON 词条校验器
- 检查必填字段
- 验证枚举值
- 检测重复 code+system

用法: 
  python scripts/validate.py              # 验证主文件
  python scripts/validate.py temp/file.json  # 验证临时文件
"""
import json
import sys
from pathlib import Path
from jsonschema import Draft7Validator

SCHEMA_FILE = Path("schema/coding_item.schema.json")
DEFAULT_DATA_FILE = Path("dictionary/coding_terms.json")


def run(data_file=None):
    """执行校验
    Args:
        data_file: 要验证的文件路径，默认为主词条文件
    """
    if data_file is None:
        data_file = DEFAULT_DATA_FILE
    
    data_file = Path(data_file)
    
    # 检查文件存在
    if not data_file.exists():
        print(f"[ERR] 缺失文件: {data_file}")
        sys.exit(1)
    if not SCHEMA_FILE.exists():
        print(f"[ERR] 缺失文件: {SCHEMA_FILE}")
        sys.exit(1)
    
    # 加载数据
    try:
        schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
        data = json.loads(data_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] JSON 解析失败: {e}")
        sys.exit(1)
    
    # 校验
    errors = []
    seen_pairs = set()
    validator = Draft7Validator(schema)
    
    for item in data:
        # Schema 校验
        for error in validator.iter_errors(item):
            errors.append(f"{item.get('id', '<no id>')} -> {error.message}")
        
        # 重复检测
        pair = (item.get("code"), item.get("system"))
        if pair in seen_pairs:
            errors.append(f"重复 code+system: {pair}")
        seen_pairs.add(pair)
    
    # 输出结果
    if errors:
        print("\n" + "=" * 50)
        print("  校验失败")
        print("=" * 50)
        for e in errors:
            print(f" - {e}")
        print("=" * 50)
        sys.exit(1)
    
    print(f"\n[✓] 校验通过，词条数: {len(data)}")


if __name__ == "__main__":
    # 支持命令行参数指定文件
    data_file = sys.argv[1] if len(sys.argv) > 1 else None
    run(data_file)
