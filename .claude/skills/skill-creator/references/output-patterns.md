# Output Patterns Reference

技能输出模式的参考指南，帮助创建一致且高质量的输出。

## 通用输出模式

### 1. 文件创建模式

```
## Files Created

- `src/components/ComponentName.tsx` - 组件主文件
- `src/components/ComponentName.types.ts` - 类型定义
- `src/components/ComponentName.test.tsx` - 测试文件
```

### 2. 代码模板模式

**React 组件模板：**
```tsx
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface ComponentNameProps {
  // Props 定义
}

export const ComponentName: React.FC<ComponentNameProps> = ({ }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(/* base classes */)}
    >
      {/* 内容 */}
    </motion.div>
  )
}
```

### 3. 步骤执行模式

```
## 执行步骤

1. ✅ 第一步完成
2. ⏳ 正在执行第二步
3. ⏸️ 待执行：第三步
```

### 4. 验证确认模式

```
## 验证检查

- [ ] 检查项 1
- [ ] 检查项 2
- [x] 已完成的检查项
```

### 5. 错误处理模式

```
## 问题与解决

| 问题 | 解决方案 |
|------|----------|
| 错误描述 | 解决方法 |
```

## ZenGarden 特定模式

### 组件生成输出

```
## 🎋 组件创建完成

**组件名称：** ComponentName
**位置：** src/components/ComponentName/

### 创建的文件
- `index.tsx` - 主组件（256 行）
- `types.ts` - TypeScript 接口
- `styles.ts` - 样式常量

### 使用方式
\`\`\`tsx
import { ComponentName } from '@/components/ComponentName'
\`\`\`

### 设计系统遵循
- ✅ 禅意绿 (#4A9470) 主色
- ✅ Noto Sans SC 字体
- ✅ Framer Motion 动画
- ✅ 响应式设计
```

### Skill 创建输出

```
## ✅ Skill 创建成功

**Skill 名称：** skill-name
**位置：** .claude/skills/skill-name/

### 目录结构
\`\`\`
skill-name/
├── SKILL.md (245 行)
├── scripts/
│   └── helper.py
└── references/
    └── api.md
\`\`\`

### 下一步
1. 测试 skill：`/skill-name [参数]`
2. 验证功能
3. 根据需要迭代
```

## 输出质量标准

### 清晰性
- 使用表格和列表组织信息
- 添加表情符号增强可读性
- 重要信息使用加粗

### 完整性
- 包含所有创建的文件路径
- 提供使用示例
- 说明下一步操作

### 一致性
- 使用相同的格式术语
- 遵循项目命名约定
- 保持风格统一
