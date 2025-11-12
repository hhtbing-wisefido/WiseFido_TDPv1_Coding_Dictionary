# ============================================================
# 新用户请先安装依赖：
#   pip install -r requirements.txt
# ============================================================
"""
JSON 词条校验器 (v2.0.0)
使用 JSON Schema 验证词条文件（精简版）
"""
# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("\n" + "=" * 70)
    print("  ⚠️  缺少必需的 Python 依赖包")
    print("=" * 70)
    print("\n[错误] 未安装 jsonschema 模块")
    print("\n[解决方案] 正在尝试自动安装...")
    
    import subprocess
    try:
        # 使用当前 Python 解释器安装依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])
        print("\n[成功] jsonschema 已安装，请重新运行脚本")
        print("\n" + "=" * 70)
        sys.exit(0)
    except subprocess.CalledProcessError:
        print("\n[失败] 自动安装失败，请手动执行：")
        print("\n  {} -m pip install -r requirements.txt".format(sys.executable))
        print("\n或：")
        print("\n  {} -m pip install jsonschema".format(sys.executable))
        print("\n" + "=" * 70)
        sys.exit(1)

DEFAULT_SRC = Path("coding_dictionary/coding_dictionary.json")
SCHEMA = Path("schema/coding_dictionary.schema.json")


def run(file_path=None):
    """校验 JSON 词条文件
    
    Args:
        file_path: 可选，要验证的 JSON 文件路径。如果为 None，使用默认文件
    """
    # 确定要验证的文件
    if file_path:
        src = Path(file_path)
    else:
        src = DEFAULT_SRC
    
    if not src.exists():
        print(f"[ERR] 缺失文件: {src}")
        return False
    
    if not SCHEMA.exists():
        print(f"[ERR] 缺失 Schema: {SCHEMA}")
        return False
    
    # 加载 Schema
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] Schema 解析失败: {e}")
        return False
    
    # 加载数据
    try:
        items = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERR] JSON 解析失败: {e}")
        return False
    except Exception as e:
        print(f"[ERR] 读取文件失败: {e}")
        return False
    
    if not isinstance(items, list):
        print("[ERR] JSON 根节点必须是数组")
        return False
    
    # 验证每个词条
    errors = []
    duplicates = {}
    
    for idx, item in enumerate(items):
        # Schema 验证
        try:
            jsonschema.validate(instance=item, schema=schema)
        except jsonschema.ValidationError as e:
            # v2.0.0: 使用 system|code 标识词条（不再有 id 字段）
            item_key = f"{item.get('system', 'unknown')}|{item.get('code', 'unknown')}"
            errors.append(f"词条 {item_key}: {e.message}")
        
        # 检查必需字段（v2.0.0: 只有4个核心字段）
        required_fields = ["system", "code", "display", "display_zh"]
        for field in required_fields:
            if field not in item or not item[field]:
                item_key = f"{item.get('system', 'unknown')}|{item.get('code', 'unknown')}"
                errors.append(f"词条 {item_key}: 缺少必需字段 '{field}'")
        
        # 检查重复 (system + code 组合)
        code = item.get("code")
        system = item.get("system")
        if code and system:
            key = f"{system}|{code}"
            if key in duplicates:
                errors.append(f"重复词条: {key} 在索引 {idx} 和 {duplicates[key]} 中重复")
            else:
                duplicates[key] = idx
    
    # 输出结果
    if errors:
        print(f"\n[ERR] 发现 {len(errors)} 个错误:\n")
        for err in errors:
            print(f"  - {err}")
        print()
        return False
    
    print(f"\n[OK] 校验通过: {len(items)} 个词条\n")
    return True


if __name__ == "__main__":
    # 支持命令行直接调用，传入文件路径
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        run(file_path)
    else:
        run()

