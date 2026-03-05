# Ralph 代理指令

## 构建命令

```bash
# 根据项目类型自动检测的构建命令
# TypeScript/JavaScript
npm run build

# Python
python -m build

# Rust
cargo build --release

# Go
go build ./...
```

## 测试命令

```bash
# 根据项目类型自动检测的测试命令
# TypeScript/JavaScript
npm test

# Python
pytest

# Rust
cargo test

# Go
go test ./...
```

## 运行命令

```bash
# 根据项目类型自动检测的运行命令
# TypeScript/JavaScript
npm run dev

# Python
python main.py

# Rust
cargo run

# Go
go run main.go
```

## 项目自动维护说明

此文件由 Ralph 自动维护，包含项目的构建、测试和运行命令。Ralph 将根据项目类型自动检测和更新这些命令。

## 工具使用权限

Ralph 被允许使用以下工具：
- `Write` - 创建新文件
- `Read` - 读取文件内容
- `Edit` - 编辑现有文件
- `Bash(git *)` - Git 命令
- `Bash(npm *)` - NPM 命令
- `Bash(pytest)` - pytest 命令
