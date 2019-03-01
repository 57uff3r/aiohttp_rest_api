from typing import List
# import phonenumbers

from aiohttp.web_response import Response
from aiohttp.web import Request

from aiohttp_rest_api import AioHTTPRestEndpoint


class DemoEndpoint(AioHTTPRestEndpoint):

    def connected_routes(self) -> List[str]:
        """
        """
        return [
            '/demo/d'
        ]

    async def get(self, request: Request) -> Response:
        return Response(
            status=200,
            body='',
            content_type='text/plain'
        )


