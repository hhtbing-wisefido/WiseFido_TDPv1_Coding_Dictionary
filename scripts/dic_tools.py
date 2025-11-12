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
from datetime import datetime

# 依赖检查与自动安装
try:
    from tqdm import tqdm
except ImportError:
    print("\n" + "=" * 70)
    print("  ⚠️  缺少必需的 Python 依赖包")
    print("=" * 70)
    print("\n[错误] 未安装 tqdm 模块")
    print("\n[解决方案] 正在尝试自动安装...")
    
    import subprocess
    try:
        # 使用当前 Python 解释器安装依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
        print("\n[成功] tqdm 已安装，请重新运行脚本")
        print("\n" + "=" * 70)
        sys.exit(0)
    except subprocess.CalledProcessError:
        print("\n[失败] 自动安装失败，请手动执行：")
        print("\n  {} -m pip install -r requirements.txt".format(sys.executable))
        print("\n或：")
        print("\n  {} -m pip install tqdm".format(sys.executable))
        print("\n" + "=" * 70)
        sys.exit(1)

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
    systems = Counter()
    detection_stats = {"direct": 0, "indirect": 0, "not_detectable": 0, "未标注": 0}
    
    print("\n[INFO] 正在统计词条数据...")
    for item in tqdm(items, desc="统计词条", ncols=70):
        categories[item.get("category", "未知")] += 1
        statuses[item.get("status", "未知")] += 1
        
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
        
        # 统计检测能力
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
    
    # 中英文对照映射
    CATEGORY_NAMES_ZH = {
        "posture_codes": "姿态编码 (Posture Codes)",
        "motion_codes": "运动编码 (Motion Codes)",
        "physiological_codes": "生理指标 (Physiological Codes)",
        "disorder_condition_codes": "疾病状况 (Disorder & Condition Codes)",
        "safety_alert_codes": "安全警报 (Safety & Alert Codes)",
        "tag": "标签 (Tag)"
    }
    
    SYSTEM_NAMES_ZH = {
        "http://snomed.info/sct": "SNOMED CT",
        "internal://tag": "Internal Tag",
        "internal://motion_state": "Internal Motion",
        "internal://posture": "Internal Posture",
        "internal://danger_level": "Internal Danger Level",
        "tdp://danger_level": "TDP Danger Level"
    }
    
    STATUS_NAMES_ZH = {
        "active": "活动 (Active)",
        "deprecated": "已弃用 (Deprecated)",
        "draft": "草稿 (Draft)"
    }
    
    DETECTION_NAMES_ZH = {
        "direct": "直接检测 (Direct)",
        "indirect": "间接检测 (Indirect)",
        "not_detectable": "无法检测 (Not Detectable)",
        "未标注": "未标注 (Not Annotated)"
    }
    
    print("\n" + "=" * 60)
    print("  📊 词条统计信息")
    print("=" * 60)
    print(f"\n✅ 总词条数: {len(items)}")
    
    print("\n📂 分类分布:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        percentage = (count / len(items)) * 100
        cat_display = CATEGORY_NAMES_ZH.get(cat, cat)
        print(f"  {cat_display:45s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\n📋 编码系统分布:")
    SYSTEM_DISPLAY_ZH = {
        "SNOMED CT": "SNOMED CT (国际医学术语)",
        "Internal": "Internal (内部编码)",
        "TDP": "TDP (协议编码)",
        "其他": "其他 (Other)"
    }
    for system, count in sorted(systems.items(), key=lambda x: -x[1]):
        percentage = (count / len(items)) * 100
        system_display = SYSTEM_DISPLAY_ZH.get(system, system)
        print(f"  {system_display:45s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\n📈 状态分布:")
    for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
        percentage = (count / len(items)) * 100
        status_display = STATUS_NAMES_ZH.get(status, status)
        print(f"  {status_display:45s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\n🔍 雷达检测能力:")
    for key, count in detection_stats.items():
        percentage = (count / len(items)) * 100 if count > 0 else 0
        detection_display = DETECTION_NAMES_ZH.get(key, key)
        print(f"  {detection_display:45s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\n" + "=" * 60)


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
    print("\n" + "=" * 60)
    print("  清理临时文件")
    print("=" * 60)
    
    if not TEMP_DIR.exists():
        print("\n[INFO] temp/ 目录不存在，无需清理")
        print("=" * 60)
        return
    
    # 统计文件
    temp_files = list(TEMP_DIR.glob("*"))
    if not temp_files:
        print("\n[INFO] temp/ 目录为空，无需清理")
        print("=" * 60)
        return
    
    print(f"\n[INFO] 发现 {len(temp_files)} 个临时文件/目录")
    print("\n将删除以下文件:")
    for f in temp_files:
        print(f"  - {f.name}")
    
    confirm = input("\n⚠️  确认删除? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y", "是"]:
        print("\n[INFO] 已取消清理操作")
        print("=" * 60)
        return
    
    # 删除
    deleted_count = 0
    for f in temp_files:
        try:
            if f.is_file():
                f.unlink()
                deleted_count += 1
            elif f.is_dir():
                shutil.rmtree(f)
                deleted_count += 1
        except Exception as e:
            print(f"[WARN] 删除失败 {f.name}: {e}")
    
    print(f"\n[INFO] ✅ 已清理 {deleted_count} 个临时文件")
    print("=" * 60)


def search_coding():
    """搜索词条"""
    print("\n" + "=" * 60)
    print("  搜索词条")
    print("=" * 60)
    
    items = safe_load_json(str(DICTIONARY_FILE))
    if items is None:
        return
    
    print("\n请选择搜索方式：")
    print("1) 按 ID 搜索")
    print("2) 按 code 搜索")
    print("3) 按 display (英文名) 搜索")
    print("4) 按 display_zh (中文名) 搜索")
    print("5) 按分类搜索")
    print("0) 返回主菜单")
    
    choice = input("\n👉 请输入选项: ").strip()
    
    if choice == "0":
        return
    
    keyword = input("👉 请输入搜索关键词: ").strip()
    if not keyword:
        print("[提示] 搜索关键词不能为空")
        return
    
    results = []
    
    if choice == "1":
        results = [item for item in items if keyword.lower() in item.get("id", "").lower()]
    elif choice == "2":
        results = [item for item in items if keyword.lower() in item.get("code", "").lower()]
    elif choice == "3":
        results = [item for item in items if keyword.lower() in item.get("display", "").lower()]
    elif choice == "4":
        results = [item for item in items if keyword in item.get("display_zh", "")]
    elif choice == "5":
        results = [item for item in items if keyword.lower() in item.get("category", "").lower()]
    else:
        print("[提示] 无效的选项")
        return
    
    if not results:
        print(f"\n[INFO] 未找到匹配 '{keyword}' 的词条")
        return
    
    print(f"\n[INFO] 找到 {len(results)} 个匹配的词条：")
    print("-" * 60)
    for idx, item in enumerate(results, 1):
        print(f"{idx}. {item.get('id')} - {item.get('display_zh')} ({item.get('display')})")
    print("-" * 60)
    
    view_choice = input("\n👉 输入词条编号查看详情 (直接回车返回): ").strip()
    if view_choice.isdigit():
        idx = int(view_choice) - 1
        if 0 <= idx < len(results):
            view_coding_detail(results[idx])


def view_coding_detail(item=None):
    """查看词条详情"""
    if item is None:
        print("\n" + "=" * 60)
        print("  查看词条详情")
        print("=" * 60)
        
        items = safe_load_json(str(DICTIONARY_FILE))
        if items is None:
            return
        
        coding_id = input("\n👉 请输入词条 ID: ").strip()
        if not coding_id:
            print("[提示] ID 不能为空")
            return
        
        item = next((i for i in items if i.get("id") == coding_id), None)
        if not item:
            print(f"[INFO] 未找到 ID 为 '{coding_id}' 的词条")
            return
    
    print("\n" + "=" * 60)
    print("  词条详细信息")
    print("=" * 60)
    print(f"ID:           {item.get('id')}")
    print(f"代码:         {item.get('code')}")
    print(f"系统:         {item.get('system')}")
    print(f"英文名称:     {item.get('display')}")
    print(f"中文名称:     {item.get('display_zh')}")
    print(f"分类:         {item.get('category')}")
    print(f"状态:         {item.get('status')}")
    print(f"版本:         {item.get('version')}")
    
    if item.get('description'):
        print(f"英文描述:     {item.get('description')}")
    if item.get('description_zh'):
        print(f"中文描述:     {item.get('description_zh')}")
    if item.get('synonyms'):
        print(f"英文同义词:   {', '.join(item.get('synonyms'))}")
    if item.get('synonyms_zh'):
        print(f"中文同义词:   {', '.join(item.get('synonyms_zh'))}")
    if item.get('source_refs'):
        refs = item.get('source_refs')
        if isinstance(refs, list) and refs:
            print(f"来源参考:")
            for ref in refs:
                if isinstance(ref, dict):
                    print(f"  - 文件: {ref.get('file', 'N/A')}, 章节: {ref.get('section', 'N/A')}")
                else:
                    print(f"  - {ref}")
    if item.get('detection'):
        print(f"检测能力:")
        for sensor, info in item.get('detection', {}).items():
            if isinstance(info, dict):
                detectable = info.get('detectable', 'N/A')
                method = info.get('method', 'N/A')
                confidence = info.get('confidence', 'N/A')
                print(f"  - {sensor}:")
                print(f"      可检测性: {detectable}")
                print(f"      方法: {method}")
                print(f"      可信度: {confidence}")
            else:
                print(f"  - {sensor}: {info}")
    print("=" * 60)


def backup_data():
    """备份数据"""
    print("\n" + "=" * 60)
    print("  备份词条数据")
    print("=" * 60)
    
    src = Path(DICTIONARY_FILE)
    if not src.exists():
        print(f"[ERR] 源文件不存在: {src}")
        return
    
    # 创建备份目录
    backup_dir = Path("auto_backup")
    backup_dir.mkdir(exist_ok=True)
    
    # 生成备份文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"coding_dictionary_backup_{timestamp}.json"
    
    try:
        shutil.copy2(src, backup_file)
        print(f"\n[INFO] ✅ 备份成功！")
        print(f"[INFO] 备份文件: {backup_file}")
        print(f"[INFO] 文件大小: {backup_file.stat().st_size / 1024:.2f} KB")
    except Exception as e:
        print(f"[ERR] 备份失败: {e}")


def restore_data():
    """恢复数据"""
    print("\n" + "=" * 60)
    print("  恢复词条数据")
    print("=" * 60)
    
    backup_dir = Path("auto_backup")
    if not backup_dir.exists() or not list(backup_dir.glob("*.json")):
        print("[INFO] 没有找到备份文件")
        return
    
    # 列出所有备份文件
    backups = sorted(backup_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    print("\n可用的备份文件：")
    print("-" * 60)
    for idx, backup in enumerate(backups, 1):
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        size_kb = backup.stat().st_size / 1024
        print(f"{idx}. {backup.name}")
        print(f"   时间: {mtime.strftime('%Y-%m-%d %H:%M:%S')} | 大小: {size_kb:.2f} KB")
    print("-" * 60)
    
    choice = input("\n👉 请选择要恢复的备份编号 (0 取消): ").strip()
    if not choice.isdigit() or choice == "0":
        print("[INFO] 已取消恢复操作")
        return
    
    idx = int(choice) - 1
    if idx < 0 or idx >= len(backups):
        print("[ERR] 无效的编号")
        return
    
    selected_backup = backups[idx]
    
    # 二次确认
    confirm = input(f"\n⚠️  确认要从 '{selected_backup.name}' 恢复数据吗？当前数据将被覆盖！(yes/no): ").strip().lower()
    if confirm not in ["yes", "y", "是"]:
        print("[INFO] 已取消恢复操作")
        return
    
    # 先备份当前数据
    print("\n[INFO] 正在备份当前数据...")
    backup_data()
    
    # 恢复数据
    try:
        shutil.copy2(selected_backup, DICTIONARY_FILE)
        print(f"\n[INFO] ✅ 数据恢复成功！")
        print(f"[INFO] 已从 '{selected_backup.name}' 恢复")
    except Exception as e:
        print(f"[ERR] 恢复失败: {e}")


def get_system_short(system: str) -> str:
    """将 system URI 转换为简短的标识符"""
    if not system:
        return "unknown"
    
    if system.startswith("http://") or system.startswith("https://"):
        parts = system.replace("http://", "").replace("https://", "").split("/")
        domain = parts[0]
        if "snomed" in domain.lower():
            return "snomed"
        return domain.split(".")[0] if "." in domain else domain
    
    if "://" in system:
        protocol = system.split("://")[0]
        return protocol
    
    return system.split("/")[-1] if "/" in system else system


def add_coding_entry():
    """交互式添加单个词条"""
    print("\n" + "=" * 60)
    print("  添加新词条")
    print("=" * 60)
    
    items = safe_load_json(str(DICTIONARY_FILE))
    if items is None:
        return
    
    # 先备份
    print("\n[INFO] 自动备份当前数据...")
    backup_data()
    
    print("\n请输入词条信息（输入 q 取消）:")
    print("-" * 60)
    
    # 输入编码系统
    print("\n编码系统选择:")
    print("1) SNOMED CT (http://snomed.info/sct)")
    print("2) Internal (internal://)")
    print("3) TDP (tdp://)")
    print("4) 自定义")
    
    system_choice = input("👉 请选择编码系统 (1-4): ").strip()
    if system_choice == "q":
        print("[INFO] 已取消添加")
        return
    
    if system_choice == "1":
        system = "http://snomed.info/sct"
    elif system_choice == "2":
        category = input("👉 请输入分类（如 motion_codes）: ").strip()
        if category == "q":
            print("[INFO] 已取消添加")
            return
        system = f"internal://{category}"
    elif system_choice == "3":
        path = input("👉 请输入 TDP 路径（如 danger_level/emergency）: ").strip()
        if path == "q":
            print("[INFO] 已取消添加")
            return
        system = f"tdp://{path}"
    elif system_choice == "4":
        system = input("👉 请输入自定义系统 URI: ").strip()
        if system == "q":
            print("[INFO] 已取消添加")
            return
    else:
        print("[ERR] 无效的选择")
        return
    
    # 输入代码
    code = input("👉 请输入代码（如 129006008）: ").strip()
    if code == "q":
        print("[INFO] 已取消添加")
        return
    
    # 生成 ID
    system_short = get_system_short(system)
    item_id = f"{system_short}:{code}"
    
    # 检查是否已存在
    existing_ids = {item.get("id") for item in items}
    if item_id in existing_ids:
        print(f"\n[ERR] 词条 ID '{item_id}' 已存在！")
        return
    
    # 输入其他字段
    display = input("👉 请输入英文名称: ").strip()
    if display == "q":
        print("[INFO] 已取消添加")
        return
    
    display_zh = input("👉 请输入中文名称: ").strip()
    if display_zh == "q":
        print("[INFO] 已取消添加")
        return
    
    # 选择分类
    print("\n可用的分类:")
    for idx, cat in enumerate(VALID_CATEGORIES, 1):
        print(f"  {idx}) {cat}")
    
    cat_choice = input(f"👉 请选择分类 (1-{len(VALID_CATEGORIES)}): ").strip()
    if cat_choice == "q":
        print("[INFO] 已取消添加")
        return
    
    try:
        cat_idx = int(cat_choice) - 1
        if 0 <= cat_idx < len(VALID_CATEGORIES):
            category = VALID_CATEGORIES[cat_idx]
        else:
            print("[ERR] 无效的分类选择")
            return
    except ValueError:
        print("[ERR] 无效的输入")
        return
    
    description = input("👉 请输入英文描述（可选，直接回车跳过）: ").strip()
    description_zh = input("👉 请输入中文描述（可选，直接回车跳过）: ").strip()
    
    # 构建新词条
    new_entry = {
        "id": item_id,
        "code": code,
        "system": system,
        "display": display,
        "display_zh": display_zh,
        "category": category,
        "status": "active",
        "version": "1.0.0"
    }
    
    if description:
        new_entry["description"] = description
    if description_zh:
        new_entry["description_zh"] = description_zh
    
    # 预览
    print("\n" + "-" * 60)
    print("新词条预览:")
    print(json.dumps(new_entry, ensure_ascii=False, indent=2))
    print("-" * 60)
    
    confirm = input("\n⚠️  确认添加此词条？(yes/no): ").strip().lower()
    if confirm not in ["yes", "y", "是"]:
        print("[INFO] 已取消添加")
        return
    
    # 添加到列表
    items.append(new_entry)
    
    # 保存
    try:
        with open(DICTIONARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"\n[INFO] ✅ 成功添加词条: {item_id}")
        print(f"[INFO] 当前总词条数: {len(items)}")
        # 记录最近添加词条供撤回
        try:
            TEMP_DIR.mkdir(exist_ok=True)
            last_added_file = TEMP_DIR / "last_added_entry.json"
            record = {
                "id": item_id,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "entry": new_entry
            }
            with open(last_added_file, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            print(f"[INFO] 已记录最近添加词条，可使用 '撤回最近添加' 功能恢复删除。")
        except Exception as e:
            print(f"[WARN] 记录最近添加词条失败: {e}")
        
        # 提示运行完整流程
        run_flow = input("\n是否立即运行完整流程（校验+生成+更新）？(yes/no): ").strip().lower()
        if run_flow in ["yes", "y", "是"]:
            run_all()
    except Exception as e:
        print(f"[ERR] 保存失败: {e}")


def run_all():
    # Run full workflow: validate -> generate Markdown -> update CHANGELOG -> update rules docs
    print("\n" + "=" * 60)
    print("  执行完整流程")
    print("=" * 60 + "\n")
    
    # 步骤 1: 校验 JSON
    print("[1/4] 校验 JSON...")
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
    print("\n[2/4] 生成 Markdown...")
    for _ in tqdm(range(30), desc="生成 Markdown", ncols=70):
        sleep(0.01)
    try:
        run_md()
    except Exception as e:
        print(f"\n[ERR] 生成 Markdown 失败: {e}")
        print("[提示] 流程已中止")
        return
    # 步骤 3: 更新 CHANGELOG
    print("\n[3/4] 更新 CHANGELOG...")
    for _ in tqdm(range(30), desc="更新 CHANGELOG", ncols=70):
        sleep(0.01)
    try:
        run_changelog()
    except Exception as e:
        print(f"\n[ERR] 更新 CHANGELOG 失败: {e}")
        print("[提示] 流程已中止")
        return
    # 步骤 4: 更新规则文档
    print("\n[4/4] 🤖 自动更新规则文档...")
    for _ in tqdm(range(20), desc="更新规则文档", ncols=70):
        sleep(0.01)
    try:
        from generate_rules_doc import main as generate_rules
        generate_rules()
        print("✅ 规则文档已自动更新")
    except Exception as e:
        print(f"\n⚠️ 更新规则文档失败: {e}")
        print("[提示] 这不影响主流程，可忽略或稍后手动更新")
    print("\n" + "=" * 60)
    print("  完整流程执行完成")
    print("=" * 60 + "\n")


def undo_last_add():
    """撤回最近一次添加的词条（基于 temp/last_added_entry.json 记录）"""
    print("\n" + "=" * 60)
    print("  撤回最近添加的词条")
    print("=" * 60)

    last_added_file = TEMP_DIR / "last_added_entry.json"
    if not last_added_file.exists():
        print("\n[INFO] 未找到最近添加记录文件，无法撤回。")
        print("[提示] 仅支持撤回通过 '添加新词条' 功能添加的最近一次操作。")
        print("=" * 60)
        return

    try:
        data = json.loads(last_added_file.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"\n[ERR] 读取记录文件失败: {e}")
        print("=" * 60)
        return

    entry_id = data.get("id")
    entry_obj = data.get("entry")
    ts = data.get("timestamp")
    if not entry_id or not entry_obj:
        print("[ERR] 记录文件内容不完整，无法撤回。")
        print("=" * 60)
        return

    # 加载主词典
    items = safe_load_json(str(DICTIONARY_FILE))
    if items is None:
        print("[ERR] 主词典加载失败，无法撤回。")
        print("=" * 60)
        return

    # 检查是否存在
    exists = any(i.get("id") == entry_id for i in items)
    if not exists:
        print(f"\n[INFO] 主词典中没有找到词条 {entry_id}，可能已被手动删除。")
        # 删除记录文件避免再次误撤回
        try:
            last_added_file.unlink()
            print("[INFO] 已清理失效的撤回记录文件。")
        except Exception:
            pass
        print("=" * 60)
        return

    # 展示将要撤回的词条内容
    print("\n最近一次添加记录：")
    print(f"  词条 ID: {entry_id}")
    print(f"  添加时间: {ts}")
    print("  预览内容:")
    print(json.dumps(entry_obj, ensure_ascii=False, indent=2))

    confirm = input("\n⚠️  确认撤回并删除该词条？(yes/no): ").strip().lower()
    if confirm not in ["yes", "y", "是"]:
        print("\n[INFO] 已取消撤回操作。")
        print("=" * 60)
        return

    # 先备份当前数据
    print("\n[INFO] 备份当前数据后再执行撤回...")
    backup_data()

    # 执行撤回
    new_items = [i for i in items if i.get("id") != entry_id]
    try:
        with open(DICTIONARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_items, f, ensure_ascii=False, indent=2)
        print(f"\n[INFO] ✅ 撤回成功，已删除词条: {entry_id}")
        print(f"[INFO] 当前总词条数: {len(new_items)}")
        # 删除记录文件
        try:
            last_added_file.unlink()
            print("[INFO] 已清理撤回记录文件。")
        except Exception:
            pass
    except Exception as e:
        print(f"[ERR] 保存修改失败: {e}")
    print("=" * 60)


def menu():
    # Interactive menu (loop)
    while True:
        print("\n" + "=" * 60)
        print("  WiseFido 医疗编码词典管理工具")
        print("  Medical Coding Dictionary Management Tool")
        print("=" * 60)
        print("【数据管理】")
        print("  1) 校验词条数据          - 检查 JSON 格式和数据规范")
        print("  2) 生成文档              - 生成可读的 Markdown 文档")
        print("  3) 更新变更日志          - 记录词条变更历史")
        print("  4) 执行完整流程          - 一键校验+生成+更新")
        print("\n【数据查询】")
        print("  5) 显示统计信息          - 查看词条分类和数量统计")
        print("  6) 搜索词条              - 按条件查找词条")
        print("  7) 查看词条详情          - 查看单个词条完整信息")
        print("\n【数据编辑】")
        print("  8) 添加新词条            - 交互式添加单个词条")
        print("  9) 撤回最近添加          - 删除最后一次添加的词条")
        print("\n【质量检测】")
        print(" 10) 运行测试套件 🧪       - 执行 6 项数据质量测试")
        print("\n【数据备份】")
        print(" 11) 备份数据              - 手动备份词条数据")
        print(" 12) 恢复数据              - 从备份恢复数据")
        print("\n【系统维护】")
        print(" 13) 清理临时文件          - 删除临时目录内容")
        print(" 14) 🤖 更新规则文档       - 自动生成目录规则文档")
        print("  0) 退出系统              - 关闭管理工具")
        print("=" * 60)
        
        choice = input("\n👉 请输入选项编号: ").strip()
        
        if choice == "0":
            print("\n✅ 感谢使用！再见！")
            sys.exit(0)
        elif choice == "1":
            print("\n" + "=" * 60)
            print("  执行：校验词条数据")
            print("=" * 60)
            run_validate()
        elif choice == "2":
            print("\n" + "=" * 60)
            print("  执行：生成文档")
            print("=" * 60)
            run_md()
            print("\n[提示] 已自动生成两份 Markdown 文档：")
            print("  - auto_generated_docs/coding_dictionary.md      (数据表格)")
            print("  - auto_generated_docs/coding_dictionary.schema.md (Schema规范)")
            print("[建议] 可用 VS Code 预览或直接打开上述文件进行查阅。")
        elif choice == "3":
            print("\n" + "=" * 60)
            print("  执行：更新变更日志")
            print("=" * 60)
            run_changelog()
        elif choice == "4":
            print("\n" + "=" * 60)
            print("  执行：完整流程")
            print("=" * 60)
            run_all()
        elif choice == "5":
            show_stats()
        elif choice == "6":
            search_coding()
        elif choice == "7":
            view_coding_detail()
        elif choice == "8":
            add_coding_entry()
        elif choice == "9":
            undo_last_add()
        elif choice == "10":
            run_tests()
        elif choice == "11":
            backup_data()
        elif choice == "12":
            restore_data()
        elif choice == "13":
            clean_temp()
        elif choice == "14":
            print("\n" + "=" * 60)
            print("  执行：更新规则文档")
            print("=" * 60)
            try:
                from generate_rules_doc import main as generate_rules
                generate_rules()
                print("\n✅ 规则文档已成功更新!")
                print("\n[提示] 已自动完成：")
                print("  - auto_generated_docs/FILE_ORGANIZATION_RULES.md      (完整规则文档)")
                print("  - README.md 目录规则部分                              (自动更新)")
            except Exception as e:
                print(f"\n❌ 更新规则文档失败: {e}")
        else:
            print("\n[提示] ❌ 无效的选项，请重新输入")
        
        # 等待用户按键继续
        if choice != "0":
            input("\n按 Enter 键继续...")

def menu_grouped():
    # 已废弃的分组显示模式，保留占位以避免引用报错。
    # 当前恢复为原始平铺数字菜单，若后续需要可重新启用实现。
    return menu()


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
    ap.add_argument("--search", type=str, help="搜索词条 (格式: 类型:关键词，如 id:snomed)")
    ap.add_argument("--view", type=str, help="查看词条详情 (提供词条ID)")
    ap.add_argument("--backup", action="store_true", help="备份数据")
    ap.add_argument("--restore", action="store_true", help="恢复数据")
    ap.add_argument("--undo-last-add", action="store_true", help="撤回最近一次添加的词条")
    ap.add_argument("--menu-after", action="store_true", help="执行完参数模式操作后进入交互菜单")
    return ap.parse_args()


def main():
    args = parse_args()
    
    # 如果没有任何参数，显示菜单
    if not any([args.validate, args.generate_md, args.changelog, args.all, args.stats, 
                args.clean, args.test, args.search, args.view, args.backup, args.restore, args.undo_last_add]):
        # 恢复：无参数直接进入原始平铺菜单
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
        if args.backup:
            backup_data()
        if args.restore:
            restore_data()
        if args.undo_last_add:
            undo_last_add()
        if args.search:
            # 命令行搜索模式 (格式: 类型:关键词)
            if ':' in args.search:
                search_type, keyword = args.search.split(':', 1)
                items = safe_load_json(str(DICTIONARY_FILE))
                if items:
                    results = []
                    if search_type == 'id':
                        results = [item for item in items if keyword.lower() in item.get("id", "").lower()]
                    elif search_type == 'code':
                        results = [item for item in items if keyword.lower() in item.get("code", "").lower()]
                    elif search_type == 'display':
                        results = [item for item in items if keyword.lower() in item.get("display", "").lower()]
                    elif search_type == 'display_zh':
                        results = [item for item in items if keyword in item.get("display_zh", "")]
                    elif search_type == 'category':
                        results = [item for item in items if keyword.lower() in item.get("category", "").lower()]
                    
                    if results:
                        print(f"\n找到 {len(results)} 个匹配的词条：")
                        for item in results:
                            print(f"  - {item.get('id')} - {item.get('display_zh')} ({item.get('display')})")
                    else:
                        print(f"\n未找到匹配 '{keyword}' 的词条")
            else:
                print("[ERR] 搜索格式错误，应为: 类型:关键词 (如 id:snomed)")
        if args.view:
            items = safe_load_json(str(DICTIONARY_FILE))
            if items:
                item = next((i for i in items if i.get("id") == args.view), None)
                if item:
                    view_coding_detail(item)
                else:
                    print(f"[INFO] 未找到 ID 为 '{args.view}' 的词条")

    # 如果指定 --menu-after，则进入交互菜单（避免递归：仅在参数模式执行后）
    if args.menu_after:
        print("\n[INFO] 进入交互菜单 (因使用 --menu-after 参数)...")
        menu()


if __name__ == "__main__":
    main()
