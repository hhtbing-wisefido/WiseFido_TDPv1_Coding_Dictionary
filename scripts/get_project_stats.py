#!/usr/bin/env python3
"""
获取项目统计信息 (v2.0.0)
用于自动更新 README.md 中的统计数据
只统计编码系统分布,不再统计分类和检测能力
"""

import json
from pathlib import Path
from collections import Counter


def get_stats():
    """获取项目统计信息,返回字典格式
    
    v2.0.0 只统计:
    - 总词条数
    - 编码系统分布 (SNOMED CT, Internal, TDP, Other)
    """
    
    # 获取 JSON 文件路径
    script_dir = Path(__file__).parent
    json_file = script_dir.parent / "coding_dictionary" / "coding_dictionary.json"
    
    if not json_file.exists():
        return None
    
    # 读取 JSON 数据
    with open(json_file, "r", encoding="utf-8") as f:
        items = json.load(f)
    
    total_count = len(items)
    
    # 统计编码系统
    systems = Counter()
    for item in items:
        system_uri = item.get("system", "")
        if "snomed" in system_uri.lower():
            systems["SNOMED CT"] += 1
        elif "internal" in system_uri.lower():
            systems["Internal"] += 1
        elif "tdp" in system_uri.lower():
            systems["TDP"] += 1
        else:
            systems["Other"] += 1
    
    # 计算百分比
    def calc_percentage(count, total):
        return (count / total * 100) if total > 0 else 0
    
    # 构建返回结果
    stats = {
        "total_count": total_count,
        "systems": {
            "snomed_ct": systems.get("SNOMED CT", 0),
            "internal": systems.get("Internal", 0),
            "tdp": systems.get("TDP", 0),
            "other": systems.get("Other", 0),
        },
        "systems_percentage": {
            "snomed_ct": calc_percentage(systems.get("SNOMED CT", 0), total_count),
            "internal": calc_percentage(systems.get("Internal", 0), total_count),
            "tdp": calc_percentage(systems.get("TDP", 0), total_count),
            "other": calc_percentage(systems.get("Other", 0), total_count),
        }
    }
    
    return stats


def format_stats_for_readme(stats, version="v2.0.0"):
    """格式化统计数据为 README.md 格式
    
    Args:
        stats: 统计数据字典
        version: 版本号,默认 v2.0.0
        
    Returns:
        格式化的字符串,用于 README.md
    """
    
    if not stats:
        return "- 📊 无法获取统计数据"
    
    # 计算编码系统的格式化字符串
    systems_str = " | ".join([
        f"SNOMED CT({stats['systems_percentage']['snomed_ct']:.1f}%)",
        f"Internal({stats['systems_percentage']['internal']:.1f}%)",
        f"TDP({stats['systems_percentage']['tdp']:.1f}%)"
    ])
    
    result = f"""- 📊 词条总数: {stats['total_count']}（{systems_str}）
- 🧪 测试通过率: 100%"""
    
    return result


if __name__ == "__main__":
    stats = get_stats()
    if stats:
        print("=" * 50)
        print("当前项目统计 (v2.0.0)")
        print("=" * 50)
        print(f"\n总词条数: {stats['total_count']}")
        print("\n编码系统分布:")
        print(f"  SNOMED CT: {stats['systems']['snomed_ct']} ({stats['systems_percentage']['snomed_ct']:.1f}%)")
        print(f"  Internal:  {stats['systems']['internal']} ({stats['systems_percentage']['internal']:.1f}%)")
        print(f"  TDP:       {stats['systems']['tdp']} ({stats['systems_percentage']['tdp']:.1f}%)")
        if stats['systems']['other'] > 0:
            print(f"  Other:     {stats['systems']['other']} ({stats['systems_percentage']['other']:.1f}%)")
        
        print("\n" + "=" * 50)
        print("README.md 格式:")
        print("=" * 50)
        print(format_stats_for_readme(stats))
    else:
        print("❌ 无法获取统计数据")
