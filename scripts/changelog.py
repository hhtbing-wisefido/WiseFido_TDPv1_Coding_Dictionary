# ============================================================
# 新用户请先安装依赖：
#   pip install -r requirements.txt
# ============================================================
"""
CHANGELOG 生成器 (v2.0.0)
基于快照对比生成变更总结报告（精简版）
"""
# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401

import json
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

# 数据源与输出路径
SRC = Path("coding_dictionary/coding_dictionary.json")
OUT = Path("auto_generated_docs/changelog.md")
SNAP = Path("auto_generated_docs/.snapshot.json")


def get_statistics(items):
    """获取统计信息 (v2.0.0 精简版)"""
    systems = Counter()
    
    for item in items:
        # 统计编码系统
        system = item.get("system", "未知")
        if "snomed" in system.lower():
            systems["SNOMED CT"] += 1
        elif "internal" in system.lower():
            systems["Internal"] += 1
        elif "tdp" in system.lower():
            systems["TDP"] += 1
        else:
            systems["其他"] += 1
    
    return systems


def generate_summary_report(items, added_items, modified_items, deprecated_items, prev_count):
    """生成详细的总结报告 (v2.0.0)"""
    current_count = len(items)
    
    lines = []
    lines.append("# Coding Dictionary 变更总结报告 (v2.0.0)")
    lines.append("")
    lines.append(f"**生成日期**: {datetime.now().strftime('%Y年%m月%d日')}")
    lines.append(f"**生成时间**: {datetime.now().strftime('%H:%M:%S')}")
    lines.append("")
    lines.append("**⚠️ DO NOT EDIT MANUALLY / 请勿手动编辑**")
    lines.append("**Auto-generated from**: `scripts/changelog.py`")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 概览部分
    lines.append("## 📊 当前状态概览")
    lines.append("")
    lines.append(f"- **总词条数**: {current_count}")
    if prev_count > 0:
        growth = current_count - prev_count
        growth_rate = (growth / prev_count) * 100 if prev_count > 0 else 0
        lines.append(f"- **较上次**: {'增加' if growth >= 0 else '减少'} {abs(growth)} 个词条 ({growth_rate:+.1f}%)")
    lines.append("")
    
    # 获取统计信息
    systems = get_statistics(items)
    
    # 编码系统分布
    lines.append("### 📋 编码系统分布")
    lines.append("")
    system_display_map = {
        "SNOMED CT": "SNOMED CT (国际医学术语)",
        "Internal": "Internal (内部编码)",
        "TDP": "TDP (协议编码)"
    }
    for system, count in sorted(systems.items(), key=lambda x: -x[1]):
        percentage = (count / current_count) * 100
        system_display = system_display_map.get(system, system)
        lines.append(f"- **{system_display}**: {count}个 ({percentage:.1f}%)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 本次变更详情
    if added_items or modified_items or deprecated_items:
        lines.append("## 📝 本次变更详情")
        lines.append("")
        lines.append(f"**变更时间**: {datetime.now(timezone.utc).isoformat().split('+')[0]}Z")
        lines.append("")
        
        if added_items:
            lines.append(f"### ✨ 新增词条 ({len(added_items)}个)")
            lines.append("")
            for item_key in added_items:
                item = next((it for it in items if f"{it['system']}|{it['code']}" == item_key), None)
                if item:
                    display_name = f"{item.get('display', '?')} / {item.get('display_zh', '?')}"
                    lines.append(f"- `{item_key}` - {display_name}")
            lines.append("")
        
        if modified_items:
            lines.append(f"### 🔄 修改词条 ({len(modified_items)}个)")
            lines.append("")
            for item_key in modified_items:
                item = next((it for it in items if f"{it['system']}|{it['code']}" == item_key), None)
                if item:
                    display_name = f"{item.get('display', '?')} / {item.get('display_zh', '?')}"
                    lines.append(f"- `{item_key}` - {display_name}")
            lines.append("")
        
        if deprecated_items:
            lines.append(f"### ⚠️ 已删除词条 ({len(deprecated_items)}个)")
            lines.append("")
            for item_key in deprecated_items:
                lines.append(f"- `{item_key}`")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # 历史统计
    lines.append("## 📈 历史统计")
    lines.append("")
    lines.append("| 日期 | 总词条数 | 新增 | 修改 | 删除 |")
    lines.append("|------|----------|------|------|------|")
    
    return "\n".join(lines)


def run():
    """生成详细的 CHANGELOG 总结报告 (v2.0.0)"""
    if not SRC.exists():
        print(f"[ERR] 缺失文件: {SRC}")
        return
    
    # 加载当前数据
    try:
        items = json.loads(SRC.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] JSON 解析失败: {e}")
        return
    
    # v2.0.0: 使用 system|code 作为唯一标识
    current = {f"{it['system']}|{it['code']}": it for it in items}
    
    # 加载快照
    prev = {}
    prev_count = 0
    if SNAP.exists():
        try:
            prev = json.loads(SNAP.read_text(encoding="utf-8"))
            prev_count = len(prev)
        except:
            pass
    
    # 对比变化
    added, modified, deprecated = [], [], []
    
    for k, v in current.items():
        if k not in prev:
            added.append(k)
        else:
            # v2.0.0: 只比较4个核心字段
            if (v.get('system') != prev[k].get('system') or
                v.get('code') != prev[k].get('code') or
                v.get('display') != prev[k].get('display') or
                v.get('display_zh') != prev[k].get('display_zh')):
                modified.append(k)
    
    # 检查删除的词条
    for k in prev:
        if k not in current:
            deprecated.append(k)
    
    # 生成完整的总结报告
    report = generate_summary_report(items, added, modified, deprecated, prev_count)
    
    # 如果有变更，追加历史记录
    if any([added, modified, deprecated]):
        ts = datetime.now().strftime('%Y-%m-%d')
        history_line = f"| {ts} | {len(items)} | {len(added)} | {len(modified)} | {len(deprecated)} |"
        
        # 读取现有内容
        existing_content = ""
        if OUT.exists():
            existing_content = OUT.read_text(encoding="utf-8")
        
        # 在历史统计表格后追加新行
        if "## 📈 历史统计" in existing_content:
            parts = existing_content.split("## 📈 历史统计")
            if len(parts) > 1:
                # 找到表格末尾
                table_end = parts[1].find("\n\n")
                if table_end > 0:
                    # 插入新的历史记录
                    parts[1] = parts[1][:table_end] + f"\n{history_line}" + parts[1][table_end:]
                    report = parts[0] + "## 📈 历史统计" + parts[1]
    
    # 写入完整报告
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(report, encoding="utf-8")
    
    print(f"\n[OK] CHANGELOG updated")
    print(f"  - Added: {len(added)}")
    print(f"  - Modified: {len(modified)}")
    print(f"  - Deprecated: {len(deprecated)}")
    print(f"  - Total items: {len(items)}")
    
    # 保存快照
    SNAP.parent.mkdir(parents=True, exist_ok=True)
    with open(SNAP, 'w', encoding='utf-8') as f:
        json.dump(current, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run()
