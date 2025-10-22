-- WebApp 部署服务数据库 Schema

-- API Keys 表
CREATE TABLE IF NOT EXISTS api_keys (
    key_id TEXT PRIMARY KEY,
    key_hash TEXT NOT NULL,
    key_name TEXT NOT NULL,
    created_by TEXT,
    created_at INTEGER NOT NULL,
    expires_at INTEGER,
    is_active INTEGER DEFAULT 1,
    usage_count INTEGER DEFAULT 0,
    max_pages INTEGER DEFAULT 100,
    permissions TEXT DEFAULT 'create,view',
    metadata TEXT
);

-- Pages 表
CREATE TABLE IF NOT EXISTS pages (
    page_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    html_content TEXT NOT NULL,
    created_by TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    expires_at INTEGER,
    access_count INTEGER DEFAULT 0,
    last_accessed INTEGER,
    is_active INTEGER DEFAULT 1,
    metadata TEXT
);

-- Access Logs 表（可选，用于审计）
CREATE TABLE IF NOT EXISTS access_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id TEXT NOT NULL,
    accessed_at INTEGER NOT NULL,
    ip_address TEXT,
    user_agent TEXT
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_pages_created_by ON pages(created_by);
CREATE INDEX IF NOT EXISTS idx_pages_expires_at ON pages(expires_at);
CREATE INDEX IF NOT EXISTS idx_pages_is_active ON pages(is_active);
CREATE INDEX IF NOT EXISTS idx_api_keys_is_active ON api_keys(is_active);
CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash);

