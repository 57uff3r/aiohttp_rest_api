from typing import Optional
import pkgutil
from inspect import getmembers, isclass

from aiohttp.web import Application

from aiohttp_rest.rest_endpoint  import AioHTTPRestEndpoint


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

        """
        All REST endpoints should be automatically connected to application router.
        Here we are looking for RestEndpoint class siblings and assemble them in the list.
        We pass this list back to Apllication() initialisation file and there we 
        attach all the endpoints via register_routes() call.
        """
        for member in getmembers(module):
            if isclass(member[1]) and AioHTTPRestEndpoint in member[1].__bases__:
                c: AioHTTPRestEndpoint = member[1]()
                c.register_routes(app.router, version_prefix)

    return app
