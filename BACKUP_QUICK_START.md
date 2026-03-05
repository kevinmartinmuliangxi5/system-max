# Python文件备份工具 - 快速开始指南

## 1分钟快速上手

### Windows用户（最简单）

```
1. 双击 backup.bat
2. 等待备份完成
3. 查看 backup 文件夹
```

### 命令行用户

```bash
python backup_py_files.py
```

## 文件说明

### 必需文件
- `backup_py_files.py` - 主程序（必须）

### 可选文件
- `backup.bat` - Windows快速启动脚本
- `test_backup.py` - 测试验证脚本

### 文档文件
- `BACKUP_README.md` - 完整说明文档
- `backup_usage.md` - 详细使用手册
- `BACKUP_PROJECT_SUMMARY.md` - 项目技术总结
- `BACKUP_QUICK_START.md` - 本文件

## 常用命令

```bash
# 备份当前目录
python backup_py_files.py

# 备份指定目录
python backup_py_files.py -s D:\MyProject

# 自定义备份文件夹名称
python backup_py_files.py -b my_backups

# 查看帮助
python backup_py_files.py -h

# 运行测试
python test_backup.py
```

## 输出位置

```
当前目录/
├── backup/                          # 备份文件夹
│   └── backup_20260203_154154/     # 带时间戳的备份
│       ├── backup_summary.txt      # 备份摘要
│       └── [所有.py文件]           # 保持原目录结构
└── backup_20260203_154154.log      # 日志文件
```

## 功能特点

- ✅ 自动备份所有.py文件
- ✅ 递归扫描子目录
- ✅ 保持目录结构
- ✅ 时间戳命名
- ✅ 详细日志记录
- ✅ 自动生成摘要

## 系统要求

- Python 3.6+
- 仅使用标准库，无需额外安装

## 常见问题

**Q: 如何只备份特定文件夹？**
```bash
python backup_py_files.py -s ./specific_folder
```

**Q: 备份在哪里？**
```
在源目录下的 backup 文件夹中
```

**Q: 如何自动定期备份？**
```
Windows: 使用任务计划程序
Linux: 使用 cron
```

## 需要帮助？

查看详细文档：
- `BACKUP_README.md` - 完整功能说明
- `backup_usage.md` - 详细使用指南

---

**开始使用**: 直接运行 `python backup_py_files.py` 或双击 `backup.bat`
