# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import log_file_service_pb2 as log__file__service__pb2


class LogFileServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_file = channel.unary_unary(
                '/com.example.grpc.LogFileService/get_file',
                request_serializer=log__file__service__pb2.GetFileRequest.SerializeToString,
                response_deserializer=log__file__service__pb2.Response.FromString,
                )
        self.create_file = channel.unary_unary(
                '/com.example.grpc.LogFileService/create_file',
                request_serializer=log__file__service__pb2.CreateFileRequest.SerializeToString,
                response_deserializer=log__file__service__pb2.Response.FromString,
                )


class LogFileServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_file(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create_file(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogFileServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_file': grpc.unary_unary_rpc_method_handler(
                    servicer.get_file,
                    request_deserializer=log__file__service__pb2.GetFileRequest.FromString,
                    response_serializer=log__file__service__pb2.Response.SerializeToString,
            ),
            'create_file': grpc.unary_unary_rpc_method_handler(
                    servicer.create_file,
                    request_deserializer=log__file__service__pb2.CreateFileRequest.FromString,
                    response_serializer=log__file__service__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.example.grpc.LogFileService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LogFileService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_file(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.example.grpc.LogFileService/get_file',
            log__file__service__pb2.GetFileRequest.SerializeToString,
            log__file__service__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create_file(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.example.grpc.LogFileService/create_file',
            log__file__service__pb2.CreateFileRequest.SerializeToString,
            log__file__service__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
