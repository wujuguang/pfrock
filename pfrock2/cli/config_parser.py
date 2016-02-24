# !/usr/bin/env python
# coding=utf8
import json
import traceback

from pfrock2.bin import logger
from pfrock2.core.lib import auto_str


@auto_str
class PfrockConfigRouter(object):
    def __init__(self, path, handler, options):
        self.path = path
        self.handler = handler
        self.options = options


@auto_str
class PfrockConfigServer(object):
    def __init__(self, routes, port=8081):
        self.routes = routes
        self.port = port


class PfrockConfigParser(object):
    CONFIG_SERVER = 'servers'
    CONFIG_ROUTER = 'routes'
    CONFIG_PORT = 'port'
    CONFIG_PATH = "path"
    CONFIG_HANDLER = "handler"
    CONFIG_OPTIONS = "options"

    @classmethod
    def _parse_router(cls, router):
        path = router[cls.CONFIG_PATH] if cls.CONFIG_PATH in router else None
        handler = router[cls.CONFIG_HANDLER] if cls.CONFIG_HANDLER in router else None
        options = router[cls.CONFIG_OPTIONS] if cls.CONFIG_OPTIONS in router else None
        if path and handler:
            return PfrockConfigRouter(path, handler, options)

    @classmethod
    def _parse_routers(cls, routers):
        router_list = []
        for router in routers:
            router_list.append(cls._parse_router(router))
        return router_list

    @classmethod
    def _parse_servers(cls, server):
        port = server[cls.CONFIG_PORT] if cls.CONFIG_ROUTER in server else 8888
        routers = cls._parse_routers(server[cls.CONFIG_ROUTER]) if cls.CONFIG_ROUTER in server else None
        if port and routers:
            return PfrockConfigServer(routers, port)

    @classmethod
    def do(cls, config_file_path):
        with open(config_file_path, 'r') as fin:

            config_data = {}
            try:
                config_data = json.load(fin)
            except:
                logger.error(traceback.format_exc())
                return None

            if cls.CONFIG_SERVER in config_data:
                config_servers = config_data[cls.CONFIG_SERVER] if cls.CONFIG_SERVER in config_data else None
                if config_servers:
                    for config_server in config_servers:
                        config_server = cls._parse_servers(config_server)
                        # first just support one server
                        return config_server