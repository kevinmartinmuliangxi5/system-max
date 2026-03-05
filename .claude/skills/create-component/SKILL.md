---
name: create-component
description: Create React components following ZenGarden project conventions. Use when user asks to create, build, or generate a new component.
argument-hint: [ComponentName] [description]
---

# Create Component Skill

一个用于快速创建符合 ZenGarden 项目规范的 React 组件的 Skill。

## 功能说明

当用户调用此 Skill 时，自动创建一个新的 React 组件，包括：
- TypeScript 组件文件
- 样式文件（如需要）
- 类型定义
- 单元测试框架（可选）
- 使用文档

## 项目技术栈

- React 19.2.0
- TypeScript 5.9.3
- Tailwind CSS v4
- Framer Motion 12.29.2
- Vite 7.2.4

## 组件模板规范

### 1. 目录结构

```
src/components/
├── ComponentName/
│   ├── index.tsx          # 组件主文件
│   ├── types.ts           # 类型定义（可选）
│   ├── styles.ts          # 样式常量（可选）
│   └── ComponentName.test.tsx  # 测试文件（可选）
```

### 2. 组件模板

```tsx
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface ComponentNameProps {
  // 在此定义 Props
}

export const ComponentName: React.FC<ComponentNameProps> = ({ }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="..."
    >
      {/* 组件内容 */}
    </motion.div>
  )
}
```

### 3. 代码规范

- 使用函数组件 + Hooks
- Props 必须定义 TypeScript 接口
- 默认导出命名组件（便于调试）
- 使用 `cn()` 工具函数合并 className
- 组件添加 Framer Motion 动画（如适用）
- 遵循项目现有的命名约定

### 4. 样式规范

- 优先使用 Tailwind CSS 类名
- 复杂样式抽离到 `styles.ts` 常量
- 动画使用 Framer Motion
- 响应式设计：移动优先

## 使用方式

用户只需说：
- "创建一个 [组件名] 组件，用于 [描述功能]"
- "新建组件 [组件名]，包含 [具体需求]"

## 输出示例

当用户说 "创建一个 CanvasToolbar 工具栏组件" 时：

1. 确认组件名称和用途
2. 在 `src/components/CanvasToolbar/` 创建文件
3. 生成符合规范的组件代码
4. 自动导出到 `src/components/index.ts`（如存在）

## 注意事项

- 检查组件是否已存在，避免覆盖
- 确认父目录 `src/components/` 存在
- 遵循项目现有代码风格
- 如组件需要特殊依赖（如图标库），提前告知用户
