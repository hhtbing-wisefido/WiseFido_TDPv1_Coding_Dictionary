# 📦 数据迁移脚本归档

本目录保存了项目重要版本迁移过程中使用的脚本，作为历史记录保留。

---

## 📋 迁移脚本列表

### 1. migrate_to_v2.py

**迁移版本**: v1.2.6 → v2.0.0  
**迁移日期**: 2025-11-12  
**迁移说明**: 

此脚本完成了从 v1.x 到 v2.0.0 的数据结构重构：

#### 移除的字段
- `id` - 词条唯一标识符
- `category` - 分类
- `status` - 状态
- `version` - 版本号
- `description` - 英文描述
- `description_zh` - 中文描述
- `synonyms` - 英文同义词
- `synonyms_zh` - 中文同义词
- `source_refs` - 来源参考
- `detection` - 检测能力信息
- `fhir` - FHIR 相关信息

#### 保留的字段 (v2.0.0 核心字段)
- `system` - 编码系统 URI
- `code` - 编码值
- `display` - 英文显示名称
- `display_zh` - 中文显示名称

#### 迁移成果
- ✅ 79 个词条成功迁移
- ✅ 97 个词条的移除字段完整归档到 `archive/removed_fields_v1.2.6/`
- ✅ 原始数据备份到 `archive/backups/v1.2.6/`
- ✅ 文件大小减少 84% (~50KB → ~8KB)
- ✅ 字段精简 64% (11+ 字段 → 4 字段)

#### 设计原则
遵循 **YAGNI (You Aren't Gonna Need It)** 原则，移除了所有未被实际使用的字段，专注于核心功能。

---

## 🔗 相关文档

- **迁移测试报告**: `../../tests/test_v2_migration.py`
- **v2.0.0 发布总结**: `../../auto_generated_docs/项目里程碑/v2.0.0_发布总结.md`
- **完整项目检查报告**: `../../auto_generated_docs/项目里程碑/v2.0.0_完整检查报告.md`
- **归档数据位置**: `../../archive/removed_fields_v1.2.6/`
- **原始数据备份**: `../../archive/backups/v1.2.6/`

---

## ⚠️ 重要说明

1. **脚本状态**: 已完成使命，仅作历史参考，不应再次运行
2. **数据恢复**: 如需恢复 v1.2.6 数据，请参考 `archive/backups/v1.2.6/` 中的备份文件
3. **归档字段**: 所有移除的字段数据已完整保存在 `archive/removed_fields_v1.2.6/` 目录

---

**归档日期**: 2025-11-13  
**归档原因**: temp/ 目录清理，保留有价值的历史脚本
