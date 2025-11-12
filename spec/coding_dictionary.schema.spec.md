# Coding Dictionary 数据结构规范 (v2.0.0)

> 本文档详细解释 `coding_dictionary.json` 的数据结构和字段定义，对应 `schema/coding_dictionary.schema.json`  
> **版本**: v2.0.0 | **更新日期**: 2025-11-12

---

## 📋 概述

v2.0.0 采用**极简设计**,仅保留 FHIR Coding 核心字段,遵循 **YAGNI 原则** (You Aren't Gonna Need It)。

每个编码词条（Coding Item）包含 **4 个必填字段**,通过 `additionalProperties: true` 支持按需扩展。

**Schema 文件**: `schema/coding_dictionary.schema.json`  
**FHIR 标准**: [FHIR Coding DataType](https://www.hl7.org/fhir/datatypes.html#Coding)

---

## 🎯 v2.0.0 重构说明

### 重构目标
- ✅ **FHIR 标准对齐**: 严格遵循 FHIR Coding 数据类型规范
- ✅ **YAGNI 原则**: 移除所有未使用的字段
- ✅ **简化维护**: 减少字段数量 (11+ → 4),降低维护成本
- ✅ **可扩展性**: 通过 `additionalProperties: true` 支持按需扩展

### 字段变更统计
- **v1.2.6**: 11+ 字段 (id, code, system, display, display_zh, category, status, version, description, synonyms, detection, source_refs, fhir)
- **v2.0.0**: 4 核心字段 (system, code, display, display_zh)
- **减少**: 64% 字段数量

### 移除字段归档
所有移除的字段数据已归档至 `archive/removed_fields_v1.2.6/`,包含 97 个 JSON 文件,可随时恢复。

---

## 🔑 必填字段 (4个)

### 1. `system` - 编码系统 URI

**类型**: `string`  
**格式**: URI (支持 `http://`, `https://`, `internal://`, `tdp://`)

**说明**: 编码系统的标准 URI，标识编码来源。

**常用系统**:
```json
"system": "http://snomed.info/sct"              // SNOMED CT
"system": "http://loinc.org"                    // LOINC
"system": "http://hl7.org/fhir/sid/icd-10"     // ICD-10
"system": "internal://wisefido/coding"          // 内部编码系统
"system": "tdp://wisefido/v1"                   // TDP v1
```

**Schema 验证**:
```json
{
  "pattern": "^(https?|internal|tdp)://.+"
}
```

---

### 2. `code` - 编码值

**类型**: `string`

**说明**: 原始编码值，来自特定编码系统。

**示例**:
```json
"code": "129006008"        // SNOMED CT 编码
"code": "0002"             // 内部编码
"code": "emergency"        // TDP 编码
```

---

### 3. `display` - 英文显示名称

**类型**: `string`

**说明**: 词条的标准英文名称，用于国际化显示。

**示例**:
```json
"display": "Standing"
"display": "Walking"
"display": "Falls"
```

---

### 4. `display_zh` - 中文显示名称

**类型**: `string`

**说明**: 词条的中文名称，用于本地化显示。

**示例**:
```json
"display_zh": "站立"
"display_zh": "步行"
"display_zh": "跌倒"
```

---

## 🔧 可扩展字段

v2.0.0 通过 Schema 的 `additionalProperties: true` 支持按需扩展字段。

**示例**:
```json
{
  "system": "http://snomed.info/sct",
  "code": "129006008",
  "display": "Walking",
  "display_zh": "步行",
  
  // 可按需添加自定义字段
  "category": "motion_codes",
  "detection": {
    "radar_60ghz": {
      "detectable": "direct",
      "confidence": "high"
    }
  },
  "custom_field": "任意自定义字段"
}
```

**说明**:
- ✅ Schema 验证只检查 4 个核心字段
- ✅ 其他字段可按需添加,不影响验证
- ✅ 支持渐进式扩展,按需增加功能

---

## 🗑️ v1.2.6 移除的字段

以下字段在 v2.0.0 中被移除,数据已归档至 `archive/removed_fields_v1.2.6/`:

### ❌ `id` - 全局唯一标识符
**原格式**: `{system_prefix}:{code}` (例: `snomed:129006008`)  
**v2.0.0 替代**: 使用 `system|code` 组合标识 (例: `http://snomed.info/sct|129006008`)

### ❌ `category` - 词条分类
**原枚举**: `posture_codes`, `motion_codes`, `physiological_codes`, `disorder_condition_codes`, `safety_alert_codes`, `tag`  
**移除原因**: 未在实际业务中使用

### ❌ `status` - 词条状态
**原枚举**: `active`, `deprecated`, `draft`  
**移除原因**: 所有词条均为 active,无需此字段

### ❌ `version` - 语义版本号
**原格式**: `MAJOR.MINOR.PATCH` (例: `1.0.0`)  
**移除原因**: 未启用版本管理机制

### ❌ `description` / `description_zh` - 详细描述
**移除原因**: 未在界面中使用

### ❌ `synonyms` / `synonyms_zh` - 同义词
**移除原因**: 未在搜索中使用

### ❌ `source_refs` - 来源追溯
**移除原因**: 未使用

### ❌ `detection` - 传感器检测能力
**移除原因**: 未在实际系统中使用

### ❌ `fhir` - FHIR 资源映射
**移除原因**: 未使用

---

## 🛡️ 验证规则

### Schema 验证

所有词条必须通过 `schema/coding_dictionary.schema.json` 的验证:

```bash
python scripts/validate_json.py
```

### 关键验证点

1. **必填字段完整性**: 4 个必填字段必须全部存在
2. **system|code 唯一性**: 同一 system+code 组合不能重复
3. **字段类型正确**: 字符串类型必须匹配
4. **URI 格式正确**: `system` 字段必须符合 URI 格式

---

## 📝 完整示例

### 最小化示例 (推荐)

```json
{
  "system": "http://snomed.info/sct",
  "code": "10904000",
  "display": "Standing",
  "display_zh": "站立"
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

### 内部编码示例

```json
{
  "system": "internal://wisefido/coding",
  "code": "0002",
  "display": "Lying Supine",
  "display_zh": "仰卧"
}
```

### TDP 协议示例

```json
{
  "system": "tdp://wisefido/v1",
  "code": "emergency",
  "display": "Emergency",
  "display_zh": "紧急"
}
```

---

## 🔧 开发指南

### 添加新词条

使用交互式工具添加:
```bash
python scripts/add_coding_dict.py
```

输入 4 个核心字段即可:
1. `system` - 编码系统 URI
2. `code` - 编码值
3. `display` - 英文名称
4. `display_zh` - 中文名称

### 验证数据

```bash
# 完整验证
python scripts/validate_json.py

# 或使用主工具
python scripts/dic_tools.py --validate
```

### 生成文档

```bash
# 生成 Markdown 文档
python scripts/generate_md.py

# 或使用主工具
python scripts/dic_tools.py --generate-md
```

---

## 📚 相关文档

- [coding_dictionary.schema.json](../schema/coding_dictionary.schema.json) - JSON Schema 验证规则
- [README.md](../README.md) - 项目主文档
- [FHIR Coding DataType](https://www.hl7.org/fhir/datatypes.html#Coding) - FHIR 官方文档
- [archive/removed_fields_v1.2.6/](../archive/removed_fields_v1.2.6/) - v1.2.6 移除字段归档

---

## 📝 变更历史

### v2.0.0 - 2025-11-12
- 🎯 **重大重构**: 精简为 4 核心字段
- ✅ FHIR 标准对齐
- ✅ YAGNI 原则应用
- ✅ 支持按需扩展 (`additionalProperties: true`)
- 📦 移除 11 个字段,数据归档至 `archive/removed_fields_v1.2.6/`

### v1.2.6 - 2025-11-12
- v2.0.0 重构前的最后版本
- 11+ 字段完整结构
- 归档至 `archive/removed_fields_v1.2.6/`

### v1.0.0 - 2024
- 初始版本，定义核心字段结构
- 支持 SNOMED CT、LOINC、ICD-10 等标准编码系统
- 实现 6 大分类体系
- 添加检测能力标注（60GHz 雷达）
- 支持 FHIR 资源映射

---

## 💡 常见问题

### Q1: 为什么移除了这么多字段?
A: 遵循 YAGNI 原则 (You Aren't Gonna Need It)。经过分析,这些字段在实际业务中未被使用,保留它们增加了维护成本。所有数据已归档,需要时可恢复。

### Q2: 如果未来需要这些字段怎么办?
A: v2.0.0 支持 `additionalProperties: true`,可按需添加任何字段。从归档数据恢复也很简单。

### Q3: v1.2.6 的数据会丢失吗?
A: 不会。所有移除的字段数据已归档至 `archive/removed_fields_v1.2.6/`,并且可以通过 Git 标签 `v1.2.6-pre-refactor` 恢复完整项目。

### Q4: 如何恢复到 v1.2.6?
A: 运行 `git checkout v1.2.6-pre-refactor` 即可恢复到重构前的完整版本。
