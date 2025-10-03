"""
Smithery Config Middleware
Parses configuration from ASGI scope for MCP HTTP transport
"""
from smithery.utils.config import parse_config_from_asgi_scope


class SmitheryConfigMiddleware:
    """Middleware to parse Smithery configuration from request scope"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get('type') == 'http':
            try:
                scope['smithery_config'] = parse_config_from_asgi_scope(scope)
            except Exception as e:
                print(f"SmitheryConfigMiddleware: Error parsing config: {e}")
                scope['smithery_config'] = {}

        await self.app(scope, receive, send)
