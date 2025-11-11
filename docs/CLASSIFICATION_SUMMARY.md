# 分类体系重构总结

## ✅ 重构完成

分类体系重构已全部完成，所有词条已迁移到新的分类体系。

## 📋 新分类体系

根据医疗编码标准，项目采用以下分类体系：

1. **posture_codes** - 姿态编码 (Posture Codes)
2. **motion_codes** - 运动编码 (Motion Codes)
3. **physiological_codes** - 生理指标编码 (Physiological Codes)
4. **disorder_condition_codes** - 疾病状况编码 (Disorder & Condition Codes)
5. **safety_alert_codes** - 安全警报编码 (Safety & Alert Codes)
6. **tag** - 自定义标签 (Tag)

## ✅ 已完成的工作

### 1. 数据迁移

- ✅ 所有词条已迁移到新分类体系
- ✅ `posture` → `posture_codes`
- ✅ `motion_state` → `motion_codes`
- ✅ `health_condition` → `physiological_codes` 或 `disorder_condition_codes`
- ✅ `danger_level` → `safety_alert_codes`
- ✅ `Falls` (snomed:217082002) → 从 `motion_state` 移到 `safety_alert_codes`

### 2. Schema 更新

- ✅ 更新了 `schema/coding_dictionary.schema.json`，仅支持新分类枚举值
- ✅ 移除了旧分类的支持

### 3. 脚本更新

- ✅ 更新了 `scripts/generate_md.py`：
  - 添加新分类名称映射
  - 更新分类显示顺序
- ✅ 更新了 `scripts/add_coding_dict.py`，使用新分类模板

### 4. 文档更新

- ✅ 更新了 README.md 中的分类说明
- ✅ 所有文档已反映新分类体系

## 🎯 使用指南

### 新词条

**必须使用新分类体系**：
- `posture_codes` - 用于身体姿态（如站立、坐姿、躺卧）
- `motion_codes` - 用于运动状态（如步行、奔跑、静止）
- `physiological_codes` - 用于生理指标异常（如心动过速、呼吸暂停）
- `disorder_condition_codes` - 用于疾病或健康状况（如睡眠障碍）
- `safety_alert_codes` - 用于安全事件和警报等级（如跌倒、紧急、警告）
- `tag` - 用于 AI 分析的语义标签

### 分类选择原则

分类选择应基于词条的实际语义：
- **姿态** → `posture_codes`
- **运动** → `motion_codes`
- **生理指标异常** → `physiological_codes`
- **疾病/状况** → `disorder_condition_codes`
- **安全事件/警报** → `safety_alert_codes`
- **语义标签** → `tag`

## 📚 相关文档

- [ID 格式规范](./id_format_guide.md) - ID 字段格式规范
- [README.md](../README.md) - 项目主文档

