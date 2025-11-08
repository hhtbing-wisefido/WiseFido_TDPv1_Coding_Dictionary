"""
批量添加占位词条
用法: python scripts/scaffold_append.py
     python scripts/scaffold_append.py --dry-run  # 生成到 temp/ 供验证
"""
import json
import sys
from pathlib import Path

FILE = Path("dictionary/coding_terms.json")
TEMP_FILE = Path("temp/coding_terms_scaffold_new_tmp.json")

TEMPLATES = [
    ("motion_state", "lying_down", "internal://motion_state", "0005", "Lying Down", "躺下", "躺下动作。", "躺下动作。"),
    ("motion_state", "sitting_down", "internal://motion_state", "0006", "Sitting Down", "坐下", "坐下动作。", "坐下动作。"),
    ("posture", "lying_prone", "internal://posture", "0011", "Lying Prone", "俯卧", "俯卧姿态。", "俯卧姿态。"),
    ("danger_level", "high", "internal://danger_level", "dl3", "High Risk", "高风险", "高风险等级。", "高风险等级。"),
    ("danger_level", "critical", "internal://danger_level", "dl4", "Critical", "严重风险", "严重风险等级。", "严重风险等级。"),
    ("tag", "new_tag_1", "internal://tag", "tag_001", "New Tag 1", "新标签1", "新增标签示例。", "新增标签示例。"),
    ("tag", "new_tag_2", "internal://tag", "tag_002", "New Tag 2", "新标签2", "新增标签示例。", "新增标签示例。"),
]


def main():
    dry_run = "--dry-run" in sys.argv
    
    if not FILE.exists():
        print(f"[ERR] 缺失文件: {FILE}")
        sys.exit(1)
    
    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] JSON 解析失败: {e}")
        sys.exit(1)
    
    existing_ids = {d.get("id") for d in data}
    added = 0
    
    for cat, key, system, code, display, display_zh, desc_en, desc_zh in TEMPLATES:
        system_short = system.split("://")[-1] if "://" in system else system.split("/")[-1]
        _id = f"{cat}.{key}.{system_short}.{code}"
        
        if _id in existing_ids:
            print(f"[SKIP] 已存在: {_id}")
            continue
        
        data.append({
            "id": _id,
            "code": code,
            "system": system,
            "display": display,
            "display_zh": display_zh,
            "category": cat,
            "status": "active",
            "version": "1.0.0",
            "description": desc_en,
            "description_zh": desc_zh
        })
        print(f"[ADD] 新增: {_id}")
        added += 1
    
    if dry_run:
        # 写入到临时文件供验证
        TEMP_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TEMP_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n[✓] 草稿已保存到临时文件: {TEMP_FILE}")
        print(f"   新增词条数: {added}")
        print(f"   总词条数: {len(data)}")
        print("\n   请运行以下命令验证:")
        print(f"   python scripts/validate.py temp/coding_terms_scaffold_new_tmp.json")
        print("\n   验证通过后，运行以下命令应用到主文件:")
        print(f"   python scripts/scaffold_append.py --apply")
    else:
        with open(FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n[✓] 完成: 新增 {added} 条，总数 {len(data)}")


if __name__ == "__main__":
    main()
