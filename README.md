# WiseFido_TDPv1_Coding_Dictionary

> 🎯 **可复用的医疗编码字典库** — JSON 作为唯一事实源 | 自动生成 Markdown | 变更追踪 | FHIR 兼容

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 📋 项目简介

WiseFido_TDPv1_Coding_Dictionary 是基于 **TDPv1 协议**和 **FHIR/SNOMED CT** 标准构建的医疗编码术语字典库。

- ✅ **机器可信**：JSON 作为"唯一事实源"，Schema 强校验
- ✅ **人类可读**：自动生成 Markdown 表格文档
- ✅ **变更追踪**：基于快照自动记录词条变化历史
- ✅ **医疗标准**：兼容 FHIR、SNOMED CT、LOINC
- ✅ **雷达检测**：标注 60GHz 毫米波雷达可检测能力
- ✅ **预警支持**：内置帕金森、卒中、心梗预警规则映射

---

## 🏗️ 项目架构

```plaintext
WiseFido_TDPv1_Coding_Dictionary/
│
├── README.md                      (M) 项目总览与使用文档
├── 原始参考文件/                   (M) 只读原始资料
│   ├── TDPv1-0916-fixed.md       
│   └── FHIR与SNOMED_CT代码.md     
│
├── dictionary/                    (M) 唯一事实源 JSON
│   └── coding_terms.json         (M) 主词条文件
│
├── schema/                        (M) JSON Schema 定义
│   └── coding_item.schema.json   
│
├── scripts/                       (M) 一键式工具脚本
│   ├── tool.py                   (主入口)
│   ├── validate.py               (校验器)
│   ├── generate_md.py            (Markdown 生成器)
│   ├── changelog.py              (CHANGELOG 生成器)
│   └── scaffold_append.py        (批量占位脚本)
│
├── generated/                     (G) 自动生成【禁止手改】
│   ├── markdown/                 
│   │   └── coding_terms.md       
│   ├── CHANGELOG.md              
│   └── .snapshot.json            
│
├── temp/                          (T) 临时文件夹【可安全删除】
│   └── *.tmp.json                (临时文件使用，生成测试等)
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
python scripts/tool.py
```

菜单选项：
- `1` - 校验 JSON 词条
- `2` - 生成 Markdown 表格
- `3` - 更新 CHANGELOG
- `0` - 退出

### 3️⃣ 命令行模式

```bash
# 校验词条
python scripts/tool.py --validate

# 生成 Markdown 文档
python scripts/tool.py --generate-md

# 更新变更日志
python scripts/tool.py --changelog
```

---

## 📝 标准工作流

```bash
# 1. 编辑词条（手动维护）
# 编辑 dictionary/coding_terms.json

# 2. 验证数据
python scripts/tool.py --validate

# 3. 生成文档
python scripts/tool.py --generate-md

# 4. 更新变更日志
python scripts/tool.py --changelog

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
| `id` | 全局唯一标识 | `motion_state.walking.snomed.129006008` |
| `code` | 编码值 | `129006008` |
| `system` | 编码系统 URI | `http://snomed.info/sct` |
| `display` | 显示名称 | `Walking` |
| `category` | 分类 | `motion_state` |
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

| 分类 | 说明 | 例子 |
|------|------|------|
| `motion_state` | 运动状态 | Walking, Tremor, Shuffling gait |
| `posture` | 身体姿态 | Sitting, Standing, Lying |
| `health_condition` | 健康状况 | Fall, Myocardial infarction |
| `danger_level` | 危险等级 | EMERGENCY, ALERT, CRITICAL |
| `tag` | AI 标签 | Tachycardia, Fall, OutOfBed |

---

## 💡 词条示例

```json
{
  "id": "motion_state.walking.snomed.129006008",
  "code": "129006008",
  "system": "http://snomed.info/sct",
  "display": "Walking",
  "category": "motion_state",
  "status": "active",
  "version": "1.0.0",
  "description": "步行：周期性步态，速度低到中等。",
  "synonyms": ["步行", "行走"],
  "source_refs": [
    {
      "file": "原始参考文件/FHIR与SNOMED_CT代码.md",
      "section": "三、实际可检测的运动状态总结"
    }
  ],
  "detection": {
    "radar_60ghz": {
      "detectable": "direct",
      "method": "速度检测（vel_x/y/z > 10 cm/s）+ 周期性步态信号（1-2 Hz）",
      "confidence": "high"
    }
  }
}
```

---

## 🎯 雷达检测能力标注

| 检测级别 | 标记 | 说明 |
|----------|------|------|
| 直接检测 | ✅ | 雷达信号可直接映射 |
| 间接检测 | ⚠️ | 需算法+模型辅助 |
| 不可检测 | ❌ | 需其他传感器 |

---

## 🚨 重要规则

### ⚠️ 禁止手改

1. **禁止修改** `generated/` 目录任何文件
2. **禁止修改** `CHANGELOG.md`（自动生成）
3. **禁止修改** `generated/markdown/coding_terms.md`（自动生成）

### 📁 临时文件夹说明

`temp/` 文件夹用于存放**临时生成文件**，完全可以安全删除：
- 所有临时输出文件都在此目录，不会污染主项目目录
- 文件命名规范：`*_tmp.json`、`*_temp.json` 等明确标记
- 用途：测试、验证中间步骤、批量编辑草稿等
- **建议**：定期清理此文件夹，保持项目整洁

```bash
# 安全删除所有临时文件
rm -r temp/*
```

### 🔄 临时文件工作流示例

如需批量添加词条但先验证再应用，使用 `--dry-run` 模式：

```bash
# 1. 生成草稿到临时文件（不修改主文件）
python scripts/scaffold_append.py --dry-run

# 2. 验证临时文件内容
python scripts/validate.py temp/coding_terms_scaffold_new_tmp.json

# 3. 验证通过后，正式应用到主文件
python scripts/scaffold_append.py

# 4. 清理临时文件
rm temp/*
```

或验证其他临时 JSON：

```bash
python scripts/validate.py temp/your_custom_coding_terms_tmp.json
```

### ✅ 必须遵守

1. 所有修改在 `dictionary/coding_terms.json` 进行
2. 提交前必须运行 `--validate`
3. `code` + `system` 组合唯一
4. 新增词条包含 `source_refs`

---

## 📈 当前统计

| 分类 | 数量 | 完成度 |
|------|------|--------|
| motion_state | 7 | 🟢 50% |
| posture | 7 | 🟢 70% |
| health_condition | 4 | 🟡 30% |
| danger_level | 6 | 🟢 100% |
| tag | 4 | 🟡 20% |
| **总计** | **28** | 🟡 **45%** |

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

# 3. 验证
python scripts/tool.py --validate

# 4. 生成文档
python scripts/tool.py --generate-md
python scripts/tool.py --changelog

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
| [TDPv1-0916-fixed.md](原始参考文件/TDPv1-0916-fixed.md) | 协议定义与危险等级 |
| [FHIR与SNOMED_CT代码.md](原始参考文件/FHIR与SNOMED_CT代码.md) | 医疗编码标准 |
| [FHIR CodeableConcept](https://www.hl7.org/fhir/datatypes.html#CodeableConcept) | FHIR 标准 |

---

## ⚠️ 风险提示

- **医疗编码仅作互操作参考**，临床使用需结合最新版本与监管要求
- **预警逻辑需二次确认**，如心梗/卒中组合需在后端规则引擎中验证
- **雷达检测能力标注**基于理论分析，实际部署需现场验证
- **本项目不构成医疗诊断依据**

---

## 📄 许可证

本项目采用 [MIT License](LICENSE)

---

**最后更新**：2025-11-08  
**版本**：v1.2.0  
**维护者**：WiseFido Team
