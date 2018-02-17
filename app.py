#!/usr/bin/env python3

# Python browser-based terminal
# Based on this guide: https://xtermjs.org/docs/guides/terminado/

import argparse
import os
from pathlib import Path

from tornado import web
from tornado.ioloop import IOLoop
from terminado import TermSocket, SingleTermManager

OUR_ROOT = Path(__file__).parent.resolve()


class OneManager(SingleTermManager):
    def on_eof(self, ptywclients):
        super().on_eof(ptywclients)

        IOLoop.current().stop()


def run(args):
    os.chdir(args.path)

    term_manager = OneManager(shell_command=['notes', args.path])
    handlers = [
        ('/socket', TermSocket, { 'term_manager': term_manager }),
        ('/()', web.StaticFileHandler, { 'path': (OUR_ROOT / 'static/index.html').as_posix() }),
        ('/static/(.*)', web.StaticFileHandler, { 'path': (OUR_ROOT / 'static').as_posix() }),
    ]  # yapf: disable

    app = web.Application(handlers)
    app.listen(args.port)
    print(f'Python browser-based terminal app listening on 127.0.0.1:{args.port}')
    IOLoop.current().start()
    IOLoop.current().close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', metavar='DIR')
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    run(args)
