# 分类体系重构总结

## ✅ 已完成的工作

### 1. 新分类体系定义

根据医疗编码标准，建立了以下新分类体系：

1. **posture_codes** - 姿态编码 (Posture Codes)
2. **motion_codes** - 运动编码 (Motion Codes)
3. **physiological_codes** - 生理指标编码 (Physiological Codes)
4. **disorder_condition_codes** - 疾病状况编码 (Disorder & Condition Codes)
5. **safety_alert_codes** - 安全警报编码 (Safety & Alert Codes)
6. **tag** - 自定义标签 (Tag) - 保持不变

### 2. 文档更新

- ✅ 创建了重构计划文档：`docs/CLASSIFICATION_REFACTOR_PLAN.md`
- ✅ 更新了分类方案文档：`docs/CLASSIFICATION_PROPOSAL.md`
- ✅ 更新了 README.md 中的分类说明

### 3. Schema 更新

- ✅ 更新了 `schema/coding_item.schema.json`，添加新分类枚举值
- ✅ 保持向后兼容，同时支持新旧分类

### 4. 脚本更新

- ✅ 更新了 `scripts/generate_md.py`：
  - 添加新分类名称映射
  - 实现旧分类到新分类的自动映射
  - 更新分类显示顺序（新分类优先）

### 5. 向后兼容性

- ✅ Schema 同时支持新旧分类
- ✅ 脚本自动将旧分类映射到新分类进行显示
- ✅ 现有数据无需立即迁移

## 📋 待完成的工作（可选）

### 数据迁移

如果需要完全迁移到新分类体系，可以执行以下步骤：

1. **迁移词条分类**：
   - `posture` → `posture_codes`
   - `motion_state` → `motion_codes`
   - `health_condition` → `physiological_codes` 或 `disorder_condition_codes`
   - `danger_level` → `safety_alert_codes`
   - `Falls` (snomed:217082002) → 从 `motion_state` 移到 `safety_alert_codes`

2. **特殊映射**：
   - `Tachycardia`, `Bradycardia`, `Apnea` → `physiological_codes`
   - `Sleep` → `disorder_condition_codes`
   - `Falls` → `safety_alert_codes`

### 脚本更新（可选）

- 更新 `scripts/add_coding_dict.py` 中的模板，使用新分类
- 更新其他可能引用旧分类的脚本

## 🎯 使用建议

### 新词条

**推荐使用新分类体系**：
- `posture_codes` - 用于身体姿态
- `motion_codes` - 用于运动状态
- `physiological_codes` - 用于生理指标异常
- `disorder_condition_codes` - 用于疾病或健康状况
- `safety_alert_codes` - 用于安全事件和警报等级
- `tag` - 用于 AI 分析的语义标签

### 现有词条

- 可以继续使用旧分类（向后兼容）
- 建议逐步迁移到新分类
- 脚本会自动将旧分类映射到新分类进行显示

## 📚 相关文档

- [分类重构计划](./CLASSIFICATION_REFACTOR_PLAN.md) - 详细的映射关系和数据迁移计划
- [分类方案文档](./CLASSIFICATION_PROPOSAL.md) - 分类文件拆分方案
- [README.md](../README.md) - 项目主文档

