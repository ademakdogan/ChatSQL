from pb import chatsql_pb2
from pb import chatsql_pb2_grpc
import grpc
import time

class Client:

    def __init__(self) -> None:

        self.prompt = "Show me the book type fiction which they height bigger than 175 and smaller than 178. The author shoudn't be 'Doyle, Arthur Conan'. "
    
    def run(self) -> None:

        start = time.time()
        channel = grpc.insecure_channel("localhost:9001")
        stub = chatsql_pb2_grpc.ChatSqlGrpcStub(channel)
        res = chatsql_pb2.SqlRequest(prompt = self.prompt)
        response = stub.SqlPredictor(res)
        print({'query' : response.query, 'raw_result' : response.rawResult, 'processed_result': response.processedResult})
        print('Time: {}'.format(str(time.time() - start)))

if __name__ == '__main__':

    Client().run()