# 🏗️ 实施计划框架

> **项目**: WiseFido 医疗编码字典 Web 服务  
> **技术栈**: Python + FastAPI + Docker + GHCR (无数据库)  
> **策略**: 先 Web 后同步，先单文件后拆分  
> **创建日期**: 2025-01-13

---

## 🎯 项目目标

将现有的医疗编码字典命令行工具转换为 Web API 服务，并实现自动对接外部医疗编码系统的功能。

### 核心需求

1. **突破 GitHub 限制**: 利用自有服务器存储大规模编码数据
2. **自动对接编码系统**: 自动连接 SNOMED CT、ICD-10、LOINC 等官方 API
3. **自动定期同步**: 无需人工干预的数据更新
4. **提供 API 服务**: 标准化的 REST API 查询接口
5. **Docker 一键部署**: 容器化部署到任意服务器

---

## 📐 整体架构

```
┌─────────────────────────────────────────────────────────┐
│  阶段 1: Web API (第 1 周)                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  app.py                                           │  │
│  │  - 封装现有 dic_tools.py                          │  │
│  │  - 提供 REST API                                  │  │
│  │  - 基于现有 79 条数据                              │  │
│  └───────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Docker + GHCR                                    │  │
│  │  - 容器化打包                                      │  │
│  │  - 自动构建发布                                    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        
┌─────────────────────────────────────────────────────────┐
│  阶段 2: 同步功能 (第 2 周)                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  sync/ 模块                                       │  │
│  │  - 连接 SNOMED CT API                            │  │
│  │  - 连接 ICD-10 数据源                             │  │
│  │  - 连接 LOINC 数据源                              │  │
│  │  - 定时自动同步                                    │  │
│  └───────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  coding_dictionary/coding_dictionary.json         │  │
│  │  79 条 → 1000 条 → 10万+ 条                       │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构规划

### 现有结构（保留）

```
WiseFido_TDPv1_Coding_Dictionary/
├── 📂 coding_dictionary/
│   └── coding_dictionary.json          ✅ 79 条数据（保留）
│
├── 📂 scripts/                         ✅ 完全保留
│   ├── _config.py
│   ├── dic_tools.py                    ✅ 核心功能（复用）
│   ├── validate_json.py                ✅ 数据验证（复用）
│   └── generate_markdown.py
│
└── 📂 schema/                          ✅ 保留
    └── coding_dictionary_schema.json
```

### 阶段 1 新增（本周）

```
WiseFido_TDPv1_Coding_Dictionary/
├── 📄 app.py                           🆕 FastAPI 应用
├── 📄 Dockerfile                       🆕 Docker 配置
├── 📄 docker-compose.yml               🆕 编排配置
├── 📄 .dockerignore                    🆕 忽略文件
├── 📄 requirements.txt                 📝 更新依赖
│
└── 📂 .github/
    └── workflows/
        └── docker-publish.yml          🆕 CI/CD 配置
```

### 阶段 2 新增（下周）

```
WiseFido_TDPv1_Coding_Dictionary/
└── 📂 sync/                            🆕 同步模块
    ├── __init__.py
    ├── snomed_sync.py                  🆕 SNOMED CT 同步
    ├── icd10_sync.py                   🆕 ICD-10 同步
    ├── loinc_sync.py                   🆕 LOINC 同步
    ├── data_merger.py                  🆕 数据合并
    └── scheduler.py                    🆕 定时任务
```

---

## 🎯 阶段 1: Web API（第 1 周 3 天）

### Day 1: FastAPI 应用

**目标**: 封装现有功能为 REST API

**任务**:
- [ ] 创建 `app.py` (80 行)
- [ ] 更新 `requirements.txt`
- [ ] 本地测试

**API 端点设计**:
```
GET  /                    # 首页/API 文档入口
GET  /api/search?q=xxx    # 搜索编码（复用 dic_tools.search_entries）
GET  /api/stats           # 统计信息（复用 dic_tools.get_statistics）
GET  /health              # 健康检查
```

**核心代码思路**:
```python
# app.py
from fastapi import FastAPI
from scripts.dic_tools import search_entries, get_statistics

app = FastAPI()

# 启动时加载现有 79 条数据
@app.on_event("startup")
async def startup():
    global data
    data = load_dictionary()  # 复用现有函数

# 封装现有函数为 API
@app.get("/api/search")
async def search(q: str):
    return search_entries(data, keyword=q)  # 复用现有函数
```

**验收标准**:
```bash
✅ python app.py 可运行
✅ http://localhost:8080/docs 显示 API 文档
✅ http://localhost:8080/api/stats 返回统计信息
✅ http://localhost:8080/api/search?q=apnea 返回搜索结果
```

---

### Day 2: Docker 化

**目标**: 容器化打包

**任务**:
- [ ] 创建 `Dockerfile` (15 行)
- [ ] 创建 `docker-compose.yml` (20 行)
- [ ] 创建 `.dockerignore` (10 行)
- [ ] 本地构建测试

**Dockerfile 策略**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

**验收标准**:
```bash
✅ docker-compose build 成功
✅ docker-compose up -d 成功
✅ docker logs 无错误
✅ curl http://localhost:8080/health 返回 200
```

---

### Day 3: 自动发布到 GHCR

**目标**: 实现 CI/CD 自动构建

**任务**:
- [ ] 创建 `.github/workflows/docker-publish.yml` (50 行)
- [ ] 推送代码到 GitHub
- [ ] 验证自动构建
- [ ] 更新 README 使用说明

**GitHub Actions 配置**:
```yaml
name: Docker Publish
on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Login to GHCR
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

**验收标准**:
```bash
✅ git push 后 Actions 自动触发
✅ Actions 构建成功（3-5 分钟）
✅ docker pull ghcr.io/用户名/项目名:latest 成功
✅ 镜像可在任意服务器运行
```

---

### 🎉 里程碑 1（Day 3 结束）

**交付物**:
- ✅ 完整可用的 Web API 服务
- ✅ 基于现有 79 条数据
- ✅ Docker 镜像（~200 MB）
- ✅ 自动发布到 GHCR
- ✅ 任何人可一键部署

**使用方式**:
```bash
docker run -d -p 8080:8080 ghcr.io/hhtbing-wisefido/wisefido_tdpv1_coding_dictionary:latest

# 访问
http://localhost:8080/docs        # API 文档
http://localhost:8080/api/stats   # 统计信息
```

---

## 🎯 阶段 2: 同步功能（第 2 周 4 天）

### Day 4-5: 同步模块开发

**目标**: 从外部 API 获取数据

**任务**:
- [ ] 创建 `sync/snomed_sync.py` (100 行)
- [ ] 创建 `sync/data_merger.py` (80 行)
- [ ] 测试 API 连接
- [ ] 测试数据转换

**数据源**:
- SNOMED CT: https://browser.ihtsdotools.org/snowstorm/snomed-ct
- 频率限制: ~50-100 请求/分钟
- 策略: 添加 1.2 秒请求间隔

**数据流程**:
```
1. snomed_sync.py
   - 连接 Snowstorm API
   - 分页获取数据（1000 条/页）
   - 转换为 coding_dictionary_schema.json 格式
   
2. data_merger.py
   - 读取现有 coding_dictionary.json
   - 合并新数据（按 id 去重）
   - 调用 validate_json.py 验证
   - 保存回 coding_dictionary.json
```

**验收标准**:
```bash
✅ python sync/snomed_sync.py 成功运行
✅ 获取 1000 条测试数据
✅ 数据格式符合 schema 定义
✅ python scripts/validate_json.py 验证通过
✅ coding_dictionary.json 从 79 条增加到 1079 条
```

---

### Day 6-7: 集成和定时任务

**目标**: 集成到 Web 应用，添加定时功能

**任务**:
- [ ] 修改 `app.py` 添加同步接口
- [ ] 创建 `sync/scheduler.py` (50 行)
- [ ] 测试手动同步
- [ ] 测试定时任务
- [ ] 更新 Docker 配置

**新增 API 端点**:
```
POST /api/sync                # 手动触发同步
GET  /api/sync/status         # 查看同步状态
GET  /api/sync/logs           # 同步日志
```

**定时任务配置**:
```python
# sync/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler

def schedule_sync():
    scheduler = BackgroundScheduler()
    # 每月 1 号凌晨 2 点同步
    scheduler.add_job(
        func=sync_all_systems,
        trigger="cron",
        day=1,
        hour=2
    )
    scheduler.start()
```

**验收标准**:
```bash
✅ curl -X POST http://localhost:8080/api/sync 触发同步
✅ 数据量增加
✅ 定时任务在日志中显示启动
✅ Docker 容器包含同步功能
```

---

### 🎉 里程碑 2（Day 7 结束）

**交付物**:
- ✅ 完整可用的 Web API 服务
- ✅ 自动同步 SNOMED CT 功能
- ✅ 定时任务（每月自动更新）
- ✅ 手动触发同步
- ✅ 数据量：79 + 1000+ 条

**系统能力**:
```
✅ 基础查询服务（阶段 1）
✅ 自动数据同步（阶段 2）
✅ 定时更新机制（阶段 2）
✅ 手动干预能力（阶段 2）
```

---

## 📊 核心文件清单

### 阶段 1 文件（7 个）

| 文件 | 行数 | 说明 |
|-----|------|------|
| `app.py` | ~80 | FastAPI 应用主文件 |
| `Dockerfile` | ~15 | Docker 镜像配置 |
| `docker-compose.yml` | ~20 | Docker 编排配置 |
| `.dockerignore` | ~10 | Docker 忽略文件 |
| `.github/workflows/docker-publish.yml` | ~50 | CI/CD 自动化 |
| `requirements.txt` | +3 | 添加 FastAPI 依赖 |
| `README.md` | +30 | 使用说明更新 |

**总代码量**: ~200 行

---

### 阶段 2 文件（5 个）

| 文件 | 行数 | 说明 |
|-----|------|------|
| `sync/__init__.py` | ~5 | 模块初始化 |
| `sync/snomed_sync.py` | ~100 | SNOMED CT 同步逻辑 |
| `sync/data_merger.py` | ~80 | 数据合并和去重 |
| `sync/scheduler.py` | ~50 | 定时任务配置 |
| `app.py` (修改) | +50 | 添加同步 API |

**总代码量**: ~285 行

---

## 🔧 技术栈详情

### 依赖清单

```txt
# requirements.txt

# 现有依赖
jsonschema>=4.17.0
pyyaml>=6.0

# 阶段 1 新增
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# 阶段 2 新增
requests>=2.31.0
apscheduler>=3.10.0
```

### Docker 镜像规格

```
基础镜像: python:3.11-slim (~150 MB)
应用代码: ~10 MB
Python 依赖: ~30 MB
数据文件: ~0.05 MB (79 条)
─────────────────────────────
总大小: ~190 MB

启动时间: 1-2 秒
内存占用: 50-100 MB
```

---

## 🚨 关键决策记录

### 决策 1: 数据存储策略

**决策**: 保持单文件 `coding_dictionary.json`

**理由**:
- ✅ 最小化对现有代码的改动
- ✅ `dic_tools.py` 无需修改
- ✅ 即使 10 万条数据，文件也只有 50-100 MB
- ✅ 容易迁移（如需拆分，2-3 小时可完成）

**触发拆分条件**:
- 文件大小 > 300 MB
- 加载时间 > 10 秒
- 内存占用 > 1 GB
- 需要独立更新不同编码系统

---

### 决策 2: 开发顺序

**决策**: 先 Web 后同步

**理由**:
- ✅ Day 3 就有完整可用系统（MVP）
- ✅ 降低风险（问题隔离）
- ✅ 复用现有 79 条数据
- ✅ 更快验证架构设计
- ✅ 符合敏捷开发原则

**对比**:
```
先 Web:  Day 3 可用 ✅
先同步: Day 6 可用 ❌
```

---

### 决策 3: 数据源选择

**决策**: 使用 SNOMED International Snowstorm API

**API 地址**: https://browser.ihtsdotools.org/snowstorm/snomed-ct

**限制**:
- 频率限制: ~50-100 请求/分钟
- 单次返回: 最大 10,000 条
- 需分页获取完整数据

**应对策略**:
- 每次请求间隔 1.2 秒
- 遇到 429 错误自动重试
- 每月同步一次（避免频繁触发限流）

**备选方案**: UMLS API（更高频率限制，需申请账号）

---

## ✅ 验收标准

### 阶段 1 验收（Day 3）

**功能验收**:
- [ ] API 文档可访问 (`/docs`)
- [ ] 搜索接口正常 (`/api/search?q=test`)
- [ ] 统计接口正常 (`/api/stats`)
- [ ] 健康检查正常 (`/health`)

**Docker 验收**:
- [ ] 镜像构建成功
- [ ] 容器可正常运行
- [ ] 容器内 API 可访问
- [ ] 容器重启数据不丢失

**GHCR 验收**:
- [ ] GitHub Actions 成功运行
- [ ] 镜像推送到 GHCR
- [ ] 可公开拉取镜像
- [ ] 拉取的镜像可正常运行

---

### 阶段 2 验收（Day 7）

**同步功能验收**:
- [ ] 能从 SNOMED API 获取数据
- [ ] 数据格式转换正确
- [ ] 数据合并无重复
- [ ] 通过 `validate_json.py` 验证

**API 验收**:
- [ ] 手动同步接口可用 (`POST /api/sync`)
- [ ] 同步状态查询可用 (`GET /api/sync/status`)
- [ ] 同步后数据量增加
- [ ] 同步后查询接口返回新数据

**定时任务验收**:
- [ ] 定时任务成功启动
- [ ] 日志显示任务调度信息
- [ ] 可手动触发测试

---

## 📋 开发检查清单

### 阶段 1 - Web API

**Day 1: FastAPI 应用**
- [ ] 创建 `app.py`
- [ ] 从 `scripts/dic_tools.py` 导入函数
- [ ] 实现 `/api/search` 端点
- [ ] 实现 `/api/stats` 端点
- [ ] 实现 `/health` 端点
- [ ] 更新 `requirements.txt`
- [ ] 本地测试：`python app.py`
- [ ] 访问文档：http://localhost:8080/docs
- [ ] 测试搜索：`curl http://localhost:8080/api/search?q=test`
- [ ] 测试统计：`curl http://localhost:8080/api/stats`

**Day 2: Docker 化**
- [ ] 创建 `Dockerfile`
- [ ] 创建 `docker-compose.yml`
- [ ] 创建 `.dockerignore`
- [ ] 构建镜像：`docker-compose build`
- [ ] 启动容器：`docker-compose up -d`
- [ ] 查看日志：`docker-compose logs`
- [ ] 测试健康检查：`curl http://localhost:8080/health`
- [ ] 停止容器：`docker-compose down`

**Day 3: GitHub Actions**
- [ ] 创建 `.github/workflows/docker-publish.yml`
- [ ] 提交代码：`git add . && git commit -m "feat: add Web API"`
- [ ] 推送代码：`git push`
- [ ] 查看 Actions 运行状态
- [ ] 等待构建完成（3-5 分钟）
- [ ] 验证镜像：`docker pull ghcr.io/hhtbing-wisefido/wisefido_tdpv1_coding_dictionary:latest`
- [ ] 运行镜像：`docker run -d -p 8080:8080 <镜像名>`
- [ ] 更新 `README.md` 添加使用说明

**✅ 里程碑 1 达成**

---

### 阶段 2 - 同步功能

**Day 4: SNOMED 同步模块**
- [ ] 创建 `sync/` 目录
- [ ] 创建 `sync/__init__.py`
- [ ] 创建 `sync/snomed_sync.py`
- [ ] 实现 API 连接逻辑
- [ ] 实现分页获取逻辑
- [ ] 实现数据转换逻辑
- [ ] 添加请求间隔（1.2 秒）
- [ ] 添加错误重试机制
- [ ] 测试获取 100 条数据
- [ ] 验证数据格式

**Day 5: 数据合并模块**
- [ ] 创建 `sync/data_merger.py`
- [ ] 实现读取现有数据
- [ ] 实现数据去重逻辑
- [ ] 实现数据合并逻辑
- [ ] 集成 `validate_json.py` 验证
- [ ] 实现保存逻辑
- [ ] 测试合并 100 条数据
- [ ] 验证 `coding_dictionary.json` 更新
- [ ] 验证数据通过 schema 验证

**Day 6: API 集成**
- [ ] 修改 `app.py` 添加同步接口
- [ ] 实现 `POST /api/sync`
- [ ] 实现 `GET /api/sync/status`
- [ ] 添加同步锁（防止并发）
- [ ] 添加同步日志记录
- [ ] 测试手动触发同步
- [ ] 测试同步后查询新数据
- [ ] 更新 API 文档

**Day 7: 定时任务**
- [ ] 创建 `sync/scheduler.py`
- [ ] 配置 APScheduler
- [ ] 设置定时任务（每月 1 号）
- [ ] 集成到 `app.py` 启动流程
- [ ] 更新 `requirements.txt`
- [ ] 测试定时任务启动
- [ ] 重新构建 Docker 镜像
- [ ] 推送到 GHCR
- [ ] 测试完整流程

**✅ 里程碑 2 达成**

---

## 🎯 成功指标

### 阶段 1 成功指标

| 指标 | 目标 | 测量方式 |
|-----|------|---------|
| **API 可用性** | 99%+ | 健康检查返回 200 |
| **响应时间** | < 100ms | 搜索 API 响应时间 |
| **镜像大小** | < 300 MB | `docker images` 查看 |
| **启动时间** | < 5 秒 | 容器启动到可访问 |
| **内存占用** | < 200 MB | `docker stats` 查看 |

---

### 阶段 2 成功指标

| 指标 | 目标 | 测量方式 |
|-----|------|---------|
| **同步成功率** | > 95% | 同步日志 |
| **数据量** | > 1000 条 | `/api/stats` 查看 |
| **同步时间** | < 15 分钟 | 同步日志时间戳 |
| **数据准确性** | 100% | `validate_json.py` 验证 |
| **定时任务稳定性** | 100% | 日志记录 |

---

## 🚨 风险和应对

### 风险 1: API 频率限制

**风险**: SNOMED API 限流导致同步失败

**概率**: 中  
**影响**: 高

**应对策略**:
- ✅ 添加请求间隔（1.2 秒）
- ✅ 遇到 429 自动重试
- ✅ 每月同步一次（降低频率）
- ✅ 备选方案：UMLS API

---

### 风险 2: 数据格式不兼容

**风险**: 外部 API 数据格式与 schema 不匹配

**概率**: 中  
**影响**: 高

**应对策略**:
- ✅ 数据转换层独立
- ✅ 严格的 schema 验证
- ✅ 转换失败记录日志
- ✅ 保留原始数据备份

---

### 风险 3: Docker 构建失败

**风险**: GitHub Actions 构建失败

**概率**: 低  
**影响**: 中

**应对策略**:
- ✅ 本地先验证构建
- ✅ 锁定依赖版本
- ✅ 多阶段构建减少失败点
- ✅ Actions 失败重试机制

---

### 风险 4: 性能问题

**风险**: 数据量大导致加载慢、查询慢

**概率**: 低（单文件策略下）  
**影响**: 中

**应对策略**:
- ✅ 阶段性测试性能
- ✅ 100 条、1000 条、1 万条分别测试
- ✅ 超过阈值立即拆分文件
- ✅ 添加内存索引优化

---

## 📅 时间规划

### Week 1: Web API 开发

```
Mon (Day 1)  - FastAPI 应用开发       ████████░░  2-3 小时
Tue (Day 2)  - Docker 化              ████████░░  2-3 小时
Wed (Day 3)  - GitHub Actions + 文档  ████████░░  2-3 小时

里程碑 1: MVP 完成 ✅
```

### Week 2: 同步功能开发

```
Thu (Day 4)  - SNOMED 同步模块        ████████████  4 小时
Fri (Day 5)  - 数据合并模块           ████████████  4 小时
Mon (Day 6)  - API 集成              ████████░░    3 小时
Tue (Day 7)  - 定时任务 + 测试        ████████░░    3 小时

里程碑 2: 完整功能 ✅
```

**总工作量**: 约 20-25 小时，分 7 个工作日完成

---

## 📖 参考资料

### 外部 API 文档

1. **SNOMED CT Snowstorm API**
   - URL: https://browser.ihtsdotools.org/snowstorm/snomed-ct
   - 文档: https://github.com/IHTSDO/snowstorm/blob/master/docs/using-the-api.md

2. **UMLS Terminology Services**
   - URL: https://uts.nlm.nih.gov/uts/
   - 文档: https://documentation.uts.nlm.nih.gov/rest/home.html

3. **FastAPI 文档**
   - 官网: https://fastapi.tiangolo.com/
   - 中文: https://fastapi.tiangolo.com/zh/

4. **Docker 文档**
   - 官网: https://docs.docker.com/
   - GHCR: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

---

## 🔄 迭代计划

### v1.0.0（当前计划）

- ✅ Web API 基础功能
- ✅ Docker 部署
- ✅ SNOMED CT 自动同步
- ✅ 单文件存储

### v1.1.0（未来 2 周）

- ⚪ ICD-10 同步
- ⚪ LOINC 同步
- ⚪ 同步日志 Web 界面
- ⚪ 监控和告警

### v2.0.0（未来 1 月）

- ⚪ 多文件存储（如需要）
- ⚪ 增量同步
- ⚪ 编码映射转换
- ⚪ 多语言支持

### v3.0.0（未来 3 月）

- ⚪ 用户认证
- ⚪ 访问控制
- ⚪ API 使用统计
- ⚪ 数据版本管理

---

## ✅ 下一步行动

### 立即开始（今天）

1. **创建 app.py**
   ```bash
   # 在项目根目录
   touch app.py
   ```

2. **更新 requirements.txt**
   ```bash
   echo "fastapi>=0.104.0" >> requirements.txt
   echo "uvicorn[standard]>=0.24.0" >> requirements.txt
   ```

3. **开始编码**
   - 参考本文档 Day 1 检查清单
   - 预计 2-3 小时完成

---

## 📝 变更记录

| 日期 | 版本 | 变更内容 |
|-----|------|---------|
| 2025-01-13 | 1.0 | 初始版本，确定整体框架和两阶段计划 |

---

## 👥 团队信息

**项目负责人**: hhtbing-wisefido  
**仓库**: WiseFido_TDPv1_Coding_Dictionary  
**分支策略**: main（主分支）

---

**文档状态**: ✅ 已确认  
**下次更新**: 阶段 1 完成后（预计 Day 3）

---

*本文档作为项目实施的核心指导文件，任何重大变更需更新此文档。*
