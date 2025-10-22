# WebApp 快速部署插件

> 通过 Cloudflare Workers 将 HTML 内容快速部署为在线可访问的网页

## ✨ 功能特性

- 🚀 **AI 一键部署**：通过简单的 API 调用将 HTML 部署为在线网页
- 🔑 **密钥管理**：支持管理员密钥和共享密钥，方便多用户使用
- 🌐 **全球加速**：基于 Cloudflare Workers，享受全球 CDN 加速
- 📊 **可视化管理**：简洁的 Web 管理界面，轻松管理页面和密钥
- 🔒 **安全可靠**：密钥哈希存储，内容大小限制，访问统计
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

#### 第二步：连接 Cloudflare

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)（没有账号的话先注册）
2. 左侧菜单选择 **Workers & Pages**
3. 点击 **Create application** → **Pages** → **Connect to Git**
4. 授权 Cloudflare 访问你的 GitHub（首次使用需要授权）
5. 选择你 fork 的 `nekro-plugin-webapp` 仓库
6. 点击 **Begin setup**
7. 配置页面：
   - **Project name**: 随意命名（如：`nekro-webapp`）
   - **Production branch**: `main`
   - **Build settings**: 保持默认（Cloudflare 自动识别）
8. 点击 **Save and Deploy**

⏱️ 等待 2-3 分钟，Cloudflare 会自动构建和部署

✅ **完成**：获得 Worker URL（格式如：`https://nekro-webapp.pages.dev`）

#### 第三步：首次访问自动初始化

1. 复制你的 Worker URL
2. 在浏览器中访问这个 URL
3. 首次访问时，数据库会**自动初始化**（无需任何操作！）
4. 看到欢迎页面，说明部署成功

✅ **完成**！Worker 现在可以使用了

#### 第四步：配置 NekroAgent 插件

1. 打开 NekroAgent
2. 进入插件配置页面
3. 找到 **WebApp 快速部署** 插件
4. 填写配置：
   - **WORKER_URL**: 粘贴你的 Worker URL
   - **ADMIN_API_KEY**: 使用默认密钥 `admin-change-me-immediately`
   - 其他保持默认即可
5. 保存配置

#### 第五步：访问管理界面并更换密钥

1. 打开管理界面：`http://localhost:8021/plugins/nekro_plugin_webapp/`
2. 如果提示输入管理员密钥，输入：`admin-change-me-immediately`
3. 管理界面会自动加载数据

⚠️ **重要安全提示**：

- 立即使用管理界面的"生成管理员密钥"工具创建新密钥
- 将新密钥保存到插件配置中
- 默认密钥仅用于首次配置，请务必更换！

#### 第六步：测试部署（30 秒）

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
- 🔧 **生成管理员密钥**：安全地生成新的管理员密钥和哈希值
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

| 配置项              | 说明                | 默认值                        | 必填 |
| ------------------- | ------------------- | ----------------------------- | ---- |
| `WORKER_URL`        | Worker 访问地址     | 无                            | ✅   |
| `ADMIN_API_KEY`     | 管理员密钥          | `admin-change-me-immediately` | ✅   |
| `DEFAULT_SHARE_KEY` | 默认共享密钥        | 空                            | ❌   |
| `PAGE_EXPIRE_DAYS`  | 页面过期天数        | 30                            | ❌   |
| `MAX_HTML_SIZE`     | HTML 最大大小（KB） | 500                           | ❌   |

**说明：**

- `WORKER_URL`：从 Cloudflare Pages 获取的 URL
- `DEFAULT_SHARE_KEY`：留空则 AI 使用管理员密钥；填写共享密钥可限制 AI 权限
- `PAGE_EXPIRE_DAYS`：设置为 0 表示永久保留

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

1. 插件配置中的 `ADMIN_API_KEY` 不正确
2. 使用了旧的密钥但已更换

**解决方案：**

1. 确认插件配置中的密钥是原始密钥（不是哈希值）
2. 如果忘记密钥，在管理界面重新生成
3. 保存新密钥到插件配置
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

1. 在管理界面使用"生成管理员密钥"工具
2. 生成新的密钥和哈希
3. 复制哈希值
4. 在 Cloudflare Dashboard 的 Worker 设置中更新 `ADMIN_KEY_HASH` 环境变量
5. 将新密钥保存到插件配置

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

1. **立即更换默认密钥**：首次部署后必须更换 `admin-change-me-immediately`
2. **使用共享密钥**：不要把管理员密钥分享给其他人，使用共享密钥分享
3. **设置合理限制**：根据实际需求调整 `MAX_HTML_SIZE` 和 `PAGE_EXPIRE_DAYS`

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
