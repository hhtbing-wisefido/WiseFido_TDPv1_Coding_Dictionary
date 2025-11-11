#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Schema 转 Markdown 生成器

功能：
1. 读取 schema/coding_dictionary.schema.json
2. 生成人类可读的 Markdown 文档
3. 输出到 auto_generated/markdown/coding_dictionary.schema.md
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import sys

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
from _config import (
    SCHEMA_FILE,
    PROJECT_ROOT,
)

# 输出文件路径
AUTO_GENERATED_DIR = PROJECT_ROOT / "auto_generated"
SCHEMA_MD_FILE = AUTO_GENERATED_DIR / "markdown" / "coding_dictionary.schema.md"


def get_type_display(prop: Dict[str, Any]) -> str:
    """获取类型的友好显示"""
    prop_type = prop.get("type", "unknown")
    
    if prop_type == "array":
        items = prop.get("items", {})
        items_type = items.get("type", "any")
        return f"Array&lt;{items_type}&gt;"
    elif prop_type == "object":
        return "Object"
    else:
        return prop_type.capitalize()


def get_constraints(prop: Dict[str, Any]) -> List[str]:
    """获取字段约束"""
    constraints = []
    
    if "enum" in prop:
        enum_values = ", ".join([f"`{v}`" for v in prop["enum"]])
        constraints.append(f"枚举值: {enum_values}")
    
    if "pattern" in prop:
        constraints.append(f"正则: `{prop['pattern']}`")
    
    if "items" in prop and isinstance(prop["items"], dict):
        if "type" in prop["items"]:
            constraints.append(f"元素类型: `{prop['items']['type']}`")
    
    return constraints


def generate_field_table(properties: Dict[str, Any], required_fields: List[str]) -> str:
    """生成字段表格"""
    rows = []
    
    for field_name, prop in properties.items():
        # 字段名
        field_display = f"**`{field_name}`**"
        
        # 是否必填
        required = "✅ 必填" if field_name in required_fields else "可选"
        
        # 类型
        field_type = get_type_display(prop)
        
        # 描述
        description = prop.get("description", "-")
        
        # 约束
        constraints = get_constraints(prop)
        constraint_str = "<br>".join(constraints) if constraints else "-"
        
        rows.append(f"| {field_display} | {required} | {field_type} | {description} | {constraint_str} |")
    
    return "\n".join(rows)


def generate_enum_details(properties: Dict[str, Any]) -> str:
    """生成枚举值详细说明"""
    sections = []
    
    for field_name, prop in properties.items():
        if "enum" in prop:
            sections.append(f"### `{field_name}` 枚举值\n")
            
            enum_values = prop["enum"]
            description = prop.get("description", "")
            
            # 尝试从描述中提取每个枚举值的说明
            sections.append(f"**说明**: {description}\n")
            sections.append("**可选值**:\n")
            
            for value in enum_values:
                sections.append(f"- `{value}`")
            
            sections.append("")  # 空行
    
    return "\n".join(sections)


def generate_nested_objects(properties: Dict[str, Any]) -> str:
    """生成嵌套对象说明"""
    sections = []
    
    for field_name, prop in properties.items():
        if prop.get("type") == "object" and "properties" in prop:
            sections.append(f"### `{field_name}` 对象结构\n")
            sections.append(f"**说明**: {prop.get('description', '-')}\n")
            sections.append("**子字段**:\n")
            
            for sub_name, sub_prop in prop["properties"].items():
                sub_type = get_type_display(sub_prop)
                sub_desc = sub_prop.get("description", "-")
                constraints = get_constraints(sub_prop)
                
                sections.append(f"- **`{sub_name}`** ({sub_type}): {sub_desc}")
                
                if constraints:
                    for constraint in constraints:
                        sections.append(f"  - {constraint}")
            
            sections.append("")  # 空行
        
        elif prop.get("type") == "array" and isinstance(prop.get("items"), dict):
            items = prop["items"]
            if items.get("type") == "object" and "properties" in items:
                sections.append(f"### `{field_name}` 数组元素结构\n")
                sections.append(f"**说明**: {prop.get('description', '-')}\n")
                sections.append("**数组元素包含以下字段**:\n")
                
                for sub_name, sub_prop in items["properties"].items():
                    sub_type = get_type_display(sub_prop)
                    sub_desc = sub_prop.get("description", "-")
                    required_in_items = "(必填)" if sub_name in items.get("required", []) else "(可选)"
                    
                    sections.append(f"- **`{sub_name}`** {required_in_items} ({sub_type}): {sub_desc}")
                
                sections.append("")  # 空行
    
    return "\n".join(sections)


def generate_schema_markdown(schema_data: Dict[str, Any]) -> str:
    """生成完整的 Schema Markdown 文档"""
    
    title = schema_data.get("title", "Schema")
    schema_uri = schema_data.get("$schema", "-")
    comment = schema_data.get("$comment", "")
    properties = schema_data.get("properties", {})
    required_fields = schema_data.get("required", [])
    additional_properties = schema_data.get("additionalProperties", True)
    
    # 构建文档
    lines = [
        f"# {title} Schema 规范",
        "",
        "> 🤖 **自动生成文档** - 本文档由 `scripts/generate_schema_md.py` 自动生成",
        "> ",
        f"> 📄 **源文件**: `schema/coding_dictionary.schema.json`",
        "",
        "---",
        "",
        "## 📋 Schema 信息",
        "",
        f"- **Schema URI**: `{schema_uri}`",
        f"- **标题**: {title}",
    ]
    
    if comment:
        lines.append(f"- **说明**: {comment}")
    
    lines.extend([
        f"- **允许额外属性**: {'❌ 否 (严格模式)' if not additional_properties else '✅ 是'}",
        f"- **必填字段数量**: {len(required_fields)} 个",
        "",
        "---",
        "",
        "## 🔑 字段列表",
        "",
        "| 字段名 | 必填/可选 | 类型 | 说明 | 约束条件 |",
        "|--------|----------|------|------|---------|",
    ])
    
    # 添加字段表格
    lines.append(generate_field_table(properties, required_fields))
    
    lines.extend([
        "",
        "---",
        "",
        "## 📊 必填字段 (Required Fields)",
        "",
        f"以下 **{len(required_fields)}** 个字段为必填：",
        "",
    ])
    
    for field in required_fields:
        prop = properties.get(field, {})
        field_type = get_type_display(prop)
        description = prop.get("description", "-")
        lines.append(f"- **`{field}`** ({field_type}): {description}")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📝 可选字段 (Optional Fields)",
        "",
    ])
    
    optional_fields = [f for f in properties.keys() if f not in required_fields]
    
    if optional_fields:
        lines.append(f"以下 **{len(optional_fields)}** 个字段为可选：")
        lines.append("")
        
        for field in optional_fields:
            prop = properties.get(field, {})
            field_type = get_type_display(prop)
            description = prop.get("description", "-")
            lines.append(f"- **`{field}`** ({field_type}): {description}")
    else:
        lines.append("*无可选字段*")
    
    lines.extend([
        "",
        "---",
        "",
        "## 🎯 枚举类型详解",
        "",
    ])
    
    # 添加枚举详解
    enum_details = generate_enum_details(properties)
    if enum_details:
        lines.append(enum_details)
    else:
        lines.append("*Schema 中无枚举类型*")
    
    lines.extend([
        "",
        "---",
        "",
        "## 🏗️ 复杂类型结构",
        "",
    ])
    
    # 添加嵌套对象说明
    nested_objects = generate_nested_objects(properties)
    if nested_objects:
        lines.append(nested_objects)
    else:
        lines.append("*Schema 中无复杂嵌套类型*")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📚 相关文档",
        "",
        "- [数据结构与字段规范](../../spec/coding_dictionary.spec.md) - 人类撰写的详细规范",
        "- [分类体系规范](../../spec/coding_dictionary_classification.md) - 分类定义",
        "- [README.md](../../README.md) - 项目主文档",
        "",
        "---",
        "",
        "## ⚠️ 注意事项",
        "",
        "1. 本文档由 Schema 自动生成，**请勿手动编辑**",
        "2. 若需修改，请编辑 `schema/coding_dictionary.schema.json`",
        "3. 运行 `python scripts/generate_schema_md.py` 重新生成",
        "4. 详细的使用说明和示例请参考 [coding_dictionary.spec.md](../../spec/coding_dictionary.spec.md)",
        "",
    ])
    
    return "\n".join(lines)


def main():
    """主函数"""
    print("=" * 60)
    print("Schema → Markdown 生成器")
    print("=" * 60)
    
    # 读取 Schema
    print(f"\n📖 读取 Schema: {SCHEMA_FILE}")
    try:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {SCHEMA_FILE}")
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ 错误: JSON 格式错误 - {e}")
        return 1
    
    # 生成 Markdown
    print("📝 生成 Markdown 文档...")
    markdown_content = generate_schema_markdown(schema_data)
    
    # 确保输出目录存在
    SCHEMA_MD_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    print(f"💾 写入文件: {SCHEMA_MD_FILE}")
    with open(SCHEMA_MD_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"\n✅ 成功生成 Schema Markdown 文档!")
    print(f"📄 文件位置: {SCHEMA_MD_FILE}")
    print(f"📊 文档大小: {len(markdown_content)} 字符")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
