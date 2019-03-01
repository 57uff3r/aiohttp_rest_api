from typing import Optional
import pkgutil
from inspect import getmembers, isclass

from aiohttp.web import Application

from aiohttp_rest_api.rest_endpoint  import AioHTTPRestEndpoint, SUPPORTED_METHODS
from aiohttp_rest_api.swagger import generate_doc_template, build_doc_from_func_doc


_swagger_documentation:dict = generate_doc_template()


def load_and_connect_all_endpoints_from_folder(path: str, app: Application, version_prefix: Optional[str] = None) -> Application:
    """

    :param path:
    :param app:
    :param version_prefix:
    :return:
    """
    __all__:list = []

    for loader, module_name, is_pkg in pkgutil.walk_packages([path]):
        __all__.append(module_name)
        module = loader.find_module(module_name).load_module(module_name)
        __all__.append(module)

        for member in getmembers(module):
            if isclass(member[1]) and AioHTTPRestEndpoint in member[1].__bases__:
                endpoint: AioHTTPRestEndpoint = member[1]()
                endpoint.register_routes(app.router, version_prefix)

                for route in endpoint.produce_routes(version_prefix=version_prefix):
                    for method in SUPPORTED_METHODS:
                        method_name = method.lower()
                        method_code = getattr(endpoint, method_name) if hasattr(endpoint, method.lower())  else None

                        if method_code is not None and callable(method_code) \
                            and method_code.__doc__ is not None and "---" in method_code.__doc__:
                            documentation = build_doc_from_func_doc(method_code, method_name)

                            _swagger_documentation['paths'][route].update(documentation)

    return app


def get_swagger_documentation() -> dict:
    """

    :return: dict with swagger documentation
    """
    return _swagger_documentation
