# Python文件自动备份工具

## 简介

这是一个功能完善、易于使用的Python文件自动备份脚本，可以自动备份指定目录下的所有`.py`文件到带时间戳的备份文件夹中。

## 文件说明

- **backup_py_files.py** - 主程序脚本
- **backup.bat** - Windows快速启动脚本（双击运行）
- **backup_usage.md** - 详细使用说明文档

## 快速开始

### Windows用户

双击 `backup.bat` 即可开始备份当前目录的所有Python文件。

### 命令行用户

```bash
python backup_py_files.py
```

## 核心特性

### 1. 自动化备份
- 递归扫描指定目录下的所有`.py`文件
- 自动创建带时间戳的备份文件夹
- 保持原有的目录结构

### 2. 时间戳命名
备份文件夹格式：`backup_YYYYMMDD_HHMMSS`
- 示例：`backup_20260203_154154`

### 3. 完善的日志系统
- 实时控制台输出
- 详细的日志文件（backup_YYYYMMDD_HHMMSS.log）
- 自动生成备份摘要文件

### 4. 异常处理
- 捕获并记录所有可能的错误
- 备份失败时继续处理其他文件
- 友好的错误提示信息

### 5. 灵活配置
- 支持自定义源目录
- 支持自定义备份文件夹名称
- 完整的命令行参数支持

## 使用示例

### 基本用法

```bash
# 备份当前目录
python backup_py_files.py

# 备份指定目录
python backup_py_files.py -s /path/to/your/project

# 自定义备份文件夹名称
python backup_py_files.py -b my_backups
```

### 高级用法

```bash
# 备份指定目录到自定义文件夹
python backup_py_files.py -s D:\Projects\MyApp -b archives

# 查看帮助
python backup_py_files.py -h
```

## 输出说明

### 备份目录结构

```
backup/
└── backup_20260203_154154/
    ├── backup_summary.txt      # 备份摘要
    ├── script1.py              # 备份的Python文件
    ├── script2.py
    └── subfolder/              # 保持原有目录结构
        └── script3.py
```

### 备份摘要内容

```
============================================================
Python文件备份摘要
============================================================

备份时间: 2026-02-03 15:41:54
源目录: D:\AI_Projects\system-max
备份目录: D:\AI_Projects\system-max\backup\backup_20260203_154154

成功备份: 68 个文件
失败: 0 个文件
总大小: 1396.54 KB (1430053 bytes)

============================================================
```

## 代码特点

### 1. 面向对象设计
```python
class PyFileBackup:
    """Python文件备份工具类"""
    def __init__(self, source_dir=".", backup_dir="backup"):
        # 初始化配置

    def run(self):
        # 执行备份
```

### 2. 类型注解
增强代码可读性和IDE支持：
```python
def find_py_files(self) -> List[Path]:
    """递归查找所有.py文件"""
```

### 3. 完善的日志
同时输出到文件和控制台：
```python
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(f"backup_{self.timestamp}.log"),
        logging.StreamHandler()
    ]
)
```

### 4. 智能异常处理
```python
try:
    # 执行备份操作
except OSError as e:
    self.logger.error(f"错误信息: {e}")
    raise
```

### 5. 保持目录结构
使用相对路径计算和目录创建：
```python
relative_path = file_path.relative_to(self.source_dir)
dest_path = backup_root / relative_path
dest_path.parent.mkdir(parents=True, exist_ok=True)
```

## 技术实现

### 使用的Python标准库

- **pathlib** - 现代化的路径操作
- **shutil** - 文件复制（保留元数据）
- **datetime** - 时间戳生成
- **logging** - 日志记录
- **argparse** - 命令行参数解析

### 关键实现细节

1. **递归扫描**：使用 `rglob("*.py")` 递归查找所有Python文件
2. **保留元数据**：使用 `shutil.copy2()` 保留修改时间等信息
3. **排除备份目录**：避免重复备份已备份的文件
4. **UTF-8编码**：完美支持中文路径和文件名

## 注意事项

1. 备份目录中的文件不会被再次备份
2. 需要有足够的磁盘空间存储备份
3. 备份操作不会修改或删除原文件
4. 支持中断操作（Ctrl+C）

## 系统要求

- Python 3.6+
- Windows/Linux/macOS

## 退出码说明

| 退出码 | 含义 |
|--------|------|
| 0 | 备份完全成功 |
| 1 | 部分文件备份失败 |
| 2 | 未找到任何Python文件 |
| 130 | 用户中断操作（Ctrl+C）|

## 常见问题

### Q: 如何只备份特定文件夹？
A: 使用 `-s` 参数指定源目录：
```bash
python backup_py_files.py -s ./specific_folder
```

### Q: 备份文件夹占用空间太大怎么办？
A: 可以定期清理旧的备份，保留最近的几个即可。

### Q: 能否备份其他类型的文件？
A: 目前只支持`.py`文件，可以修改代码中的 `rglob("*.py")` 来支持其他扩展名。

### Q: 如何自动化定期备份？
A: 可以配合操作系统的任务计划程序（Windows）或cron（Linux）实现定期自动备份。

## 更新日志

### v1.0.0 (2026-02-03)
- 初始版本发布
- 支持递归备份所有.py文件
- 添加时间戳命名
- 完善的日志和异常处理
- 命令行参数支持
- 自动生成备份摘要

## 许可证

本工具为开源软件，可自由使用和修改。

## 技术支持

如有问题或建议，欢迎反馈。
