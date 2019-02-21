from typing import List
# import phonenumbers

from aiohttp.web_response import Response
from aiohttp.web import Request

from aiohttp_rest.rest_endpoint import AioHTTPRestEndpoint

# # from athena_components.crypto import acquire_key_id_from_headers
# from athena_components.rest_endpoint import RestEndpoint
# from athena_components.responses import respond_with_protobuf
# from athena_components.decorators.exeptions_into_responses import exceptions_into_responses
# from athena_components.decorators.protobufs import catch_invalid_porotobufs
#
#
# from google.protobuf.message import DecodeError
# from athena_components.responses import respond_with_protobuf
#
# from protobufs.athena.GeneralRESTError_pb2 import GeneralRESTError
# from athena_components.constants import (
#     GENERAL_ERROR_INVALID_PROTOBUF_FORMAT,
#     HTTP_STATUS_GENERAL_ERROR
# )
#
# from protobufs.athena.AuthResponsesAndRequests_pb2 import RegisterUserAndDeviceRequest
# from protobufs.athena.AuthResponsesAndRequests_pb2 import RegisterUserAndDeviceResponse
#
# from t20.access.auth_requests import AuthRequests

# from t20.cryptography import generate_RSA


# from t20.protobufs.system.athena.Crypto_pb2 import GetDeviceCreationKeyResponse, SuperKey

# from restserver.main import app


class DemoEndpoint(AioHTTPRestEndpoint):

    def connected_routes(self) -> List[str]:
        """
        """
        return [
            '/demo'
        ]

    async def get(self, request: Request) -> Response:
        """
        ---
        description: Method returns a crypt key for  device registration. Each key can be used only once
        produces:
        - application/protobuf
        responses:
            "200":
                description: successful operation. Secret key was produced
        """

        return Response(
            status=200,
            body='Hello world',
            content_type='text/plain'
        )
