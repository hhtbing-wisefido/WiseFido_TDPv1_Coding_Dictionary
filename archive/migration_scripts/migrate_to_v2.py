"""
数据迁移脚本：v1.x → v2.0.0
移除字段：id, category, status, version, description, description_zh, synonyms, synonyms_zh, 
          source_refs, detection, fhir
保留字段：system, code, display, display_zh
"""
import json
from pathlib import Path
from datetime import datetime

def migrate_coding_entry(old_entry):
    """迁移单个词条"""
    return {
        "system": old_entry["system"],
        "code": old_entry["code"],
        "display": old_entry["display"],
        "display_zh": old_entry["display_zh"]
    }

def archive_removed_fields(old_entry, archive_dir):
    """归档被移除的字段"""
    # 使用 system|code 组合作为文件名（避免 Windows 文件名非法字符）
    system = old_entry.get("system", "unknown")
    code = old_entry["code"]
    # 替换文件名中的非法字符
    safe_filename = f"{system}_{code}".replace("://", "_").replace("/", "_").replace(":", "_")
    
    removed_data = {}
    
    fields_to_archive = [
        "id", "category", "status", "version", 
        "description", "description_zh",
        "synonyms", "synonyms_zh",
        "source_refs", "detection", "fhir"
    ]
    
    for field in fields_to_archive:
        if field in old_entry:
            removed_data[field] = old_entry[field]
    
    if removed_data:
        archive_file = archive_dir / f"{safe_filename}.json"
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(removed_data, f, ensure_ascii=False, indent=2)
        return True
    return False

def main():
    print("=== 开始数据迁移 v1.x → v2.0.0 ===\n")
    
    # 文件路径
    dict_file = Path("coding_dictionary/coding_dictionary.json")
    archive_dir = Path("archive/removed_fields_v1.2.6")
    backup_file = Path("temp/backups/coding_dictionary.json.v1.backup")
    
    # 创建归档目录
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取原始数据
    print(f"📖 读取原始数据: {dict_file}")
    with open(dict_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    old_codings = old_data if isinstance(old_data, list) else old_data.get("codings", [])
    print(f"   原词条数: {len(old_codings)}")
    
    # 备份原文件
    print(f"\n💾 备份原文件: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)
    
    # 迁移数据
    print(f"\n🔄 开始迁移...")
    new_codings = []
    archived_count = 0
    
    for idx, old_entry in enumerate(old_codings, 1):
        # 归档被移除的字段
        if archive_removed_fields(old_entry, archive_dir):
            archived_count += 1
        
        # 迁移到新结构
        new_entry = migrate_coding_entry(old_entry)
        new_codings.append(new_entry)
        
        # 显示进度
        if idx % 10 == 0 or idx == len(old_codings):
            print(f"   进度: {idx}/{len(old_codings)}")
    
    # 写入新数据（保持原有的列表格式）
    print(f"\n💾 写入新数据: {dict_file}")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(new_codings, f, ensure_ascii=False, indent=2)
    
    # 统计
    print(f"\n✅ 迁移完成！")
    print(f"   新词条数: {len(new_codings)}")
    print(f"   归档词条数: {archived_count}")
    print(f"   归档目录: {archive_dir}")
    print(f"   备份文件: {backup_file}")

if __name__ == "__main__":
    main()
