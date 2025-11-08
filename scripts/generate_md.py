"""
Markdown 生成器（双语支持版）
从 JSON 生成双语 Markdown 文档，按分类分组展示
"""
import json
from pathlib import Path
from collections import defaultdict

SRC = Path("dictionary/coding_terms.json")
OUT_DIR = Path("generated/markdown")

# 分类名称映射
CATEGORY_NAMES = {
    "motion_state": "运动状态 (Motion State)",
    "posture": "体位 (Posture)",
    "health_condition": "健康状况 (Health Condition)",
    "danger_level": "危险等级 (Danger Level)",
    "tag": "标签 (Tag)"
}


def run():
    """生成双语 Markdown 文档"""
    if not SRC.exists():
        print(f"[ERR] 缺失文件: {SRC}")
        return
    
    # 加载数据
    try:
        items = json.loads(SRC.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] JSON 解析失败: {e}")
        return
    
    # 按分类分组
    grouped = defaultdict(list)
    for item in items:
        grouped[item['category']].append(item)
    
    # 创建输出目录
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成文档
    lines = [
        "# Coding Terms Dictionary / 编码词典",
        "",
        f"**Total Items / 总词条数**: {len(items)}",
        "",
        "**Auto-generated from**: `dictionary/coding_terms.json`  ",
        "**⚠️ DO NOT EDIT MANUALLY / 请勿手动编辑**",
        "",
        "---",
        "",
        "## 📋 字段说明 (Field Description)",
        "",
        "| 字段 | 含义 |",
        "|------|------|",
        "| `id` | 全局唯一标识符 |",
        "| `code` | 编码值 |",
        "| `display` / `display_zh` | 英文/中文显示名 |",
        "| `description` / `description_zh` | 英文/中文详细描述 |",
        "| `system` | 编码系统 |",
        "| `status` | 状态 (active/deprecated/draft) |",
        "| `version` | 版本号 |",
        "| `synonyms` / `synonyms_zh` | 英文/中文同义词 |",
        "",
        "---",
        ""
    ]
    
    # 按分类顺序输出
    category_order = ["motion_state", "posture", "health_condition", "danger_level", "tag"]
    
    for category in category_order:
        if category not in grouped:
            continue
            
        items_in_category = grouped[category]
        category_name = CATEGORY_NAMES.get(category, category)
        
        lines.extend([
            f"## {category_name}",
            "",
            f"**词条数 / Count**: {len(items_in_category)}",
            "",
            "| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |",
            "|-----|------|------------------|-------------------|--------|--------|---------|"
        ])
        
        for item in items_in_category:
            item_id = item['id']
            code = item['code']
            display = f"{item['display']} / {item.get('display_zh', '')}"
            desc_en = item.get('description', '')[:40] + "..." if len(item.get('description', '')) > 40 else item.get('description', '')
            desc_zh = item.get('description_zh', '')[:40] + "..." if len(item.get('description_zh', '')) > 40 else item.get('description_zh', '')
            description = f"{desc_en}<br>{desc_zh}" if desc_en and desc_zh else (desc_en or desc_zh or "")
            system = item['system'].replace('http://snomed.info/sct', 'SNOMED CT').replace('internal://', '').replace('tdp://', 'TDP:')
            status = item['status']
            version = item.get('version', '')
            
            lines.append(
                f"| `{item_id}` | `{code}` | {display} | {description} | {system} | {status} | {version} |"
            )
        
        lines.extend(["", ""])
    
    # 写入文件
    output_file = OUT_DIR / "coding_terms.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"\n[✓] Markdown 已生成: {output_file}")


if __name__ == "__main__":
    run()
