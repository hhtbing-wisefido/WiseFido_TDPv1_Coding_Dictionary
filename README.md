# WiseFido_TDPv1_Coding_Dictionary

> 🎯 **可复用医疗编码字典库** — JSON 作为唯一事实源 | 自动生成 Markdown | 变更追踪 | FHIR 兼容

[![Copyright: WiseFido](https://img.shields.io/badge/Copyright-WiseFido-blue.svg)](https://www.wisefido.com)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 📋 项目简介

WiseFido_TDPv1_Coding_Dictionary 是基于 **TDPv1 协议**和 **FHIR/SNOMED CT** 标准构建的医疗编码术语字典库，服务于 **OWL Monitor System**（老人健康监测系统）的完整术语体系。

本字典库涵盖整个系统的多传感器健康检测能力，包括：

- **60GHz 毫米波雷达**：运动状态、姿态、跌倒检测、生命体征监测
- **睡眠板（Sleep Pad）**：心率、呼吸、翻身、抽搐检测（PTZ压电传感器 + 应变传感器）
- **MEMS 地震传感器**：跌倒检测、振动事件识别
- **SOS 紧急呼叫系统**：手动报警、语音通信
- ✅ **机器可信**：JSON 作为"唯一事实源"，Schema 强校验
- ✅ **人类可读**：自动生成 Markdown 表格文档
- ✅ **变更追踪**：基于快照自动记录词条变化历史
- ✅ **医疗标准**：兼容 FHIR、SNOMED CT、LOINC
- ✅ **多传感器检测**：标注各传感器（雷达、睡眠板、地震仪等）的检测能力
- ✅ **预警支持**：内置帕金森、卒中、心梗预警规则映射

---

## 🏗️ 项目架构

```plaintext
WiseFido_TDPv1_Coding_Dictionary/
│
├── README.md                      (M) 项目总览与使用文档
│
├── coding_dictionary/             (M) 核心数据源【唯一事实源】
│   └── coding_dictionary.json         主词条文件（JSON格式）
│
├── schema/                        (M) 验证规范【机器读】
│   └── coding_dictionary.schema.json  JSON Schema 自动验证规则
│
├── spec/                          (M) 规范文档【人类读】
│   └── coding_dictionary.schema.spec.md  数据结构与字段规范（含分类体系详解）
│
├── scripts/                       (M) 工具脚本集【开发使用】
│   ├── _config.py                     公共配置（统一 __pycache__ 到 temp）
│   ├── dic_tools.py                   主工具入口（交互式菜单 + 命令行）
│   ├── validate_json.py               数据校验器（Schema + 逻辑验证）
│   ├── generate_md.py                 文档生成器（双 Markdown 输出）
│   ├── changelog.py                   变更日志生成器
│   └── add_coding_dict.py             批量添加词条脚本
│
├── requirements.txt               (M) Python 依赖配置
│
├── auto_generated/                (G) 自动生成【禁止手动编辑】
│   ├── coding_dictionary.md           数据表格文档（按分类展示）
│   ├── coding_dictionary.schema.md    Schema 规范文档（字段说明）
│   ├── changelog.md                   变更历史记录
│   └── .snapshot.json                 数据快照（用于变更对比）
│
├── 原始参考文件/                   (M) 业务参考资料【只读】
│   ├── tdpv1-0916-fixed.md            TDP v1 协议规范
│   ├── fhir与snomed_ct代码.md         FHIR 与 SNOMED CT 参考
│   └── fda-v0923.md                   OWL Monitor System 架构参考
│
├── .github/workflows/             (M) CI/CD 自动化配置
│   └── ci.yml                         GitHub Actions 工作流
│
├── temp/                          (T) 临时文件【可安全删除】
│   ├── __pycache__/                   Python 缓存（自动生成）
│   └── *.tmp.json, *.py               临时文件、测试脚本、迁移工具等
│
├── auto_backup/                   (L) 自动备份【不纳入版本控制】
│   └── coding_dictionary_backup_*.json  时间戳备份（dic_tools.py 自动生成）
│
├── .gitignore                     (M) Git 忽略规则
└── LICENSE                        (M) MIT 开源许可证

图例说明：
  (M) = 手动维护    - 需要人工编辑和管理
  (G) = 自动生成    - 脚本自动创建，禁止手动修改
  (T) = 临时文件    - 可随时删除，不影响项目运行
  (L) = 本地备份    - Git 忽略，仅本地保存
```

---

## 🚀 快速开始


### 1️⃣ 安装依赖（首次使用必做）

请确保已安装 Python 3.8 及以上版本。

**方式1：自动安装（推荐）**
```bash
python scripts/dic_tools.py
```
如果缺少依赖，脚本会自动尝试安装，安装成功后重新运行即可。

**方式2：手动安装**
```bash
pip install -r requirements.txt
```

**方式3：使用当前 Python 环境安装**
```bash
python -m pip install -r requirements.txt
```

**💡 跨环境兼容说明**：
- 脚本会使用**当前运行的 Python 解释器**安装依赖
- 支持系统 Python、conda、venv 等各种环境
- 无需手动切换环境，直接运行即可

### 2️⃣ 交互式菜单

```bash
python scripts/dic_tools.py
```

菜单选项：
（进入循环模式，执行完一个操作后按 Enter 返回主菜单）

| 编号 | 分组           | 功能说明                          |
| ---- | -------------- | --------------------------------- |
| 1    | 数据管理       | 校验词条数据（Schema + 逻辑）     |
| 2    | 数据管理       | 生成 Markdown 文档                |
| 3    | 数据管理       | 更新变更日志                      |
| 4    | 数据管理       | 完整流程（1→2→3）                 |
| 5    | 数据查询       | 显示统计信息（分类/系统/状态等）  |
| 6    | 数据查询       | 搜索词条（交互式多条件）          |
| 7    | 数据查询       | 查看词条详情                      |
| 8    | 数据编辑       | 交互式添加单个词条（自动备份）    |
| 9    | 数据编辑       | 撤回最近一次添加（基于临时记录）  |
| 10   | 质量检测       | 运行测试套件 🧪（6 项数据质量）    |
| 11   | 数据备份       | 手动备份主字典文件                |
| 12   | 数据备份       | 从备份恢复（含二次确认 + 先备份） |
| 13   | 系统维护       | 清理临时文件与 __pycache__        |
| 0    | 系统           | 退出工具                          |

### 3️⃣ 命令行模式

支持长选项（`--`）和短选项（`-`）两种格式：

```bash
# 校验词条
python scripts/dic_tools.py --validate    # 或: python scripts/dic_tools.py -v

# 生成 Markdown 文档
python scripts/dic_tools.py --generate-md # 或: python scripts/dic_tools.py -g

# 更新变更日志
python scripts/dic_tools.py --changelog   # 或: python scripts/dic_tools.py -c

# 完整流程（一次性执行校验+生成+更新）
python scripts/dic_tools.py --all         # 或: python scripts/dic_tools.py -a

# 显示统计信息
python scripts/dic_tools.py --stats       # 或: python scripts/dic_tools.py -s

# 运行测试套件 🧪
python scripts/dic_tools.py --test        # 或: python scripts/dic_tools.py -t

# 清理临时文件
python scripts/dic_tools.py --clean

# 数据统计
python scripts/dic_tools.py --stats

# 备份 / 恢复
python scripts/dic_tools.py --backup
python scripts/dic_tools.py --restore

# 搜索（格式: 类型:关键词）
python scripts/dic_tools.py --search id:snomed
python scripts/dic_tools.py --search category:motion_codes

# 查看详情
python scripts/dic_tools.py --view snomed:129006008

# 执行后继续进入菜单（混合模式）
python scripts/dic_tools.py --stats --menu-after

# 撤回最近一次添加的词条（需之前通过菜单添加成功）
python scripts/dic_tools.py --undo-last-add
```

### 运行模式说明

| 模式类型         | 触发方式                                          | 特点                                  | 适用场景                     |
| ---------------- | ------------------------------------------------- | ------------------------------------- | ---------------------------- |
| 交互循环模式     | `python scripts/dic_tools.py`                     | 菜单循环，人工选择，连续操作          | 日常维护、人工核对            |
| 参数一次性模式   | `python scripts/dic_tools.py --stats`             | 执行后直接退出                        | CI、脚本自动化、批处理        |
| 参数+菜单混合模式| `python scripts/dic_tools.py --stats --menu-after`| 先执行参数指定操作，再进入交互菜单    | 先跑一个任务再继续多步操作    |
| 撤回操作模式     | `python scripts/dic_tools.py --undo-last-add`     | 删除最近一次添加（自动备份后执行）    | 误添加立即恢复               |

> 提示：`--menu-after` 不改变默认行为，只在需要“执行一次再继续”时手动添加。

---

## 🧪 测试套件

项目内置了完整的测试套件，用于验证数据质量和完整性。

### 测试项目

| 测试项                       | 说明                     | 检查内容                                                         |
| ---------------------------- | ------------------------ | ---------------------------------------------------------------- |
| **必填字段检查**       | 验证所有词条包含必填字段 | id, code, system, display, display_zh, category, status, version |
| **ID 格式检查**        | 验证 ID 格式正确         | 格式为 `prefix:code` 或 `prefix:protocol://path`             |
| **重复 ID 检查**       | 验证无重复 ID            | 每个 ID 在字典中唯一                                             |
| **code+system 唯一性** | 验证编码组合唯一         | 同一编码系统中 code 不重复                                       |
| **分类有效性检查**     | 验证使用有效分类         | 分类必须在预定义列表中                                           |
| **版本号格式检查**     | 验证版本号符合语义化版本 | 格式为 `X.Y.Z`                                                 |

### 运行测试

```bash
# 运行完整测试套件
python scripts/dic_tools.py --test

# 或使用短选项
python scripts/dic_tools.py -t
```

### 测试输出示例

```
============================================================
  测试套件
============================================================

[测试 1/6] 检查必填字段...
  ✅ 通过: 所有词条包含必填字段

[测试 2/6] 检查 ID 格式...
  ✅ 通过: 所有 ID 格式正确

[测试 3/6] 检查重复 ID...
  ✅ 通过: 无重复 ID

[测试 4/6] 检查 code+system 唯一性...
  ✅ 通过: code+system 组合唯一

[测试 5/6] 检查分类有效性...
  ✅ 通过: 所有分类有效

[测试 6/6] 检查版本号格式...
  ✅ 通过: 所有版本号格式正确

============================================================
  测试总结
============================================================
总测试数: 6
✅ 通过: 6
❌ 失败: 0

🎉 所有测试通过!
============================================================
```

### 测试最佳实践

1. **提交前必测**：在 `git commit` 前运行测试确保数据质量
2. **新增词条后测**：添加新词条后立即运行测试验证
3. **批量修改后测**：批量编辑后运行测试检查一致性
4. **CI/CD 集成**：在 GitHub Actions 中自动运行测试

---

## 📝 标准工作流

```bash
# 1. 编辑词条（手动维护）
# 编辑 coding_dictionary/coding_dictionary.json

# 2-4. 一键执行完整流程（推荐）
python scripts/dic_tools.py --all

# 或者分步执行：
# 2. 验证数据
python scripts/dic_tools.py --validate

# 3. 生成文档
python scripts/dic_tools.py --generate-md

# 4. 更新变更日志
python scripts/dic_tools.py --changelog

# 5. 提交到 GitHub
git add coding_dictionary/ auto_generated/
git commit -m "feat: 添加新词条"
git push
```

---

## 📊 数据字段规范

### 必填字段

| 字段         | 说明         | 示例                       |
| ------------ | ------------ | -------------------------- |
| `id`       | 全局唯一标识 | `snomed:129006008`       |
| `code`     | 编码值       | `129006008`              |
| `system`   | 编码系统 URI | `http://snomed.info/sct` |
| `display`  | 显示名称     | `Walking`                |
| `category` | 分类         | `motion_codes`           |
| `status`   | 状态         | `active`                 |
| `version`  | 语义版本     | `1.0.0`                  |

### 可选字段

| 字段            | 说明         |
| --------------- | ------------ |
| `description` | 中文描述     |
| `synonyms`    | 同义词列表   |
| `source_refs` | 来源追溯     |
| `detection`   | 雷达检测能力 |

### 词条分类

本字典库采用统一的分类体系，所有词条必须使用以下分类之一：

| 分类                         | 说明              | 例子                                         |
| ---------------------------- | ----------------- | -------------------------------------------- |
| `posture_codes`            | 姿态编码          | Standing, Sitting, Lying Supine, Lying Prone |
| `motion_codes`             | 运动编码          | Walking, Running, Static, Falling Down       |
| `physiological_codes`      | 生理指标编码      | Tachycardia, Bradycardia, Apnea, Tachypnea   |
| `disorder_condition_codes` | 疾病状况编码      | Sleep, Sleep Disorder                        |
| `safety_alert_codes`       | 安全警报编码      | Falls, Emergency, Alert, Warning, Critical   |
| `tag`                      | AI 标签（自定义） | Fall Risk, Mobility Impaired, Elderly        |

> **注意**：所有新词条必须使用上述分类之一。分类选择应基于词条的实际语义，而非历史习惯。

---

## 💡 词条示例

```json
{
  "id": "snomed:129006008",
  "code": "129006008",
  "system": "http://snomed.info/sct",
  "display": "Walking",
  "display_zh": "步行",
  "category": "motion_codes",
  "status": "active",
  "version": "1.0.0",
  "description": "Periodic gait pattern with low to moderate speed.",
  "description_zh": "周期性步态，速度低到中等。",
  "synonyms": ["Ambulation", "Gait"],
  "synonyms_zh": ["行走", "走路"],
  "source_refs": [
    {
      "file": "原始参考文件/fhir与snomed_ct代码.md",
      "section": "三、实际可检测的运动状态总结"
    }
  ],
  "detection": {
    "radar_60ghz": {
      "detectable": "direct",
      "method": "速度检测（vel_x/y/z > 10 cm/s）+ 周期性步态信号（1-2 Hz）",
      "confidence": "high"
    },
    "sleep_pad": {
      "detectable": "indirect",
      "method": "通过体动模式间接推断",
      "confidence": "medium"
    }
  }
}
```

---

## 🎯 多传感器检测能力标注

本字典库为每个词条标注了不同传感器的检测能力，包括：

### 传感器类型

- **radar_60ghz**：60GHz 毫米波雷达（运动、姿态、跌倒、生命体征）
- **sleep_pad**：睡眠板传感器（心率、呼吸、翻身、抽搐）
- **mems_seismic**：MEMS 地震传感器（跌倒、振动事件）
- **sos_handle**：SOS 紧急呼叫手柄（手动报警）

### 检测级别

| 检测级别 | 标记 | 说明                 |
| -------- | ---- | -------------------- |
| 直接检测 | ✅   | 传感器信号可直接映射 |
| 间接检测 | ⚠️ | 需算法+模型辅助      |
| 不可检测 | ❌   | 需其他传感器或方法   |

---

## 🚨 重要规则

### ⚠️ 禁止手改

1. **禁止修改** `auto_generated/` 目录任何文件
2. **禁止修改** `changelog.md`（自动生成）
3. **禁止修改** `auto_generated/markdown/coding_terms.md`（自动生成）

### 📁 临时文件夹说明

`temp/` 文件夹用于存放**临时生成文件**，完全可以安全删除：

- 所有临时输出文件都在此目录，不会污染主项目目录
- **Python 缓存**：所有 `__pycache__` 统一生成到 `temp/__pycache__/`，保持项目结构整洁
- 文件命名规范：`*_tmp.json`、`*_temp.json` 等明确标记
- 用途：测试、验证中间步骤、批量编辑草稿、Python 字节码缓存等
- **建议**：定期清理此文件夹，保持项目整洁

```bash
# 安全删除所有临时文件
rm -r temp/*
```

### 🔄 临时文件工作流示例

如需批量添加词条但先验证再应用，使用 `--dry-run` 模式：

```bash
# 1. 生成草稿到临时文件（不修改主文件）
python scripts/add_coding_dict.py --dry-run

# 2. 验证临时文件内容
python scripts/validate_json.py temp/coding_terms_scaffold_new_tmp.json

# 3. 验证通过后，正式应用到主文件
python scripts/add_coding_dict.py

# 4. 清理临时文件
rm temp/*
```

或验证其他临时 JSON：

```bash
python scripts/validate_json.py temp/your_custom_coding_terms_tmp.json
```

### ✅ 必须遵守

1. 所有修改在 `coding_dictionary/coding_dictionary.json` 进行
2. 提交前必须运行 `--validate`
3. `code` + `system` 组合唯一
4. 新增词条包含 `source_refs`

---

## 📈 当前统计

| 分类                         | 数量         | 说明                                           |
| ---------------------------- | ------------ | ---------------------------------------------- |
| `motion_codes`             | 8            | 运动编码（步行、奔跑、静止、跌倒等）           |
| `posture_codes`            | 8            | 姿态编码（站立、坐、仰卧、俯卧等）             |
| `physiological_codes`      | 3            | 生理指标编码（心动过速、心动过缓、呼吸暂停等） |
| `disorder_condition_codes` | 1            | 疾病状况编码（睡眠、睡眠障碍等）               |
| `safety_alert_codes`       | 9            | 安全警报编码（跌倒、紧急、警告、严重等）       |
| `tag`                      | 5            | AI 标签（跌倒风险、行动不便、老年人等）        |
| **总计**               | **34** | 持续更新中                                     |

---

## 🛠️ 扩展计划

### 近期

- [ ] 补充异常步态词条
- [ ] 添加呼吸异常类
- [ ] 完善 Tag 分类

### 中期

- [ ] FHIR 派生生成器
- [ ] 外部数据合并工具
- [ ] 多文件拆分支持

### 长期

- [ ] NPM/PyPI 包发布
- [ ] REST API 接口
- [ ] Web 编辑器

---

## 🤝 贡献指南

```bash
# 1. 创建分支
git checkout -b feature/new-terms

# 2. 编辑词条
vim coding_dictionary/coding_dictionary.json

# 3. 验证并生成文档（推荐使用完整流程）
python scripts/dic_tools.py --all

# 或者分步执行：
# python scripts/dic_tools.py --validate
# python scripts/dic_tools.py --generate-md
# python scripts/dic_tools.py --changelog

# 5. 提交
git commit -m "feat: 添加新词条"
git push origin feature/new-terms

# 6. 开启 PR
```

提交信息规范：

```
feat: 添加新词条
fix: 修复重复代码
docs: 更新文档
```

---

## 📚 参考文档

| 文档                                                                         | 说明                                                                   |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [tdpv1-0916-fixed.md](原始参考文件/tdpv1-0916-fixed.md)                         | 协议定义与危险等级                                                     |
| [fhir与snomed_ct代码.md](原始参考文件/fhir与snomed_ct代码.md)                   | 医疗编码标准                                                           |
| [fda-v0923.md](原始参考文件/fda-v0923.md)                                       | OWL Monitor System 完整系统架构（雷达、睡眠板、地震传感器、SOS系统等） |
| [FHIR CodeableConcept](https://www.hl7.org/fhir/datatypes.html#CodeableConcept) | FHIR 标准                                                              |

---

## ⚠️ 风险提示

- **医疗编码仅作互操作参考**，临床使用需结合最新版本与监管要求
- **预警逻辑需二次确认**，如心梗/卒中组合需在后端规则引擎中验证
- **多传感器检测能力标注**基于理论分析和系统设计，实际部署需现场验证
- **本项目不构成医疗诊断依据**
- **系统参考**：本字典库服务于 OWL Monitor System，涵盖雷达、睡眠板、地震传感器、SOS 等完整传感器体系

---

## 📄 许可证

本项目的使用受公司政策约束，未经公司许可，不得用于商业目的或进行修改和分发。如有疑问，请联系：benson@wisefido.com。

---

**最后更新**：2025-11-08
**最后更新说明**：新增撤回最近一次添加功能（选项 13 / --undo-last-add），完善运行模式说明。
**版本**：v1.2.2
**维护者**：WiseFido Team
