/**
 * Example component created by the /create-component skill
 *
 * 这是一个使用 Framer Motion 和 Tailwind CSS 的示例组件
 * 展示了 Skill 生成代码的规范和风格
 */

import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

// ============================================
// 类型定义
// ============================================

export interface ZenGardenCardProps {
  /** 卡片标题 */
  title: string
  /** 卡片描述 */
  description?: string
  /** 是否显示动画 */
  animated?: boolean
  /** 点击回调 */
  onClick?: () => void
  /** 自定义类名 */
  className?: string
  /** 子元素 */
  children?: React.ReactNode
}

// ============================================
// 组件实现
// ============================================

/**
 * ZenGarden 卡片组件
 *
 * @example
 * ```tsx
 * <ZenGardenCard
 *   title="示例标题"
 *   description="这是一段描述文字"
 *   animated
 *   onClick={() => console.log('clicked')}
 * />
 * ```
 */
export const ZenGardenCard: React.FC<ZenGardenCardProps> = ({
  title,
  description,
  animated = true,
  onClick,
  className,
  children,
}) => {
  // 动画配置
  const motionProps = animated ? {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.3, ease: 'easeOut' }
  } : {}

  return (
    <motion.div
      {...motionProps}
      onClick={onClick}
      className={cn(
        // 基础样式
        'bg-white dark:bg-gray-800 rounded-lg shadow-md p-6',
        // 响应式
        'w-full max-w-md',
        // 交互状态
        onClick && 'cursor-pointer hover:shadow-lg transition-shadow',
        // 自定义类名
        className
      )}
    >
      {/* 标题 */}
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>

      {/* 描述 */}
      {description && (
        <p className="text-gray-600 dark:text-gray-300 text-sm">
          {description}
        </p>
      )}

      {/* 子元素 */}
      {children && (
        <div className="mt-4">
          {children}
        </div>
      )}
    </motion.div>
  )
}

// ============================================
// 导出
// ============================================

export default ZenGardenCard
