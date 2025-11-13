# temp/ 目录说明

此目录存放临时文件，可以随时安全删除。

## 子目录

- `temp/backups/` - 临时备份文件
- `temp/migration/` - 迁移脚本和日志
- `temp/logs/` - 运行日志

## 清理

迁移完成且测试通过后，可以删除：
```bash
rm -rf temp/
```

## Git

此目录已添加到 `.gitignore`，不会提交到版本控制。
