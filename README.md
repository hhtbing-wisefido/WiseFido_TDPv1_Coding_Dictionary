# 📦 WiseFido_TDPv1_Coding_Dictionary

> 🎯 **FHIR 标准医疗编码字典库** | v2.0.0 精简版 | JSON Schema 验证 | 自动文档生成 | YAGNI 原则

[![Copyright: WiseFido](https://img.shields.io/badge/Copyright-WiseFido-blue.svg)](https://www.wisefid---

## 🧪 测试套件

脚本内置 **数据质量校验**,验证必填字段、数据格式、system|code 唯一性等。

运行:

```bash
python scripts/dic_tools.py --test
```

所有项通过后会输出"🎉 所有测试通过!"。

---

## 🎯 v2.0.0 设计原则

### YAGNI 原则 (You Aren't Gonna Need It)

v2.0.0 移除了所有**当前未使用**的字段:
- ❌ `category` - 分类信息 (未在实际业务中使用)
- ❌ `status` - 所有词条均为 active,无需此字段
- ❌ `version` - 未启用版本管理机制
- ❌ `detection` - 传感器检测能力 (未实际使用)
- ❌ `synonyms` - 同义词 (未在搜索中使用)
- ❌ `source_refs` - 来源追溯 (未使用)

### FHIR 标准对齐

严格遵循 [FHIR Coding](https://www.hl7.org/fhir/datatypes.html#Coding) 数据类型:

```json
{
  "system": "uri",      // 编码系统标识
  "code": "string",     // 编码值
  "display": "string"   // 显示名称
}
```

我们增加了 `display_zh` 以支持中文本地化。

### 可扩展性保障

通过 Schema 的 `additionalProperties: true` 支持按需扩展:

```json
{
  "system": "http://snomed.info/sct",
  "code": "129006008",
  "display": "Walking",
  "display_zh": "步行",
  
  // 未来可按需添加
  "category": "motion_codes",
  "confidence": 0.95,
  "custom_field": "任意自定义字段"
}
```

### 数据安全

所有移除的字段数据已归档至 `archive/removed_fields_v1.2.6/`,可随时恢复:

```bash
# 查看归档文件
ls archive/removed_fields_v1.2.6/

# 恢复到 v1.2.6 (重构前)
git checkout v1.2.6-pre-refactor
```thon 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v2.0.0-green.svg)](https://github.com/hhtbing-wisefido/WiseFido_TDPv1_Coding_Dictionary/releases/tag/v2.0.0)

---

## 💡 项目简介

WiseFido_TDPv1_Coding_Dictionary 是基于 **FHIR Coding 标准**构建的医疗编码字典库，用于 OWL Monitor System（多传感器老人健康监测系统）的统一术语管理。

### ✨ v2.0.0 核心特性

- 🎯 **FHIR 标准兼容**：严格遵循 FHIR Coding 核心字段规范 (system, code, display)
- 🔒 **极简数据模型**：仅保留 4 个核心字段，遵循 YAGNI 原则
- 🤖 **JSON Schema 验证**：自动验证数据完整性和合法性
- 📖 **自动文档生成**：一键生成 Markdown 文档和变更日志
- 🔄 **可扩展架构**：支持通过 `additionalProperties` 按需扩展字段
- 🏥 **多编码系统支持**：SNOMED CT、Internal、TDP 等编码系统

---

## 📁 仓库结构oding_Dictionary

> 🎯 **可复用医疗编码字典库**｜JSON 唯一事实源｜自动生成 Markdown｜变更追踪｜FHIR/SNOMED CT 兼容

[![Copyright: WiseFido](https://img.shields.io/badge/Copyright-WiseFido-blue.svg)](https://www.wisefido.com)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 项目简介

WiseFido_TDPv1_Coding_Dictionary 基于 **TDPv1 协议** 与 **FHIR/SNOMED CT** 标准构建，是 OWL Monitor System（多传感器老人健康监测系统）的统一术语库。

主要特性：

- **多传感器覆盖**：60 GHz 雷达、睡眠板、MEMS 地震传感器、SOS 手柄等能力统一建模
- **机器可信**：JSON 作为唯一事实源，配套 JSON Schema 与自动验证脚本
- **人类可读**：一键生成中英文对照的 Markdown 文档和变更日志
- **变更追踪**：快照对比与自动 changelog，便于审计与回滚
- **医疗标准**：兼容 FHIR、SNOMED CT、LOINC，并支持内部编码
- **预警支撑**：可映射帕金森、卒中、心梗等预警规则

---

## 📂 目录组织规范

**保持项目根目录整洁,所有文件按类型放置到正确目录:**

```plaintext
项目根目录/
├── README.md              ✅ 项目说明文档
├── requirements.txt       ✅ Python 依赖配置
├── .gitignore            ✅ Git 忽略规则
├── .git/                 ✅ Git 版本控制
├── .venv/                ✅ Python 虚拟环境
├── .github/              ✅ GitHub Actions 配置
│
├── coding_dictionary/    📁 核心数据源 (唯一可手动编辑)
├── auto_generated_docs/  📁 自动生成的文档和报告 (禁止手动修改)
├── temp/                 📁 临时文件、草稿、测试文件 (可定期清理)
├── scripts/              📁 维护脚本和工具
├── schema/               📁 JSON Schema 定义
├── spec/                 📁 数据规范说明文档
├── auto_backup/          📁 自动备份文件 (本地备份,不提交到 Git)
├── Project_backup/       📁 项目里程碑备份 (本地备份,不提交到 Git)
└── 原始参考文件/          📁 参考资料
```

**⚠️ 重要规则:**
- ❌ **禁止在项目根目录创建任何总结报告 (`*_SUMMARY.md`)、临时文件 (`*.tmp`)、测试文件**
- ✅ **所有自动生成的文档** → `auto_generated_docs/`
- ✅ **所有临时文件** → `temp/`
- 📖 详细规则见 [`auto_generated_docs/FILE_ORGANIZATION_RULES.md`](auto_generated_docs/FILE_ORGANIZATION_RULES.md)

---

## 📁 仓库结构

```plaintext
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
```

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
# 首次执行（自动安装缺失依赖）
python scripts/dic_tools.py

# 或手动安装
pip install -r requirements.txt
```

### 2️⃣ 交互式菜单

```bash
python scripts/dic_tools.py
```

完整菜单结构：

#### 📊 【数据管理】
1. 校验词条数据 - 检查 JSON 格式和数据规范
2. 生成文档 - 生成可读的 Markdown 文档
3. 更新变更日志 - 记录词条变更历史
4. 执行完整流程 - 一键校验+生成+更新

#### 🔍 【数据查询】
5. 显示统计信息 - 查看词条分类和数量统计
6. 搜索词条 - 按条件查找词条
7. 查看词条详情 - 查看单个词条完整信息

#### ✏️ 【数据编辑】
8. 添加新词条 - 交互式添加单个词条
9. 撤回最近添加 - 删除最后一次添加的词条

#### 🧪 【质量检测】
10. 运行测试套件 - 执行 6 项数据质量测试

#### 💾 【数据备份】
11. 备份数据 - 手动备份词条数据
12. 恢复数据 - 从备份恢复数据

#### 🔧 【系统维护】
13. 清理临时文件 - 删除临时目录内容
0. 退出系统 - 关闭管理工具

### 3️⃣ 常用参数模式

```bash
python scripts/dic_tools.py --validate      # 校验
python scripts/dic_tools.py --generate-md   # 生成 Markdown
python scripts/dic_tools.py --changelog     # 更新变更日志
python scripts/dic_tools.py --all           # 完整流程
python scripts/dic_tools.py --stats         # 统计信息
python scripts/dic_tools.py --test          # 测试套件
python scripts/dic_tools.py --clean         # 清理 temp/
python scripts/dic_tools.py --backup        # 备份 JSON
python scripts/dic_tools.py --restore       # 恢复 JSON（含确认）
python scripts/dic_tools.py --undo-last-add # 撤回最近一次添加
python scripts/dic_tools.py --search id:snomed   # 条件搜索
python scripts/dic_tools.py --view snomed:129006008 # 查看详情
python scripts/dic_tools.py --stats --menu-after  # 先执行再回菜单
```

> `--menu-after` 便于“先跑一项任务再继续人工操作”。

#### 精简模式(短选项 `-`)
```bash
python scripts/dic_tools.py -v             # 校验
python scripts/dic_tools.py -g             # 生成 Markdown
python scripts/dic_tools.py -c             # 更新变更日志
python scripts/dic_tools.py -a             # 完整流程
python scripts/dic_tools.py -s             # 统计信息
python scripts/dic_tools.py -t             # 测试套件
```

> **提示**:
> - 精简模式仅支持常用功能，复杂操作需使用完整模式
> - `--menu-after` 可与任何参数组合，先执行命令再进入交互菜单

---

## 🧪 测试套件

脚本内置 **6 项校验**：必填字段、ID 格式、重复 ID、code+system 唯一性、分类合法性、版本号格式。

运行：

```bash
python scripts/dic_tools.py --test
```

所有项通过后会输出“🎉 所有测试通过!”。

---

## 🔄 标准工作流

```bash
# 1. 编辑 JSON（coding_dictionary/coding_dictionary.json）
# 2. 运行完整流程
python scripts/dic_tools.py --all
# 3. 提交变更
git add coding_dictionary/ auto_generated_docs/
git commit -m "feat: xxx"
git push
```

> 提交前务必运行 `--validate` 或 `--all`，确保自动生成文件已更新。

---

## 📋 数据结构 (v2.0.0)

### ✅ 核心字段 (必填)

> v2.0.0 采用极简设计，仅保留 FHIR Coding 核心字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `system` | string | 编码系统 URI | `http://snomed.info/sct` |
| `code` | string | 编码值 | `129006008` |
| `display` | string | 英文显示名称 | `Walking` |
| `display_zh` | string | 中文显示名称 | `步行` |

### � 可扩展字段

通过 Schema 的 `additionalProperties: true` 支持按需扩展:

```json
{
  "system": "http://snomed.info/sct",
  "code": "129006008",
  "display": "Walking",
  "display_zh": "步行",
  "custom_field": "按需添加的字段"
}
```

### 🏷️ 编码系统分布

- **SNOMED CT** (58.2%): 国际标准医疗编码
- **Internal** (34.2%): WiseFido 内部编码
- **TDP** (7.6%): TDPv1 协议编码

---

## 📝 词条示例

### 最小化示例
```json
{
  "system": "http://snomed.info/sct",
  "code": "129006008",
  "display": "Walking",
  "display_zh": "步行"
}
```

### 扩展示例
```json
{
  "system": "http://snomed.info/sct",
  "code": "129006008",
  "display": "Walking",
  "display_zh": "步行",
  "description": "Periodic gait pattern with low to moderate speed.",
  "description_zh": "周期性步态，速度低至中等。",
  "category": "motion_codes"
}
```

---

## ⚠️ 重要规则

### 📁 数据编辑规则

1. **唯一可编辑的数据源**: `coding_dictionary/coding_dictionary.json` (所有词条修改必须在此文件进行)
2. **禁止手动修改**: `auto_generated_docs/` 目录下的任何文件 (由脚本自动生成)
3. **禁止手动修改**: `changelog.md` 和 `.snapshot.json` (自动维护,包含完整统计和分类信息)
4. **查看变更总结**: `auto_generated_docs/changelog.md` 提供详细的统计报告,包括分类分布、编码系统、雷达检测能力等

### 📂 目录使用规范

| 目录 | 用途 | 可编辑 | 说明 |
|------|------|--------|------|
| `auto_generated_docs/` | 脚本自动生成的产品文档 | ❌ 否 | **仅存放脚本自动生成的产品文档**,禁止手动修改 |
| `temp/` | 临时文件、草稿、测试文件、**过程记录文档** | ✅ 是 | 草稿、测试文件、**过程记录文档**,可定期清理 |
| `coding_dictionary/` | 核心数据源 | ✅ 是 | 唯一可手动编辑的数据文件 |
| `scripts/` | 维护脚本 | ✅ 是 | Python 脚本,不放数据文件 |
| `schema/` | Schema 定义 | ✅ 是 | JSON Schema 规范定义 |
| `spec/` | 规范文档 | ✅ 是 | 数据结构说明文档 |
| `auto_backup/` | 自动备份 | ❌ 否 | 脚本自动创建,本地保留,不提交 Git |
| `Project_backup/` | 项目备份 | ❌ 否 | 里程碑备份,本地保留,不提交 Git |
| `原始参考文件/` | 参考资料 | ✅ 是 | 医疗标准文档等 |
| `项目根目录` | 核心配置 | ⚠️ 限制 | **仅放 README.md、requirements.txt、.gitignore 等核心配置** |

### 📋 文件分类规则

**`auto_generated_docs/` 只放这些文件**:
- ✅ `changelog.md` - 变更日志 (脚本生成)
- ✅ `coding_dictionary.md` - 词条表格 (脚本生成)
- ✅ `coding_dictionary.schema.md` - Schema说明 (脚本生成)
- ✅ `.snapshot.json` - 快照文件 (脚本维护)
- ✅ `FILE_ORGANIZATION_RULES.md` - 目录规则文档 (脚本生成)

**`temp/` 应存放这些文件**:
- ✅ `*_SUMMARY.md` - 开发过程记录
- ✅ `*_PROPOSAL.md` - 优化提案文档
- ✅ `*_IMPROVEMENT.md` - 改进记录
- ✅ `*_CLARIFICATION.md` - 说明文档
- ✅ `*_backup.*` - 临时备份

**重要原则**: 
- ❌ **过程记录文档** (如优化总结、改进记录) → `temp/`
- ✅ **产品文档** (如自动生成的表格、changelog) → `auto_generated_docs/`

### 🗂️ 临时目录 `temp/`

- 统一存放 `__pycache__`、批量导入草稿、校验中间文件
- 建议定期清理：

```bash
# 跨平台清理
python scripts/dic_tools.py --clean
# 或手动
rm -rf temp/*
Remove-Item -Recurse -Force temp\*
```

### 🔄 临时文件工作流

```bash
python scripts/add_coding_dict.py --dry-run
python scripts/validate_json.py temp/coding_terms_scaffold_new_tmp.json
python scripts/add_coding_dict.py   # 确认无误后正式写入
python scripts/dic_tools.py --clean
```

---

## 📚 参考文档

| 文档                                                                         | 说明                                                  |
| ---------------------------------------------------------------------------- | ----------------------------------------------------- |
| tdpv1-0916-fixed.md                                                          | TDPv1 协议与风险等级                                  |
| fhir与snomed_ct代码.md                                                       | 医疗编码标准参考                                      |
| fda-v0923.md                                                                 | OWL Monitor System 架构（雷达/睡眠板/地震传感器/SOS） |
| [FHIR CodeableConcept](https://www.hl7.org/fhir/datatypes.html#CodeableConcept) | 官方 FHIR 文档                                        |

---

## ⚠️ 风险提示

- ⚕️ 医疗编码仅用于系统互操作，临床使用须结合最新监管要求
- 🔐 预警逻辑需在后端规则引擎中再次验证
- 📡 传感器检测能力需在现场环境复核
- 🚫 本项目不构成医疗诊断依据

---

## 📄 许可

本项目为公司内部资源，未经书面许可不得对外分发或商业使用。如需授权请联系：benson@wisefido.com。

---

## 🔧 环境与编码

- 推荐使用虚拟环境：
  - Windows PowerShell：`python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt`
  - Linux/macOS：`python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Windows 终端若出现中文乱码，可运行 `chcp 65001` 或设置 `$OutputEncoding` 为 UTF-8
- 请使用 UTF-8 编码保存所有文件

## 🤖 CI/CD 自动化

- GitHub Actions：`.github/workflows/ci.yml`
  - 步骤：`--validate` → `--generate-md` → `--changelog` → `git diff`
  - 建议提交包含 `auto_generated_docs/` 目录，方便在 PR 中审阅

## 📊 统计信息获取

- 运行 `python scripts/dic_tools.py --stats` 查看最新分类/状态/系统分布
- README 不再固定展示静态“当前统计”，以免与真实数据漂移

---

最后更新日期: 2025-11-12  
最后更新说明: v2.0.0 重构 - 精简为 4 核心字段,遵循 FHIR 标准和 YAGNI 原则  
版本: v2.0.0  
维护者: WiseFido Team

---

## 🏆 版本里程碑

### 📌 v2.0.0 (2025-11-12) - 当前版本 ✅

**重大变更**: 数据结构重构，精简为 FHIR 核心字段

#### 🎯 重构目标
- **YAGNI 原则**: You Aren't Gonna Need It - 移除所有未使用的字段
- **FHIR 标准对齐**: 严格遵循 FHIR Coding 数据类型规范
- **简化维护**: 减少字段数量，降低维护成本
- **可扩展性**: 通过 `additionalProperties: true` 支持按需扩展

#### 📊 变更统计
- ✅ **词条总数**: 79 (保持不变)
- 📉 **字段数量**: 11+ 字段 → 4 核心字段 (减少 64%)
- 🗂️ **文件大小**: ~50KB → ~8KB (减少 84%)
- 📦 **归档文件**: 97 个 JSON 文件保存移除的字段数据

#### 🔄 字段变更

**保留字段** (4个):
- ✅ `system` - 编码系统 URI
- ✅ `code` - 编码值
- ✅ `display` - 英文显示名称
- ✅ `display_zh` - 中文显示名称

**移除字段** (11个,已归档至 `archive/removed_fields_v1.2.6/`):
- ❌ `id` - 使用 `system|code` 组合标识
- ❌ `category` - 分类信息 (未使用)
- ❌ `status` - 状态字段 (全部为 active)
- ❌ `version` - 版本号 (未使用)
- ❌ `description` / `description_zh` - 详细描述
- ❌ `synonyms` / `synonyms_zh` - 同义词
- ❌ `source_refs` - 来源追溯
- ❌ `detection` - 传感器检测能力
- ❌ `fhir` - FHIR 资源映射

#### � 归档说明
所有移除的字段数据已归档至:
- **路径**: `archive/removed_fields_v1.2.6/`
- **文件数**: 97 个 JSON 文件
- **命名格式**: `{system}_{code}.json` (例: `http___snomed.info_sct_129006008.json`)
- **内容**: 每个文件包含该词条的所有移除字段

#### 🔧 脚本更新
所有 6 个维护脚本已更新适配 v2.0.0:
- ✅ `validate_json.py` - 验证 4 核心字段
- ✅ `generate_md.py` - 生成简化文档
- ✅ `changelog.py` - 使用 system|code 标识
- ✅ `add_coding_dict.py` - 交互式 4 字段输入
- ✅ `dic_tools.py` - 简化统计和搜索
- ✅ `get_project_stats.py` - 仅统计编码系统分布

#### 📊 当前统计
- 📊 词条总数: 79 (SNOMED CT 58.2% | Internal 34.2% | TDP 7.6%)
- 🧪 测试通过率: 100%

#### 🔗 恢复到上一版本
如需恢复到 v1.2.6 (重构前版本):
```bash
git checkout v1.2.6-pre-refactor
```

---

### 📌 v1.2.6-pre-refactor (2025-11-12)

**Git Tag**: `v1.2.6-pre-refactor` | **状态**: v2.0.0 重构前备份版本 ✅

这是 v2.0.0 重构前的最后一个稳定版本,包含 79 个词条和完整的 11+ 字段结构。

#### � 版本快照
- 📊 词条总数: 79
- 📂 字段数量: 11+ 字段 (含 id, category, status, version, description, synonyms, detection 等)
- 🗂️ 文件大小: ~50KB
- 🧪 测试通过率: 100%

#### 🔄 恢复方法
```bash
# 查看此版本
git checkout v1.2.6-pre-refactor

# 基于此版本创建新分支
git checkout -b feature/new-work v1.2.6-pre-refactor
```

#### 📦 本地备份
- **路径**: `Project_backup/v1.2.6-pre-refactor_20251112_170815/`
- **内容**: 完整项目文件备份

---

### 📌 v1.2.4 (2025-11-12)

**状态**: 历史版本 | **词条数**: 79

扩展了 45 个新词条 (从 34 → 79),增长 132.4%,并应用了 Emoji-Enhanced Documentation 风格。

---

### 📌 v1.2.3-milestone (2025-11-11)

**Git Tag**: `v1.2.3-milestone` | **状态**: 首个稳定里程碑 ✅

第一个稳定里程碑，包含 34 个编码词条和完整基础功能。

#### 📸 版本快照
- 📊 词条总数: 34 (SNOMED CT 44.1% | Internal 38.2% | TDP 17.6%)
- 📂 分类数: 6 大类
- 🧪 测试通过率: 100%

---
