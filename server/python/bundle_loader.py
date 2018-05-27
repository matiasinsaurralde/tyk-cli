import importlib
from types import ModuleType

import inspect, sys, os, json
from time import sleep

import sys, json, os, imp
from pathlib import Path

import tyk.decorators as decorators
from tyk import gateway
HandlerDecorators = list( map( lambda m: m[1], inspect.getmembers(decorators, inspect.isclass) ) )

class Bundle():
    def __init__(self, manifest, root_path):
        self.manifest = manifest
        self.root_path = root_path
        self.package_path = Path(os.path.dirname(os.path.realpath(__file__)))
        self.handlers = {}
        self.entrypoint = self.root_path.joinpath("middleware.py")

        # Fallback for single file bundles:
        if len(self.manifest['file_list']) == 1:
            self.entrypoint = self.root_path.joinpath(self.manifest['file_list'][0])

        # Inject the bunde directory into the path:
        sys.path.append(str(self.root_path))

        # Also add the built-in Tyk module from this project:
        tyk_path = self.package_path.joinpath("tyk")
        sys.path.append(str(tyk_path))

        self.module = importlib.import_module("middleware")
        self.register_handlers()

    def register_handlers(self):
        new_handlers = {}
        for hook_name in dir(self.module):
            attr_value = getattr(self.module, hook_name)
            if callable(attr_value):
                attr_type = type(attr_value)
                if attr_type in HandlerDecorators:
                    handler_type = attr_value.__class__.__name__.lower()
                    if handler_type not in new_handlers:
                        new_handlers[handler_type] = []
                    new_handlers[handler_type].append(attr_value)
        self.handlers = new_handlers

    def find_hook(self, name):
        hook = None
        for hook in self.handlers['hook']:
            if name == hook.name:
                hook = hook
        return hook

    def process_hook(self, hook, object):
        handlerType = type(hook)

        if handlerType == decorators.Event:
            hook(object, object.spec)
            return
        elif hook.arg_count == 4:
            object.request, object.session, object.metadata = hook(object.request, object.session, object.metadata, object.spec)
        elif hook.arg_count == 3:
            object.request, object.session = hook(object.request, object.session, object.spec)
            # req, sess = hook(object.request, object.session, object.spec)
            # object.request.CopyFrom(req)
            # object.session.CopyFrom(sess)
        return object

    def reload(self):
        self.module = importlib.reload(self.module)
        self.register_handlers()


def load(p):
    # Load manifest file:
    manifest_file_path = p.joinpath("manifest.json")
    f = open(str(manifest_file_path), 'r')
    manifest_data = f.read()
    f.close()
    manifest = json.loads(manifest_data)
    b = Bundle(manifest, p)
    return b