# 🚀 快速参考卡片

> **快速查看实施计划的关键信息**

---

## 📅 时间线

```
Week 1: Web API
├── Day 1: app.py
├── Day 2: Docker
└── Day 3: GHCR ✅ 里程碑 1

Week 2: 同步功能
├── Day 4-5: sync 模块
└── Day 6-7: 集成 ✅ 里程碑 2
```

---

## 📁 新增文件清单

### 阶段 1（本周）
```
✅ app.py
✅ Dockerfile
✅ docker-compose.yml
✅ .dockerignore
✅ .github/workflows/docker-publish.yml
✅ requirements.txt (更新)
```

### 阶段 2（下周）
```
⚪ sync/snomed_sync.py
⚪ sync/data_merger.py
⚪ sync/scheduler.py
⚪ app.py (修改)
```

---

## 🎯 核心决策

| 决策 | 选择 | 理由 |
|-----|------|------|
| **开发顺序** | 先 Web 后同步 | Day 3 就可用 |
| **数据存储** | 单文件 | 简单，易测试 |
| **数据源** | Snowstorm API | 免费，无需注册 |
| **同步频率** | 每月一次 | 避免限流 |

---

## ✅ 验收标准速查

### 阶段 1
```bash
✅ python app.py 可运行
✅ http://localhost:8080/docs 可访问
✅ docker-compose up 成功
✅ docker pull ghcr.io/... 成功
```

### 阶段 2
```bash
✅ python sync/snomed_sync.py 成功
✅ curl -X POST http://localhost:8080/api/sync 可用
✅ 数据量从 79 增加到 1000+
✅ validate_json.py 验证通过
```

---

## 🚨 常见问题

**Q: API 被限流怎么办？**  
A: 已添加 1.2 秒请求间隔，遇到 429 自动重试

**Q: 数据文件会不会太大？**  
A: 先测试，超过 300 MB 再拆分（预计不会）

**Q: Docker 镜像多大？**  
A: 预计 ~200 MB

**Q: 能一键部署吗？**  
A: 是的，`docker run -d -p 8080:8080 ghcr.io/...`

---

## 📞 联系方式

- 仓库: WiseFido_TDPv1_Coding_Dictionary
- 负责人: hhtbing-wisefido
- 详细文档: `docs/IMPLEMENTATION_PLAN.md`

---

**最后更新**: 2025-01-13  
**状态**: 准备就绪，可以开始 Day 1 ✅
