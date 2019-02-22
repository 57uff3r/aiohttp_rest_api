import ujson as json
from frozendict import frozendict
from aiohttp.web_response import Response
from typing import Optional
from multidict import CIMultiDict


def respond_with_json(data, status: int=200, additional_headers: Optional[dict] = frozendict({})) -> Response:
    """

    :param data:  response data
    :param status: status code
    :param additional_headers:
    :return:
    """

    return Response(
        status=status,
        body=json.dumps(data),
        content_type='application/json',
        headers=_prepare_headers(additional_headers=additional_headers)
    )


def respond_with_plaintext(data: str, status: int=200, additional_headers: Optional[dict] = frozendict({})) -> Response:
    """

    :param data:  response data
    :param status: status code
    :param additional_headers:
    :return:
    """

    return Response(
        status=status,
        body=data,
        content_type='text/plain',
        headers=_prepare_headers(additional_headers=additional_headers)
    )


def respond_with_html(data: str, status: int=200, additional_headers: Optional[dict] = frozendict({})) -> Response:
    """

    :param data:  response data
    :param status: status code
    :param additional_headers:
    :return:
    """

    return Response(
        status=status,
        body=data,
        content_type='text/html',
        headers=_prepare_headers(additional_headers=additional_headers)
    )


def _prepare_headers(additional_headers: Optional[dict] = frozendict({})) -> CIMultiDict:
    """

    :param resource:
    :return:
    """

    headers = CIMultiDict()
    # if isinstance(resource, RestEndpoint):
    #     pass

    for header in additional_headers:
        headers[header] = additional_headers[header]

    # headers['Content-Disposition'] = 'inline;filename="f.txt"'


    return headers

