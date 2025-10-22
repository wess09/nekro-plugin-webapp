"""Web 路由处理"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from nekro_agent.core import logger

from .plugin import config, plugin


@plugin.mount_router()
def create_router() -> APIRouter:
    """创建并配置插件路由"""
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse, summary="管理界面")
    async def index() -> HTMLResponse:
        """返回管理界面"""
        static_path = Path(__file__).parent / "static" / "index.html"
        if not static_path.exists():
            raise HTTPException(404, "管理界面未找到")

        try:
            html_content = static_path.read_text(encoding="utf-8")
            return HTMLResponse(content=html_content)
        except Exception as e:
            logger.exception("读取管理界面失败")
            raise HTTPException(500, f"读取管理界面失败: {e}") from e

    @router.get("/health", summary="获取 Worker 配置")
    async def health_check() -> dict:
        """返回 Worker URL 配置，供前端使用"""
        return {
            "status": "ok",
            "worker_url": config.WORKER_URL,
        }

    return router
