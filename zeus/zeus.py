"""
Created on May 29, 2019

@author: ionut
"""

import logging
import signal
import sys
import tornado.ioloop
import tornado.web

import handlers
import settings
from utils import format_frame


def app_exit():
    """Stop IOLoop and exit"""
    tornado.ioloop.IOLoop.current().stop()
    logging.info("finished")
    sys.exit()


def cleanup_hook(exc_type, exc_value, exc_traceback):
    """Log exception details and call app_exit"""
    logging.error("Uncaught exception, stopping", exc_info=(exc_type, exc_value, exc_traceback))
    app_exit()


def configure_signals():
    """Configure signal handling to cleanly exit the application"""

    def stopping_handler(signum, frame):
        """Log frame details and call app_exit"""
        frame_data = format_frame(frame)
        logging.info("interrupt signal %s, frame %s received, stopping", signum, frame_data)
        app_exit()

    signal.signal(signal.SIGINT, stopping_handler)
    signal.signal(signal.SIGTERM, stopping_handler)


def make_app(io_loop=None):
    """
    Create and return tornado.web.Application object so it can be used in tests too
    :param io_loop: already existing io_loop (used for testing)
    :return: application instance
    """
    app = tornado.web.Application(
        [
            (r"/", handlers.HomeHandler),
            (r"/forecast/?", handlers.ForecastHandler),
            (r"/geocode/?", handlers.GeocodingHandler),
            (r"/(manifest\.json)", tornado.web.StaticFileHandler, {"path": "static"}),
            (r"/(service\-worker\.js)", tornado.web.StaticFileHandler, {"path": "static"}),
        ],
        template_path=settings.TEMPLATE_PATH,
        static_path=settings.STATIC_PATH
    )
    app.config = settings
    app.cache = {}
    app.io_loop = io_loop
    return app


def main():
    """Start Tornado application instance"""
    application = make_app()
    logging.info("starting zeus on %s:%s", application.config.ADDRESS, application.config.PORT)
    application.listen(application.config.PORT, address=application.config.ADDRESS)
    if application.io_loop:
        application.io_loop.start()
    else:
        tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    sys.excepthook = cleanup_hook
    configure_signals()
    main()
