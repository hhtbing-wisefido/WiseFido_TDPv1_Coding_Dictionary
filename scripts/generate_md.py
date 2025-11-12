# ============================================================
# 新用户请先安装依赖：
#   pip install -r requirements.txt
# ============================================================
"""
Markdown 生成器 (v2.0.0 精简版)
从 JSON 生成 Markdown 文档，展示 4 个核心字段
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


def run():
    """生成 Markdown 文档和 Schema Markdown文档 (v2.0.0)"""
    if not SRC.exists():
        print(f"[ERR] 缺失文件: {SRC}")
        return
    
    # 加载数据
    try:
        items = json.loads(SRC.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] JSON 解析失败: {e}")
        return
    
    # 按 system 分组统计
    system_stats = defaultdict(int)
    for item in items:
        system = item['system']
        system_stats[system] += 1
    
    # 创建输出目录
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成文档
    lines = [
        "# Coding Terms Dictionary / 编码词典",
        "",
        f"**版本 (Version)**: v2.0.0",
        f"**总词条数 (Total Items)**: {len(items)}",
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
        "| `system` | 编码系统 URI |",
        "| `code` | 编码值 |",
        "| `display` | 英文显示名称 |",
        "| `display_zh` | 中文显示名称 |",
        "",
        "---",
        "",
        "## 📊 编码系统统计 (System Statistics)",
        ""
    ]
    
    # 添加系统统计
    for system, count in sorted(system_stats.items(), key=lambda x: -x[1]):
        percentage = (count / len(items)) * 100
        system_display = system.replace('http://snomed.info/sct', 'SNOMED CT')
        lines.append(f"- **{system_display}**: {count} 个词条 ({percentage:.1f}%)")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📚 词条列表 (Coding List)",
        "",
        "| System | Code | Display (EN) | Display (ZH) |",
        "|--------|------|--------------|--------------|"
    ])
    
    # 按 code 排序输出所有词条
    sorted_items = sorted(items, key=lambda x: (x['system'], x['code']))
    
    for item in sorted_items:
        system = item['system'].replace('http://snomed.info/sct', 'SNOMED CT').replace('internal://', 'internal:').replace('tdp://', 'tdp:')
        code = item['code']
        display = item['display']
        display_zh = item['display_zh']
        
        lines.append(
            f"| {system} | `{code}` | {display} | {display_zh} |"
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
