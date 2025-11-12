# Coding Terms Dictionary / 编码词典

**Total Items / 总词条数**: 79

**Auto-generated from**: `coding_dictionary/coding_dictionary.json`  
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

## 姿态编码 (Posture Codes)

**词条数 / Count**: 16

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
| `snomed:383370001` | `383370001` | Standing Position / 站立姿势 | General standing posture, suitable for m...<br>通用站立姿势，适用于大多数场景，如站立监测或姿势评估。 | SNOMED CT | active | 1.0.0 |
| `snomed:402120000` | `402120000` | Sitting Position / 坐姿 | General sitting posture, suitable for de...<br>通用坐姿，适用于描述患者处于坐位状态。 | SNOMED CT | active | 1.0.0 |
| `snomed:109030009` | `109030009` | Lying Position / 躺卧姿势 | General lying position, suitable for des...<br>通用躺卧姿势，适用于描述平躺或侧卧等状态。 | SNOMED CT | active | 1.0.0 |
| `snomed:26527006` | `26527006` | Supine Position / 仰卧位 | Supine lying position for routine examin...<br>仰卧姿势，常规检查、休息状态监测。 | SNOMED CT | active | 1.0.0 |
| `snomed:271587009` | `271587009` | Prone Position / 俯卧位 | Prone position for surgical positioning ...<br>俯卧姿势，手术体位、呼吸治疗。 | SNOMED CT | active | 1.0.0 |
| `snomed:414585002` | `414585002` | Semi-Fowler's Position / 半卧位 | Semi-recumbent position with head elevat...<br>半卧位（床头抬高30-45度），用于呼吸困难患者、术后护理。 | SNOMED CT | active | 1.0.0 |
| `snomed:17535004` | `17535004` | Lying in Bed / 躺在床上 | Patient in bed, specific state of being ...<br>躺在床上，特指卧床状态。 | SNOMED CT | active | 1.0.0 |
| `snomed:43029002` | `43029002` | Abnormal Posture / 异常姿势 | Atypical or irregular body posture.<br>非典型或不规则的身体姿势。 | SNOMED CT | active | 1.0.0 |


## 运动编码 (Motion Codes)

**词条数 / Count**: 17

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `snomed:129006008` | `129006008` | Walking / 步行 | Periodic gait pattern with low to modera...<br>周期性步态，速度低到中等。 | SNOMED CT | active | 1.0.0 |
| `internal:0002` | `0002` | Running / 奔跑 | Fast movement with increased step freque...<br>速度较快,步频提升。 | motion_state | active | 1.0.0 |
| `internal:0004` | `0004` | Standing Still / 静止站立 | Stationary position without horizontal d...<br>无水平位移的静止状态。 | motion_state | active | 1.0.0 |
| `snomed:263821009` | `263821009` | Static / 静止 | No significant displacement or movement.<br>无明显位移或运动。 | SNOMED CT | active | 1.0.0 |
| `snomed:22325002` | `22325002` | Abnormal Gait / 异常步态 | Irregular or pathological walking patter...<br>不规则或病理性行走模式。 | SNOMED CT | active | 1.0.0 |
| `snomed:228439008` | `228439008` | Slow Walking / 缓慢行走 | Walking at reduced speed.<br>以较慢速度行走。 | SNOMED CT | active | 1.0.0 |
| `internal:0005` | `0005` | Lying Down / 躺下 | 躺下动作。<br>躺下动作。 | motion_state | active | 1.0.0 |
| `internal:0006` | `0006` | Sitting Down / 坐下 | 坐下动作。<br>坐下动作。 | motion_state | active | 1.0.0 |
| `snomed:415568008` | `415568008` | Moving / 移动中 | General movement without specific gait p...<br>移动中，无特定步态模式。 | SNOMED CT | active | 1.0.0 |
| `snomed:414549008` | `414549008` | Standing Up / 起立中 | Movement from sitting or lying to standi...<br>从坐姿或躺卧到站立的动作过程。 | SNOMED CT | active | 1.0.0 |
| `snomed:300845008` | `300845008` | Sitting Down / 坐下中 | Movement from standing to sitting positi...<br>从站立到坐姿的动作过程。 | SNOMED CT | active | 1.0.0 |
| `snomed:249911004` | `249911004` | Shuffling Gait / 拖曳步态 | Gait with small steps and dragging feet,...<br>小步幅、拖步特征，帕金森病典型步态。 | SNOMED CT | active | 1.0.0 |
| `snomed:16973004` | `16973004` | Ataxic Gait / 共济失调步态 | Uncoordinated gait with irregular trajec...<br>协调性差的运动，步态轨迹不规则，常见于中风患者。 | SNOMED CT | active | 1.0.0 |
| `snomed:397776000` | `397776000` | Freezing of Gait / 步态冻结 | Sudden inability to initiate or continue...<br>步态冻结，突然无法启动或继续行走，帕金森病严重症状。 | SNOMED CT | active | 1.0.0 |
| `snomed:22160007` | `22160007` | Festinating Gait / 慌张步态 | Fast, short steps with forward-leaning p...<br>快速小步伴前倾姿势，见于帕金森病。 | SNOMED CT | active | 1.0.0 |
| `snomed:1055001` | `1055001` | Bradykinesia / 运动迟缓 | Slowness of movement, a cardinal feature...<br>运动迟缓，帕金森病的主要特征之一。 | SNOMED CT | active | 1.0.0 |
| `snomed:102557002` | `102557002` | Difficulty Walking / 行走困难 | Impaired ability to walk, may indicate n...<br>行走能力受损，可能提示神经或肌肉骨骼问题。 | SNOMED CT | active | 1.0.0 |


## 生理指标编码 (Physiological Codes)

**词条数 / Count**: 13

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `snomed:3424008` | `3424008` | Tachycardia / 心动过速 | Abnormally fast heart rate (>100 bpm).<br>心率异常过快（>100次/分钟）。 | SNOMED CT | active | 1.0.0 |
| `snomed:48867003` | `48867003` | Bradycardia / 心动过缓 | Abnormally slow heart rate (<60 bpm).<br>心率异常过慢（<60次/分钟）。 | SNOMED CT | active | 1.0.0 |
| `snomed:1023001` | `1023001` | Apnea / 呼吸暂停 | Temporary cessation of breathing.<br>暂时性呼吸停止。 | SNOMED CT | active | 1.0.0 |
| `snomed:26079004` | `26079004` | Tremor / 震颤 | Involuntary rhythmic muscle contraction,...<br>不自主的节律性肌肉收缩，常见于帕金森和中风。 | SNOMED CT | active | 1.0.0 |
| `snomed:314207007` | `314207007` | Resting Tremor / 静止性震颤 | Tremor occurring when muscles are at res...<br>静止时发生的震颤，帕金森病的经典征象。 | SNOMED CT | active | 1.0.0 |
| `snomed:271823003` | `271823003` | Abnormal Breathing / 异常呼吸 | Irregular or abnormal respiratory patter...<br>不规则或异常的呼吸模式。 | SNOMED CT | active | 1.0.0 |
| `snomed:30128008` | `30128008` | Tachypnea / 呼吸过速 | Abnormally rapid breathing (>20 breaths/...<br>呼吸异常过快（>20次/分钟）。 | SNOMED CT | active | 1.0.0 |
| `snomed:248546003` | `248546003` | Bradypnea / 呼吸过缓 | Abnormally slow breathing (<12 breaths/m...<br>呼吸异常过慢（<12次/分钟）。 | SNOMED CT | active | 1.0.0 |
| `snomed:49817004` | `49817004` | Irregular Heart Rate / 心率不规则 | Irregular cardiac rhythm, may indicate a...<br>心律不规则，可能提示心律失常。 | SNOMED CT | active | 1.0.0 |
| `snomed:271636001` | `271636001` | Tachycardia Finding / 心动过速发现 | Clinical finding of abnormally fast hear...<br>心动过速的临床发现。 | SNOMED CT | active | 1.0.0 |
| `snomed:342400002` | `342400002` | Bradycardia Finding / 心动过缓发现 | Clinical finding of abnormally slow hear...<br>心动过缓的临床发现。 | SNOMED CT | active | 1.0.0 |
| `snomed:29857009` | `29857009` | Chest Pain / 胸痛 | Pain or discomfort in the chest area, po...<br>胸部疼痛或不适，心梗的潜在预警信号。 | SNOMED CT | active | 1.0.0 |
| `snomed:225602000` | `225602000` | Unable to Sit Unsupported / 无法独立坐稳 | Inability to maintain sitting position w...<br>无法独立坐稳，可能提示中风、神经系统疾病或肌力不足。 | SNOMED CT | active | 1.0.0 |


## 疾病状况编码 (Disorder & Condition Codes)

**词条数 / Count**: 4

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `snomed:258158006` | `258158006` | Sleep / 睡眠 | Natural periodic state of rest.<br>自然周期性休息状态。 | SNOMED CT | active | 1.0.0 |
| `snomed:49049000` | `49049000` | Parkinson's Disease / 帕金森病 | Progressive neurodegenerative disorder a...<br>进行性神经退行性疾病，影响运动功能。 | SNOMED CT | active | 1.0.0 |
| `snomed:230690007` | `230690007` | Cerebrovascular Accident / 脑血管意外 | Stroke or cerebrovascular accident, sudd...<br>中风或脑血管意外，脑功能突然丧失。 | SNOMED CT | active | 1.0.0 |
| `snomed:22298006` | `22298006` | Myocardial Infarction / 心肌梗死 | Heart attack, death of heart muscle due ...<br>心肌梗死，由于血流阻塞导致的心肌死亡。 | SNOMED CT | active | 1.0.0 |


## 安全警报编码 (Safety & Alert Codes)

**词条数 / Count**: 10

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `snomed:217082002` | `217082002` | Falls / 跌倒 | Unintentional descent to lower level.<br>非自主性地下降到较低水平。 | SNOMED CT | active | 1.0.0 |
| `tdp:tdp://danger_level/emergency` | `tdp://danger_level/emergency` | Emergency / 紧急 | Immediate life-threatening situation req...<br>立即威胁生命的情况，需要紧急干预。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/alert` | `tdp://danger_level/alert` | Alert / 警报 | Serious situation requiring prompt atten...<br>严重情况，需要及时关注。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/critical` | `tdp://danger_level/critical` | Critical / 危急 | Severe abnormality requiring immediate e...<br>严重异常，需要立即评估。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/warning` | `tdp://danger_level/warning` | Warning / 警告 | Abnormal situation requiring monitoring.<br>异常情况，需要监测。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/normal` | `tdp://danger_level/normal` | Normal / 正常 | Within expected parameters, no concern.<br>在预期范围内，无需担心。 | TDP:danger_level | active | 1.0.0 |
| `tdp:tdp://danger_level/unknown` | `tdp://danger_level/unknown` | Unknown / 未知 | Insufficient data to determine danger le...<br>数据不足，无法确定危险等级。 | TDP:danger_level | active | 1.0.0 |
| `internal:dl3` | `dl3` | High Risk / 高风险 | 高风险等级。<br>高风险等级。 | danger_level | active | 1.0.0 |
| `internal:dl4` | `dl4` | Critical / 严重风险 | 严重风险等级。<br>严重风险等级。 | danger_level | active | 1.0.0 |
| `snomed:129839007` | `129839007` | At Risk for Falls / 跌倒风险 | Patient at increased risk of falling.<br>患者有较高的跌倒风险。 | SNOMED CT | active | 1.0.0 |


## 标签 (Tag)

**词条数 / Count**: 19

| ID | Code | Display / 显示名 | Description / 描述 | System | Status | Version |
|-----|------|------------------|-------------------|--------|--------|---------|
| `internal:fall_risk` | `fall_risk` | Fall Risk / 跌倒风险 | Indicator for potential fall hazard.<br>潜在跌倒危险的指示器。 | tag | active | 1.0.0 |
| `internal:mobility_impaired` | `mobility_impaired` | Mobility Impaired / 行动受限 | Reduced or limited movement capability.<br>运动能力减弱或受限。 | tag | active | 1.0.0 |
| `internal:elderly` | `elderly` | Elderly / 老年人 | Aged population requiring special attent...<br>需要特别关注的老年人群。 | tag | active | 1.0.0 |
| `internal:tag_001` | `tag_001` | New Tag 1 / 新标签1 | 新增标签示例。<br>新增标签示例。 | tag | active | 1.0.0 |
| `internal:tag_002` | `tag_002` | New Tag 2 / 新标签2 | 新增标签示例。<br>新增标签示例。 | tag | active | 1.0.0 |
| `internal:apnea_confirmed` | `Apnea.Confirmed` | Apnea Confirmed / 确诊呼吸暂停 | Confirmed apnea event (>=60S), respirato...<br>确诊呼吸暂停 (>=60S)，即呼吸率 < 5 次/分钟 且持续超过 10 秒。 | tag | active | 1.0.0 |
| `internal:apnea_suspected` | `Apnea.Suspected` | Apnea Suspected / 疑似呼吸暂停 | Suspected apnea event (>=10S).<br>疑似呼吸暂停 (>=10S)。 | tag | active | 1.0.0 |
| `internal:cardiac_pause_confirmed` | `CardiacPause.Confirmed` | Cardiac Pause Confirmed / 确诊心率暂停 | Confirmed cardiac pause (>=3S).<br>确诊心率暂停 (>=3S)。 | tag | active | 1.0.0 |
| `internal:cardiac_pause_suspected` | `CardiacPause.Suspected` | Cardiac Pause Suspected / 疑似心率暂停 | Suspected cardiac pause.<br>疑似心率暂停。 | tag | active | 1.0.0 |
| `internal:convulsion` | `Convulsion` | Convulsion / 抽搐 | Involuntary muscle contraction and spasm...<br>不自主的肌肉收缩和痉挛。 | tag | active | 1.0.0 |
| `internal:convulsion_suspected` | `Convulsion.Suspected` | Convulsion Suspected / 疑似抽搐 | Suspected convulsion activity.<br>疑似抽搐活动。 | tag | active | 1.0.0 |
| `internal:fall_suspected` | `Fall.Suspected` | Fall Suspected / 疑似跌倒 | Suspected fall event requiring verificat...<br>疑似跌倒事件，需要验证。 | tag | active | 1.0.0 |
| `internal:on_floor` | `OnFloor` | On Floor / 在地面上 | Person detected on the floor (sitting on...<br>在地面上（坐地）。 | tag | active | 1.0.0 |
| `internal:prolonged_stay` | `ProlongedStay` | Prolonged Stay / 长时间滞留 | Extended stay in one location beyond nor...<br>在一个位置停留超过正常时长。 | tag | active | 1.0.0 |
| `internal:no_turning` | `NoTurning` | No Turning / 未翻身 | No body position change detected during ...<br>睡眠期间未检测到身体位置变化。 | tag | active | 1.0.0 |
| `internal:lying_in_bed` | `LyingInBed` | Lying in Bed / 躺床 | Person lying in bed.<br>躺在床上。 | tag | active | 1.0.0 |
| `internal:sitting_in_bed` | `SittingInBed` | Sitting in Bed / 床上坐起 | Person sitting up in bed.<br>床上坐起。 | tag | active | 1.0.0 |
| `internal:into_bed` | `IntoBed` | Into Bed / 上床 | Person getting into bed.<br>上床动作。 | tag | active | 1.0.0 |
| `internal:out_of_bed` | `OutOfBed` | Out of Bed / 离床 | Person getting out of bed.<br>离床动作。 | tag | active | 1.0.0 |

