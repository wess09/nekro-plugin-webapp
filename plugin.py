"""WebApp 快速部署插件配置"""

from pydantic import Field

from nekro_agent.services.plugin.base import ConfigBase, NekroPlugin

# 插件元信息
plugin = NekroPlugin(
    name="WebApp 快速部署",
    module_name="nekro_plugin_webapp",
    description="将 HTML 内容快速部署到 Cloudflare Workers 并生成在线访问链接",
    version="1.0.0",
    author="KroMiose",
    url="https://github.com/KroMiose/nekro-plugin-webapp",
)


@plugin.mount_config()
class WebAppConfig(ConfigBase):
    """WebApp 部署配置"""

    WORKER_URL: str = Field(
        default="",
        title="Worker 访问地址",
        description="Cloudflare Worker 的完整 URL (如: https://your-worker.workers.dev)",
    )

    ADMIN_API_KEY: str = Field(
        default="",
        title="管理员密钥",
        description="Worker 管理员密钥，用于管理操作",
        json_schema_extra={"is_secret": True},
    )

    DEFAULT_SHARE_KEY: str = Field(
        default="",
        title="默认共享密钥",
        description="AI 调用时使用的密钥（留空则使用管理员密钥）",
        json_schema_extra={"is_secret": True},
    )

    PAGE_EXPIRE_DAYS: int = Field(
        default=30,
        title="页面过期天数",
        description="创建的页面默认保留天数（0=永久保留）",
        ge=0,
        le=365,
    )

    MAX_HTML_SIZE: int = Field(
        default=500,
        title="HTML 最大大小(KB)",
        description="单个 HTML 文件的最大大小限制",
        ge=10,
        le=2000,
    )


# 获取配置实例
config: WebAppConfig = plugin.get_config(WebAppConfig)
