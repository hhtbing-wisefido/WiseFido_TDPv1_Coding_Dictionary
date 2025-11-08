"""
WiseFido Coding Dictionary 主工具
用法:
  python scripts/tools.py              # 交互菜单
  python scripts/tools.py --validate   # 仅校验
  python scripts/tools.py --generate-md # 仅生成 Markdown
  python scripts/tools.py --changelog  # 仅更新 CHANGELOG
  python scripts/tools.py --all        # 完整流程（校验+生成+更新）
  python scripts/tools.py --stats      # 显示统计信息
  python scripts/tools.py --clean      # 清理临时文件
"""
# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from validate_json import run as run_validate
from generate_md import run as run_md
from changelog import run as run_changelog


def show_stats():
    """显示词条统计信息"""
    src = Path("dictionary/coding_terms.json")
    if not src.exists():
        print(f"[ERR] 缺失文件: {src}")
        return
    
    try:
        items = json.loads(src.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] 读取失败: {e}")
        return
    
    if not isinstance(items, list):
        print("[ERR] JSON 根节点必须是数组")
        return
    
    # 统计分类
    categories = Counter(item.get("category", "未知") for item in items)
    statuses = Counter(item.get("status", "未知") for item in items)
    
    # 统计检测能力
    detection_stats = {"direct": 0, "indirect": 0, "not_detectable": 0, "未标注": 0}
    for item in items:
        detection = item.get("detection", {}).get("radar_60ghz", {})
        detectable = detection.get("detectable", "")
        if detectable == "direct":
            detection_stats["direct"] += 1
        elif detectable == "indirect":
            detection_stats["indirect"] += 1
        elif detectable == "not_detectable":
            detection_stats["not_detectable"] += 1
        else:
            detection_stats["未标注"] += 1
    
    print("\n" + "=" * 60)
    print("  词条统计信息")
    print("=" * 60)
    print(f"\n总词条数: {len(items)}")
    
    print("\n📊 分类分布:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat:20s}: {count:3d}")
    
    print("\n📈 状态分布:")
    for status, count in sorted(statuses.items()):
        print(f"  {status:20s}: {count:3d}")
    
    print("\n🔍 雷达检测能力:")
    for key, count in detection_stats.items():
        print(f"  {key:20s}: {count:3d}")
    
    print("\n" + "=" * 60 + "\n")


def clean_temp():
    """清理临时文件"""
    temp_dir = Path("temp")
    if not temp_dir.exists():
        print("\n[INFO] temp/ 目录不存在，无需清理\n")
        return
    
    # 统计文件
    temp_files = list(temp_dir.glob("*"))
    if not temp_files:
        print("\n[INFO] temp/ 目录为空，无需清理\n")
        return
    
    print(f"\n[INFO] 发现 {len(temp_files)} 个临时文件/目录")
    print("\n将删除以下文件:")
    for f in temp_files:
        print(f"  - {f}")
    
    confirm = input("\n确认删除? (y/N): ").strip().lower()
    if confirm != "y":
        print("已取消\n")
        return
    
    # 删除
    for f in temp_files:
        try:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)
        except Exception as e:
            print(f"[WARN] 删除失败 {f}: {e}")
    
    print(f"\n[OK] 已清理 {len(temp_files)} 个临时文件\n")


def run_all():
    """执行完整流程：校验 -> 生成 Markdown -> 更新 CHANGELOG"""
    print("\n" + "=" * 60)
    print("  执行完整流程")
    print("=" * 60 + "\n")
    
    print("[1/3] 校验 JSON...")
    run_validate()
    
    print("\n[2/3] 生成 Markdown...")
    run_md()
    
    print("\n[3/3] 更新 CHANGELOG...")
    run_changelog()
    
    print("\n" + "=" * 60)
    print("  完整流程执行完成")
    print("=" * 60 + "\n")


def menu():
    """交互式菜单（循环）"""
    while True:
        print("\n" + "=" * 60)
        print("  WiseFido Coding Dictionary Tool")
        print("=" * 60)
        print("1) 校验 JSON")
        print("2) 生成 Markdown")
        print("3) 更新 CHANGELOG")
        print("4) 完整流程（校验+生成+更新）")
        print("5) 显示统计信息")
        print("6) 清理临时文件")
        print("0) 退出")
        print("=" * 60)
        
        choice = input("请选择: ").strip()
        
        if choice == "1":
            run_validate()
        elif choice == "2":
            run_md()
        elif choice == "3":
            run_changelog()
        elif choice == "4":
            run_all()
        elif choice == "5":
            show_stats()
        elif choice == "6":
            clean_temp()
        elif choice == "0":
            print("\n退出\n")
            sys.exit(0)
        else:
            print("\n[ERR] 无效选择\n")
        
        # 等待用户按键继续
        if choice != "0":
            input("\n按 Enter 键继续...")


def parse_args():
    """解析命令行参数"""
    ap = argparse.ArgumentParser(description="WiseFido Dictionary Tool")
    ap.add_argument("--validate", action="store_true", help="校验 JSON")
    ap.add_argument("--generate-md", action="store_true", help="生成 Markdown")
    ap.add_argument("--changelog", action="store_true", help="更新 CHANGELOG")
    ap.add_argument("--all", action="store_true", help="完整流程（校验+生成+更新）")
    ap.add_argument("--stats", action="store_true", help="显示统计信息")
    ap.add_argument("--clean", action="store_true", help="清理临时文件")
    return ap.parse_args()


def main():
    args = parse_args()
    
    # 如果没有任何参数，显示菜单
    if not any([args.validate, args.generate_md, args.changelog, args.all, args.stats, args.clean]):
        return menu()
    
    # 执行命令行参数指定的操作
    if args.all:
        run_all()
    else:
        if args.validate:
            run_validate()
        if args.generate_md:
            run_md()
        if args.changelog:
            run_changelog()
        if args.stats:
            show_stats()
        if args.clean:
            clean_temp()


if __name__ == "__main__":
    main()
