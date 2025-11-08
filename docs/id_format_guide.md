# ID 格式规范

## 📋 概述

本文档定义了 WiseFido_TDPv1_Coding_Dictionary 项目中 ID 字段的格式规范。所有词条的 `id` 字段必须遵循本规范。

## ✅ 标准格式

ID 使用简洁格式，直接反映编码系统和编码值：

### 格式规则

```
{system_prefix}:{code}
```

### 示例

| 编码系统 | ID 格式示例 | 说明 |
|---------|------------|------|
| **SNOMED CT** | `snomed:129006008` | SNOMED CT 编码 |
| **Internal** | `internal:0002` | 内部编码 |
| **TDP** | `tdp:tdp://danger_level/emergency` 或 `tdp:emergency` | TDP 协议编码 |

### 格式要求

1. **系统前缀**：使用小写字母，如 `snomed`、`internal`、`tdp`
2. **分隔符**：使用冒号 `:` 分隔系统前缀和编码值
3. **编码值**：直接使用原始编码值，不添加额外信息
4. **唯一性**：每个 ID 在字典中必须全局唯一

## ❌ 禁止格式

以下格式不符合规范，**禁止使用**：

- ❌ `motion_state.walking.snomed.129006008`（包含分类信息）
- ❌ `posture.sitting.internal.posture.0001`（重复信息）
- ❌ `danger_level.emergency.tdp.emergency`（臃肿格式）

**原因**：这些格式包含冗余的分类信息，违反了简洁性原则，且可能导致维护困难。

## 🛡️ 开发规范

### 1. 数据源规范

在 `dictionary/coding_terms.json` 中，ID 字段必须：

- ✅ 使用标准格式：`{system_prefix}:{code}`
- ✅ 与 `code` 和 `system` 字段保持一致
- ✅ 确保全局唯一性

### 2. 生成脚本规范

所有生成脚本（如 `generate_md.py`）必须：

- ✅ **直接使用 JSON 中的 ID**，不进行任何转换
- ✅ **不重新构造 ID**，不拼接 `category`、`code`、`system`
- ✅ **保持 ID 原样输出**

**正确示例**：
```python
item_id = item['id']  # 直接使用，不转换
```

**错误示例**：
```python
# ❌ 禁止：不要重新构造 ID
item_id = f"{item['category']}.{item['code']}.{item['system']}"
```

### 3. 验证机制

`scripts/validate_json.py` 包含 ID 格式验证：

- 自动检测不符合规范的 ID 格式
- 验证 ID 的唯一性
- 在验证时报告格式错误

**运行验证**：
```bash
python scripts/validate_json.py
```

### 4. 快照文件同步

`scripts/changelog.py` 在每次运行时：

- 自动更新 `.snapshot.json` 文件
- 使用当前 JSON 文件中的 ID 格式
- 确保快照文件与源文件格式一致

## 📝 最佳实践

1. **始终使用简洁格式**：`system_prefix:code`
2. **直接使用 JSON 中的 ID**：不在生成脚本中重新构造
3. **保持文件同步**：确保快照文件与源文件格式一致
4. **定期验证**：在提交前运行验证脚本
5. **文档化变更**：如果必须修改 ID 格式，更新相关文档

## 🔗 相关文件

- `dictionary/coding_terms.json` - 源数据文件
- `generated/.snapshot.json` - 快照文件（用于变更追踪）
- `scripts/validate_json.py` - 验证脚本（包含 ID 格式检查）
- `scripts/generate_md.py` - Markdown 生成脚本
- `scripts/changelog.py` - 变更日志生成脚本

## 📚 参考

- [FHIR CodeableConcept](https://www.hl7.org/fhir/datatypes.html#CodeableConcept)
- [SNOMED CT](https://www.snomed.org/)
- [TDPv1 协议规范](../原始参考文件/tdpv1-0916-fixed.md)
