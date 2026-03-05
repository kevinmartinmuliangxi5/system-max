PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- 1) 会话表
CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL CHECK (length(trim(title)) > 0),
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  archived_at INTEGER
);

-- 2) 消息表（支持文本、图像、mask）
CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  parent_message_id TEXT,
  role TEXT NOT NULL CHECK (role IN ('system', 'user', 'assistant')),
  text TEXT,
  image_uri TEXT,
  mask_uri TEXT,
  model TEXT,
  status TEXT NOT NULL CHECK (status IN ('pending', 'running', 'succeeded', 'failed', 'cancelled')),
  error_code TEXT,
  width INTEGER CHECK (width IS NULL OR width > 0),
  height INTEGER CHECK (height IS NULL OR height > 0),
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
  FOREIGN KEY (parent_message_id) REFERENCES messages(id) ON DELETE SET NULL,
  CHECK (text IS NOT NULL OR image_uri IS NOT NULL),
  CHECK (
    image_uri IS NULL OR
    image_uri LIKE 'file://%' OR
    image_uri LIKE 'https://%' OR
    image_uri LIKE 'http://%'
  ),
  CHECK (mask_uri IS NULL OR mask_uri LIKE 'file://%')
);

-- 3) 请求日志（用于成本、耗时、状态码追踪）
CREATE TABLE IF NOT EXISTS request_logs (
  id TEXT PRIMARY KEY,
  conversation_id TEXT,
  message_id TEXT,
  request_type TEXT NOT NULL CHECK (request_type IN ('prompt_enhance', 'image_generation', 'image_edit')),
  provider TEXT NOT NULL DEFAULT 'siliconflow',
  model TEXT,
  request_id TEXT,
  status_code INTEGER,
  retry_count INTEGER NOT NULL DEFAULT 0 CHECK (retry_count >= 0),
  duration_ms INTEGER NOT NULL CHECK (duration_ms >= 0),
  cost_estimate REAL NOT NULL DEFAULT 0 CHECK (cost_estimate >= 0),
  success INTEGER NOT NULL CHECK (success IN (0, 1)),
  error_code TEXT,
  created_at INTEGER NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE SET NULL
);

-- 4) 失败回放日志（只存脱敏摘要）
CREATE TABLE IF NOT EXISTS replay_logs (
  id TEXT PRIMARY KEY,
  request_log_id TEXT,
  request_type TEXT NOT NULL CHECK (request_type IN ('prompt_enhance', 'image_generation', 'image_edit')),
  masked_prompt TEXT NOT NULL,
  error_code TEXT NOT NULL,
  status_code INTEGER,
  created_at INTEGER NOT NULL,
  FOREIGN KEY (request_log_id) REFERENCES request_logs(id) ON DELETE SET NULL
);

-- 索引：查询热点 + 清理策略
CREATE INDEX IF NOT EXISTS idx_conversations_updated_at
  ON conversations(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_created
  ON messages(conversation_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_messages_parent
  ON messages(parent_message_id);

CREATE INDEX IF NOT EXISTS idx_messages_status
  ON messages(status);

CREATE INDEX IF NOT EXISTS idx_request_logs_created
  ON request_logs(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_request_logs_type_created
  ON request_logs(request_type, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_request_logs_message
  ON request_logs(message_id);

CREATE INDEX IF NOT EXISTS idx_replay_logs_created
  ON replay_logs(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_replay_logs_type_created
  ON replay_logs(request_type, created_at DESC);

COMMIT;
