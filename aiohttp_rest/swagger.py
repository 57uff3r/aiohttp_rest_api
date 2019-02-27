import yaml
from collections import defaultdict
from typing_extensions import Final
import ujson as json
from os.path import abspath, dirname, join

from aiohttp.web import Application
from aiohttp import web

from aiohttp_rest.responses import respond_with_json, respond_with_html


STATIC_PATH: Final = abspath(join(dirname(__file__), "swagger_ui"))

def build_doc_from_func_doc(handler, method):
    """

    :param handler:
    :param method:
    :return:
    """
    end_point_doc = handler.__doc__.splitlines()

    # Find Swagger start point in doc
    end_point_swagger_start = 0
    for i, doc_line in enumerate(end_point_doc):
        if "---" in doc_line:
            end_point_swagger_start = i + 1
            break

    # Build JSON YAML Obj
    try:
        end_point_swagger_doc = (
            yaml.load("\n".join(end_point_doc[end_point_swagger_start:]))
        )
    except yaml.YAMLError:
        end_point_swagger_doc = {
            "description": "⚠ Swagger document could not be loaded "
                           "from docstring ⚠",
            "tags": ["Invalid Swagger"]
        }

    # Add to general Swagger doc
    return {method.lower(): end_point_swagger_doc}


def generate_doc_template(api_base_url: str = "",
                            description: str = "Swagger API definition",
                            api_version: str = "v1",
                            title: str = "Swagger API",
                            schemes: list  = ('http', 'https')
                          ) -> dict:
    return  {
        "swagger": "2.0",
         "info": {
            "description": description.strip()
         },
         'version': api_version,
         'title': title,
         'basePath': api_base_url,
         'schemes': schemes,
         'paths': defaultdict(dict)
    }




async def _swagger_home(request):
    """
    Return the index.html main file
    """
    return respond_with_html(request.app["SWAGGER_TEMPLATE_CONTENT"])

async def _swagger_def(request):
    """
    Returns the Swagger JSON Definition
    """
    return respond_with_json(request.app["SWAGGER_DEF_CONTENT"])



def setup_swagger(app: Application,
                  swagger_url: str = "/doc",
                  # api_base_url: str = "/lol",
                  description: str = "Swagger API definition",
                  api_version: str = "1.0.0",
                  title: str = "Swagger API",
                  contact: str = "",
                  swagger_info: dict = None):
    _swagger_url = ("/{}".format(swagger_url)
                    if not swagger_url.startswith("/")
                    else swagger_url)
    _base_swagger_url = _swagger_url.rstrip('/')
    _swagger_def_url = '{}/swagger.json'.format(_base_swagger_url)
    swagger_info = swagger_info

    # Add API routes
    # app.router.add_route('GET', _swagger_url, _swagger_home)
    # app.router.add_route('GET', "{}/".format(_base_swagger_url), _swagger_home)
    # app.router.add_route('GET', _swagger_def_url, _swagger_def)
    app.router.add_route('GET', _swagger_url, _swagger_home)
    app.router.add_route('GET', "{}/".format(_base_swagger_url), _swagger_home)
    app.router.add_route('GET', _swagger_def_url, _swagger_def)

    # Set statics
    statics_path = '{}/swagger_static'.format(_base_swagger_url)
    app.router.add_static(statics_path, STATIC_PATH)

    # --------------------------------------------------------------------------
    # Build templates
    # --------------------------------------------------------------------------
    app["SWAGGER_DEF_CONTENT"] = swagger_info
    with open(join(STATIC_PATH, "index.html"), "r") as f:
        app["SWAGGER_TEMPLATE_CONTENT"] = (
            f.read()
            # .replace("##SWAGGER_CONFIG##", '/{}{}'.
            #          format(api_base_url.lstrip('/'), _swagger_def_url))
            .replace("##SWAGGER_CONFIG##",  _swagger_def_url)
            .replace("##STATIC_PATH##", '{}'.
                     format(statics_path))
            # .replace("##STATIC_PATH##", '{}{}'.
            #          format(api_base_url.lstrip('/'), statics_path))
        )


__all__ = ("setup_swagger")