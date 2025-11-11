# 导入配置模块（必须在其他导入之前，确保 __pycache__ 统一生成到 temp 目录）
import _config  # noqa: F401
from _config import (
    DICTIONARY_FILE,
    TEMP_DIR,
    VALID_CATEGORIES,
    VALID_STATUSES,
    REQUIRED_FIELDS,
    VERSION_PATTERN,
    MAX_ERROR_DISPLAY
)

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from tqdm import tqdm

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from validate_json import run as run_validate
from generate_md import run as run_md
from changelog import run as run_changelog


# 错误处理辅助函数
def safe_load_json(file_path):
    """安全加载 JSON 文件，带完整错误处理"""
    src = Path(file_path)
    
    if not src.exists():
        print(f"\n[ERR] 文件不存在: {src}")
        print(f"[提示] 请确保 {file_path} 文件存在")
        return None
    
    try:
        content = src.read_text(encoding="utf-8")
        items = json.loads(content)
        if not isinstance(items, list):
            print(f"\n[ERR] JSON 格式错误: 根节点必须是数组")
            print(f"[提示] 当前根节点类型: {type(items).__name__}")
            return None
        return items
    except json.JSONDecodeError as e:
        print(f"\n[ERR] JSON 解析失败")
        print(f"[详细] 第 {e.lineno} 行, 第 {e.colno} 列: {e.msg}")
        print(f"[提示] 请使用 JSON 验证工具检查语法")
        return None
    except UnicodeDecodeError as e:
        print(f"\n[ERR] 文件编码错误: {e}")
        print(f"[提示] 请确保文件使用 UTF-8 编码保存")
        return None
    except Exception as e:
        print(f"\n[ERR] 读取文件失败: {e}")
        return None


def show_stats():
    # Show coding term statistics
    items = safe_load_json(str(DICTIONARY_FILE))
    if items is None:
        return
    
    # 统计分类
    categories = Counter()
    statuses = Counter()
    detection_stats = {"direct": 0, "indirect": 0, "not_detectable": 0, "未标注": 0}
    for item in tqdm(items, desc="统计词条", ncols=70):
        categories[item.get("category", "未知")] += 1
        statuses[item.get("status", "未知")] += 1
        detection = item.get("detection", {}).get("radar_60ghz", {})
        detectable = detection.get("detectable", "")
        if detectable == "direct":
            detection_stats["direct"] += 1
        elif detectable == "indirect":
            detection_stats["indirect"] += 1
        elif detectable == "not_detectable":
            detection_stats["not_detectable"] += 1
        # WiseFido Coding Dictionary Main Tool
        # Usage:
        #   python scripts/tools.py              # Interactive menu
        #   python scripts/tools.py -v, --validate   # Validate only
        #   python scripts/tools.py -g, --generate-md # Generate Markdown only
        #   python scripts/tools.py -c, --changelog  # Update CHANGELOG only
        #   python scripts/tools.py -a, --all        # Full workflow (validate+generate+update)
        #   python scripts/tools.py -s, --stats      # Show statistics
        #   python scripts/tools.py -t, --test       # Run test suite
        #   python scripts/tools.py --clean          # Clean temp files
        # ------------------------------------------------------------
        # New users: Please install dependencies first:
        #   pip install -r requirements.txt
        # ------------------------------------------------------------
    print("\n🔍 雷达检测能力:")
    for key, count in detection_stats.items():
        print(f"  {key:20s}: {count:3d}")
    
    print("\n" + "=" * 60 + "\n")


def run_tests():
    # Run test suite
    print("\n" + "=" * 60)
    print("  测试套件")
    print("=" * 60 + "\n")
    
    items = safe_load_json(str(DICTIONARY_FILE))
    if items is None:
        return
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    # 测试 1: 检查必填字段
    print("[测试 1/6] 检查必填字段...")
    missing_fields = []
    for item in tqdm(items, desc="字段检查", ncols=70):
        for field in REQUIRED_FIELDS:
            if field not in item or not item[field]:
                missing_fields.append(f"词条 {item.get('id', '未知')} 缺少字段: {field}")
    
    total_tests += 1
    if not missing_fields:
        print("  ✅ 通过: 所有词条包含必填字段")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(missing_fields)} 个缺失字段")
        for err in missing_fields[:MAX_ERROR_DISPLAY]:
            print(f"     - {err}")
        if len(missing_fields) > MAX_ERROR_DISPLAY:
            print(f"     ... 还有 {len(missing_fields) - MAX_ERROR_DISPLAY} 个错误")
        failed_tests += 1
    
    # 测试 2: 检查 ID 格式
    print("\n[测试 2/6] 检查 ID 格式...")
    invalid_ids = []
    for item in tqdm(items, desc="ID格式检查", ncols=70):
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
        for err in invalid_ids[:MAX_ERROR_DISPLAY]:
            print(f"     - {err}")
        if len(invalid_ids) > MAX_ERROR_DISPLAY:
            print(f"     ... 还有 {len(invalid_ids) - MAX_ERROR_DISPLAY} 个错误")
        failed_tests += 1
    
    # 测试 3: 检查重复 ID
    print("\n[测试 3/6] 检查重复 ID...")
    ids = [item.get("id") for item in tqdm(items, desc="重复ID检查", ncols=70)]
    id_counts = Counter(ids)
    duplicates = [item_id for item_id, count in id_counts.items() if count > 1]
    
    total_tests += 1
    if not duplicates:
        print("  ✅ 通过: 无重复 ID")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(duplicates)} 个重复 ID")
        for dup_id in duplicates[:MAX_ERROR_DISPLAY]:
            print(f"     - {dup_id} (出现 {id_counts[dup_id]} 次)")
        if len(duplicates) > MAX_ERROR_DISPLAY:
            print(f"     ... 还有 {len(duplicates) - MAX_ERROR_DISPLAY} 个重复")
        failed_tests += 1
    
    # 测试 4: 检查 code + system 唯一性
    print("\n[测试 4/6] 检查 code+system 唯一性...")
    code_system_pairs = [(item.get("code"), item.get("system")) for item in tqdm(items, desc="code+system检查", ncols=70)]
    pair_counts = Counter(code_system_pairs)
    dup_pairs = [(code, system) for (code, system), count in pair_counts.items() if count > 1]
    
    total_tests += 1
    if not dup_pairs:
        print("  ✅ 通过: code+system 组合唯一")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(dup_pairs)} 个重复的 code+system 组合")
        for code, system in dup_pairs[:MAX_ERROR_DISPLAY]:
            print(f"     - code={code}, system={system} (出现 {pair_counts[(code, system)]} 次)")
        if len(dup_pairs) > MAX_ERROR_DISPLAY:
            print(f"     ... 还有 {len(dup_pairs) - MAX_ERROR_DISPLAY} 个重复")
        failed_tests += 1
    
    # 测试 5: 检查分类有效性
    print("\n[测试 5/6] 检查分类有效性...")
    invalid_categories = []
    for item in tqdm(items, desc="分类有效性检查", ncols=70):
        category = item.get("category", "")
        if category not in VALID_CATEGORIES:
            invalid_categories.append(f"词条 {item.get('id')} 使用了无效分类: {category}")
    
    total_tests += 1
    if not invalid_categories:
        print("  ✅ 通过: 所有分类有效")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(invalid_categories)} 个无效分类")
        for err in invalid_categories[:MAX_ERROR_DISPLAY]:
            print(f"     - {err}")
        if len(invalid_categories) > MAX_ERROR_DISPLAY:
            print(f"     ... 还有 {len(invalid_categories) - MAX_ERROR_DISPLAY} 个错误")
        failed_tests += 1
    
    # 测试 6: 检查版本号格式
    print("\n[测试 6/6] 检查版本号格式...")
    invalid_versions = []
    import re
    version_pattern = re.compile(VERSION_PATTERN)
    for item in tqdm(items, desc="版本号格式检查", ncols=70):
        version = item.get("version", "")
        if not version_pattern.match(version):
            invalid_versions.append(f"词条 {item.get('id')} 版本号格式错误: {version} (应为 X.Y.Z)")
    
    total_tests += 1
    if not invalid_versions:
        print("  ✅ 通过: 所有版本号格式正确")
        passed_tests += 1
    else:
        print(f"  ❌ 失败: 发现 {len(invalid_versions)} 个格式错误的版本号")
        for err in invalid_versions[:MAX_ERROR_DISPLAY]:
            print(f"     - {err}")
        if len(invalid_versions) > MAX_ERROR_DISPLAY:
            print(f"     ... 还有 {len(invalid_versions) - MAX_ERROR_DISPLAY} 个错误")
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
    # Clean temp files
    if not TEMP_DIR.exists():
        print("\n[INFO] temp/ 目录不存在，无需清理\n")
        return
    
    # 统计文件
    temp_files = list(TEMP_DIR.glob("*"))
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
    # Run full workflow: validate -> generate Markdown -> update CHANGELOG
    print("\n" + "=" * 60)
    print("  执行完整流程")
    print("=" * 60 + "\n")
    
    # 步骤 1: 校验 JSON
    print("[1/3] 校验 JSON...")
    from time import sleep
    for _ in tqdm(range(30), desc="校验中", ncols=70):
        sleep(0.01)
    try:
        run_validate()
    except SystemExit:
        print("\n[ERR] 校验失败，流程已中止")
        print("[提示] 请修复错误后重新运行")
        return
    except Exception as e:
        print(f"\n[ERR] 校验过程出错: {e}")
        print("[提示] 流程已中止")
        return
    # 步骤 2: 生成 Markdown
    print("\n[2/3] 生成 Markdown...")
    for _ in tqdm(range(30), desc="生成 Markdown", ncols=70):
        sleep(0.01)
    try:
        run_md()
    except Exception as e:
        print(f"\n[ERR] 生成 Markdown 失败: {e}")
        print("[提示] 流程已中止")
        return
    # 步骤 3: 更新 CHANGELOG
    print("\n[3/3] 更新 CHANGELOG...")
    for _ in tqdm(range(30), desc="更新 CHANGELOG", ncols=70):
        sleep(0.01)
    try:
        run_changelog()
    except Exception as e:
        print(f"\n[ERR] 更新 CHANGELOG 失败: {e}")
        print("[提示] 流程已中止")
        return
    print("\n" + "=" * 60)
    print("  完整流程执行完成")
    print("=" * 60 + "\n")


def menu():
    # Interactive menu (loop)
    while True:
        print("\n" + "=" * 60)
        print("  WiseFido Coding Dictionary Tool")
        print("=" * 60)
        print("1) 校验 JSON               - 验证词条数据格式和规范")
        print("2) 生成 Markdown           - 生成可读的文档表格")
        print("3) 更新 CHANGELOG          - 记录词条变更历史")
        print("4) 完整流程（校验+生成+更新） - 一键执行所有操作")
        print("5) 显示统计信息             - 查看词条分类和数量")
        print("6) 清理临时文件             - 删除 temp 目录内容")
        print("7) 运行测试套件 🧪          - 执行 6 项数据质量测试")
        print("0) 退出                    - 关闭程序")
        print("=" * 60)
        
        choice = input("请选择: ").strip()
        if not choice.isdigit() or int(choice) not in range(0, 8):
            print("\n[ERR] 无效选择，请输入 0-7 之间的数字。\n")
            continue
        if choice == "1":
            print("\n[提示] 正在校验 JSON ...")
            run_validate()
        elif choice == "2":
            print("\n[提示] 正在生成 Markdown ...")
            run_md()
        elif choice == "3":
            print("\n[提示] 正在更新 CHANGELOG ...")
            run_changelog()
        elif choice == "4":
            print("\n[提示] 正在执行完整流程 ...")
            run_all()
        elif choice == "5":
            print("\n[提示] 正在统计信息 ...")
            show_stats()
        elif choice == "6":
            print("\n[提示] 正在清理临时文件 ...")
            clean_temp()
        elif choice == "7":
            print("\n[提示] 正在运行测试套件 ...")
            run_tests()
        elif choice == "0":
            print("\n退出\n")
            sys.exit(0)
        # 等待用户按键继续
        if choice != "0":
            input("\n按 Enter 键继续...")


def parse_args():
    # Parse command line arguments
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
