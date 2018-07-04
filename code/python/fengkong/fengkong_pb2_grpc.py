# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import fengkong_pb2 as fengkong__pb2


class FKPredictStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CardPredict = channel.unary_unary(
        '/fengkong.FKPredict/CardPredict',
        request_serializer=fengkong__pb2.DataReq.SerializeToString,
        response_deserializer=fengkong__pb2.DataResp.FromString,
        )


class FKPredictServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CardPredict(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_FKPredictServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CardPredict': grpc.unary_unary_rpc_method_handler(
          servicer.CardPredict,
          request_deserializer=fengkong__pb2.DataReq.FromString,
          response_serializer=fengkong__pb2.DataResp.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'fengkong.FKPredict', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
