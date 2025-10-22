"""
# WebApp 快速部署插件

将 HTML 内容快速部署到 Cloudflare Workers 并生成在线访问链接。

## 主要功能

- **AI 一键部署**：通过简单的 API 调用将 HTML 部署为在线网页
- **密钥权限管理**：管理密钥管理系统，访问密钥创建页面
- **Web 管理界面**：可视化管理已部署的页面和访问密钥
- **全球加速**：基于 Cloudflare Workers，享受全球 CDN 加速
"""

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
        str: 部署的页面访问链接（URL）

    Examples:
        # 单页面
        url = create_web_app(html_content="<html>...</html>", title="我的页面", description="...")
        # 返回: https://worker.pages.dev/abc123

        # 多页面：先创建子页面，再创建包含链接的主页
        about_url = create_web_app(html_content="<html>关于内容</html>", title="关于", description="...")
        contact_url = create_web_app(html_content="<html>联系内容</html>", title="联系", description="...")
        home_url = create_web_app(
            html_content=f'<nav><a href="{about_url}">关于</a> | <a href="{contact_url}">联系</a></nav>',
            title="首页", description="..."
        )
        # 返回主页链接即可，用户点击导航可访问子页面
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

    api_key = config.ACCESS_KEY
    if not api_key:
        raise ValueError("未配置访问密钥，请先在管理界面创建访问密钥并填写到 ACCESS_KEY 配置中")

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

            logger.info(f"网页部署成功: {result.url} (标题: {result.title}, ID: {result.page_id})")

            # 6. 返回页面访问链接
            return result.url

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
