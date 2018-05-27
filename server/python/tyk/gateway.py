"""
This module provides interface compatibility and flexibility for the C glue code in tyk/gateway_wrapper.c
"""
from sys import exc_info

class TykGateway:
    @classmethod
    def store_data(cls, key, value, ttl):
        # gw.store_data(key, value, ttl)
        pass

    @classmethod
    def get_data(cls, key):
        # return gw.get_data(key)
        pass

    @classmethod
    def trigger_event(cls, event_name, payload):
        # gw.trigger_event(event_name, payload)
        pass

    @classmethod
    def log(cls, msg, level):
        # gw.log(msg, level)
        pass

    @classmethod
    def log_error(cls, *args):
        excp = exc_info()
        nargs = len(args)
        # For simpler errors:
        if nargs == 1:
            cls.log(args[0], "error")
            return
        if nargs == 0:
            cls.log("{0} {1}".format(excp[0], excp[1]), "error")
        else:
            cls.log("{0} {1} {2}".format(args[0], excp[0], excp[1]), "error")
