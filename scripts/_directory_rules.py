"""
目录规则配置
单一事实源 - 所有目录规则从这里读取
"""

# 目录规则配置
DIRECTORY_RULES = {
    "auto_generated_docs": {
        "name": "auto_generated_docs",
        "display_name": "auto_generated_docs/",
        "purpose": "脚本自动生成的产品文档",
        "editable": False,
        "description": "**仅存放脚本自动生成的产品文档**,禁止手动修改",
        "allowed_files": [
            {"file": "changelog.md", "desc": "变更日志", "source": "脚本生成"},
            {"file": "coding_dictionary.md", "desc": "词条表格", "source": "脚本生成"},
            {"file": "coding_dictionary.schema.md", "desc": "Schema说明", "source": "脚本生成"},
            {"file": ".snapshot.json", "desc": "快照文件", "source": "脚本维护"},
            {"file": "FILE_ORGANIZATION_RULES.md", "desc": "目录规则文档", "source": "脚本生成"},
        ],
        "forbidden_patterns": [
            "*_SUMMARY.md",
            "*_PROPOSAL.md",
            "*_IMPROVEMENT.md",
            "*_CLARIFICATION.md",
        ],
        "forbidden_desc": "所有过程记录文档",
    },
    "temp": {
        "name": "temp",
        "display_name": "temp/",
        "purpose": "临时文件、草稿、测试文件、**过程记录文档**",
        "editable": True,
        "description": "草稿、测试文件、**过程记录文档**,可定期清理",
        "allowed_patterns": [
            {"pattern": "*_SUMMARY.md", "desc": "开发过程记录"},
            {"pattern": "*_PROPOSAL.md", "desc": "优化提案文档"},
            {"pattern": "*_IMPROVEMENT.md", "desc": "改进记录"},
            {"pattern": "*_CLARIFICATION.md", "desc": "说明文档"},
            {"pattern": "*_backup.*", "desc": "临时备份"},
            {"pattern": "*.tmp", "desc": "临时文件"},
            {"pattern": "test_*.*", "desc": "测试文件"},
            {"pattern": "draft_*.*", "desc": "草稿"},
        ],
        "can_clean": True,
    },
    "coding_dictionary": {
        "name": "coding_dictionary",
        "display_name": "coding_dictionary/",
        "purpose": "核心数据源",
        "editable": True,
        "description": "唯一可手动编辑的数据文件",
        "allowed_files": [
            {"file": "coding_dictionary.json", "desc": "主数据文件", "source": "手动编辑"},
        ],
    },
    "scripts": {
        "name": "scripts",
        "display_name": "scripts/",
        "purpose": "维护脚本",
        "editable": True,
        "description": "Python 脚本,不放数据文件",
    },
    "schema": {
        "name": "schema",
        "display_name": "schema/",
        "purpose": "Schema 定义",
        "editable": True,
        "description": "JSON Schema 规范定义",
    },
    "spec": {
        "name": "spec",
        "display_name": "spec/",
        "purpose": "规范文档",
        "editable": True,
        "description": "数据结构说明文档",
    },
    "auto_backup": {
        "name": "auto_backup",
        "display_name": "auto_backup/",
        "purpose": "自动备份",
        "editable": False,
        "description": "脚本自动创建,本地保留,不提交 Git",
        "local_only": True,
    },
    "Project_backup": {
        "name": "Project_backup",
        "display_name": "Project_backup/",
        "purpose": "项目备份",
        "editable": False,
        "description": "里程碑备份,本地保留,不提交 Git",
        "local_only": True,
    },
    "原始参考文件": {
        "name": "原始参考文件",
        "display_name": "原始参考文件/",
        "purpose": "参考资料",
        "editable": True,
        "description": "医疗标准文档等",
    },
    "root": {
        "name": "root",
        "display_name": "项目根目录",
        "purpose": "核心配置",
        "editable": "restricted",
        "description": "**仅放 README.md、requirements.txt、.gitignore 等核心配置**",
        "allowed_files": [
            "README.md",
            "requirements.txt",
            ".gitignore",
        ],
    },
}

# 文件分类规则
FILE_CLASSIFICATION_RULES = {
    "product_docs": {
        "location": "auto_generated_docs",
        "criteria": [
            "由脚本自动生成或自动维护",
            "是面向用户的产品文档",
            "需要长期保留",
            "会被用户查阅或引用",
        ],
        "examples": [
            "changelog.md",
            "coding_dictionary.md",
            "coding_dictionary.schema.md",
            ".snapshot.json",
        ],
    },
    "process_records": {
        "location": "temp",
        "criteria": [
            "开发过程记录文档",
            "优化提案文档",
            "临时备份文件",
            "可以定期清理",
        ],
        "patterns": [
            "*_SUMMARY.md",
            "*_PROPOSAL.md",
            "*_IMPROVEMENT.md",
            "*_backup.*",
        ],
    },
}

# 核心原则
CORE_PRINCIPLES = [
    "🤖 **脚本生成的产品文档** → `auto_generated_docs/`",
    "📝 **人工编写的过程记录** → `temp/`",
    "📂 **核心数据文件** → `coding_dictionary/`",
    "⚠️ **项目根目录** → 仅核心配置文件",
]

# 快速决策流程
QUICK_DECISION = {
    "question1": {
        "text": "这个文件是脚本自动生成的吗?",
        "yes": "继续问题2",
        "no": "放到 temp/",
    },
    "question2": {
        "text": "这是面向用户的产品文档吗?",
        "yes": "放到 auto_generated_docs/",
        "no": "放到 temp/",
    },
}

# 项目版本信息
PROJECT_VERSION = "v1.2.5"
LAST_UPDATE_DATE = "2025-11-12"
