# Coding Dictionary 数据结构规范

> 本文档详细解释 `coding_dictionary.json` 的数据结构和字段定义，对应 `schema/coding_dictionary.schema.json`

---

## 📋 概述

每个编码词条（Coding Item）是一个 JSON 对象，包含必填字段和可选字段。所有词条必须通过 JSON Schema 验证。

**Schema 文件**: `schema/coding_dictionary.schema.json`

---

## 🔑 必填字段

### 1. `id` - 全局唯一标识符

**类型**: `string`  
**格式**: `{system_prefix}:{code}`  
**正则**: `^[a-z0-9_./:+-]+$`

**说明**: 词条的唯一标识符，由编码系统前缀和编码值组成。

**示例**:
```json
"id": "snomed:129006008"
"id": "internal:0002"
"id": "tdp:emergency"
```

**格式要求**:
- 系统前缀使用小写字母（如 `snomed`、`internal`、`tdp`）
- 使用冒号 `:` 分隔系统前缀和编码值
- 全局唯一，不可重复

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

### 3. `system` - 编码系统 URI

**类型**: `string`

**说明**: 编码系统的标准 URI，标识编码来源。

**常用系统**:
```json
"system": "http://snomed.info/sct"              // SNOMED CT
"system": "http://loinc.org"                    // LOINC
"system": "http://hl7.org/fhir/sid/icd-10"     // ICD-10
"system": "http://wisefido.com/tdp/v1"         // TDP v1 (内部)
"system": "http://wisefido.com/internal"       // 内部编码系统
```

---

### 4. `display` - 英文显示名称

**类型**: `string`

**说明**: 词条的标准英文名称，用于国际化显示。

**示例**:
```json
"display": "Standing"
"display": "Walking"
"display": "Falls"
```

---

### 5. `display_zh` - 中文显示名称

**类型**: `string`

**说明**: 词条的中文名称，用于本地化显示。

**示例**:
```json
"display_zh": "站立"
"display_zh": "步行"
"display_zh": "跌倒"
```

---

### 6. `category` - 词条分类

**类型**: `string`  
**枚举值**: 6 个固定分类

**说明**: 词条所属的功能分类，用于组织和检索。

**分类枚举**:
```json
"category": "posture_codes"              // 姿态编码
"category": "motion_codes"               // 运动编码
"category": "physiological_codes"        // 生理指标编码
"category": "disorder_condition_codes"   // 疾病状况编码
"category": "safety_alert_codes"         // 安全警报编码
"category": "tag"                        // 自定义标签
```

**详细说明**: 参见 [分类体系规范](./coding_dictionary_classification.md)

---

### 7. `status` - 词条状态

**类型**: `string`  
**枚举值**: `active` | `deprecated` | `draft`

**说明**: 词条的生命周期状态。

**状态说明**:
- **`active`**: 活跃状态，可正常使用
- **`deprecated`**: 已弃用，不推荐使用（向后兼容）
- **`draft`**: 草稿状态，尚未正式发布

**示例**:
```json
"status": "active"
```

---

### 8. `version` - 语义版本号

**类型**: `string`  
**格式**: `MAJOR.MINOR.PATCH`  
**正则**: `^[0-9]+\.[0-9]+\.[0-9]+$`

**说明**: 词条的版本号，遵循语义化版本规范。

**版本规则**:
- **MAJOR**: 不兼容的重大变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

**示例**:
```json
"version": "1.0.0"
"version": "1.2.3"
```

---

## 📝 可选字段

### 9. `description` - 英文详细描述

**类型**: `string`

**说明**: 词条的详细英文描述，解释含义、用途、适用场景等。

**示例**:
```json
"description": "Patient is in a standing posture, detected by 60GHz radar sensor."
```

---

### 10. `description_zh` - 中文详细描述

**类型**: `string`

**说明**: 词条的详细中文描述。

**示例**:
```json
"description_zh": "患者处于站立姿态，由60GHz雷达传感器检测。"
```

---

### 11. `synonyms` - 英文同义词

**类型**: `array<string>`

**说明**: 英文同义词列表，用于搜索和匹配。

**示例**:
```json
"synonyms": ["Standing position", "Upright posture", "Standing up"]
```

---

### 12. `synonyms_zh` - 中文同义词

**类型**: `array<string>`

**说明**: 中文同义词列表。

**示例**:
```json
"synonyms_zh": ["站立姿势", "直立", "站立状态"]
```

---

### 13. `source_refs` - 来源追溯

**类型**: `array<object>`

**说明**: 词条的来源参考信息，用于可追溯性。

**对象结构**:
- `file` (必填): 来源文件名
- `section` (可选): 来源章节

**示例**:
```json
"source_refs": [
  {
    "file": "tdpv1-0916-fixed.md",
    "section": "姿态检测"
  },
  {
    "file": "fda-v0923.md"
  }
]
```

---

### 14. `detection` - 检测能力标注

**类型**: `object`

**说明**: 标注各传感器对该词条的检测能力。

**支持的传感器**: `radar_60ghz` (60GHz 毫米波雷达)

**子字段**:
- `detectable`: 可检测性 (`direct` | `indirect` | `not_detectable`)
- `method`: 检测方法
- `confidence`: 检测置信度 (`low` | `medium` | `high`)
- `frequency_range`: 频率范围
- `velocity_threshold`: 速度阈值
- `requires_ml`: 是否需要机器学习

**示例**:
```json
"detection": {
  "radar_60ghz": {
    "detectable": "direct",
    "method": "Doppler velocity analysis",
    "confidence": "high",
    "frequency_range": "60-64 GHz",
    "velocity_threshold": "0.1 m/s",
    "requires_ml": false
  }
}
```

---

### 15. `fhir` - FHIR 资源映射

**类型**: `object`

**说明**: 映射到 FHIR 标准资源，用于互操作性。

**子字段**:
- `resource_type`: FHIR 资源类型
- `loinc_code`: LOINC 编码（用于观测值）

**示例**:
```json
"fhir": {
  "resource_type": "Observation",
  "loinc_code": "8867-4"
}
```

---

## 🛡️ 验证规则

### Schema 验证

所有词条必须通过 `schema/coding_dictionary.schema.json` 的验证：

```bash
python scripts/validate_json.py
```

### 关键验证点

1. **必填字段完整性**: 8 个必填字段必须全部存在
2. **ID 唯一性**: 同一 ID 不能重复
3. **枚举值合法性**: `category` 和 `status` 必须是枚举值之一
4. **版本号格式**: 必须符合语义化版本规范
5. **字段类型正确**: 字符串、数组、对象类型必须匹配
6. **无额外字段**: `additionalProperties: false`，禁止未定义字段

---

## � 完整示例

### 示例 1: SNOMED CT 词条

```json
{
  "id": "snomed:10904000",
  "code": "10904000",
  "system": "http://snomed.info/sct",
  "display": "Standing",
  "display_zh": "站立",
  "category": "posture_codes",
  "status": "active",
  "version": "1.0.0",
  "description": "Patient is in a standing posture.",
  "description_zh": "患者处于站立姿态。",
  "synonyms": ["Standing position", "Upright posture"],
  "synonyms_zh": ["站立姿势", "直立姿态"],
  "source_refs": [
    {
      "file": "tdpv1-0916-fixed.md",
      "section": "姿态检测"
    }
  ],
  "detection": {
    "radar_60ghz": {
      "detectable": "direct",
      "method": "Static posture analysis",
      "confidence": "high"
    }
  }
}
```

### 示例 2: 内部编码词条

```json
{
  "id": "internal:0002",
  "code": "0002",
  "system": "http://wisefido.com/internal",
  "display": "Lying Supine",
  "display_zh": "仰卧",
  "category": "posture_codes",
  "status": "active",
  "version": "1.0.0"
}
```

### 示例 3: TDP 协议词条

```json
{
  "id": "tdp:emergency",
  "code": "emergency",
  "system": "http://wisefido.com/tdp/v1",
  "display": "Emergency",
  "display_zh": "紧急",
  "category": "safety_alert_codes",
  "status": "active",
  "version": "1.0.0",
  "description": "Highest priority alert level requiring immediate attention.",
  "description_zh": "最高优先级警报，需要立即关注。"
}
```

---

## 🔧 开发指南

### 添加新词条

使用交互式工具添加：
```bash
python scripts/dic_tools.py
# 选择选项 8：交互式添加单个词条
```

或使用批量添加脚本：
```bash
python scripts/add_coding_dict.py
```

### 验证数据

```bash
# 完整验证（Schema + 逻辑）
python scripts/validate_json.py

# 或使用主工具
python scripts/dic_tools.py
# 选择选项 1：校验词条数据
```

### 生成文档

```bash
# 生成 Markdown 文档
python scripts/generate_md.py

# 或使用主工具
python scripts/dic_tools.py
# 选择选项 2：生成 Markdown 文档
```

---

## 📚 相关文档

- [分类体系规范](./coding_dictionary_classification.md) - 6 大分类详细说明
- [coding_dictionary.schema.json](../schema/coding_dictionary.schema.json) - JSON Schema 验证规则
- [README.md](../README.md) - 项目主文档

---

## 📝 变更历史

### v1.0.0 - 2024
- 初始版本，定义核心字段结构
- 支持 SNOMED CT、LOINC、ICD-10 等标准编码系统
- 实现 6 大分类体系
- 添加检测能力标注（60GHz 雷达）
- 支持 FHIR 资源映射

