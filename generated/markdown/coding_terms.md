# Coding Terms Dictionary / 编码词典

**Total Items / 总词条数**: 34

**Auto-generated from**: `dictionary/coding_terms.json`  
**⚠️ DO NOT EDIT MANUALLY / 请勿手动编辑**

---

## 📋 字段说明 (Field Description)

| 字段 | 含义 |
|------|------|
| `id` | 全局唯一标识符 |
| `code` | 编码值 |
| `display` / `display_zh` | 英文/中文显示名 |
| `description` / `description_zh` | 英文/中文详细描述 |
| `system` | 编码系统 |
| `status` | 状态 (active/deprecated/draft) |
| `version` | 版本号 |
| `synonyms` / `synonyms_zh` | 英文/中文同义词 |

---

## 运动状态 (Motion State)

**词条数 / Count**: 9

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `snomed:129006008` | `129006008` | Walking / 步行 | Periodic gait pattern with low to modera...<br>周期性步态，速度低到中等。 | SNOMED CT | active | 1.0.0 |
| `internal:0002` | `0002` | Running / 奔跑 | Fast movement with increased step freque...<br>速度较快,步频提升。 | motion_state | active | 1.0.0 |
| `internal:0004` | `0004` | Standing Still / 静止站立 | Stationary position without horizontal d...<br>无水平位移的静止状态。 | motion_state | active | 1.0.0 |
| `snomed:263821009` | `263821009` | Static / 静止 | No significant displacement or movement.<br>无明显位移或运动。 | SNOMED CT | active | 1.0.0 |
| `snomed:22325002` | `22325002` | Abnormal Gait / 异常步态 | Irregular or pathological walking patter...<br>不规则或病理性行走模式。 | SNOMED CT | active | 1.0.0 |
| `snomed:228439008` | `228439008` | Slow Walking / 缓慢行走 | Walking at reduced speed.<br>以较慢速度行走。 | SNOMED CT | active | 1.0.0 |
| `snomed:217082002` | `217082002` | Falls / 跌倒 | Unintentional descent to lower level.<br>非自主性地下降到较低水平。 | SNOMED CT | active | 1.0.0 |
| `internal:0005` | `0005` | Lying Down / 躺下 | 躺下动作。<br>躺下动作。 | motion_state | active | 1.0.0 |
| `internal:0006` | `0006` | Sitting Down / 坐下 | 坐下动作。<br>坐下动作。 | motion_state | active | 1.0.0 |


## 体位 (Posture)

**词条数 / Count**: 8

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `snomed:10904000` | `10904000` | Standing / 站立 | Upright body position on feet.<br>双脚支撑的直立身体姿势。 | SNOMED CT | active | 1.0.0 |
| `snomed:33586001` | `33586001` | Sitting / 坐姿 | Seated position with support.<br>有支撑的坐着姿势。 | SNOMED CT | active | 1.0.0 |
| `snomed:40199007` | `40199007` | Lying Supine / 仰卧 | Lying on back with face upward.<br>背部着地，面部朝上的躺卧姿势。 | SNOMED CT | active | 1.0.0 |
| `snomed:1240000` | `1240000` | Lying Prone / 俯卧 | Lying face down.<br>面部朝下的躺卧姿势。 | SNOMED CT | active | 1.0.0 |
| `snomed:102538003` | `102538003` | Lying Lateral / 侧卧 | Lying on side.<br>侧身躺卧的姿势。 | SNOMED CT | active | 1.0.0 |
| `snomed:102536004` | `102536004` | Recumbent / 斜倚 | Reclining or leaning back position.<br>斜靠或后仰的姿势。 | SNOMED CT | active | 1.0.0 |
| `internal:0007` | `0007` | Crouching / 蹲伏 | Squatting or crouched position.<br>蹲下或蜷缩的姿势。 | posture | active | 1.0.0 |
| `internal:0011` | `0011` | Lying Prone / 俯卧 | 俯卧姿态。<br>俯卧姿态。 | posture | active | 1.0.0 |


## 健康状况 (Health Condition)

**词条数 / Count**: 4

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `snomed:3424008` | `3424008` | Tachycardia / 心动过速 | Abnormally fast heart rate (>100 bpm).<br>心率异常过快（>100次/分钟）。 | SNOMED CT | active | 1.0.0 |
| `snomed:48867003` | `48867003` | Bradycardia / 心动过缓 | Abnormally slow heart rate (<60 bpm).<br>心率异常过慢（<60次/分钟）。 | SNOMED CT | active | 1.0.0 |
| `snomed:1023001` | `1023001` | Apnea / 呼吸暂停 | Temporary cessation of breathing.<br>暂时性呼吸停止。 | SNOMED CT | active | 1.0.0 |
| `snomed:258158006` | `258158006` | Sleep / 睡眠 | Natural periodic state of rest.<br>自然周期性休息状态。 | SNOMED CT | active | 1.0.0 |


## 危险等级 (Danger Level)

**词条数 / Count**: 8

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `tdp:tdp://danger_level/emergency` | `tdp://danger_level/emergency` | Emergency / 紧急 | Immediate life-threatening situation req...<br>立即威胁生命的情况，需要紧急干预。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/alert` | `tdp://danger_level/alert` | Alert / 警报 | Serious situation requiring prompt atten...<br>严重情况，需要及时关注。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/critical` | `tdp://danger_level/critical` | Critical / 危急 | Severe abnormality requiring immediate e...<br>严重异常，需要立即评估。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/warning` | `tdp://danger_level/warning` | Warning / 警告 | Abnormal situation requiring monitoring.<br>异常情况，需要监测。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/normal` | `tdp://danger_level/normal` | Normal / 正常 | Within expected parameters, no concern.<br>在预期范围内，无需担心。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/unknown` | `tdp://danger_level/unknown` | Unknown / 未知 | Insufficient data to determine danger le...<br>数据不足，无法确定危险等级。 | TDP:danger_level | active | 1.0.0 |
| `internal:dl3` | `dl3` | High Risk / 高风险 | 高风险等级。<br>高风险等级。 | danger_level | active | 1.0.0 |
| `internal:dl4` | `dl4` | Critical / 严重风险 | 严重风险等级。<br>严重风险等级。 | danger_level | active | 1.0.0 |


## 标签 (Tag)

**词条数 / Count**: 5

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `internal:fall_risk` | `fall_risk` | Fall Risk / 跌倒风险 | Indicator for potential fall hazard.<br>潜在跌倒危险的指示器。 | tag | active | 1.0.0 |
| `internal:mobility_impaired` | `mobility_impaired` | Mobility Impaired / 行动受限 | Reduced or limited movement capability.<br>运动能力减弱或受限。 | tag | active | 1.0.0 |
| `internal:elderly` | `elderly` | Elderly / 老年人 | Aged population requiring special attent...<br>需要特别关注的老年人群。 | tag | active | 1.0.0 |
| `internal:tag_001` | `tag_001` | New Tag 1 / 新标签1 | 新增标签示例。<br>新增标签示例。 | tag | active | 1.0.0 |
| `internal:tag_002` | `tag_002` | New Tag 2 / 新标签2 | 新增标签示例。<br>新增标签示例。 | tag | active | 1.0.0 |

