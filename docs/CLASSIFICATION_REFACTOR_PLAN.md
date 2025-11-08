# 分类重构方案

## 新分类体系

根据医疗编码标准，将现有分类重构为以下体系：

### 新分类列表

1. **posture_codes** - 姿态编码 (Posture Codes)
2. **motion_codes** - 运动编码 (Motion Codes)
3. **physiological_codes** - 生理指标编码 (Physiological Codes)
4. **disorder_condition_codes** - 疾病状况编码 (Disorder & Condition Codes)
5. **safety_alert_codes** - 安全警报编码 (Safety & Alert Codes)
6. **tag** - 自定义标签 (Tag) - 保持不变

## 映射关系

### 当前分类 → 新分类

| 当前分类 | 新分类 | 说明 |
|---------|--------|------|
| `posture` | `posture_codes` | 直接映射，重命名 |
| `motion_state` | `motion_codes` | 直接映射，重命名 |
| `health_condition` | `physiological_codes` | 生理指标类（心率、呼吸等） |
| `health_condition` | `disorder_condition_codes` | 疾病状况类（睡眠障碍等） |
| `danger_level` | `safety_alert_codes` | 直接映射，重命名 |
| `tag` | `tag` | 保持不变 |

### 具体词条映射

#### posture → posture_codes
- 所有 `category: "posture"` 的词条保持不变，仅更新 category 值

#### motion_state → motion_codes
- 大部分 `category: "motion_state"` 的词条 → `motion_codes`
- **例外**：`Falls` (snomed:217082002) → `safety_alert_codes`（跌倒属于安全事件）

#### health_condition → physiological_codes
- `Tachycardia` (snomed:3424008) - 心动过速
- `Bradycardia` (snomed:48867003) - 心动过缓
- `Apnea` (snomed:1023001) - 呼吸暂停

#### health_condition → disorder_condition_codes
- `Sleep` (snomed:258158006) - 睡眠（作为生理状态/状况）

#### danger_level → safety_alert_codes
- 所有 `category: "danger_level"` 的词条 → `safety_alert_codes`

#### tag → tag
- 保持不变

## 需要迁移的词条

### 需要更改分类的词条

1. **Falls** (snomed:217082002)
   - 当前：`category: "motion_state"`
   - 新分类：`category: "safety_alert_codes"`
   - 理由：跌倒是安全事件，不是运动状态

2. **Tachycardia, Bradycardia, Apnea**
   - 当前：`category: "health_condition"`
   - 新分类：`category: "physiological_codes"`
   - 理由：这些是生理指标异常

3. **Sleep**
   - 当前：`category: "health_condition"`
   - 新分类：`category: "disorder_condition_codes"`
   - 理由：睡眠是生理状态/状况

## 实施步骤

1. ✅ 创建重构方案文档
2. ⏳ 更新 JSON Schema
3. ⏳ 更新脚本中的分类映射
4. ⏳ 迁移现有数据
5. ⏳ 更新文档
6. ⏳ 验证和测试

## 向后兼容性

考虑保持向后兼容：
- 方案 A：完全迁移，更新所有引用
- 方案 B：支持新旧分类并存，逐步迁移（推荐）

建议采用方案 B，在脚本中支持新旧分类的映射。

