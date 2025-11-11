# ============================================================
# 新用户请先安装依赖：
#   pip install -r requirements.txt
# ============================================================
"""
JSON 词条校验器
使用 JSON Schema 验证词条文件
"""
# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("[ERR] 缺少依赖: jsonschema")
    print("请运行: pip install -r requirements.txt")
    exit(1)

DEFAULT_SRC = Path("coding_dictionary/coding_terms.json")
SCHEMA = Path("schema/coding_item.schema.json")


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
            item_id = item.get("id", f"索引{idx}")
            errors.append(f"词条 {item_id}: {e.message}")
        
        # ID 格式验证：确保使用简洁格式，避免臃肿格式
        item_id = item.get("id", "")
        if item_id:
            # 检查是否使用了旧格式（category.code.system.code 的臃肿格式）
            if "." in item_id and len(item_id.split(".")) >= 4:
                # 检查是否匹配旧格式模式：category.xxx.system.xxx
                parts = item_id.split(".")
                if len(parts) >= 4:
                    # 可能是旧格式，检查是否包含 category 和 system 信息
                    category = item.get("category", "")
                    system = item.get("system", "")
                    if category and parts[0] == category:
                        errors.append(
                            f"词条 {item_id}: ID 使用了旧格式（臃肿格式）。"
                            f"应使用简洁格式，如 'snomed:129006008' 或 'internal:0002'，"
                            f"而不是 '{item_id}'"
                        )
            
            # 验证新格式：应该是 system_prefix:code 或 tdp:uri 格式
            # 允许的格式：snomed:xxx, internal:xxx, tdp:xxx
            if not any(item_id.startswith(prefix) for prefix in ["snomed:", "internal:", "tdp:"]):
                if not item_id.startswith("tdp://"):
                    # 如果不是标准格式，给出警告（但不阻止，因为可能有其他合法格式）
                    pass
        
        # 检查重复 (code + system)
        code = item.get("code")
        system = item.get("system")
        if code and system:
            key = f"{system}|{code}"
            if key in duplicates:
                errors.append(f"重复词条: {item.get('id', '未知')} 与 {duplicates[key]} 的 code+system 相同")
            else:
                duplicates[key] = item.get("id", f"索引{idx}")
    
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

