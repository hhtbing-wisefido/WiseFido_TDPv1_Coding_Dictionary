# WiseFido_TDPv1_Coding_Dictionary

> 🎯 **可复用的医疗编码字典库** — JSON 作为唯一事实源 | 自动生成 Markdown | 变更追踪 | FHIR 兼容

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
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
├── docs/                          (M) 开发规范文档
│   └── id_format_guide.md        (ID 格式规范)
├── 原始参考文件/                   (M) 业务参考文档（只读）
│   ├── tdpv1-0916-fixed.md       
│   ├── fhir与snomed_ct代码.md
│   └── fda-v0923.md              (OWL Monitor System 系统架构参考)     
│
├── dictionary/                    (M) 唯一事实源 JSON
│   └── coding_terms.json         (M) 主词条文件
│
├── schema/                        (M) JSON Schema 定义
│   └── coding_item.schema.json   
│
├── scripts/                       (M) 一键式工具脚本
│   ├── _config.py                (公共配置：统一 __pycache__ 到 temp 目录)
│   ├── tools.py                  (主入口)
│   ├── validate_json.py          (校验器)
│   ├── generate_md.py            (Markdown 生成器)
│   ├── changelog.py              (CHANGELOG 生成器)
│   └── add_coding_dict.py        (批量添加编码字典词条脚本)
│
├── generated/                     (G) 自动生成【禁止手改】
│   ├── markdown/                 
│   │   └── coding_terms.md       
│   ├── changelog.md              
│   └── .snapshot.json            
│
├── temp/                          (T) 临时文件夹【可安全删除】
│   ├── __pycache__/              (Python 缓存文件，自动生成)
│   └── *.tmp.json, *.py, etc.    (临时文件、测试脚本、迁移工具等)
│
├── .github/workflows/             (M) CI/CD 自动化
│   └── ci.yml                    
│
├── requirements.txt               (M) Python 依赖
├── .gitignore                    (M) Git 忽略规则
└── LICENSE                       (M) MIT 许可证

(M)=手动维护  (G)=自动生成  (T)=临时文件（可删除）
```

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 交互式菜单

```bash
python scripts/tools.py
```

菜单选项：
- `1` - 校验 JSON 词条
- `2` - 生成 Markdown 表格
- `3` - 更新 changelog
- `4` - 完整流程（校验+生成+更新）
- `5` - 显示统计信息
- `6` - 清理临时文件
- `7` - 运行测试套件 🧪
- `0` - 退出

### 3️⃣ 命令行模式

支持长选项（`--`）和短选项（`-`）两种格式：

```bash
# 校验词条
python scripts/tools.py --validate    # 或: python scripts/tools.py -v

# 生成 Markdown 文档
python scripts/tools.py --generate-md # 或: python scripts/tools.py -g

# 更新变更日志
python scripts/tools.py --changelog   # 或: python scripts/tools.py -c

# 完整流程（一次性执行校验+生成+更新）
python scripts/tools.py --all         # 或: python scripts/tools.py -a

# 显示统计信息
python scripts/tools.py --stats       # 或: python scripts/tools.py -s

# 运行测试套件 🧪
python scripts/tools.py --test        # 或: python scripts/tools.py -t

# 清理临时文件
python scripts/tools.py --clean
```

---

## 🧪 测试套件

项目内置了完整的测试套件，用于验证数据质量和完整性。

### 测试项目

| 测试项 | 说明 | 检查内容 |
|--------|------|----------|
| **必填字段检查** | 验证所有词条包含必填字段 | id, code, system, display, display_zh, category, status, version |
| **ID 格式检查** | 验证 ID 格式正确 | 格式为 `prefix:code` 或 `prefix:protocol://path` |
| **重复 ID 检查** | 验证无重复 ID | 每个 ID 在字典中唯一 |
| **code+system 唯一性** | 验证编码组合唯一 | 同一编码系统中 code 不重复 |
| **分类有效性检查** | 验证使用有效分类 | 分类必须在预定义列表中 |
| **版本号格式检查** | 验证版本号符合语义化版本 | 格式为 `X.Y.Z` |

### 运行测试

```bash
# 运行完整测试套件
python scripts/tools.py --test

# 或使用短选项
python scripts/tools.py -t
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
# 编辑 dictionary/coding_terms.json

# 2-4. 一键执行完整流程（推荐）
python scripts/tools.py --all

# 或者分步执行：
# 2. 验证数据
python scripts/tools.py --validate

# 3. 生成文档
python scripts/tools.py --generate-md

# 4. 更新变更日志
python scripts/tools.py --changelog

# 5. 提交到 GitHub
git add dictionary/ generated/
git commit -m "feat: 添加新词条"
git push
```

---

## 📊 数据字段规范

### 必填字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 全局唯一标识 | `snomed:129006008` |
| `code` | 编码值 | `129006008` |
| `system` | 编码系统 URI | `http://snomed.info/sct` |
| `display` | 显示名称 | `Walking` |
| `category` | 分类 | `motion_codes` |
| `status` | 状态 | `active` |
| `version` | 语义版本 | `1.0.0` |

### 可选字段

| 字段 | 说明 |
|------|------|
| `description` | 中文描述 |
| `synonyms` | 同义词列表 |
| `source_refs` | 来源追溯 |
| `detection` | 雷达检测能力 |

### 词条分类

本字典库采用统一的分类体系，所有词条必须使用以下分类之一：

| 分类 | 说明 | 例子 |
|------|------|------|
| `posture_codes` | 姿态编码 | Standing, Sitting, Lying Supine, Lying Prone |
| `motion_codes` | 运动编码 | Walking, Running, Static, Falling Down |
| `physiological_codes` | 生理指标编码 | Tachycardia, Bradycardia, Apnea, Tachypnea |
| `disorder_condition_codes` | 疾病状况编码 | Sleep, Sleep Disorder |
| `safety_alert_codes` | 安全警报编码 | Falls, Emergency, Alert, Warning, Critical |
| `tag` | AI 标签（自定义） | Fall Risk, Mobility Impaired, Elderly |

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

| 检测级别 | 标记 | 说明 |
|----------|------|------|
| 直接检测 | ✅ | 传感器信号可直接映射 |
| 间接检测 | ⚠️ | 需算法+模型辅助 |
| 不可检测 | ❌ | 需其他传感器或方法 |

---

## 🚨 重要规则

### ⚠️ 禁止手改

1. **禁止修改** `generated/` 目录任何文件
2. **禁止修改** `changelog.md`（自动生成）
3. **禁止修改** `generated/markdown/coding_terms.md`（自动生成）

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

1. 所有修改在 `dictionary/coding_terms.json` 进行
2. 提交前必须运行 `--validate`
3. `code` + `system` 组合唯一
4. 新增词条包含 `source_refs`

---

## 📈 当前统计

| 分类 | 数量 | 说明 |
|------|------|------|
| `motion_codes` | 8 | 运动编码（步行、奔跑、静止、跌倒等） |
| `posture_codes` | 8 | 姿态编码（站立、坐、仰卧、俯卧等） |
| `physiological_codes` | 3 | 生理指标编码（心动过速、心动过缓、呼吸暂停等） |
| `disorder_condition_codes` | 1 | 疾病状况编码（睡眠、睡眠障碍等） |
| `safety_alert_codes` | 9 | 安全警报编码（跌倒、紧急、警告、严重等） |
| `tag` | 5 | AI 标签（跌倒风险、行动不便、老年人等） |
| **总计** | **34** | 持续更新中 |

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
vim dictionary/coding_terms.json

# 3. 验证并生成文档（推荐使用完整流程）
python scripts/tools.py --all

# 或者分步执行：
# python scripts/tools.py --validate
# python scripts/tools.py --generate-md
# python scripts/tools.py --changelog

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

| 文档 | 说明 |
|------|------|
| [tdpv1-0916-fixed.md](原始参考文件/tdpv1-0916-fixed.md) | 协议定义与危险等级 |
| [fhir与snomed_ct代码.md](原始参考文件/fhir与snomed_ct代码.md) | 医疗编码标准 |
| [fda-v0923.md](原始参考文件/fda-v0923.md) | OWL Monitor System 完整系统架构（雷达、睡眠板、地震传感器、SOS系统等） |
| [FHIR CodeableConcept](https://www.hl7.org/fhir/datatypes.html#CodeableConcept) | FHIR 标准 |

---

## ⚠️ 风险提示

- **医疗编码仅作互操作参考**，临床使用需结合最新版本与监管要求
- **预警逻辑需二次确认**，如心梗/卒中组合需在后端规则引擎中验证
- **多传感器检测能力标注**基于理论分析和系统设计，实际部署需现场验证
- **本项目不构成医疗诊断依据**
- **系统参考**：本字典库服务于 OWL Monitor System，涵盖雷达、睡眠板、地震传感器、SOS 等完整传感器体系

---

## 📄 许可证

本项目采用 [MIT License](LICENSE)

---

**最后更新**：2025-11-08  
**版本**：v1.2.0  
**维护者**：WiseFido Team
