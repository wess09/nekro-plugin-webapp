"""
# WebApp 快速部署插件

将 HTML 内容快速部署到 Cloudflare Workers 并生成在线访问链接。

## 主要功能

- **AI 一键部署**：通过简单的 API 调用将 HTML 部署为在线网页
- **密钥管理**：支持管理员密钥和共享密钥，方便多用户使用
- **Web 管理界面**：可视化管理已部署的页面和 API 密钥
- **全球加速**：基于 Cloudflare Workers，享受全球 CDN 加速

## 使用方法

### 配置插件

1. 部署 Cloudflare Worker（详见 `README.md`）
2. 在插件配置中填写：
   - `WORKER_URL`: Worker 访问地址
   - `DEFAULT_SHARE_KEY`: 共享密钥（在管理界面创建）

### AI 调用示例

AI 可以直接调用 `create_web_app` 方法部署网页：

```python
url = create_web_app(
    html_content="<html>...</html>",
    title="我的网页",
    description="这是一个示例页面"
)
```

## 注意事项

- 页面标题和描述为必填项，用于管理和识别
- HTML 内容大小限制默认为 500KB，可在配置中调整
- 页面默认保留 30 天，可设置为永久保留（0 天）
- 生成的页面 URL 可公开访问，请勿包含敏感信息

## 管理界面

访问 `http://localhost:8021/plugins/nekro_plugin_webapp/` 打开管理界面，可以：

- 创建和管理 API 密钥
- 查看已部署的页面列表
- 查看访问统计信息
- 删除不需要的页面

## 密钥分享

如果要分享给其他用户使用：

1. 在管理界面创建共享密钥
2. 将密钥和 Worker URL 提供给其他用户
3. 其他用户在自己的插件配置中填写即可使用
"""

from datetime import datetime

import httpx

from nekro_agent.api.schemas import AgentCtx
from nekro_agent.core import logger
from nekro_agent.services.plugin.base import SandboxMethodType

from .handlers import create_router  # noqa: F401
from .models import CreatePageRequest, CreatePageResponse
from .plugin import config, plugin

__all__ = ["plugin"]


@plugin.mount_sandbox_method(SandboxMethodType.TOOL, "创建网页应用")
async def create_web_app(
    _ctx: AgentCtx,
    html_content: str,
    title: str,
    description: str,
) -> str:
    """将 HTML 内容部署为在线可访问的网页

    Args:
        html_content: 完整的 HTML 内容，包括 CSS 和 JavaScript
        title: 页面标题（必填，用于标识和管理）
        description: 页面描述（必填，说明页面用途）

    Returns:
        str: 部署成功信息，包含访问 URL 和相关信息

    Example:
        创建一个简单的网页:
        html = '''
        <!DOCTYPE html>
        <html>
        <head><title>Hello</title></head>
        <body><h1>Hello World!</h1></body>
        </html>
        '''
        url = create_web_app(
            html_content=html,
            title="问候页面",
            description="一个简单的Hello World示例页面"
        )
    """

    # 1. 验证参数
    if not title or not title.strip():
        raise ValueError("页面标题不能为空")
    if not description or not description.strip():
        raise ValueError("页面描述不能为空")
    if not html_content or not html_content.strip():
        raise ValueError("HTML 内容不能为空")

    # 2. 验证 HTML 大小
    html_size_kb = len(html_content.encode("utf-8")) / 1024
    if html_size_kb > config.MAX_HTML_SIZE:
        raise ValueError(
            f"HTML 内容过大 ({html_size_kb:.1f}KB)，最大允许 {config.MAX_HTML_SIZE}KB",
        )

    # 3. 验证配置
    if not config.WORKER_URL:
        raise ValueError("未配置 Worker 地址，请先在插件配置中设置 WORKER_URL")

    api_key = config.DEFAULT_SHARE_KEY
    if not api_key:
        raise ValueError("未配置 API 密钥，请先在管理界面创建密钥并填写到 DEFAULT_SHARE_KEY 配置中")

    # 4. 构造请求
    request_data = CreatePageRequest(
        title=title.strip(),
        description=description.strip(),
        html_content=html_content,
        expires_in_days=config.PAGE_EXPIRE_DAYS,
    )

    # 5. 调用 Worker API
    try:
        logger.info(f"正在部署网页: {title}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config.WORKER_URL.rstrip('/')}/api/pages",
                json=request_data.model_dump(),
                headers={"Authorization": f"Bearer {api_key}"},
            )
            response.raise_for_status()

            result = CreatePageResponse.model_validate(response.json())

            logger.info(f"网页部署成功: {result.url}")

            # 6. 返回友好的结果信息
            created_time = datetime.fromtimestamp(result.created_at).strftime("%Y-%m-%d %H:%M:%S")
            if result.expires_at:
                expires_time = datetime.fromtimestamp(result.expires_at).strftime("%Y-%m-%d %H:%M:%S")
                expires_info = f"📅 过期时间: {expires_time!s}"
            else:
                expires_info = "♾️  永久保留"

            return (
                f"✅ 网页部署成功！\n"
                f"📄 标题: {result.title}\n"
                f"🔗 访问链接: {result.url}\n"
                f"🆔 页面ID: {result.page_id}\n"
                f"⏰ 创建时间: {created_time!s}\n"
                f"{expires_info}"
            )

    except httpx.HTTPStatusError as e:
        error_detail = e.response.text
        logger.error(f"部署失败 (HTTP {e.response.status_code}): {error_detail}")
        raise Exception(f"部署失败: {error_detail}") from e
    except httpx.HTTPError as e:
        error_msg = str(e)
        logger.error(f"网络请求失败: {error_msg}")
        raise Exception(f"网络请求失败: {error_msg}") from e
    except Exception as e:
        error_msg = str(e)
        logger.exception("部署出错")
        raise Exception(f"部署出错: {error_msg}") from e


@plugin.mount_cleanup_method()
async def clean_up() -> None:
    """清理插件资源"""
    logger.info("WebApp 快速部署插件资源已清理")
