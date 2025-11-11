# 快速恢复指南

## 🎯 里程碑: v1.2.3-milestone

**提交哈希**: `c20b54a`  
**标签**: `v1.2.3-milestone`  
**日期**: 2025-11-11

---

## 🚀 三种恢复方法

### 方法 1: 使用标签（最简单）
```bash
# 切换到里程碑版本
git checkout v1.2.3-milestone

# 基于里程碑创建新功能分支
git checkout -b feature/new-coding-terms v1.2.3-milestone
```

### 方法 2: 使用提交哈希
```bash
# 查看历史
git log --oneline --all

# 恢复到指定提交
git checkout c20b54a

# 创建新分支
git checkout -b backup-v1.2.3
```

### 方法 3: 从 GitHub 下载
```bash
# 下载特定标签的压缩包
https://github.com/hhtbing-wisefido/WiseFido_TDPv1_Coding_Dictionary/archive/refs/tags/v1.2.3-milestone.zip

# 或使用 git clone
git clone --branch v1.2.3-milestone https://github.com/hhtbing-wisefido/WiseFido_TDPv1_Coding_Dictionary.git
```

---

## 🔍 验证完整性

```bash
# 进入项目目录
cd WiseFido_TDPv1_Coding_Dictionary

# 激活虚拟环境（如果有）
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/macOS

# 运行测试
python scripts/dic_tools.py --test

# 查看统计
python scripts/dic_tools.py --stats

# 输出应显示：
# ✅ 总词条数: 34
# ✅ 所有测试通过
```

---

## 📊 里程碑状态快照

| 项目 | 数值 |
|------|------|
| 总词条数 | 34 |
| SNOMED CT | 15 (44.1%) |
| Internal | 13 (38.2%) |
| TDP | 6 (17.6%) |
| 分类数 | 6 |
| 测试通过率 | 100% |

---

## ⚠️ 重要提示

1. **不要直接修改标签对应的提交** - 标签应该是不可变的
2. **扩展词条时创建新分支** - 例如 `feature/expand-v1.3`
3. **保持主分支稳定** - 合并前必须通过所有测试
4. **定期备份** - 在重大更新前创建新里程碑

---

## 📝 相关文档

- 完整说明: `MILESTONE_v1.2.3.md`
- 项目文档: `README.md`
- 变更日志: `auto_generated/changelog.md`

---

**最后更新**: 2025-11-11
