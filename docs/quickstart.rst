.. _quickstart:

Quickstart
==========

.. currentmodule:: aiohttp_rest_api

It's time to write your first REST API. This guide assumes you have a working
understanding of `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_, and that you have already
installed aiohttp_rest_api.

Kicking off demo REST API app
-----------------------------

Create and empty directory and put there files in following order ::

    /
      - main.py
      /endpoints
        - __init__.py
        - demo_endpoint.py

* **main.py** creates aiohttp app and connects API endpoints to it
* **/endpoints** — a python module with API endpoints
* **/endpoints/demo_endpoint.py** — a sample API endpoint


Put the following content into the files



**main.py**: ::

    import os
    from aiohttp import web
    from aiohttp_rest_api.loader import load_and_connect_all_endpoints_from_folder, get_swagger_documentation
    from aiohttp_rest_api.swagger import setup_swagger

    import logging
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    load_and_connect_all_endpoints_from_folder(
        path='{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__)), 'endpoints'),
        app=app,
        version_prefix='v1'
    )

    setup_swagger(app, swagger_info=get_swagger_documentation())

    web.run_app(app)


**/endpoints/demo_endpoint.py**: ::

    from typing import List

    from aiohttp.web_response import Response
    from aiohttp.web import Request

    from aiohttp_rest_api.rest_endpoint import AioHTTPRestEndpoint
    from aiohttp_rest_api.responses import respond_with_plaintext


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
            description: Method returns a crypto key for device registration. Each key can be used only once
            produces:
            - application/protobuf
            responses:
                "200":
                    description: successful operation. Secret key was produced
            """

            return respond_with_plaintext('Hello world')


And after that you can start your server: ::


    $ python main.py
    ======== Running on http://0.0.0.0:8080 ========
    (Press CTRL+C to quit)


And that's it! Swagger documentation is going to be available on http://127.0.0.1:8080/doc


How demo example works
----------------------

Every API endpoint is a class s deriving from **AioHTTPRestEndpoint** class.

In your endpoint class you have to specify a few methods.

* `connected_routes()` returns  a list of URIs for endpoints.
* `get(self, request: Request)`, `post(self, request: Request)`, `put(self, request: Request)`, `path(self, request: Request)`, `delete(self, request: Request)` methods for **GET**, **POST**, **PUT**, **PATCH**, **DELETE** requests respectively.
    * Each method accepts `aiohttp.web.Request` object as a default parameter.


After specifying your API endpoints you have to load all your classes and connect them with `aiohttp.web.Application` ::


    load_and_connect_all_endpoints_from_folder(
        path='{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__)), 'endpoints'),
        app=app,
        version_prefix='v1'
    )

This code loads and initializes all endpoints from `endpoints` directory. It also creates URLs for each endpoint.
It also supports versioning for APIs. In this example each API endpoint will get the URI with  **v1** prefix.
So if you created an API resource connected to **/demo** and with version **v1** final URI will be **/v1/demo**.


You also can enable Swagged documentation page just like that ::


    setup_swagger(app, swagger_info=get_swagger_documentation())


Swagger documentation
---------------------

Every HTTP-verb related method (**get**, **post**, **put**, **path**, **delete**) might documented via Swagger docstrings. ::


    async def get(self, request: Request) -> Response:
        """
        ---
        description: Method returns a crypto key for device registration. Each key can be used only once
        produces:
        - application/protobuf
        responses:
            "200":
                description: successful operation. Secret key was produced
        """

        return respond_with_plaintext('Hello world')

Just add `---` separator and wright your Swagger documentation in YAML format format right after it.
