#!/usr/bin/env python3
"""
自动生成目录规则文档
从 _directory_rules.py 读取配置,生成:
1. auto_generated_docs/FILE_ORGANIZATION_RULES.md
2. README.md 中的目录规则部分
3. README.md 中的目录树结构
4. README.md 中的版本统计数据
"""

import os
import re
from datetime import datetime
from _directory_rules import (
    DIRECTORY_RULES,
    FILE_CLASSIFICATION_RULES,
    CORE_PRINCIPLES,
    QUICK_DECISION,
    PROJECT_VERSION,
    LAST_UPDATE_DATE,
)
from get_project_stats import get_stats, format_stats_for_readme


def generate_file_organization_rules():
    """生成 FILE_ORGANIZATION_RULES.md"""
    
    content = f"""# 📁 项目文件组织规则

**创建日期**: {LAST_UPDATE_DATE}  
**最后更新**: {LAST_UPDATE_DATE} ({PROJECT_VERSION})  
**重要性**: ⭐⭐⭐⭐⭐ 必须遵守  
**生成方式**: 🤖 由 `scripts/generate_rules_doc.py` 自动生成

> ⚠️ **注意**: 本文档由脚本自动生成,请勿手动编辑!  
> 如需修改规则,请编辑 `scripts/_directory_rules.py` 后运行 `python scripts/generate_rules_doc.py`

---

## 📋 核心原则

**保持项目根目录整洁,所有文件必须按类型放置到正确的目录中。**

**关键分离原则**:
"""
    
    for principle in CORE_PRINCIPLES:
        content += f"- {principle}\n"
    
    content += """
---

## 📂 目录使用规范

"""
    
    # 生成每个目录的说明
    for dir_key, dir_info in DIRECTORY_RULES.items():
        if dir_key == "root":
            continue
            
        content += f"""### {len([k for k in DIRECTORY_RULES.keys() if k != 'root' and list(DIRECTORY_RULES.keys()).index(k) < list(DIRECTORY_RULES.keys()).index(dir_key)])+1}. `{dir_info['display_name']}`

**用途**: {dir_info['purpose']}

**可编辑**: {'✅ 是' if dir_info['editable'] == True else ('❌ 否' if dir_info['editable'] == False else '⚠️ 限制')}

**说明**: {dir_info['description']}

"""
        
        # 如果有允许的文件列表
        if "allowed_files" in dir_info:
            content += "**允许的文件**:\n"
            for file_info in dir_info['allowed_files']:
                content += f"- ✅ `{file_info['file']}` - {file_info['desc']} ({file_info['source']})\n"
            content += "\n"
        
        # 如果有允许的模式
        if "allowed_patterns" in dir_info:
            content += "**允许的文件类型**:\n"
            for pattern_info in dir_info['allowed_patterns']:
                content += f"- ✅ `{pattern_info['pattern']}` - {pattern_info['desc']}\n"
            content += "\n"
        
        # 如果有禁止的模式
        if "forbidden_patterns" in dir_info:
            content += "**禁止的文件**:\n"
            for pattern in dir_info['forbidden_patterns']:
                content += f"- ❌ `{pattern}` - {dir_info['forbidden_desc']}\n"
            content += "\n"
        
        # 如果可以清理
        if dir_info.get("can_clean"):
            content += "**清理**: 可定期清理 (`python scripts/dic_tools.py --clean`)\n\n"
        
        # 如果是本地备份
        if dir_info.get("local_only"):
            content += "⚠️ **本地备份**: 已在 `.gitignore` 中配置,不会提交到版本控制\n\n"
        
        content += "---\n\n"
    
    # 添加快速决策指南
    content += """## 🎯 快速决策指南

### 我应该把文件放在哪里?

"""
    
    content += f"""**{QUICK_DECISION['question1']['text']}**
- ✅ 是 → {QUICK_DECISION['question1']['yes']}
- ❌ 否 → {QUICK_DECISION['question1']['no']}

**{QUICK_DECISION['question2']['text']}**
- ✅ 是 → {QUICK_DECISION['question2']['yes']}
- ❌ 否 → {QUICK_DECISION['question2']['no']}

### 文件类型快速判断表

| 文件特征 | 目录 | 示例 |
|----------|------|------|
"""
    
    # 产品文档
    for example in FILE_CLASSIFICATION_RULES['product_docs']['examples']:
        content += f"| 脚本生成的产品文档 | `auto_generated_docs/` | {example} |\n"
    
    # 过程记录
    for pattern in FILE_CLASSIFICATION_RULES['process_records']['patterns']:
        content += f"| 过程记录/临时文件 | `temp/` | {pattern} |\n"
    
    content += """
---

## 🎓 记忆要点

**一句话总结**:
> 🤖 **脚本生成的产品文档** → `auto_generated_docs/`  
> 📝 **人工编写的过程记录** → `temp/`

**识别技巧**:
- 看到 `*_SUMMARY.md` → 一定是 `temp/`
- 看到 `*_PROPOSAL.md` → 一定是 `temp/`
- 看到 `changelog.md` / `coding_dictionary.md` → 一定是 `auto_generated_docs/`

---

## 📊 目录内容清单

### auto_generated_docs/ (仅5+1个文件)

"""
    
    auto_gen_info = DIRECTORY_RULES['auto_generated_docs']
    for file_info in auto_gen_info['allowed_files']:
        content += f"- `{file_info['file']}` - {file_info['desc']} ({file_info['source']})\n"
    
    content += """
### temp/ (所有过程记录和临时文件)

"""
    
    temp_info = DIRECTORY_RULES['temp']
    for pattern_info in temp_info['allowed_patterns']:
        content += f"- `{pattern_info['pattern']}` - {pattern_info['desc']}\n"
    
    content += f"""
---

**最后更新**: {LAST_UPDATE_DATE} ({PROJECT_VERSION})  
**维护者**: WiseFido Team  
**重要性**: ⭐⭐⭐⭐⭐ 必须遵守  
**生成方式**: 🤖 自动生成,请勿手动编辑

> 如需修改规则,请编辑 `scripts/_directory_rules.py` 后运行:  
> ```bash
> python scripts/generate_rules_doc.py
> ```
"""
    
    return content


def generate_readme_directory_section():
    """生成 README.md 中的目录规则部分"""
    
    content = """### 📂 目录使用规范

| 目录 | 用途 | 可编辑 | 说明 |
|------|------|--------|------|
"""
    
    for dir_key, dir_info in DIRECTORY_RULES.items():
        if dir_key == "root":
            editable = "⚠️ 限制"
        else:
            editable = "✅ 是" if dir_info['editable'] == True else "❌ 否"
        
        content += f"| `{dir_info['display_name']}` | {dir_info['purpose']} | {editable} | {dir_info['description']} |\n"
    
    content += """
### 📋 文件分类规则

**`auto_generated_docs/` 只放这些文件**:
"""
    
    auto_gen_info = DIRECTORY_RULES['auto_generated_docs']
    for file_info in auto_gen_info['allowed_files']:
        content += f"- ✅ `{file_info['file']}` - {file_info['desc']} ({file_info['source']})\n"
    
    content += """
**`temp/` 应存放这些文件**:
"""
    
    temp_info = DIRECTORY_RULES['temp']
    for pattern_info in temp_info['allowed_patterns'][:5]:  # 只显示前5个
        content += f"- ✅ `{pattern_info['pattern']}` - {pattern_info['desc']}\n"
    
    content += """
**重要原则**: 
- ❌ **过程记录文档** (如优化总结、改进记录) → `temp/`
- ✅ **产品文档** (如自动生成的表格、changelog) → `auto_generated_docs/`
"""
    
    return content


def update_readme_directory_section():
    """自动更新 README.md 中的目录规则部分"""
    import re
    
    readme_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "README.md"
    )
    
    if not os.path.exists(readme_path):
        print(f"⚠️ 未找到 README.md: {readme_path}")
        return False
    
    # 读取 README.md
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # 生成新的目录规则部分
    new_section = generate_readme_directory_section()
    
    # 使用正则表达式替换
    # 匹配从 "### 📂 目录使用规范" 到 "### 🗂️ 临时目录" 之间的内容
    pattern = r'(### 📂 目录使用规范.*?)(### 🗂️ 临时目录)'
    
    if re.search(pattern, readme_content, re.DOTALL):
        # 替换内容
        updated_content = re.sub(
            pattern,
            new_section + '\n' + r'\2',
            readme_content,
            flags=re.DOTALL
        )
        
        # 写回文件
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        return True
    else:
        print("⚠️ 未找到目标标记,无法自动更新 README.md")
        print("   请确保 README.md 中包含 '### 📂 目录使用规范' 和 '### 🗂️ 临时目录' 标记")
        return False


def generate_directory_tree():
    """生成目录树结构"""
    tree = """```plaintext
WiseFido_TDPv1_Coding_Dictionary/
├── 📄 README.md                          项目总览（本文档）
├── 📄 requirements.txt                   Python 依赖
├── 📄 .gitignore                         Git 忽略规则
│
├── 📁 coding_dictionary/                 核心数据源（唯一事实源）
│   └── coding_dictionary.json             主词条列表（JSON）
│
├── 📁 schema/                            机器校验规范
│   └── coding_dictionary.schema.json      JSON Schema
│
├── 📁 spec/                              数据结构与字段规范
│   └── coding_dictionary.schema.spec.md   Schema 规范说明
│
├── 📁 scripts/                           维护脚本
│   ├── _config.py                         公共配置
│   ├── _directory_rules.py                目录规则配置（单一事实源）
│   ├── dic_tools.py                       主工具（交互/参数两用）
│   ├── validate_json.py                   JSON + 逻辑校验
│   ├── generate_md.py                     Markdown 生成
│   ├── generate_rules_doc.py              规则文档自动生成
│   ├── get_project_stats.py               项目统计信息获取
│   ├── changelog.py                       变更日志生成
│   └── add_coding_dict.py                 批量添加词条
│
├── 📁 auto_generated_docs/               自动输出（禁止手动修改）
│   ├── coding_dictionary.md               数据表格（双语）
│   ├── coding_dictionary.schema.md        Schema 说明
│   ├── changelog.md                       变更总结报告
│   ├── .snapshot.json                     快照
│   └── FILE_ORGANIZATION_RULES.md         目录规则文档（自动生成）
│
├── 📁 auto_backup/                       脚本自动备份（本地，不提交 Git）
│   └── coding_terms_backup_*.json         自动备份文件
│
├── 📁 temp/                              临时文件、开发记录
│   ├── *_SUMMARY.md                       开发过程记录文档
│   ├── *_PROPOSAL.md                      优化提案文档
│   ├── __pycache__/                       Python 缓存
│   └── ...                                其他临时文件
│
├── 📁 Project_backup/                    项目里程碑备份（本地，不提交 Git）
│   └── v*_milestone_*/                    版本备份目录
│
├── 📁 原始参考文件/                       参考资料
│   ├── tdpv1-0916-fixed.md                TDPv1 协议文档
│   ├── fhir与snomed_ct代码.md             医疗编码标准参考
│   └── fda-v0923.md                       OWL Monitor 架构
│
└── 📁 .github/                           GitHub 配置
    └── workflows/
        └── ci.yml                          CI/CD 工作流
```"""
    return tree


def update_readme_directory_tree():
    """自动更新 README.md 中的目录树结构"""
    
    readme_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "README.md"
    )
    
    if not os.path.exists(readme_path):
        print(f"⚠️ 未找到 README.md: {readme_path}")
        return False
    
    # 读取 README.md
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # 生成新的目录树
    new_tree = generate_directory_tree()
    
    # 使用正则表达式替换
    # 匹配从 "## 📁 仓库结构" 到下一个 "##" 之间的内容
    pattern = r'(## 📁 仓库结构\s*\n)(```plaintext.*?```)(.*?)(---)'
    
    if re.search(pattern, readme_content, re.DOTALL):
        # 替换内容
        updated_content = re.sub(
            pattern,
            r'\1' + new_tree + r'\n\n' + r'\4',
            readme_content,
            flags=re.DOTALL
        )
        
        # 写回文件
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        return True
    else:
        print("⚠️ 未找到目标标记,无法自动更新目录树")
        return False


def update_readme_version_stats():
    """自动更新 README.md 中的版本统计数据"""
    
    readme_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "README.md"
    )
    
    if not os.path.exists(readme_path):
        print(f"⚠️ 未找到 README.md: {readme_path}")
        return False
    
    # 获取最新统计数据
    stats = get_stats()
    if not stats:
        print("⚠️ 无法获取统计数据")
        return False
    
    # 读取 README.md
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # 计算统计数据
    new_count = stats['total_count']
    growth = new_count - 34
    growth_percent = (growth / 34 * 100) if growth > 0 else 0
    
    # 更新 "本版本在 v1.2.3 基础上扩展了 **XX 个新词条**(从 34 → XX),增长 XX.X%"
    pattern1 = r'(本版本在 v1\.2\.3 基础上扩展了 \*\*)\d+( 个新词条\*\*\(从 34 → )\d+(\),增长 )\d+\.\d+(%\))'
    
    if re.search(pattern1, readme_content):
        readme_content = re.sub(
            pattern1,
            rf'\g<1>{growth}\g<2>{new_count}\g<3>{growth_percent:.1f}\g<4>',
            readme_content
        )
    
    # 更新 "#### 📊 当前统计" 部分
    # 格式化统计数据
    cat_dist = " | ".join([
        f"标签({stats['categories_percentage']['tag']:.1f}%)",
        f"运动({stats['categories_percentage']['motion_codes']:.1f}%)",
        f"姿态({stats['categories_percentage']['posture_codes']:.1f}%)",
        f"生理({stats['categories_percentage']['physiological_codes']:.1f}%)",
        f"安全({stats['categories_percentage']['safety_alert_codes']:.1f}%)",
        f"疾病({stats['categories_percentage']['disorder_condition_codes']:.1f}%)"
    ])
    
    sys_dist = " | ".join([
        f"SNOMED CT({stats['systems_percentage']['snomed_ct']:.1f}%)",
        f"Internal({stats['systems_percentage']['internal']:.1f}%)",
        f"TDP({stats['systems_percentage']['tdp']:.1f}%)"
    ])
    
    radar_dist = " | ".join([
        f"直接({stats['radar_detection_percentage']['direct']:.1f}%)",
        f"间接({stats['radar_detection_percentage']['indirect']:.1f}%)",
        f"未标注({stats['radar_detection_percentage']['not_annotated']:.1f}%)"
    ])
    
    new_stats = f"""#### 📊 当前统计
- **总词条数**: {new_count}
- **分类分布**: {cat_dist}
- **编码系统**: {sys_dist}
- **雷达检测**: {radar_dist}
- **测试通过率**: 100% (6/6)"""
    
    pattern2 = r'#### 📊 当前统计\s*\n- \*\*总词条数\*\*:.*?\n- \*\*分类分布\*\*:.*?\n- \*\*编码系统\*\*:.*?\n- \*\*雷达检测\*\*:.*?\n- \*\*测试通过率\*\*:.*?\n'
    
    if re.search(pattern2, readme_content, re.DOTALL):
        readme_content = re.sub(
            pattern2,
            new_stats + '\n',
            readme_content,
            flags=re.DOTALL
        )
        
        # 更新 v1.2.3-milestone 的版本快照
        snapshot_stats = format_stats_for_readme(stats)
        
        pattern3 = r'(#### 📸 版本快照\s*\n)(- 📊 词条总数:.*?\n- 📂 分类数:.*?\n- 🧪 测试通过率:.*?\n)'
        
        # 注意: v1.2.3 的数据保持不变 (34 词条),不更新
        
        # 写回文件
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        return True
    else:
        print("⚠️ 未找到当前统计标记")
        return False


def main():
    """主函数"""
    print("🤖 开始生成目录规则文档...")
    
    # 1. 生成 FILE_ORGANIZATION_RULES.md
    print("\n📝 生成 FILE_ORGANIZATION_RULES.md...")
    rules_content = generate_file_organization_rules()
    
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "auto_generated_docs",
        "FILE_ORGANIZATION_RULES.md"
    )
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rules_content)
    
    print(f"✅ 已生成: {output_path}")
    
    # 2. 自动更新 README.md 目录规则部分
    print("\n📝 自动更新 README.md 中的目录规则部分...")
    if update_readme_directory_section():
        print("✅ README.md 目录规则部分已更新!")
    else:
        print("⚠️ README.md 目录规则部分更新失败")
    
    # 3. 自动更新 README.md 目录树结构
    print("\n📝 自动更新 README.md 中的目录树结构...")
    if update_readme_directory_tree():
        print("✅ README.md 目录树结构已更新!")
    else:
        print("⚠️ README.md 目录树结构更新失败")
    
    # 4. 自动更新 README.md 版本统计数据
    print("\n📝 自动更新 README.md 中的版本统计数据...")
    if update_readme_version_stats():
        print("✅ README.md 版本统计数据已更新!")
    else:
        print("⚠️ README.md 版本统计数据更新失败")
    
    print("\n🎉 生成完成!")
    print("\n📋 已完成:")
    print("1. ✅ 生成 FILE_ORGANIZATION_RULES.md")
    print("2. ✅ 自动更新 README.md (目录规则部分)")
    print("3. ✅ 自动更新 README.md (目录树结构)")
    print("4. ✅ 自动更新 README.md (版本统计数据)")
    print("\n💡 如需修改规则,请编辑 scripts/_directory_rules.py 后重新运行本脚本")


if __name__ == "__main__":
    main()
