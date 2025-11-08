"""
WiseFido Coding Dictionary 主工具
用法:
  python scripts/tool.py              # 交互菜单
  python scripts/tool.py --validate   # 仅校验
  python scripts/tool.py --generate-md # 仅生成 Markdown
  python scripts/tool.py --changelog  # 仅更新 CHANGELOG
"""
import argparse
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from validate import run as run_validate
from generate_md import run as run_md
from changelog import run as run_changelog


def menu():
    """交互式菜单"""
    print("\n" + "=" * 50)
    print("  WiseFido Coding Dictionary Tool")
    print("=" * 50)
    print("1) 校验 JSON")
    print("2) 生成 Markdown")
    print("3) 更新 CHANGELOG")
    print("0) 退出")
    print("=" * 50)
    
    choice = input("请选择: ").strip()
    
    if choice == "1":
        run_validate()
    elif choice == "2":
        run_md()
    elif choice == "3":
        run_changelog()
    elif choice == "0":
        print("退出")
        sys.exit(0)
    else:
        print("无效选择")


def parse_args():
    """解析命令行参数"""
    ap = argparse.ArgumentParser(description="WiseFido Dictionary Tool")
    ap.add_argument("--validate", action="store_true", help="校验 JSON")
    ap.add_argument("--generate-md", action="store_true", help="生成 Markdown")
    ap.add_argument("--changelog", action="store_true", help="更新 CHANGELOG")
    return ap.parse_args()


def main():
    args = parse_args()
    
    # 如果没有任何参数，显示菜单
    if not any([args.validate, args.generate_md, args.changelog]):
        return menu()
    
    # 执行命令行参数指定的操作
    if args.validate:
        run_validate()
    if args.generate_md:
        run_md()
    if args.changelog:
        run_changelog()


if __name__ == "__main__":
    main()
