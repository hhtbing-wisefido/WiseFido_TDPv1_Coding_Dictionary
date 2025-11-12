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


SCHEMA_FILE = _config.SCHEMA_FILE
SCHEMA_MD_FILE = Path("auto_generated_docs/coding_dictionary.schema.md")

# 数据源与输出路径
SRC = Path("coding_dictionary/coding_dictionary.json")
OUT_DIR = Path("auto_generated_docs")

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


# 直接合并原 generate_schema_markdown 函数实现
def generate_schema_markdown(schema: dict) -> str:
    """
    根据 JSON Schema 生成 Markdown 规范文档
    :param schema: dict, 解析后的 JSON Schema
    :return: str, Markdown 文本
    """
    lines = []
    title = schema.get("title", "CodingItem Schema 规范")
    description = schema.get("description", "")
    lines.append(f"# {title} 规范")
    if description:
        lines.append(f"> {description}")
    lines.append("")
    # Schema 信息
    lines.append("## 📋 Schema 信息")
    lines.append(f"- **Schema URI**: `{schema.get('$schema', '')}`")
    lines.append(f"- **标题**: {title}")
    lines.append(f"- **说明**: {description}")
    lines.append(f"- **允许额外属性**: {'✅ 是' if schema.get('additionalProperties', True) else '❌ 否 (严格模式)'}")
    required_fields = schema.get("required", [])
    lines.append(f"- **必填字段数量**: {len(required_fields)} 个")
    lines.append("\n---\n")

    # 字段列表
    lines.append("## 🔑 字段列表")
    lines.append("| 字段名 | 必填/可选 | 类型 | 说明 | 约束条件 |")
    lines.append("|--------|----------|------|------|---------|")
    properties = schema.get("properties", {})
    for field, prop in properties.items():
        is_required = "✅ 必填" if field in required_fields else "可选"
        typ = prop.get("type", "-")
        desc = prop.get("description", "-")
        constraint = "-"
        if "enum" in prop:
            constraint = f"枚举值: {', '.join([f'`{v}`' for v in prop['enum']])}"
        elif "pattern" in prop:
            constraint = f"正则: `{prop['pattern']}`"
        lines.append(f"| **`{field}`** | {is_required} | {typ} | {desc} | {constraint} |")
    lines.append("\n---\n")

    # 枚举类型详细说明
    for field, prop in properties.items():
        if "enum" in prop:
            lines.append(f"### `{field}` 枚举值说明")
            lines.append(f"**说明**: {prop.get('description', '-')}")
            lines.append("**可选值**:")
            for v in prop["enum"]:
                lines.append(f"- `{v}`")
            lines.append("")

    # 相关文档
    lines.append("## 📚 相关文档")
    lines.append("- [Schema 数据结构与字段规范](../../spec/coding_dictionary.schema.spec.md) - 人类撰写的详细规范（含分类体系详解）")
    lines.append("- [README.md](../../README.md) - 项目主文档")
    lines.append("\n---\n")

    # 注意事项
    lines.append("## ⚠️ 注意事项")
    lines.append("1. 本文档由 Schema 自动生成，请勿手动编辑")
    lines.append(f"2. 如需修改，请编辑 `schema/coding_dictionary.schema.json`")
    lines.append("3. 详细的使用说明和示例请参考 [coding_dictionary.schema.spec.md](../../spec/coding_dictionary.schema.spec.md)")
    return "\n".join(lines)


if __name__ == "__main__":
    run()
