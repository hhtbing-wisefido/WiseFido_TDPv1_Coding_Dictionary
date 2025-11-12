# ============================================================
# 新用户请先安装依赖：
#   pip install -r requirements.txt
# ============================================================
"""
添加编码字典词条 (v2.0.0 精简版)
用法: python scripts/add_coding_dict.py
交互式添加单个词条，只需输入 4 个核心字段
"""
# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401

import json
import sys
from pathlib import Path

FILE = Path("coding_dictionary/coding_dictionary.json")


def main():
    """交互式添加词条 (v2.0.0)"""
    print("=== 添加新编码词条 (v2.0.0) ===\n")
    
    if not FILE.exists():
        print(f"[ERR] 缺失文件: {FILE}")
        sys.exit(1)
    
    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] JSON 解析失败: {e}")
        sys.exit(1)
    
    # 输入 4 个核心字段
    print("请输入词条信息（4个核心字段）:\n")
    system = input("1. 编码系统 URI (如 http://snomed.info/sct): ").strip()
    code = input("2. 编码值 (如 217082002): ").strip()
    display = input("3. 英文名称 (如 Accidental fall): ").strip()
    display_zh = input("4. 中文名称 (如 意外跌倒): ").strip()
    
    # 验证必填字段
    if not all([system, code, display, display_zh]):
        print("\n[ERR] 所有字段都是必填的！")
        sys.exit(1)
    
    # 检查重复
    for item in data:
        if item['system'] == system and item['code'] == code:
            print(f"\n[ERR] 词条已存在: {system}|{code}")
            print(f"     {item['display']} / {item['display_zh']}")
            sys.exit(1)
    
    # 构建新词条
    new_entry = {
        "system": system,
        "code": code,
        "display": display,
        "display_zh": display_zh
    }
    
    # 显示预览
    print("\n=== 词条预览 ===")
    print(json.dumps(new_entry, ensure_ascii=False, indent=2))
    
    # 确认添加
    confirm = input("\n确认添加？(y/n): ").strip().lower()
    if confirm != 'y':
        print("[CANCEL] 已取消")
        sys.exit(0)
    
    # 添加到列表
    data.append(new_entry)
    
    # 保存
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 成功添加词条！")
    print(f"     {system}|{code}")
    print(f"     {display} / {display_zh}")
    print(f"     当前总词条数: {len(data)}")
    print(f"\n建议运行验证: python scripts/validate_json.py")


if __name__ == "__main__":
    main()

