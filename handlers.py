"""Web 路由处理"""

from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from nekro_agent.core import logger

from .models import WorkerHealthResponse
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

    @router.get("/health", summary="健康检查")
    async def health_check() -> dict:
        """检查 Worker 是否正常运行"""
        if not config.WORKER_URL:
            return {
                "status": "not_configured",
                "message": "Worker 未配置，请在插件配置中设置 WORKER_URL",
            }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{config.WORKER_URL.rstrip('/')}/api/health")
                response.raise_for_status()

                worker_health = WorkerHealthResponse.model_validate(response.json())
                return {
                    "status": "healthy",
                    "worker_status": worker_health.status,
                    "worker_timestamp": worker_health.timestamp,
                    "worker_url": config.WORKER_URL,
                    "admin_key_configured": bool(config.ADMIN_API_KEY),
                    "message": "Worker 运行正常",
                }
        except httpx.HTTPError as e:
            logger.error(f"Worker 健康检查失败: {e}")
            return {
                "status": "error",
                "message": f"Worker 无法访问: {e!s}",
            }
        except Exception as e:
            logger.exception("健康检查出错")
            return {
                "status": "error",
                "message": f"检查出错: {e!s}",
            }

    return router
