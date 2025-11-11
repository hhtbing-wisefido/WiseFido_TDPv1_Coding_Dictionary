# Coding Dictionary 分类体系

> 本文档定义 WiseFido_TDPv1_Coding_Dictionary 的分类架构和使用规范

---

## 📋 分类体系概览

根据医疗编码标准和系统需求，本项目采用以下 6 大分类体系：

| 分类代码 | 中文名称 | 英文名称 | 用途说明 |
|---------|---------|---------|---------|
| **posture_codes** | 姿态编码 | Posture Codes | 描述人体姿态（站、坐、卧等） |
| **motion_codes** | 运动编码 | Motion Codes | 描述运动状态（步行、奔跑、静止等） |
| **physiological_codes** | 生理指标编码 | Physiological Codes | 描述生理指标异常（心率、呼吸等） |
| **disorder_condition_codes** | 疾病状况编码 | Disorder & Condition Codes | 描述疾病或健康状况 |
| **safety_alert_codes** | 安全警报编码 | Safety & Alert Codes | 描述安全事件和警报等级 |
| **tag** | 自定义标签 | Custom Tags | AI 分析的语义标签 |

---

## 🎯 分类详细说明

### 1. posture_codes - 姿态编码

**定义**: 描述人体静态或相对静态的身体姿态。

**适用场景**:
- 身体位置和方向
- 相对稳定的体位

**典型词条**:
- 站立 (Standing)
- 坐姿 (Sitting)
- 仰卧 (Lying Supine)
- 俯卧 (Lying Prone)
- 侧卧 (Lying on Side)

**检测方式**: 主要由 60GHz 毫米波雷达检测

---

### 2. motion_codes - 运动编码

**定义**: 描述人体动态运动状态和动作。

**适用场景**:
- 身体移动行为
- 动作状态变化

**典型词条**:
- 步行 (Walking)
- 奔跑 (Running)
- 静止 (Stationary)
- 跌倒 (Falls) - 注：跌倒同时也是安全事件

**检测方式**: 60GHz 雷达、MEMS 地震传感器

---

### 3. physiological_codes - 生理指标编码

**定义**: 描述可量化的生理参数异常状态。

**适用场景**:
- 心率、呼吸等生命体征异常
- 可通过传感器直接测量的指标

**典型词条**:
- 心动过速 (Tachycardia)
- 心动过缓 (Bradycardia)
- 呼吸暂停 (Apnea)

**检测方式**: 睡眠板 (Sleep Pad)、60GHz 雷达

---

### 4. disorder_condition_codes - 疾病状况编码

**定义**: 描述疾病、症状或健康状况。

**适用场景**:
- 医学诊断相关
- 健康状态描述

**典型词条**:
- 睡眠 (Sleep)
- 睡眠障碍 (Sleep Disorder)
- 慢性病状态

**编码标准**: 优先使用 SNOMED CT 编码

---

### 5. safety_alert_codes - 安全警报编码

**定义**: 描述安全相关的事件、警报和风险等级。

**适用场景**:
- 紧急事件
- 危险等级标注
- 系统警报

**典型词条**:
- 跌倒 (Falls) - 安全事件
- 紧急 (Emergency)
- 警告 (Warning)
- 严重 (Critical)
- 高风险 (High Risk)

**特殊说明**: 跌倒既是运动事件，也是安全事件，归类为 `safety_alert_codes`

---

### 6. tag - 自定义标签

**定义**: AI 分析使用的语义标签，用于辅助分析和关联。

**适用场景**:
- 多维度分析
- 风险预测
- 人群特征标注

**典型词条**:
- 跌倒风险 (Fall Risk)
- 行动不便 (Mobility Impairment)
- 老年人 (Elderly)
- 独居 (Living Alone)

**特点**: 灵活、可扩展，不受严格医疗编码标准约束

---

## 📐 分类选择原则

### 决策流程图

```
问题：这个词条描述的是什么？
│
├─ 身体姿态？ → posture_codes
│
├─ 运动状态？
│   ├─ 是安全事件（如跌倒）？ → safety_alert_codes
│   └─ 否 → motion_codes
│
├─ 生理指标异常？ → physiological_codes
│
├─ 疾病/健康状况？ → disorder_condition_codes
│
├─ 安全事件/警报等级？ → safety_alert_codes
│
└─ 辅助分析标签？ → tag
```

### 常见疑问

**Q: 跌倒应该归类为 motion_codes 还是 safety_alert_codes？**
A: `safety_alert_codes`。虽然跌倒是运动事件，但其核心语义是安全风险，应优先考虑安全属性。

**Q: 心率过快是 physiological_codes 还是 disorder_condition_codes？**
A: `physiological_codes`。这是可直接测量的生理指标异常，而非疾病诊断。

**Q: 如何区分 tag 和其他分类？**
A: `tag` 用于辅助分析和多维关联，不是核心医疗编码。例如"跌倒风险"是预测性标签，而"跌倒"是实际事件。

---

## 🔧 技术实现

### Schema 定义

分类在 `schema/coding_dictionary.schema.json` 中定义为枚举类型：

```json
{
  "category": {
    "type": "string",
    "enum": [
      "posture_codes",
      "motion_codes",
      "physiological_codes",
      "disorder_condition_codes",
      "safety_alert_codes",
      "tag"
    ]
  }
}
```

### 数据示例

```json
{
  "id": "snomed:10904000",
  "code": "10904000",
  "system": "http://snomed.info/sct",
  "display": "Standing",
  "display_zh": "站立",
  "category": "posture_codes",
  "status": "active",
  "version": "1.0.0"
}
```

---

## 📚 相关文档

- [ID 格式规范](./id_format_guide.md) - ID 字段格式规范
- [README.md](../README.md) - 项目主文档
- [coding_dictionary.json](../coding_dictionary/coding_dictionary.json) - 主数据文件

---

## 📝 历史说明

本分类体系经过重构优化，旧版分类已全部迁移：
- `posture` → `posture_codes`
- `motion_state` → `motion_codes`
- `health_condition` → `physiological_codes` 或 `disorder_condition_codes`
- `danger_level` → `safety_alert_codes`

所有词条已完成迁移，Schema 仅支持新分类体系。
