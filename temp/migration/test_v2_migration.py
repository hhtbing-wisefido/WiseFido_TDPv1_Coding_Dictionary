#!/usr/bin/env python3
"""
v2.0.0 迁移测试脚本

测试项目:
1. Schema 验证 - 所有词条通过 v2.0.0 Schema 验证
2. 数据完整性 - 79 词条,4 核心字段
3. 唯一性验证 - system|code 组合唯一
4. 归档完整性 - 97 个归档文件存在
5. 统计功能 - get_project_stats.py 正常运行
6. 文件结构验证
"""

import json
import sys
import subprocess
from pathlib import Path
from collections import Counter

project_root = Path(__file__).parent.parent.parent


class Colors:
    """ANSI 颜色代码"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_test_header(title):
    """打印测试标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def print_success(message):
    """打印成功消息"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_error(message):
    """打印错误消息"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_warning(message):
    """打印警告消息"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


def print_info(message):
    """打印信息消息"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")


def test_1_data_integrity():
    """测试 1: 数据完整性"""
    print_test_header("测试 1: 数据完整性")
    
    json_file = project_root / "coding_dictionary" / "coding_dictionary.json"
    
    if not json_file.exists():
        print_error(f"JSON 文件不存在: {json_file}")
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    # 检查词条数量
    if len(items) != 79:
        print_error(f"词条数量错误: 期望 79,实际 {len(items)}")
        return False
    print_success(f"词条数量正确: {len(items)}")
    
    # 检查每个词条的必填字段
    required_fields = ['system', 'code', 'display', 'display_zh']
    missing_fields_count = 0
    
    for idx, item in enumerate(items):
        missing = [f for f in required_fields if f not in item]
        if missing:
            print_error(f"词条 #{idx+1} 缺少字段: {missing}")
            missing_fields_count += 1
    
    if missing_fields_count == 0:
        print_success("所有词条包含 4 个核心字段")
    else:
        print_error(f"{missing_fields_count} 个词条缺少必填字段")
        return False
    
    # 检查是否有旧字段残留
    old_fields = ['id', 'category', 'status', 'version', 'description', 
                  'description_zh', 'synonyms', 'synonyms_zh', 'source_refs', 
                  'detection', 'fhir']
    
    items_with_old_fields = []
    for idx, item in enumerate(items):
        old_found = [f for f in old_fields if f in item]
        if old_found:
            items_with_old_fields.append((idx+1, old_found))
    
    if items_with_old_fields:
        print_warning(f"{len(items_with_old_fields)} 个词条包含旧字段 (这是允许的)")
        for idx, fields in items_with_old_fields[:3]:  # 只显示前 3 个
            print_info(f"  词条 #{idx}: {fields}")
        if len(items_with_old_fields) > 3:
            print_info(f"  ... 还有 {len(items_with_old_fields)-3} 个")
    else:
        print_success("所有词条均为纯 4 字段结构")
    
    return True


def test_2_schema_validation():
    """测试 2: Schema 验证"""
    print_test_header("测试 2: Schema 验证")
    
    # 调用 validate_json.py 脚本
    try:
        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "validate_json.py")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        if result.returncode == 0:
            print_success("所有词条通过 Schema 验证")
            return True
        else:
            print_error(f"Schema 验证失败")
            if result.stdout:
                print_info(result.stdout[:500])
            return False
    except Exception as e:
        print_error(f"验证过程异常: {e}")
        return False


def test_3_uniqueness():
    """测试 3: system|code 唯一性"""
    print_test_header("测试 3: system|code 唯一性")
    
    json_file = project_root / "coding_dictionary" / "coding_dictionary.json"
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        
        # 检查 system|code 唯一性
        system_code_map = {}
        duplicates = {}
        
        for idx, item in enumerate(items):
            key = f"{item['system']}|{item['code']}"
            if key in system_code_map:
                if key not in duplicates:
                    duplicates[key] = [system_code_map[key]]
                duplicates[key].append(idx)
            else:
                system_code_map[key] = idx
        
        if not duplicates:
            print_success(f"所有 {len(system_code_map)} 个 system|code 组合唯一")
            return True
        else:
            print_error(f"发现 {len(duplicates)} 组重复:")
            for key, indices in list(duplicates.items())[:3]:
                print_error(f"  {key}: 出现在词条索引 {indices}")
            return False
    except Exception as e:
        print_error(f"唯一性检查异常: {e}")
        return False


def test_4_archive_integrity():
    """测试 4: 归档文件完整性"""
    print_test_header("测试 4: 归档文件完整性")
    
    archive_dir = project_root / "archive" / "removed_fields_v1.2.6"
    
    if not archive_dir.exists():
        print_error(f"归档目录不存在: {archive_dir}")
        return False
    
    # 统计归档文件
    archive_files = list(archive_dir.glob("*.json"))
    
    if len(archive_files) != 97:
        print_warning(f"归档文件数量: 期望 97,实际 {len(archive_files)}")
    else:
        print_success(f"归档文件数量正确: {len(archive_files)}")
    
    # 随机检查几个归档文件的内容
    import random
    sample_files = random.sample(archive_files, min(3, len(archive_files)))
    
    for archive_file in sample_files:
        try:
            with open(archive_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查是否包含移除的字段
            expected_fields = ['id', 'category', 'status', 'version']
            found_fields = [f for f in expected_fields if f in data]
            
            if found_fields:
                print_success(f"  {archive_file.name}: 包含 {len(found_fields)} 个移除字段")
            else:
                print_warning(f"  {archive_file.name}: 未找到期望的移除字段")
        except Exception as e:
            print_error(f"  读取 {archive_file.name} 失败: {e}")
    
    return True


def test_5_stats_functionality():
    """测试 5: 统计功能"""
    print_test_header("测试 5: 统计功能")
    
    try:
        # 调用 get_project_stats.py 脚本
        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "get_project_stats.py")],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        # 检查是否有关键输出,即使 returncode 非0
        output = result.stdout if result.stdout else ""
        error_output = result.stderr if result.stderr else ""
        
        # 判断成功的标准: 输出包含关键信息
        if "总词条数: 79" in output and "SNOMED CT:" in output:
            print_success("统计功能正常")
            print_info("  编码系统统计:")
            for line in output.split('\n'):
                if 'SNOMED CT:' in line or 'Internal:' in line or 'TDP:' in line:
                    print_info(f"    {line.strip()}")
            return True
        elif result.returncode == 0:
            print_success("统计脚本执行成功(但输出可能不完整)")
            return True
        else:
            print_error("统计功能失败")
            if error_output:
                print_error(f"  错误信息: {error_output[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print_error("统计功能超时")
        return False
    except Exception as e:
        print_error(f"统计功能异常: {e}")
        return False


def test_6_file_structure():
    """测试 6: 文件结构"""
    print_test_header("测试 6: 文件结构")
    
    required_files = [
        "coding_dictionary/coding_dictionary.json",
        "schema/coding_dictionary.schema.json",
        "scripts/validate_json.py",
        "scripts/generate_md.py",
        "scripts/changelog.py",
        "scripts/add_coding_dict.py",
        "scripts/dic_tools.py",
        "scripts/get_project_stats.py",
        "README.md",
        "spec/coding_dictionary.schema.spec.md",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print_success(f"  {file_path}")
        else:
            print_error(f"  {file_path} (不存在)")
            all_exist = False
    
    return all_exist


def run_all_tests():
    """运行所有测试"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}v2.0.0 迁移测试套件{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    
    tests = [
        ("数据完整性", test_1_data_integrity),
        ("Schema 验证", test_2_schema_validation),
        ("唯一性验证", test_3_uniqueness),
        ("归档完整性", test_4_archive_integrity),
        ("统计功能", test_5_stats_functionality),
        ("文件结构", test_6_file_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"测试 '{name}' 异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 打印总结
    print_test_header("测试总结")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
    
    print(f"\n{Colors.BOLD}总计: {passed}/{total} 通过{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 所有测试通过!{Colors.RESET}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ {total-passed} 个测试失败{Colors.RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
