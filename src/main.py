#!/usr/bin/env python
# encoding: utf-8

import argparse
from pb import chatsql_pb2
from pb import chatsql_pb2_grpc
from chatsql import ChatSql

import grpc
from concurrent import futures
 

class ChatSqlGrpcServicer(chatsql_pb2_grpc.ChatSqlGrpcServicer):

    def __init__(self) -> None:

        self.csql = ChatSql()
        self.llm = self.csql.llm
        
    def SqlPredictor(self, request: object, context: object) -> object:

        print("CHATGPT QUERY------------------:")
        query = self.csql.prompt_to_query(request.prompt)
        print(query)
        raw_result = self.csql.query_to_result(query)
        print("RAW RESULT------------------: ")
        print(raw_result)
        print("PROCESSED RESULT------------------ :")
        processed_res = self.csql.raw_result_to_processed(raw_result)
        print(processed_res)

        response = chatsql_pb2.SqlResponse(query = str(query['query']), rawResult = str(raw_result), processedResult = str(processed_res))

        return response
    
def main(port: int) -> None:
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 32))
    chatsql_pb2_grpc.add_ChatSqlGrpcServicer_to_server(ChatSqlGrpcServicer(), server)
    print("Listening...")
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":

    ap = argparse.ArgumentParser()  
    ap.add_argument("-p", "--port", required=False, help = "port number", default = "9001")
    args = vars(ap.parse_args())
    main(args["port"])

