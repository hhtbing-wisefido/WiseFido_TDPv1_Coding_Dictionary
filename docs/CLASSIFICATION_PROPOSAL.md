# 字典文件分类方案

## 问题分析

当前 `dictionary/coding_terms.json` 是单个文件，包含所有词条。随着字典规模增长，会遇到以下问题：

1. **性能问题**：文件变大后，加载和解析变慢
2. **编辑困难**：大文件在编辑器中响应慢
3. **合并冲突**：多人协作时容易产生 Git 冲突
4. **维护成本**：查找和修改特定分类的词条不便

## 解决方案：按分类拆分

### 文件结构

```
dictionary/
├── coding_terms.json          # 主索引文件（向后兼容）
├── categories/
│   ├── posture_codes.json           # 姿态编码词条
│   ├── motion_codes.json             # 运动编码词条
│   ├── physiological_codes.json      # 生理指标编码词条
│   ├── disorder_condition_codes.json # 疾病状况编码词条
│   ├── safety_alert_codes.json       # 安全警报编码词条
│   └── tag.json                      # 标签词条（自定义）
└── .categories.json           # 分类元数据（可选）
```

### 新分类体系说明

根据医疗编码标准，采用以下分类：

1. **posture_codes** - 姿态编码：身体姿态（如站立、坐姿、躺卧）
2. **motion_codes** - 运动编码：运动状态（如步行、奔跑、静止）
3. **physiological_codes** - 生理指标编码：生理指标异常（如心动过速、呼吸暂停）
4. **disorder_condition_codes** - 疾病状况编码：疾病或健康状况（如睡眠障碍）
5. **safety_alert_codes** - 安全警报编码：安全事件和警报等级（如跌倒、紧急、警告）
6. **tag** - 自定义标签：用于 AI 分析的语义标签

### 方案优势

1. **按需加载**：脚本可以只加载需要的分类
2. **并行编辑**：不同分类可以同时编辑，减少冲突
3. **易于维护**：每个分类文件独立，便于管理
4. **向后兼容**：保留主文件作为索引，现有工具仍可使用
5. **性能提升**：小文件加载更快，编辑器响应更灵敏

### 实现策略

#### 方案 A：完全拆分（推荐）

- 每个分类独立文件
- 主文件作为合并后的完整索引（自动生成）
- 脚本优先使用分类文件

#### 方案 B：混合模式

- 保留主文件作为主要数据源
- 分类文件作为可选扩展
- 脚本支持两种模式

## 迁移计划

1. **阶段 1**：创建分类文件结构
2. **阶段 2**：更新脚本支持分类文件
3. **阶段 3**：迁移现有数据到分类文件
4. **阶段 4**：更新文档和工具说明

## 脚本更新清单

需要更新的脚本：
- [x] `scripts/generate_md.py` - 支持从分类文件加载
- [x] `scripts/changelog.py` - 支持分类文件快照
- [x] `scripts/add_coding_dict.py` - 支持写入分类文件
- [x] `scripts/validate_json.py` - 支持验证分类文件
- [ ] `scripts/tools.py` - 更新工具函数

## 分类重构

### 从旧分类到新分类的映射

| 旧分类 | 新分类 | 说明 |
|--------|--------|------|
| `posture` | `posture_codes` | 直接映射 |
| `motion_state` | `motion_codes` | 直接映射（跌倒事件移至 `safety_alert_codes`） |
| `health_condition` | `physiological_codes` | 生理指标类（心率、呼吸等） |
| `health_condition` | `disorder_condition_codes` | 疾病状况类（睡眠等） |
| `danger_level` | `safety_alert_codes` | 直接映射 |
| `tag` | `tag` | 保持不变 |

详细的重构计划请参考：[CLASSIFICATION_REFACTOR_PLAN.md](./CLASSIFICATION_REFACTOR_PLAN.md)

## 使用建议

### 何时拆分？

- **当前**：34 个词条，21KB - **暂不需要拆分**
- **建议阈值**：
  - 文件大小 > 500KB
  - 词条数量 > 200
  - 或出现性能问题时

### 渐进式迁移

1. 先实现分类加载逻辑（向后兼容）
2. 当文件变大时，再执行数据迁移
3. 保持主文件作为备份和兼容层

