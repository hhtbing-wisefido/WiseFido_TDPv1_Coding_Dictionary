# CodingItem Schema 规范

> 🤖 **自动生成文档** - 本文档由 `scripts/generate_schema_md.py` 自动生成
> 
> 📄 **源文件**: `schema/coding_dictionary.schema.json`

---

## 📋 Schema 信息

- **Schema URI**: `http://json-schema.org/draft-07/schema#`
- **标题**: CodingItem
- **说明**: VS Code JSON Schema Validator compatible version
- **允许额外属性**: ❌ 否 (严格模式)
- **必填字段数量**: 8 个

---

## 🔑 字段列表

| 字段名 | 必填/可选 | 类型 | 说明 | 约束条件 |
|--------|----------|------|------|---------|
| **`id`** | ✅ 必填 | String | 全局唯一标识符 | 正则: `^[a-z0-9_./:+-]+$` |
| **`code`** | ✅ 必填 | String | 编码值 | - |
| **`system`** | ✅ 必填 | String | 编码系统 URI | - |
| **`display`** | ✅ 必填 | String | 英文显示名称 | - |
| **`display_zh`** | ✅ 必填 | String | 中文显示名称 | - |
| **`category`** | ✅ 必填 | String | 词条分类：posture_codes（姿态编码）、motion_codes（运动编码）、physiological_codes（生理指标编码）、disorder_condition_codes（疾病状况编码）、safety_alert_codes（安全警报编码）、tag（标签） | 枚举值: `posture_codes`, `motion_codes`, `physiological_codes`, `disorder_condition_codes`, `safety_alert_codes`, `tag` |
| **`status`** | ✅ 必填 | String | 词条状态 | 枚举值: `active`, `deprecated`, `draft` |
| **`version`** | ✅ 必填 | String | 语义版本号 | 正则: `^[0-9]+\.[0-9]+\.[0-9]+$` |
| **`description`** | 可选 | String | 英文详细描述 | - |
| **`description_zh`** | 可选 | String | 中文详细描述 | - |
| **`synonyms`** | 可选 | Array&lt;string&gt; | 英文同义词列表 | 元素类型: `string` |
| **`synonyms_zh`** | 可选 | Array&lt;string&gt; | 中文同义词列表 | 元素类型: `string` |
| **`source_refs`** | 可选 | Array&lt;object&gt; | 来源追溯 | 元素类型: `object` |
| **`detection`** | 可选 | Object | 检测能力标注 | - |
| **`fhir`** | 可选 | Object | FHIR 资源映射 | - |

---

## 📊 必填字段 (Required Fields)

以下 **8** 个字段为必填：

- **`id`** (String): 全局唯一标识符
- **`code`** (String): 编码值
- **`system`** (String): 编码系统 URI
- **`display`** (String): 英文显示名称
- **`display_zh`** (String): 中文显示名称
- **`category`** (String): 词条分类：posture_codes（姿态编码）、motion_codes（运动编码）、physiological_codes（生理指标编码）、disorder_condition_codes（疾病状况编码）、safety_alert_codes（安全警报编码）、tag（标签）
- **`status`** (String): 词条状态
- **`version`** (String): 语义版本号

---

## 📝 可选字段 (Optional Fields)

以下 **7** 个字段为可选：

- **`description`** (String): 英文详细描述
- **`description_zh`** (String): 中文详细描述
- **`synonyms`** (Array&lt;string&gt;): 英文同义词列表
- **`synonyms_zh`** (Array&lt;string&gt;): 中文同义词列表
- **`source_refs`** (Array&lt;object&gt;): 来源追溯
- **`detection`** (Object): 检测能力标注
- **`fhir`** (Object): FHIR 资源映射

---

## 🎯 枚举类型详解

### `category` 枚举值

**说明**: 词条分类：posture_codes（姿态编码）、motion_codes（运动编码）、physiological_codes（生理指标编码）、disorder_condition_codes（疾病状况编码）、safety_alert_codes（安全警报编码）、tag（标签）

**可选值**:

- `posture_codes`
- `motion_codes`
- `physiological_codes`
- `disorder_condition_codes`
- `safety_alert_codes`
- `tag`

### `status` 枚举值

**说明**: 词条状态

**可选值**:

- `active`
- `deprecated`
- `draft`


---

## 🏗️ 复杂类型结构

### `source_refs` 数组元素结构

**说明**: 来源追溯

**数组元素包含以下字段**:

- **`file`** (必填) (String): 来源文件
- **`section`** (可选) (String): 来源章节

### `detection` 对象结构

**说明**: 检测能力标注

**子字段**:

- **`radar_60ghz`** (Object): -

### `fhir` 对象结构

**说明**: FHIR 资源映射

**子字段**:

- **`resource_type`** (String): -
- **`loinc_code`** (String): -


---

## 📚 相关文档

- [数据结构与字段规范](../../spec/coding_dictionary.spec.md) - 人类撰写的详细规范
- [分类体系规范](../../spec/coding_dictionary_classification.md) - 分类定义
- [README.md](../../README.md) - 项目主文档

---

## ⚠️ 注意事项

1. 本文档由 Schema 自动生成，**请勿手动编辑**
2. 若需修改，请编辑 `schema/coding_dictionary.schema.json`
3. 运行 `python scripts/generate_schema_md.py` 重新生成
4. 详细的使用说明和示例请参考 [coding_dictionary.spec.md](../../spec/coding_dictionary.spec.md)
