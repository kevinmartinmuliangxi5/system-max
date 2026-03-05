# 系统架构图（Mermaid）

```mermaid
flowchart TB
  %% ========== Frontend Layer ==========
  subgraph FE[前端层 Mobile App (Expo + React Native)]
    UI[UI 页面层\n对话页/编辑页/结果页]
    STATE[状态管理\nZustand]
    EDITOR[图像编辑引擎\nSkia + Gesture + Reanimated]
  end

  %% ========== API Layer ==========
  subgraph API[API 层]
    CLIENT[API Client\nAxios]
    RETRY[重试与超时拦截\n429/503 指数退避]
    AUTH[认证注入\nBearer BYOK Key]
    CONTRACT[响应契约校验\nZod/JSON Schema]
  end

  %% ========== Business Logic Layer ==========
  subgraph BL[业务逻辑层]
    ORCH[生成编排\nPrompt增强/文生图/图生图/局部重绘]
    FILEPIPE[文件管道\nBase64 短驻留 -> 落盘 file://]
    ERRFLOW[错误恢复\n统一错误映射与重试策略]
    COST[可观测性\n成本日志 + 失败回放]
    EXPORT[导出与合规\nAIGC 标识 + EXIF 写入]
  end

  %% ========== Data Layer ==========
  subgraph DATA[数据层（本地）]
    SQLITE[(SQLite\nconversations/messages/request_logs/replay_logs)]
    FS[(File System\n图片与 mask 文件)]
    SECURE[(Secure Store\n用户 API Key)]
    MMKV[(MMKV\n轻量配置)]
  end

  %% ========== External Services ==========
  subgraph EXT[外部服务]
    SFCHAT[SiliconFlow\n/v1/chat/completions]
    SFIMG[SiliconFlow\n/v1/images/generations]
    ALBUM[系统相册\nMedia Library]
  end

  %% Frontend internal flow
  UI --> STATE
  UI --> EDITOR

  %% FE -> API
  STATE --> CLIENT
  EDITOR --> ORCH
  UI --> ORCH

  %% API pipeline
  CLIENT --> AUTH
  AUTH --> RETRY
  RETRY --> CONTRACT

  %% API -> External
  CONTRACT --> SFCHAT
  CONTRACT --> SFIMG

  %% External -> Business
  SFCHAT --> ORCH
  SFIMG --> FILEPIPE

  %% Business -> Data
  FILEPIPE --> FS
  ORCH --> SQLITE
  ERRFLOW --> SQLITE
  COST --> SQLITE
  AUTH -.读取/更新.-> SECURE
  STATE --> MMKV

  %% Business internal
  ORCH --> ERRFLOW
  ORCH --> COST
  FILEPIPE --> ORCH
  ORCH --> EXPORT

  %% Export
  EXPORT --> ALBUM
  EXPORT --> FS
```

