# WiseFido_TDPv1_Coding_Dictionary

> 🎯 **可复用医疗编码字典库**｜JSON 唯一事实源｜自动生成 Markdown｜变更追踪｜FHIR/SNOMED CT 兼容

[![Copyright: WiseFido](https://img.shields.io/badge/Copyright-WiseFido-blue.svg)](https://www.wisefido.com)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 项目简介

WiseFido_TDPv1_Coding_Dictionary 基于 **TDPv1 协议** 与 **FHIR/SNOMED CT** 标准构建，是 OWL Monitor System（多传感器老人健康监测系统）的统一术语库。

主要特性：

- **多传感器覆盖**：60 GHz 雷达、睡眠板、MEMS 地震传感器、SOS 手柄等能力统一建模
- **机器可信**：JSON 作为唯一事实源，配套 JSON Schema 与自动验证脚本
- **人类可读**：一键生成中英文对照的 Markdown 文档和变更日志
- **变更追踪**：快照对比与自动 changelog，便于审计与回滚
- **医疗标准**：兼容 FHIR、SNOMED CT、LOINC，并支持内部编码
- **预警支撑**：可映射帕金森、卒中、心梗等预警规则

---

## 仓库结构

```plaintext
WiseFido_TDPv1_Coding_Dictionary/
├── README.md                      项目总览（本文档）
├── coding_dictionary/             核心数据源（唯一事实源）
│   └── coding_dictionary.json      主词条列表（JSON）
├── schema/                        机器校验规范
│   └── coding_dictionary.schema.json  JSON Schema
├── spec/                          数据结构与字段规范
│   └── coding_dictionary.schema.spec.md
├── scripts/                       维护脚本
│   ├── _config.py                 公共配置
│   ├── dic_tools.py               主工具（交互/参数两用）
│   ├── validate_json.py           JSON + 逻辑校验
│   ├── generate_md.py             Markdown 生成
│   ├── changelog.py               变更日志生成
│   └── add_coding_dict.py         批量添加词条
├── auto_generated/                自动输出（禁止手动修改）
│   ├── coding_dictionary.md       数据表格（双语）
│   ├── coding_dictionary.schema.md Schema 说明
│   ├── changelog.md               变更历史
│   └── .snapshot.json             快照
├── auto_backup/                   脚本创建的 JSON 备份
├── temp/                          临时文件与统一 __pycache__
├── .github/workflows/ci.yml       GitHub Actions 工作流
├── requirements.txt               Python 依赖
├── .gitignore
└── （无 LICENSE 文件，内部使用）
```

---

## 快速开始

### 1. 安装依赖

```bash
# 首次执行（自动安装缺失依赖）
python scripts/dic_tools.py

# 或手动安装
pip install -r requirements.txt
```

### 2. 交互式菜单

```bash
python scripts/dic_tools.py
```

完整菜单结构：

#### 【数据管理】
1. 校验词条数据 - 检查 JSON 格式和数据规范
2. 生成文档 - 生成可读的 Markdown 文档
3. 更新变更日志 - 记录词条变更历史
4. 执行完整流程 - 一键校验+生成+更新

#### 【数据查询】
5. 显示统计信息 - 查看词条分类和数量统计
6. 搜索词条 - 按条件查找词条
7. 查看词条详情 - 查看单个词条完整信息

#### 【数据编辑】
8. 添加新词条 - 交互式添加单个词条
9. 撤回最近添加 - 删除最后一次添加的词条

#### 【质量检测】
10. 运行测试套件 🧪 - 执行 6 项数据质量测试

#### 【数据备份】
11. 备份数据 - 手动备份词条数据
12. 恢复数据 - 从备份恢复数据

#### 【系统维护】
13. 清理临时文件 - 删除临时目录内容
0. 退出系统 - 关闭管理工具

### 3. 常用参数模式

```bash
python scripts/dic_tools.py --validate      # 校验
python scripts/dic_tools.py --generate-md   # 生成 Markdown
python scripts/dic_tools.py --changelog     # 更新变更日志
python scripts/dic_tools.py --all           # 完整流程
python scripts/dic_tools.py --stats         # 统计信息
python scripts/dic_tools.py --test          # 测试套件
python scripts/dic_tools.py --clean         # 清理 temp/
python scripts/dic_tools.py --backup        # 备份 JSON
python scripts/dic_tools.py --restore       # 恢复 JSON（含确认）
python scripts/dic_tools.py --undo-last-add # 撤回最近一次添加
python scripts/dic_tools.py --search id:snomed   # 条件搜索
python scripts/dic_tools.py --view snomed:129006008 # 查看详情
python scripts/dic_tools.py --stats --menu-after  # 先执行再回菜单
```

> `--menu-after` 便于“先跑一项任务再继续人工操作”。

#### 精简模式(短选项 `-`)
```bash
python scripts/dic_tools.py -v             # 校验
python scripts/dic_tools.py -g             # 生成 Markdown
python scripts/dic_tools.py -c             # 更新变更日志
python scripts/dic_tools.py -a             # 完整流程
python scripts/dic_tools.py -s             # 统计信息
python scripts/dic_tools.py -t             # 测试套件
```

> **提示**:
> - 精简模式仅支持常用功能，复杂操作需使用完整模式
> - `--menu-after` 可与任何参数组合，先执行命令再进入交互菜单

---

## 测试套件

脚本内置 6 项校验：必填字段、ID 格式、重复 ID、code+system 唯一性、分类合法性、版本号格式。

运行：

```bash
python scripts/dic_tools.py --test
```

所有项通过后会输出“🎉 所有测试通过!”。

---

## 标准工作流

```bash
# 1. 编辑 JSON（coding_dictionary/coding_dictionary.json）
# 2. 运行完整流程
python scripts/dic_tools.py --all
# 3. 提交变更
git add coding_dictionary/ auto_generated/
git commit -m "feat: xxx"
git push
```

> 提交前务必运行 `--validate` 或 `--all`，确保自动生成文件已更新。

---

## 数据字段

### 必填字段

| 字段                         | 说明                        | 示例                       |
| ---------------------------- | --------------------------- | -------------------------- |
| `id`                       | 全局唯一（`prefix:code`） | `snomed:129006008`       |
| `code`                     | 编码值                      | `129006008`              |
| `system`                   | 编码系统 URI                | `http://snomed.info/sct` |
| `display` / `display_zh` | 英文/中文名称               | `Walking / 步行`         |
| `category`                 | 分类（见下）                | `motion_codes`           |
| `status`                   | 状态                        | `active`                 |
| `version`                  | 语义版本                    | `1.0.0`                  |

### 可选字段

| 字段                                 | 说明           |
| ------------------------------------ | -------------- |
| `description` / `description_zh` | 详细描述       |
| `synonyms` / `synonyms_zh`       | 同义词         |
| `source_refs`                      | 来源追溯       |
| `detection`                        | 传感器检测能力 |

### 分类枚举

`posture_codes`｜`motion_codes`｜`physiological_codes`｜`disorder_condition_codes`｜`safety_alert_codes`｜`tag`

---

## 词条示例

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
  "description_zh": "周期性步态，速度低至中等。",
  "synonyms": ["Ambulation", "Gait"],
  "source_refs": [{
    "file": "原始参考文件/fhir与snomed_ct代码.md",
    "section": "三、实际可检测的运动状态总结"
  }],
  "detection": {
    "radar_60ghz": {
      "detectable": "direct",
      "method": "速度 >10 cm/s 且 1–2 Hz 周期步态",
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

## 重要规则

1. **唯一可编辑的数据源**:`coding_dictionary/coding_dictionary.json`(所有词条修改必须在此文件进行)
2. **禁止手动修改** `auto_generated/` 目录下的任何文件(由脚本自动生成)
3. **禁止手动修改** `changelog.md` 和 `.snapshot.json`(自动维护)

### 临时目录 `temp/`

- 统一存放 `__pycache__`、批量导入草稿、校验中间文件
- 建议定期清理：

```bash
# 跨平台清理
python scripts/dic_tools.py --clean
# 或手动
rm -rf temp/*
Remove-Item -Recurse -Force temp\*
```

### 临时文件工作流

```bash
python scripts/add_coding_dict.py --dry-run
python scripts/validate_json.py temp/coding_terms_scaffold_new_tmp.json
python scripts/add_coding_dict.py   # 确认无误后正式写入
python scripts/dic_tools.py --clean
```

---

## 参考文档

| 文档                                                                         | 说明                                                  |
| ---------------------------------------------------------------------------- | ----------------------------------------------------- |
| tdpv1-0916-fixed.md                                                          | TDPv1 协议与风险等级                                  |
| fhir与snomed_ct代码.md                                                       | 医疗编码标准参考                                      |
| fda-v0923.md                                                                 | OWL Monitor System 架构（雷达/睡眠板/地震传感器/SOS） |
| [FHIR CodeableConcept](https://www.hl7.org/fhir/datatypes.html#CodeableConcept) | 官方 FHIR 文档                                        |

---

## 风险提示

- 医疗编码仅用于系统互操作，临床使用须结合最新监管要求
- 预警逻辑需在后端规则引擎中再次验证
- 传感器检测能力需在现场环境复核
- 本项目不构成医疗诊断依据

---

## 许可

本项目为公司内部资源，未经书面许可不得对外分发或商业使用。如需授权请联系：benson@wisefido.com。

---

## 环境与编码

- 推荐使用虚拟环境：
  - Windows PowerShell：`python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt`
  - Linux/macOS：`python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Windows 终端若出现中文乱码，可运行 `chcp 65001` 或设置 `$OutputEncoding` 为 UTF-8
- 请使用 UTF-8 编码保存所有文件

## CI/CD 自动化

- GitHub Actions：`.github/workflows/ci.yml`
  - 步骤：`--validate` → `--generate-md` → `--changelog` → `git diff`
  - 建议提交包含 `auto_generated/` 目录，方便在 PR 中审阅

## 统计信息获取

- 运行 `python scripts/dic_tools.py --stats` 查看最新分类/状态/系统分布
- README 不再固定展示静态“当前统计”，以免与真实数据漂移

## 更正说明

- 交互菜单中“撤回最近一次添加”为 **选项 9**（命令行 `--undo-last-add`）。早期文档写作 13，现已修正。

---

最后更新日期: 2025-11-11
最后更新说明: 添加精简模式参数、修正文件路径错误、优化规则表述、修正PowerShell命令语法
版本: v1.2.3
维护者: WiseFido Team
