from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["user"] = AnonymousUser()

        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)
        token_key = params.get("token", [None])[0]

        logger.debug(f"[WS] query_string: {query_string}")
        logger.debug(f"[WS] token_key: {token_key}")

        if token_key:
            user = await self.get_user(token_key)
            logger.debug(f"[WS] resolved user: {user}")
            if user:
                scope["user"] = user

        logger.debug(f"[WS] scope user: {scope['user']}")
        return await self.app(scope, receive, send)

    @sync_to_async
    def get_user(self, token_key):
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.select_related("user").get(key=token_key)
            return token.user
        except Exception as e:
            logger.debug(f"[WS] token lookup failed: {e}")
            return None
