# README.md 目录规则部分 (供参考)

> 复制下面的内容替换 README.md 中的对应部分

---

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
