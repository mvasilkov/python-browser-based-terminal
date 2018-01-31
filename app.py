#!/usr/bin/env python3

# Python browser-based terminal
# Based on this guide: https://xtermjs.org/docs/guides/terminado/

from tornado import web
from tornado.ioloop import IOLoop
from terminado import TermSocket, SingleTermManager


def run():
    term_manager = SingleTermManager(shell_command=['bash'])
    handlers = [
        ('/socket', TermSocket, { 'term_manager': term_manager }),
        ('/()', web.StaticFileHandler, { 'path': 'index.html' }),
        ('/(.*)', web.StaticFileHandler, { 'path': '.' }),
    ]  # yapf: disable
    app = web.Application(handlers)
    app.listen(8086)
    IOLoop.current().start()


if __name__ == '__main__':
    run()
