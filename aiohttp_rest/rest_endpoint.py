from typing import List, Optional, Iterable, Union
import inspect
import logging

from aiohttp.web_response import Response
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_request import Request
from aiohttp.web_urldispatcher import UrlDispatcher


METHODS_SUPPORTED_BY_DEFAULT = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')


class AioHTTPRestEndpoint:
    """
    Basic api endpoint
    """

    def __init__(self):
        """

        """
        self.methods:dict = {}

        for method_name in METHODS_SUPPORTED_BY_DEFAULT:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def _produce_route(self, route:str, version_prefix:str) -> str:
        """

        :param route:
        :param version_prefix:
        :return:
        """
        return '/{0}{1}'.format(version_prefix, route)

    def produce_routes(self, version_prefix:str) -> list:
        """

        :param version_prefix:
        :return:
        """
        return [self._produce_route(route, version_prefix) for route in self.connected_routes()]

    def register_routes(self, router:UrlDispatcher, version_prefix:Optional[str] = None):
        """

        :param router:
        :param version_prefix:
        :return:
        """
        routes = self.connected_routes()
        if isinstance(routes, str):
            routes = [routes]

        for route in self.connected_routes():
            try:
                if not route.startswith('/'):
                    route = '/{0}'.format(route)

                if isinstance(version_prefix, str):
                    route = '/{0}{1}'.format(version_prefix, route)

                router.add_route('*', route, self.dispatch)
                if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                    logging.info('{0} is connected {1}'.format(
                            self.__class__, route
                        ))
            except RuntimeError as e:
                raise RuntimeError('Seems URL {0}, described in {1}, is already connected to another endpoint'.format(route, self.__class__))

    def connected_routes(self) -> Union[str, List[str]]:
        """
        """
        return NotImplementedError

    def register_method(self, method_name, method):
        """

        :param method_name:
        :param method:
        :return:
        """
        self.methods[method_name.upper()] = method

    async def dispatch(self, request:Request):
        """

        :param request:
        :return:
        """
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', METHODS_SUPPORTED_BY_DEFAULT)

        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()

        for aa in available_args:
            if aa not in wanted_args:
                raise Exception('REST endpoint method {0} should be able to process URL "{1}" parameter.'.format(
                    request.method.upper(), aa
                ))

        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            # Expected match info that doesn't exist
            raise HttpBadRequest('')

        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})


