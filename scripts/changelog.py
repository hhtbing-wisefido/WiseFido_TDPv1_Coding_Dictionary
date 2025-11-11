# ============================================================
# 新用户请先安装依赖：
#   pip install -r requirements.txt
# ============================================================
"""
CHANGELOG 生成器
基于快照对比生成变更日志
"""
# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401

import json
from datetime import datetime, timezone
from pathlib import Path

SRC = Path("dictionary/coding_terms.json")
OUT = Path("generated/changelog.md")
SNAP = Path("generated/.snapshot.json")


def run():
    """生成 CHANGELOG"""
    if not SRC.exists():
        print(f"[ERR] 缺失文件: {SRC}")
        return
    
    # 加载当前数据
    try:
        items = json.loads(SRC.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] JSON 解析失败: {e}")
        return
    
    current = {it["id"]: it for it in items}
    
    # 加载快照
    prev = {}
    if SNAP.exists():
        try:
            prev = json.loads(SNAP.read_text(encoding="utf-8"))
        except:
            pass
    
    # 对比变化
    added, modified, deprecated = [], [], []
    
    for k, v in current.items():
        if k not in prev:
            added.append(k)
        else:
            if v != prev[k]:
                if v.get("status") == "deprecated" and prev[k].get("status") != "deprecated":
                    deprecated.append(k)
                else:
                    modified.append(k)
    
    # 生成 CHANGELOG
    ts = datetime.now(timezone.utc).isoformat()
    # 移除微秒，只保留到秒
    ts = ts.split('+')[0] + "Z"
    
    if any([added, modified, deprecated]):
        lines = [f"\n## {ts}\n"]
        
        if added:
            lines.append("### Added")
            lines.extend([f"- {i}" for i in added])
            lines.append("")
        
        if modified:
            lines.append("### Modified")
            lines.extend([f"- {i}" for i in modified])
            lines.append("")
        
        if deprecated:
            lines.append("### Deprecated")
            lines.extend([f"- {i}" for i in deprecated])
            lines.append("")
        
        # 追加到 CHANGELOG
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("a", encoding="utf-8") as w:
            w.write("\n".join(lines))
        
        print(f"\n[OK] CHANGELOG updated")
        print(f"  - Added: {len(added)}")
        print(f"  - Modified: {len(modified)}")
        print(f"  - Deprecated: {len(deprecated)}")
    else:
        print("\n[OK] No changes")
    
    # 保存快照
    SNAP.parent.mkdir(parents=True, exist_ok=True)
    with open(SNAP, 'w', encoding='utf-8') as f:
        json.dump(current, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run()
