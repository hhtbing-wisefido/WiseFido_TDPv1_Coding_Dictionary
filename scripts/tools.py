"""
WiseFido Coding Dictionary 主工具
用法:
  python scripts/tools.py              # 交互菜单
  python scripts/tools.py -v, --validate   # 仅校验
  python scripts/tools.py -g, --generate-md # 仅生成 Markdown
  python scripts/tools.py -c, --changelog  # 仅更新 CHANGELOG
  python scripts/tools.py -a, --all        # 完整流程（校验+生成+更新）
  python scripts/tools.py -s, --stats      # 显示统计信息
  python scripts/tools.py -t, --test       # 运行测试套件
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


def run_tests():
    """运行测试套件"""
    print("\n" + "=" * 60)
    print("  测试套件")
    print("=" * 60 + "\n")
    
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
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    # 测试 1: 检查必填字段
    print("[测试 1/6] 检查必填字段...")
    required_fields = ["id", "code", "system", "display", "display_zh", "category", "status", "version"]
    missing_fields = []
    for item in items:
        for field in required_fields:
            if field not in item or not item[field]:
                missing_fields.append(f"词条 {item.get('id', '未知')} 缺少字段: {field}")
    
    total_tests += 1
    if not missing_fields:
        print("  ✅ 通过: 所有词条包含必填字段")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(missing_fields)} 个缺失字段")
        for err in missing_fields[:5]:  # 只显示前5个
            print(f"     - {err}")
        if len(missing_fields) > 5:
            print(f"     ... 还有 {len(missing_fields) - 5} 个错误")
        failed_tests += 1
    
    # 测试 2: 检查 ID 格式
    print("\n[测试 2/6] 检查 ID 格式...")
    invalid_ids = []
    for item in items:
        item_id = item.get("id", "")
        # ID 格式应为 prefix:code 或 prefix:protocol://path
        if ":" not in item_id:
            invalid_ids.append(f"ID 格式错误: {item_id} (应包含冒号,如 snomed:123456)")
        else:
            # 分离前缀和代码部分
            parts = item_id.split(":", 1)
            if len(parts) != 2 or not parts[0] or not parts[1]:
                invalid_ids.append(f"ID 格式错误: {item_id} (格式应为 prefix:code)")
    
    total_tests += 1
    if not invalid_ids:
        print("  ✅ 通过: 所有 ID 格式正确")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(invalid_ids)} 个格式错误的 ID")
        for err in invalid_ids[:5]:
            print(f"     - {err}")
        if len(invalid_ids) > 5:
            print(f"     ... 还有 {len(invalid_ids) - 5} 个错误")
        failed_tests += 1
    
    # 测试 3: 检查重复 ID
    print("\n[测试 3/6] 检查重复 ID...")
    ids = [item.get("id") for item in items]
    id_counts = Counter(ids)
    duplicates = [item_id for item_id, count in id_counts.items() if count > 1]
    
    total_tests += 1
    if not duplicates:
        print("  ✅ 通过: 无重复 ID")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(duplicates)} 个重复 ID")
        for dup_id in duplicates[:5]:
            print(f"     - {dup_id} (出现 {id_counts[dup_id]} 次)")
        if len(duplicates) > 5:
            print(f"     ... 还有 {len(duplicates) - 5} 个重复")
        failed_tests += 1
    
    # 测试 4: 检查 code + system 唯一性
    print("\n[测试 4/6] 检查 code+system 唯一性...")
    code_system_pairs = [(item.get("code"), item.get("system")) for item in items]
    pair_counts = Counter(code_system_pairs)
    dup_pairs = [(code, system) for (code, system), count in pair_counts.items() if count > 1]
    
    total_tests += 1
    if not dup_pairs:
        print("  ✅ 通过: code+system 组合唯一")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(dup_pairs)} 个重复的 code+system 组合")
        for code, system in dup_pairs[:5]:
            print(f"     - code={code}, system={system} (出现 {pair_counts[(code, system)]} 次)")
        if len(dup_pairs) > 5:
            print(f"     ... 还有 {len(dup_pairs) - 5} 个重复")
        failed_tests += 1
    
    # 测试 5: 检查分类有效性
    print("\n[测试 5/6] 检查分类有效性...")
    valid_categories = [
        "posture_codes",
        "motion_codes",
        "physiological_codes",
        "disorder_condition_codes",
        "safety_alert_codes",
        "tag"
    ]
    invalid_categories = []
    for item in items:
        category = item.get("category", "")
        if category not in valid_categories:
            invalid_categories.append(f"词条 {item.get('id')} 使用了无效分类: {category}")
    
    total_tests += 1
    if not invalid_categories:
        print("  ✅ 通过: 所有分类有效")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(invalid_categories)} 个无效分类")
        for err in invalid_categories[:5]:
            print(f"     - {err}")
        if len(invalid_categories) > 5:
            print(f"     ... 还有 {len(invalid_categories) - 5} 个错误")
        failed_tests += 1
    
    # 测试 6: 检查版本号格式
    print("\n[测试 6/6] 检查版本号格式...")
    invalid_versions = []
    import re
    version_pattern = re.compile(r'^\d+\.\d+\.\d+$')
    for item in items:
        version = item.get("version", "")
        if not version_pattern.match(version):
            invalid_versions.append(f"词条 {item.get('id')} 版本号格式错误: {version} (应为 X.Y.Z)")
    
    total_tests += 1
    if not invalid_versions:
        print("  ✅ 通过: 所有版本号格式正确")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(invalid_versions)} 个格式错误的版本号")
        for err in invalid_versions[:5]:
            print(f"     - {err}")
        if len(invalid_versions) > 5:
            print(f"     ... 还有 {len(invalid_versions) - 5} 个错误")
        failed_tests += 1
    
    # 测试总结
    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)
    print(f"总测试数: {total_tests}")
    print(f"✅ 通过: {passed_tests}")
    print(f"❌ 失败: {failed_tests}")
    
    if failed_tests == 0:
        print("\n🎉 所有测试通过!")
    else:
        print(f"\n⚠️  有 {failed_tests} 个测试失败,请检查并修复")
    
    print("=" * 60 + "\n")


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
        print("7) 运行测试套件 🧪")
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
        elif choice == "7":
            run_tests()
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
    ap.add_argument("-v", "--validate", action="store_true", help="校验 JSON")
    ap.add_argument("-g", "--generate-md", action="store_true", help="生成 Markdown")
    ap.add_argument("-c", "--changelog", action="store_true", help="更新 CHANGELOG")
    ap.add_argument("-a", "--all", action="store_true", help="完整流程（校验+生成+更新）")
    ap.add_argument("-s", "--stats", action="store_true", help="显示统计信息")
    ap.add_argument("--clean", action="store_true", help="清理临时文件")
    ap.add_argument("-t", "--test", action="store_true", help="运行测试套件")
    return ap.parse_args()


def main():
    args = parse_args()
    
    # 如果没有任何参数，显示菜单
    if not any([args.validate, args.generate_md, args.changelog, args.all, args.stats, args.clean, args.test]):
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
        if args.test:
            run_tests()


if __name__ == "__main__":
    main()
