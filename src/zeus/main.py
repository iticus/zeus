"""
Created on May 29, 2019

@author: ionut
"""

import logging
import aiohttp_jinja2
import jinja2
from aiohttp import web, ClientSession

from zeus import appkeys, settings, views


async def startup(app):
    app[appkeys.client] = ClientSession()


async def shutdown(app):
    await app[appkeys.client].close()


def make_app():
    """
    Create and return aiohttp.web.Application object
    :returns: application instance
    """
    app = web.Application()
    app.router.add_view("/", views.Home)
    app.router.add_view("/weather{tail:.*}", views.Weather)
    app.router.add_view("/geocode{tail:.*}", views.Geocoder)
    # app.router.add_view("/manifest.json{tail:.*}", views.Test)
    # app.router.add_view("/service-worker.js{tail:.*}", views.Test)
    app[appkeys.config] = settings
    app.router.add_static("/static", app[appkeys.config].STATIC_PATH)
    app[appkeys.cache] = {}
    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(app[appkeys.config].TEMPLATE_PATH))
    return app


def main():
    """Start aiohttp application instance"""
    app = make_app()
    logging.info(
        "starting zeus on %s:%s ...",
        app[appkeys.config].ADDRESS,
        app[appkeys.config].PORT,
    )
    web.run_app(
        app,
        host=app[appkeys.config].ADDRESS,
        port=app[appkeys.config].PORT,
        access_log=None,
    )


if __name__ == "__main__":
    main()
