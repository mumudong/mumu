# --coding:utf-8--
import grpc
import time
from concurrent import futures
from score import ScoreModel
import fengkong_pb2,fengkong_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '44444'
model = ScoreModel()
class FKPredict(fengkong_pb2_grpc.FKPredictServicer):
    def CardPredict(self,request,context):
        record = request.text
        id,score = model.getScore(record)
        print(time.asctime(time.localtime(time.time())),"\tself=",self,"\t","id=%d,score=%d"%(id,score))
        return fengkong_pb2.DataResp(id=id,result=score)
def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    fengkong_pb2_grpc.add_FKPredictServicer_to_server(FKPredict(),grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()

