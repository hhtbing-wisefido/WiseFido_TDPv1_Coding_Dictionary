# 📦 WiseFido_TDPv1_Coding_Dictionary

> 🎯 **FHIR 标准医疗编码字典库** | v2.0.0 | JSON Schema 验证 | 自动文档生成

[![Copyright: WiseFido](https://img.shields.io/badge/Copyright-WiseFido-blue.svg)](https://www.wisefido.com)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v2.0.0-green.svg)](https://github.com/hhtbing-wisefido/WiseFido_TDPv1_Coding_Dictionary/releases/tag/v2.0.0)

---

## 💡 项目简介

WiseFido_TDPv1_Coding_Dictionary 是基于 FHIR Coding 标准构建的医疗编码字典库，用于 OWL Monitor System（多传感器老人健康监测系统）的统一术语管理。

**v2.0.0 核心特性:**
- 🎯 FHIR 标准兼容 - 严格遵循 FHIR Coding 核心字段
- 🔒 极简数据模型 - 仅保留 4 个核心字段  
- 🤖 JSON Schema 验证 - 自动验证数据完整性
- 📖 自动文档生成 - 一键生成文档和变更日志
- 🔄 可扩展架构 - 支持按需扩展字段

---

## � 目录结构

```plaintext
WiseFido_TDPv1_Coding_Dictionary/
├── 📄 README.md                          项目说明
├── 📄 requirements.txt                   Python 依赖
├── 📄 .gitignore                         Git 忽略规则
│
├── 📁 coding_dictionary/                 核心数据源（唯一事实源）
│   └── coding_dictionary.json             主词条列表
│
├── 📁 schema/                            JSON Schema 定义
│   └── coding_dictionary.schema.json      数据验证规范
│
├── 📁 spec/                              规范文档
│   └── coding_dictionary.schema.spec.md   v2.0.0 数据结构说明
│
├── 📁 scripts/                           维护脚本
│   ├── _config.py                         公共配置
│   ├── _directory_rules.py                目录规则（单一事实源）
│   ├── dic_tools.py                       主工具（交互/参数模式）
│   ├── validate_json.py                   数据校验
│   ├── generate_md.py                     文档生成
│   ├── changelog.py                       变更日志
│   ├── add_coding_dict.py                 添加词条
│   ├── get_project_stats.py               统计信息
│   └── generate_rules_doc.py              规则文档生成
│
├── 📁 auto_generated_docs/               自动生成（禁止手动修改）
│   ├── changelog.md                       词条数据变更日志
│   ├── coding_dictionary.md               词条表格
│   ├── coding_dictionary.schema.md        Schema 说明
│   ├── V2.0.0_RELEASE_SUMMARY.md          v2.0.0 发布总结
│   ├── FILE_ORGANIZATION_RULES.md         目录规则文档
│   ├── .snapshot.json                     快照文件
│   ├── AI决策日志系统/                   AI 决策和会话记录
│   │   ├── 项目决策日志.md                 重要决策记录
│   │   ├── 开发会话笔记.md                 会话进度记录
│   │   └── 使用说明.md                     系统说明
│   └── Web服务开发文档/                  Web API 开发文档
│       ├── README.md                       文档目录说明
│       ├── 实施计划.md                     完整开发计划
│       ├── Day1完成总结.md                 Day 1 完成报告
│       ├── API测试报告.md                  测试结果
│       ├── 快速参考.md                     决策快速参考
│       └── Curl与GET对比.md                命令对比
│
├── 📁 archive/                           归档数据
│   └── removed_fields_v1.2.6/             v2.0.0 移除的字段（97个文件）
│
├── 📁 temp/                              临时文件（可定期清理）
│   ├── *_SUMMARY.md                       开发记录
│   └── __pycache__/                       Python 缓存
│
├── 📁 auto_backup/                       自动备份（本地，不提交 Git）
├── 📁 Project_backup/                    项目备份（本地，不提交 Git）
└── 📁 原始参考文件/                       参考资料
    ├── tdpv1-0916-fixed.md                TDPv1 协议
    ├── fhir与snomed_ct代码.md             医疗编码标准
    └── fda-v0923.md                       OWL Monitor 架构
```

---

## 📂 目录使用规范

### 核心原则

**保持项目根目录整洁** - 所有文件按类型放置到正确目录

| 目录 | 用途 | 可编辑 | 说明 |
|------|------|--------|------|
| `coding_dictionary/` | 核心数据源 | ✅ 是 | 唯一可手动编辑的数据文件 |
| `auto_generated_docs/` | 自动生成文档 | ❌ 否 | **仅存放脚本生成的产品文档和子目录** |
| `temp/` | 临时文件 | ✅ 是 | 草稿、测试、开发记录，可定期清理 |
| `scripts/` | 维护脚本 | ✅ 是 | Python 脚本，不放数据文件 |
| `schema/` | Schema 定义 | ✅ 是 | JSON Schema 规范 |
| `spec/` | 规范文档 | ✅ 是 | 数据结构说明文档 |
| `archive/` | 归档数据 | ✅ 是 | v2.0.0 重构移除的字段 |
| `auto_backup/` | 自动备份 | ❌ 否 | 脚本自动创建，本地保留 |
| `Project_backup/` | 项目备份 | ❌ 否 | 里程碑备份，本地保留 |
| `0_refer_files/` | 参考资料 | ✅ 是 | 医疗标准文档 |

### 文件分类规则

**`auto_generated_docs/` 只放这些**:
- ✅ `changelog.md` - 词条数据变更日志（脚本生成）
- ✅ `coding_dictionary.md` - 词条表格（脚本生成）
- ✅ `coding_dictionary.schema.md` - Schema 说明（脚本生成）
- ✅ `V2.0.0_RELEASE_SUMMARY.md` - 发布总结
- ✅ `FILE_ORGANIZATION_RULES.md` - 目录规则
- ✅ `.snapshot.json` - 快照文件
- ✅ `AI决策日志系统/` - 决策和会话记录子目录
- ✅ `Web服务开发文档/` - Web API 开发文档子目录

**`temp/` 应存放这些**:
- ✅ `*_SUMMARY.md` - 开发过程记录
- ✅ `*_PROPOSAL.md` - 优化提案
- ✅ `*_backup.*` - 临时备份

**重要原则**:
- ❌ **禁止在项目根目录**创建总结报告、临时文件
- ❌ **过程记录文档** → `temp/`
- ✅ **产品文档** → `auto_generated_docs/`

详细规则见: [`auto_generated_docs/FILE_ORGANIZATION_RULES.md`](auto_generated_docs/FILE_ORGANIZATION_RULES.md)

---

## �🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用交互式菜单

```bash
python scripts/dic_tools.py
```

**菜单功能列表**:

#### 【数据管理】
1. 校验词条数据 - 检查 JSON 格式和数据规范
2. 生成文档 - 生成可读的 Markdown 文档
3. 更新变更日志 - 记录词条变更历史
4. 执行完整流程 - 一键校验+生成+更新

#### 【数据查询】
5. 显示统计信息 - 查看词条分类和数量统计
6. 搜索词条 - 按条件查找词条
7. 查看词条详情 - 查看单个词条完整信息

#### 【数据编辑】
8. 添加新词条 - 交互式添加单个词条
9. 撤回最近添加 - 删除最后一次添加的词条

#### 【质量检测】
10. 运行测试套件 - 执行数据质量测试

#### 【数据备份】
11. 备份数据 - 手动备份词条数据
12. 恢复数据 - 从备份恢复数据

#### 【系统维护】
13. 清理临时文件 - 删除临时目录内容
14. 更新规则文档 - 自动生成目录规则文档
0. 退出系统 - 关闭管理工具

---

### 常用命令

#### 完整参数列表

```bash
# 数据管理
python scripts/dic_tools.py --validate      # 校验数据
python scripts/dic_tools.py --generate-md   # 生成文档
python scripts/dic_tools.py --changelog     # 更新变更日志
python scripts/dic_tools.py --all           # 完整流程(校验+生成+changelog)

# 数据查询
python scripts/dic_tools.py --stats         # 统计信息
python scripts/dic_tools.py --search "system:snomed"   # 搜索词条
python scripts/dic_tools.py --view "http://snomed.info/sct|129006008"  # 查看详情

# 数据编辑
# (添加词条请使用交互式菜单)

# 质量检测
python scripts/dic_tools.py --test          # 运行测试套件

# 数据备份
python scripts/dic_tools.py --backup        # 备份数据
python scripts/dic_tools.py --restore       # 恢复数据
python scripts/dic_tools.py --undo-last-add # 撤回最近添加

# 系统维护
python scripts/dic_tools.py --clean         # 清理临时文件

# 组合使用
python scripts/dic_tools.py --stats --menu-after  # 先查看统计再进入菜单
```

#### 精简模式(短选项)

```bash
python scripts/dic_tools.py -v             # 校验
python scripts/dic_tools.py -g             # 生成文档
python scripts/dic_tools.py -c             # 更新changelog
python scripts/dic_tools.py -a             # 完整流程
python scripts/dic_tools.py -s             # 统计信息
python scripts/dic_tools.py -t             # 测试套件
```

---

## 📋 数据结构 (v2.0.0)

v2.0.0 采用极简设计，仅保留 FHIR Coding 核心字段:

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| system | string | 编码系统 URI | http://snomed.info/sct |
| code | string | 编码值 | 129006008 |
| display | string | 英文显示名称 | Walking |
| display_zh | string | 中文显示名称 | 步行 |

---

## 🎯 v2.0.0 设计原则

### YAGNI 原则

移除了所有当前未使用的字段:
- ❌ id - 使用 system|code 组合替代
- ❌ category - 未在业务中使用
- ❌ status - 所有词条均为 active
- ❌ version - 未启用版本管理
- ❌ description - 未在界面显示
- ❌ synonyms - 未在搜索中使用
- ❌ detection - 传感器检测能力未使用

### FHIR 标准对齐

严格遵循 FHIR Coding DataType 规范

### 数据安全

所有移除的字段数据已归档至 archive/removed_fields_v1.2.6/ (97 个文件)

---

## ⚠️ 重要规则

### 数据编辑规则

1. **唯一可编辑的数据源**: `coding_dictionary/coding_dictionary.json`
2. **禁止手动修改**: `auto_generated_docs/` 目录下任何文件
3. **禁止手动修改**: `changelog.md` 和 `.snapshot.json`（自动维护）
4. **提交前必须**: 运行 `--validate` 或 `--all` 确保文档同步

### 工作流规范

```bash
# 1. 编辑 JSON
vim coding_dictionary/coding_dictionary.json

# 2. 运行完整流程
python scripts/dic_tools.py --all

# 3. 提交变更
git add coding_dictionary/ auto_generated_docs/
git commit -m "feat: 添加新词条"
git push
```

### 临时文件清理

```bash
# 定期清理临时目录
python scripts/dic_tools.py --clean

# 或手动删除
rm -rf temp/*
Remove-Item -Recurse -Force temp\*
```

---

## 📊 当前统计

- 📊 词条总数: 79
- 🏥 SNOMED CT: 58.2%
- 🔧 Internal: 34.2%
- 📋 TDP: 7.6%
- 🧪 测试通过率: 100%

---

## 🏆 版本里程碑

### v2.0.0 (2025-11-12) - 当前版本

**重大变更**: 数据结构重构，精简为 FHIR 核心字段

**变更统计**:
- ✅ 词条总数: 79 (保持不变)
- 📉 字段数量: 11+  4 (减少 64%)
- 🗂️ 文件大小: ~50KB  ~8KB (减少 84%)

**恢复方法**:
```bash
# 恢复到 v1.2.6 (重构前)
git checkout v1.2.6-pre-refactor
```

---

## 📚 参考文档

- FHIR Coding DataType: https://www.hl7.org/fhir/datatypes.html#Coding
- SNOMED CT: https://www.snomed.org/

---

## 📄 许可

本项目为公司内部资源，未经书面许可不得对外分发或商业使用。

联系方式: benson@wisefido.com

---

**最后更新**: 2025-11-12  
**版本**: v2.0.0  
**维护者**: WiseFido Team
