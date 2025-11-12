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

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用交互式菜单

```bash
python scripts/dic_tools.py
```

### 常用命令

```bash
python scripts/dic_tools.py --validate      # 校验数据
python scripts/dic_tools.py --generate-md   # 生成文档  
python scripts/dic_tools.py --changelog     # 更新变更日志
python scripts/dic_tools.py --all           # 完整流程
python scripts/dic_tools.py --stats         # 统计信息
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

1. **唯一可编辑**: coding_dictionary/coding_dictionary.json
2. **禁止手动修改**: auto_generated_docs/ 目录  
3. **提交前必须**: 运行 --validate 或 --all

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
