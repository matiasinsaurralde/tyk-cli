import coprocess_object_pb2
import coprocess_object_pb2_grpc
from coprocess_session_state_pb2 import SessionState

from tyk.object import TykCoProcessObject
import bundle_loader

from pathlib import Path
import grpc, time, json, sys

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

from concurrent import futures

bundle = None

class MyDispatcher(coprocess_object_pb2_grpc.DispatcherServicer):
    def Dispatch(self, coprocess_object, context):
        # Handle internal reload events:
        if coprocess_object.hook_name == '_reload':
            bundle.reload()
            return coprocess_object
        object = TykCoProcessObject(coprocess_object)
        print("Dispatching '{0}'".format(coprocess_object.hook_name))
        hook = bundle.find_hook(coprocess_object.hook_name)
        output = bundle.process_hook(hook, object)
        return output.object

def DispatchEvent(self, event_wrapper, context):
    event = json.loads(event_wrapper.payload)
    return coprocess_object_pb2.EventReply()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    coprocess_object_pb2_grpc.add_DispatcherServicer_to_server(MyDispatcher(), server)
    server.add_insecure_port('[::]:5555')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    cwd = Path(sys.argv[1])
    print("Loading bundle from: {0}".format(str(cwd)))
    bundle = bundle_loader.load(cwd)
    serve()
