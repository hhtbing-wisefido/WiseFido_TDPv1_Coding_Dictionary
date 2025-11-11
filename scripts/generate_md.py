# ============================================================
# 新用户请先安装依赖：
#   pip install -r requirements.txt
# ============================================================
"""
Markdown 生成器（双语支持版）
从 JSON 生成双语 Markdown 文档，按分类分组展示
"""
# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401

import json
from pathlib import Path
from collections import defaultdict

from pathlib import Path
import sys

# 引入Schema Markdown生成逻辑
from generate_schema_md import generate_schema_markdown
import _config

SCHEMA_FILE = _config.SCHEMA_FILE
SCHEMA_MD_FILE = Path("auto_generated/markdown/coding_dictionary.schema.md")

# 数据源与输出路径
SRC = Path("coding_dictionary/coding_dictionary.json")
OUT_DIR = Path("auto_generated/markdown")

# 分类名称映射
CATEGORY_NAMES = {
    "posture_codes": "姿态编码 (Posture Codes)",
    "motion_codes": "运动编码 (Motion Codes)",
    "physiological_codes": "生理指标编码 (Physiological Codes)",
    "disorder_condition_codes": "疾病状况编码 (Disorder & Condition Codes)",
    "safety_alert_codes": "安全警报编码 (Safety & Alert Codes)",
    "tag": "标签 (Tag)"
}


def run():
    """生成双语 Markdown 文档和 Schema Markdown文档"""
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
        category = item['category']
        grouped[category].append(item)
    
    # 创建输出目录
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成文档
    lines = [
        "# Coding Terms Dictionary / 编码词典",
        "",
        f"**Total Items / 总词条数**: {len(items)}",
        "",
        "**Auto-generated from**: `coding_dictionary/coding_dictionary.json`  ",
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
    category_order = [
        "posture_codes",
        "motion_codes",
        "physiological_codes",
        "disorder_condition_codes",
        "safety_alert_codes",
        "tag"
    ]
    
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
            item_id = item['id']  # 直接使用 JSON 中的 ID，不进行任何转换
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
    
    # 写入数据表格文件
    output_file = OUT_DIR / "coding_dictionary.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"\n[OK] Markdown generated: {output_file}")

    # 新增：生成Schema Markdown文档
    try:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_data = json.load(f)
        schema_md = generate_schema_markdown(schema_data)
        SCHEMA_MD_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SCHEMA_MD_FILE, "w", encoding="utf-8") as f:
            f.write(schema_md)
        print(f"[OK] Schema Markdown generated: {SCHEMA_MD_FILE}")
    except Exception as e:
        print(f"[ERR] Schema Markdown生成失败: {e}")


if __name__ == "__main__":
    run()
