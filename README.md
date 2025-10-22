# WebApp 快速部署插件

> 通过 Cloudflare Workers 将 HTML 内容快速部署为在线可访问的网页

## ✨ 功能特性

- 🚀 **AI 一键部署**：通过简单的 API 调用将 HTML 部署为在线网页
- 🔑 **密钥管理**：支持管理员密钥和共享密钥，方便多用户使用
- 🌐 **全球加速**：基于 Cloudflare Workers，享受全球 CDN 加速
- 📊 **可视化管理**：简洁的 Web 管理界面，轻松管理页面和密钥
- 🔒 **安全可靠**：密钥明文存储（简化设计），内容大小限制，访问统计
- 🎯 **零配置部署**：自动初始化数据库，开箱即用

## 📦 快速开始

### 前置要求

- ✅ [Cloudflare 账号](https://dash.cloudflare.com/sign-up)（免费，无需信用卡）
- ✅ [GitHub 账号](https://github.com)

### 🚀 部署步骤（5 分钟完成）

#### 第一步：Fork 仓库

1. 访问此项目的 GitHub 页面
2. 点击页面右上角的 **Fork** 按钮
3. 选择你的账号，点击 **Create fork**
4. 等待 fork 完成（通常几秒钟）

✅ **检查点**：你的 GitHub 账号下现在有一个 `nekro-plugin-webapp` 仓库

#### 第二步：创建 D1 数据库

1. 在 Cloudflare Dashboard 左侧菜单选择 **Workers & Pages** → **D1**
2. 点击 **Create database**
3. 填写数据库名称：`nekro-webapp-db`（或其他名称）
4. 点击 **Create**
5. 创建成功后，在数据库详情页面找到 **Database ID**
6. **复制这个 Database ID**（格式如：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

✅ **检查点**：已获得 Database ID

#### 第三步：填写 Database ID

1. 在你 fork 的 GitHub 仓库中，打开 `worker/wrangler.toml` 文件
2. 找到 [[d1_databases]] 部分：
   ```toml
   database_id = "1469ae3f-62bd-448e-833c-b39703e0b953"  # 请替换为你的 Database ID
   ```
3. 点击编辑（铅笔图标）
4. **将 `1469ae3f-62bd-448e-833c-b39703e0b953` 替换为你刚才复制的 Database ID**
5. 提交更改（Commit changes）

✅ **检查点**：`wrangler.toml` 中已填写你的 Database ID

#### 第四步：初始化数据库表结构

1. 回到 Cloudflare Dashboard 的 D1 数据库页面
2. 点击你刚创建的数据库
3. 点击 **Console** 标签
4. 在你的 GitHub 仓库中打开 `worker/schema.sql` 文件
5. 复制所有 SQL 内容
6. 粘贴到 D1 Console 中
7. 点击 **Execute** 执行

✅ **检查点**：数据库表已创建（应该看到成功信息）

#### 第五步：连接 GitHub 部署 Worker

1. 在 Cloudflare Dashboard 左侧菜单选择 **Workers & Pages**
2. 点击 **Create application** → **Pages** → **Connect to Git**
3. 授权 Cloudflare 访问你的 GitHub（首次使用需要授权）
4. 选择你 fork 的 `nekro-plugin-webapp` 仓库
5. 点击 **Begin setup**
6. **重要配置**：
   - **Project name**: 随意命名（如：`nekro-webapp`）
   - **Production branch**: `main`
   - **Build settings**: 
     - **Framework preset**: 无（None）
     - **Build command**: `pnpm run build` ⚠️ **重要！必须填这个命令**
     - **Build output directory**: 留空
     - **Root directory (根目录)**: `/worker` ⚠️ **重要！必须填 `/worker`**
7. 点击 **Save and Deploy**

⏱️ 等待 2-3 分钟，Cloudflare 会自动构建和部署

✅ **完成**：获得 Worker URL（格式如：`https://nekro-webapp.pages.dev`）

#### 第六步：验证部署

1. 复制你的 Worker URL
2. 在浏览器中访问这个 URL
3. 首次访问时，数据库会**自动初始化**（无需任何操作！）
4. 看到欢迎页面，说明部署成功

✅ **完成**！Worker 现在可以使用了

#### 第七步：配置 NekroAgent 插件

1. 打开 NekroAgent
2. 进入插件配置页面
3. 找到 **WebApp 快速部署** 插件
4. 填写配置：
   - **WORKER_URL**: 粘贴你的 Worker URL
   - 其他保持默认即可
5. 保存配置
6. 访问管理界面：`http://localhost:8021/plugins/KroMiose.nekro_plugin_webapp/`
7. 首次访问会提示设置管理员密钥（至少 8 个字符）

#### 第八步：完成设置

1. 在首次设置界面输入你的管理员密钥
2. 系统会自动初始化并进入管理界面
3. 开始使用！

⚠️ **重要安全提示**：

- 请设置一个强密钥（建议使用随机字符串）
- 妥善保管你的管理员密钥
- 如需修改密钥，在管理界面的"系统管理"中操作

#### 第九步：测试部署

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

## 🎯 使用方法

### AI 自动调用

AI 会自动调用 `create_web_app` 方法部署网页，你只需要描述需求：

**场景 1：创建简单网页**

```
用户：帮我创建一个显示当前时间的网页

AI：我来创建一个显示实时时间的网页...
✅ 部署成功！访问链接：https://...
```

**场景 2：创建交互式工具**

```
用户：做个计算器网页

AI：我来创建一个功能完整的计算器...
✅ 部署成功！访问链接：https://...
```

### 管理界面功能

访问 [管理界面](http://localhost:8021/plugins/KroMiose.nekro_plugin_webapp/) 可以：

- 📊 **查看统计信息**：页面总数、访问次数、密钥数量
- 🔑 **管理 API 密钥**：创建、查看、删除密钥
- 📄 **管理页面**：查看所有部署的页面，一键访问或删除
- 🔧 **密钥管理**：创建和管理 API 密钥，密钥直接可见
- 🔗 **快速访问**：点击页面链接直接跳转

---

## 🔐 密钥管理

### 密钥类型

**管理员密钥（Admin Key）**：

- ✅ 拥有完全权限（创建、查看、删除、管理）
- ✅ 在插件配置中填写
- ✅ 用于管理操作和创建其他密钥
- ⚠️ 不要分享给其他人

**共享密钥（Shared Key）**：

- ✅ 只能创建和查看页面
- ✅ 可以安全分享给其他用户
- ✅ 在管理界面中创建和管理

### 分享给其他用户使用

如果你想让其他人也能使用你的 Worker：

1. 在管理界面创建一个共享密钥
2. 将以下信息提供给其他用户：
   - Worker URL：`https://your-worker.pages.dev`
   - 共享密钥：`shared-key-xxxxx`
3. 其他用户在自己的 NekroAgent 插件配置中填写即可使用

这样你就能轻松与朋友共享部署服务！

---

## ⚙️ 配置说明

| 配置项              | 说明                | 默认值 | 必填 |
| ------------------- | ------------------- | ------ | ---- |
| `WORKER_URL`        | Worker 访问地址     | 无     | ✅   |
| `DEFAULT_SHARE_KEY` | 默认共享密钥        | 空     | ❌   |
| `PAGE_EXPIRE_DAYS`  | 页面过期天数        | 30     | ❌   |
| `MAX_HTML_SIZE`     | HTML 最大大小（KB） | 500    | ❌   |

**说明：**

- `WORKER_URL`：从 Cloudflare Pages 获取的 URL
- `DEFAULT_SHARE_KEY`：留空则需要在管理界面创建 API 密钥供 AI 使用；填写共享密钥可限制 AI 权限
- `PAGE_EXPIRE_DAYS`：设置为 0 表示永久保留
- **管理员密钥**：首次访问管理界面时设置，存储在数据库中

---

## 🔧 高级功能

### 自定义域名

在 Cloudflare Workers 设置中可以绑定自定义域名：

1. 在 Worker 设置中选择 **Triggers** → **Custom Domains**
2. 点击 **Add Custom Domain**
3. 输入你的域名（域名需要在 Cloudflare 托管）
4. 完成 DNS 配置
5. 更新插件配置中的 `WORKER_URL` 为你的自定义域名

### 定期清理过期页面

Worker 会在每次访问时自动检查并标记过期页面为不活跃状态。

如果需要彻底删除过期数据，可以在 D1 Console 中运行：

```sql
-- 删除过期且已停用的页面
DELETE FROM pages
WHERE is_active = 0
  AND expires_at < datetime('now');
```

---

## ❓ 常见问题

<details>
<summary><strong>Q: Worker 部署后无法访问？</strong></summary>

**检查步骤：**

1. Worker 是否部署成功（在 Cloudflare Dashboard 查看部署状态）
2. 访问 `/api/health` 检查 Worker 状态
3. 查看 Worker 日志是否有错误信息
4. 确认浏览器中输入的 URL 正确

**常见原因：**

- 部署尚未完成（等待几分钟）
- URL 输入错误（注意 http vs https）
- 网络连接问题

</details>

<details>
<summary><strong>Q: 提示 401 Unauthorized 错误？</strong></summary>

**可能原因：**

1. 管理员密钥输入错误
2. 使用了旧的密钥但已更换

**解决方案：**

1. 在管理界面退出登录后重新输入正确的管理员密钥
2. 如果忘记密钥，需要在 Cloudflare Dashboard 的 D1 数据库中查看或重置
3. 确保 Worker URL 配置正确
4. 重启 NekroAgent

</details>

<details>
<summary><strong>Q: 数据库初始化失败？</strong></summary>

首次访问时 Worker 会自动初始化数据库。如果失败：

1. 查看 Worker 日志中的错误信息
2. 确认 D1 数据库已正确创建
3. 在 Cloudflare Dashboard 的 D1 Console 中手动执行 `worker/schema.sql`

</details>

<details>
<summary><strong>Q: 密钥丢失怎么办？</strong></summary>

**管理员密钥丢失：**

1. 登录 Cloudflare Dashboard
2. 进入你的 Worker 的 D1 数据库
3. 查询 `settings` 表：`SELECT * FROM settings WHERE key = 'admin_api_key'`
4. 查看或更新管理员密钥
5. 或者直接使用管理界面的"修改管理密钥"功能（需要提供旧密钥）

**共享密钥丢失：**

1. 使用管理员密钥登录管理界面
2. 删除旧密钥
3. 创建新的共享密钥
4. 分享给需要的用户

</details>

<details>
<summary><strong>Q: HTML 内容有什么限制？</strong></summary>

- **大小限制**：默认 500KB，可在配置中调整（`MAX_HTML_SIZE`）
- **安全性**：不进行内容过滤，请合理使用
- **外部资源**：可以引用 CDN 上的 CSS、JS 库
- **示例**：
  ```html
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    rel="stylesheet"
  />
  ```

</details>

---

## 🛡️ 安全建议

1. **设置强密钥**：首次设置管理员密钥时使用强随机字符串（至少 8 个字符）
2. **使用共享密钥**：不要把管理员密钥分享给其他人，在管理界面创建共享密钥分享
3. **设置合理限制**：根据实际需求调整 `MAX_HTML_SIZE` 和 `PAGE_EXPIRE_DAYS`
4. **妥善保管密钥**：管理员密钥拥有完全权限，丢失后只能通过数据库查看

---

## 📝 注意事项

- ⚠️ HTML 内容大小限制默认为 500KB，可在配置中调整
- ⚠️ 页面默认保留 30 天，可设置为永久保留（0 天）
- ⚠️ 生成的页面 URL 可公开访问，请勿包含敏感信息
- ⚠️ 管理员密钥拥有完全权限，请妥善保管
- ⚠️ 数据存储在 Cloudflare D1 中，受 Cloudflare 服务条款约束

---

## 📚 相关资源

**官方文档：**

- [Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)
- [D1 数据库文档](https://developers.cloudflare.com/d1/)
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)

**开发文档：**

- [开发指南](./DEVELOPMENT.md) - 面向开发者的完整开发文档
- [快速参考](./QUICK_START.md) - 常用命令速查表
- [贡献指南](./CONTRIBUTING.md) - 如何贡献代码

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

- 🐛 [报告 Bug](https://github.com/KroMiose/nekro-plugin-webapp/issues/new?template=bug_report.md)
- 💡 [提出功能建议](https://github.com/KroMiose/nekro-plugin-webapp/issues/new?template=feature_request.md)
- 📖 [查看贡献指南](./CONTRIBUTING.md)

---

## 📮 联系方式

- **GitHub**: [@KroMiose](https://github.com/KroMiose)
- **项目主页**: [nekro-plugin-webapp](https://github.com/KroMiose/nekro-plugin-webapp)
- **Issues**: [提交问题](https://github.com/KroMiose/nekro-plugin-webapp/issues)

---

**Made with ❤️ by NekroAgent Team**

如果觉得这个插件有用，欢迎给个 ⭐ Star！
