"""
Created on May 29, 2019

@author: ionut
"""

import logging
import aiohttp_jinja2
import jinja2
from aiohttp import web, ClientSession

from zeus import views
from zeus import settings


async def startup(app):
    app.client = ClientSession()


async def shutdown(app):
    await app.client.close()


def make_app():
    """
    Create and return aiohttp.web.Application object
    :returns: application instance
    """
    app = web.Application()
    app.router.add_view("/", views.Home)
    app.router.add_view("/forecast{tail:.*}", views.Forecast)
    app.router.add_view("/geocode{tail:.*}", views.Geocoder)
    # app.router.add_view("/manifest.json{tail:.*}", views.Test)
    # app.router.add_view("/service-worker.js{tail:.*}", views.Test)
    app.config = settings
    app.router.add_static("/static", app.config.STATIC_PATH)
    app.cache = {}
    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(app.config.TEMPLATE_PATH))
    return app


def main():
    """Start aiohttp application instance"""
    application = make_app()
    logging.info(
        "starting zeus on %s:%s ...",
        application.config.ADDRESS,
        application.config.PORT,
    )
    web.run_app(
        application,
        host=application.config.ADDRESS,
        port=application.config.PORT,
        access_log=None,
    )


if __name__ == "__main__":
    main()
