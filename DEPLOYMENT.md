# WebApp 快速部署插件 - 部署指南

> 完整的 Cloudflare Workers 部署步骤和配置说明

## 📋 目录

- [前置要求](#前置要求)
- [部署步骤](#部署步骤)
- [配置说明](#配置说明)
- [密钥管理](#密钥管理)
- [高级配置](#高级配置)
- [故障排除](#故障排除)

---

## 🔧 前置要求

### 必需账号

- ✅ [Cloudflare 账号](https://dash.cloudflare.com/sign-up) - 免费，无需信用卡
- ✅ [GitHub 账号](https://github.com) - 用于代码托管和自动部署

### 推荐工具（可选）

- `wrangler` CLI - Cloudflare Workers 命令行工具
- `pnpm` - 快速的包管理器
- Node.js >= 18.0.0 - 用于本地开发测试

---

## 🚀 部署步骤

### 第一步：Fork 仓库

1. 访问项目 GitHub 页面：[nekro-plugin-webapp](https://github.com/KroMiose/nekro-plugin-webapp)
2. 点击页面右上角的 **Fork** 按钮
3. 选择你的账号，点击 **Create fork**
4. 等待 fork 完成（通常几秒钟）

✅ **检查点**：你的 GitHub 账号下现在有一个 `nekro-plugin-webapp` 仓库

---

### 第二步：创建 D1 数据库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 在左侧菜单选择 **Workers & Pages** → **D1**
3. 点击 **Create database** 按钮
4. 填写数据库名称：`nekro-webapp-db`（或其他你喜欢的名称）
5. 点击 **Create** 创建数据库
6. 创建成功后，在数据库详情页面找到 **Database ID**
7. **复制这个 Database ID**（格式如：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

✅ **检查点**：已获得 Database ID

---

### 第三步：配置 Database ID

1. 在你 fork 的 GitHub 仓库中，打开 `worker/wrangler.toml` 文件
2. 找到 `[[d1_databases]]` 部分：
   ```toml
   [[d1_databases]]
   binding = "DB"
   database_name = "webapp-db"
   database_id = "2fc7f7a6-3370-4430-9093-e907cb68f761"  # 请替换为你的 Database ID
   ```
3. 点击文件编辑按钮（铅笔图标）
4. **将示例 Database ID 替换为你刚才复制的实际 Database ID**
5. 提交更改：
   - Commit message: `chore: update database id`
   - 点击 **Commit changes**

✅ **检查点**：`wrangler.toml` 中已填写你的 Database ID

---

### 第四步：初始化数据库表结构

1. 回到 Cloudflare Dashboard 的 D1 数据库页面
2. 点击你刚创建的数据库进入详情页
3. 点击顶部的 **Console** 标签
4. 在你的 GitHub 仓库中打开 `worker/schema.sql` 文件
5. 复制所有 SQL 内容（4 个表 + 索引）
6. 粘贴到 D1 Console 的输入框中
7. 点击 **Execute** 按钮执行 SQL

执行成功后，你应该看到类似以下的输出：
```
Query succeeded: 4 rows affected
```

✅ **检查点**：数据库表已创建（settings, api_keys, pages, access_logs）

---

### 第五步：连接 GitHub 部署 Worker

1. 在 Cloudflare Dashboard 左侧菜单选择 **Workers & Pages**
2. 点击 **Create application** 按钮
3. 选择 **Pages** 标签
4. 点击 **Connect to Git** 按钮
5. 如果是首次使用，需要授权 Cloudflare 访问你的 GitHub
6. 在仓库列表中选择你 fork 的 `nekro-plugin-webapp` 仓库
7. 点击 **Begin setup** 开始配置

**重要配置项：**

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **Project name** | `nekro-webapp`（或自定义） | 项目名称，会成为域名的一部分 |
| **Production branch** | `main` | 生产环境分支 |
| **Framework preset** | `None` | 不使用框架预设 |
| **Build command** | `pnpm run build` | ⚠️ 必填！ |
| **Build output directory** | 留空 | 不需要填写 |
| **Root directory** | `/worker` | ⚠️ 必填！指向 worker 子目录 |

8. 配置完成后，点击 **Save and Deploy** 按钮

⏱️ **等待构建**：Cloudflare 会自动构建和部署，通常需要 2-3 分钟。

✅ **完成**：部署成功后，你将获得 Worker URL（格式如：`https://nekro-webapp.pages.dev`）

---

### 第六步：验证部署

1. 复制你的 Worker URL
2. 在浏览器中访问这个 URL
3. 首次访问时，数据库会**自动初始化**（包括创建 settings 表等）
4. 你应该看到一个欢迎页面，显示 "WebApp 快速部署服务"

**检查健康状态：**
```bash
curl https://your-worker.pages.dev/api/health
# 应该返回: {"status":"healthy","timestamp":...,"initialized":false}
```

✅ **完成**！Worker 现在可以使用了

---

### 第七步：设置管理密钥

1. 打开 NekroAgent
2. 进入插件管理页面
3. 找到 **WebApp 快速部署** 插件
4. 填写配置：
   - **WORKER_URL**: 你的 Worker URL（如：`https://nekro-webapp.pages.dev`）
   - **ACCESS_KEY**: 暂时留空（稍后填写）
5. 保存配置

6. 访问管理界面：`http://localhost:8021/plugins/KroMiose.nekro_plugin_webapp/`

7. 首次访问会提示设置管理密钥：
   - 输入一个强密钥（至少 8 个字符）
   - 建议使用随机字符串，如：`Admin@2024!Secure`
   - 点击"设置管理密钥"按钮

8. 设置成功后，系统会自动使用管理密钥登录进入管理界面

✅ **完成**！管理密钥已设置

---

### 第八步：创建访问密钥

**为什么需要访问密钥？**
- 管理密钥权限过大，不应用于日常操作
- 访问密钥专门用于创建页面，权限受限，更安全
- 符合最小权限原则

**创建步骤：**

1. 在管理界面中，点击"密钥管理"标签
2. 点击"创建访问密钥"按钮
3. 输入密钥名称，如：`nekro-agent-access`
4. 点击"创建"按钮
5. **重要**：复制生成的访问密钥（只显示这一次！）

6. 回到 NekroAgent 插件配置页面
7. 填写 **ACCESS_KEY**：粘贴刚才复制的访问密钥
8. 保存配置

✅ **配置完成**！现在 AI 可以自动部署网页了

---

### 第九步：测试部署

让 AI 帮你创建第一个网页：

```
你：帮我创建一个简单的 Hello World 网页

AI：好的，我来创建一个 Hello World 页面。
[AI 调用 create_web_app]

返回：
✅ 网页部署成功！
📄 标题: Hello World
🔗 访问链接: https://your-worker.pages.dev/abc12345
🆔 页面ID: abc12345
⏰ 创建时间: 2025-10-22 15:30:00
📅 过期时间: 2025-11-21 15:30:00
```

点击链接，应该能看到你的网页！

✅ **大功告成**！🎉

---

## ⚙️ 配置说明

### 环境变量

在 `wrangler.toml` 中配置的环境变量：

```toml
[vars]
DB_INITIALIZED = "false"  # 数据库初始化标志
```

### 数据库绑定

```toml
[[d1_databases]]
binding = "DB"                    # 绑定名称（代码中使用）
database_name = "webapp-db"       # 数据库逻辑名称
database_id = "your-database-id"  # 实际的数据库 ID
```

### 构建配置

Worker 使用 TypeScript 编写，通过 `esbuild` 构建：

```json
{
  "scripts": {
    "build": "esbuild src/index.ts --bundle --format=esm --outfile=_worker.js --platform=browser --target=esnext"
  }
}
```

---

## 🔐 密钥管理

### 密钥类型对比

| 特性 | 管理密钥 | 访问密钥 |
|------|---------|---------|
| **用途** | 管理系统 | 创建页面 |
| **权限** | manage（完全权限） | create, view |
| **能创建页面** | ❌ 不能 | ✅ 能 |
| **能管理密钥** | ✅ 能 | ❌ 不能 |
| **能删除页面** | ✅ 能 | ❌ 不能 |
| **存储位置** | settings 表 | api_keys 表 |
| **设置方式** | 首次访问管理界面 | 管理界面创建 |

### 密钥权限详解

**管理密钥（Admin Key）**：
- 权限：`manage`（包含所有权限）
- 可以做：
  - ✅ 创建/删除访问密钥
  - ✅ 查看所有页面列表
  - ✅ 删除任何页面
  - ✅ 查看统计信息
  - ✅ 修改管理密钥
- 不能做：
  - ❌ 创建页面（权限分离设计）

**访问密钥（Access Key）**：
- 权限：`create, view`
- 可以做：
  - ✅ 创建页面
  - ✅ 查看单个页面信息
- 不能做：
  - ❌ 查看所有页面列表
  - ❌ 删除页面
  - ❌ 管理密钥

### 修改管理密钥

1. 使用旧管理密钥登录管理界面
2. 进入"系统管理"标签
3. 点击"修改管理密钥"
4. 输入旧密钥和新密钥
5. 确认修改

**注意**：修改后需要用新密钥重新登录。

---

## 🔧 高级配置

### 自定义域名

1. 在 Cloudflare Dashboard 中进入你的 Pages 项目
2. 选择 **Custom domains** 标签
3. 点击 **Add a custom domain**
4. 输入你的域名（域名需要在 Cloudflare 托管）
5. 完成 DNS 配置
6. 更新插件配置中的 `WORKER_URL` 为你的自定义域名

### 定期清理过期页面

Worker 会在每次访问时自动检查并标记过期页面为不活跃状态。

如果需要彻底删除过期数据，可以在 D1 Console 中运行：

```sql
-- 删除过期且已停用的页面
DELETE FROM pages
WHERE is_active = 0
  AND expires_at < CAST((julianday('now') - 2440587.5) * 86400000 AS INTEGER);
```

### 启用访问日志

访问日志表 `access_logs` 默认已创建，但未启用。

如需启用，修改 `worker/src/storage.ts` 中的 `incrementAccessCount` 函数：

```typescript
export async function incrementAccessCount(pageId: string, env: Env): Promise<void> {
  const now = Date.now();
  
  // 更新访问计数
  await env.DB.prepare(`
    UPDATE pages 
    SET access_count = access_count + 1, last_accessed = ?
    WHERE page_id = ?
  `)
    .bind(now, pageId)
    .run();
  
  // 记录访问日志（新增）
  await env.DB.prepare(`
    INSERT INTO access_logs (page_id, accessed_at)
    VALUES (?, ?)
  `)
    .bind(pageId, now)
    .run();
}
```

---

## 🛠️ 故障排除

### Worker 部署失败

**症状**：构建过程中出现错误

**可能原因**：
1. 未设置正确的 Build command
2. Root directory 未设置为 `/worker`
3. Database ID 未替换

**解决方案**：
1. 检查 Pages 项目的构建设置
2. 确认 Build command 为 `pnpm run build`
3. 确认 Root directory 为 `/worker`
4. 重新部署：Settings → Builds & deployments → Retry deployment

### 数据库初始化失败

**症状**：访问 Worker 时提示 "no such table: settings"

**原因**：数据库表结构未正确初始化

**解决方案**：
1. 进入 Cloudflare Dashboard → D1 → 你的数据库
2. 点击 Console 标签
3. 复制 `worker/schema.sql` 的完整内容
4. 粘贴并执行
5. 或使用 wrangler CLI：
   ```bash
   wrangler d1 execute webapp-db --file=worker/schema.sql
   ```

### 管理界面无法访问

**症状**：访问管理界面时提示 404 或无法加载

**可能原因**：
1. WORKER_URL 配置错误
2. Worker 未部署成功
3. 网络连接问题

**解决方案**：
1. 检查 `WORKER_URL` 配置是否正确（不要包含尾部斜杠）
2. 直接在浏览器访问 Worker URL 验证是否可用
3. 检查 `/api/health` 端点是否响应正常
4. 查看 Worker 日志：Dashboard → Pages → your-project → Logs

### 访问密钥创建失败

**症状**：点击"创建访问密钥"后无响应或报错

**可能原因**：
1. 管理密钥验证失败
2. 数据库连接问题
3. api_keys 表不存在

**解决方案**：
1. 退出登录后重新使用管理密钥登录
2. 检查数据库中 api_keys 表是否存在：
   ```sql
   SELECT name FROM sqlite_master WHERE type='table' AND name='api_keys';
   ```
3. 如果表不存在，重新执行 schema.sql

### AI 创建页面失败（401错误）

**症状**：AI 调用插件时返回 401 Unauthorized

**可能原因**：
1. ACCESS_KEY 未配置或配置错误
2. 访问密钥已被删除
3. 访问密钥过期

**解决方案**：
1. 检查插件配置中的 `ACCESS_KEY` 是否正确
2. 在管理界面查看访问密钥列表，确认密钥存在且活跃
3. 重新创建访问密钥并更新配置
4. 重启 NekroAgent 使配置生效

### 时间显示错误（年份异常）

**症状**：页面创建时间显示为遥远的未来（如 57778 年）

**原因**：时间戳单位转换错误

**解决方案**：
- 已在最新版本修复
- 如果仍有问题，确保使用最新版本的插件代码
- JavaScript 返回毫秒级时间戳，Python 需要除以 1000

---

## 📊 资源限制

### Cloudflare 免费计划

| 资源 | 限制 |
|------|------|
| D1 存储 | 10 GB |
| 每天读取 | 500 万次 |
| 每天写入 | 10 万次 |
| Worker 请求 | 每天 10 万次 |
| Worker 执行时间 | 每次 50ms (免费) |

### 推荐配置

| 场景 | PAGE_EXPIRE_DAYS | MAX_HTML_SIZE |
|------|------------------|---------------|
| 临时展示 | 7 天 | 300 KB |
| 一般使用 | 30 天 | 500 KB |
| 长期保存 | 0（永久） | 500 KB |
| 大型页面 | 30 天 | 1000 KB |

---

## 🔄 更新部署

### 自动更新（推荐）

1. 在 GitHub 仓库中同步上游更新：
   ```bash
   git remote add upstream https://github.com/KroMiose/nekro-plugin-webapp.git
   git fetch upstream
   git merge upstream/main
   git push origin main
   ```

2. Cloudflare Pages 会自动检测到更改并重新部署

### 手动更新

1. 登录 Cloudflare Dashboard
2. 进入你的 Pages 项目
3. 选择 **Deployments** 标签
4. 点击 **Retry deployment** 重新部署最新代码

---

## 📞 获取帮助

如果遇到问题：

1. 📖 查阅本文档的故障排除部分
2. 🔍 在 [Issues](https://github.com/KroMiose/nekro-plugin-webapp/issues) 中搜索类似问题
3. 🐛 [创建新 Issue](https://github.com/KroMiose/nekro-plugin-webapp/issues/new) 描述你的问题
4. 💬 加入社区讨论

---

## 📚 相关链接

- [README.md](./README.md) - 用户使用指南
- [DEVELOPMENT.md](./DEVELOPMENT.md) - 开发者文档
- [Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)
- [D1 数据库文档](https://developers.cloudflare.com/d1/)
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)

---

**最后更新**: 2025-10-22  
**维护者**: NekroAgent Team

