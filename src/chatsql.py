from typing import Any, Dict
import json
import argparse
from langchain import PromptTemplate
from langchain.llms import OpenAI
from utils import get_final_path, read_json
from sql_connector import SqlConnector


class ChatSql:

    def __init__(self) -> None:

        conf_path: str = get_final_path(1, ["conf.json"])
        self.conf: Dict[str, Any] = read_json(conf_path)
        self.llm: object = OpenAI(openai_api_key=self.conf["OPEN_AI_KEY"])
        self.info: str = str(read_json(get_final_path(1, ["info.json"])))
        # llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)

    def prompt_to_query(self, prompt: str) -> Dict[str, str]:

        info = self.info
        template = """
        Your mission is convert SQL query from given {prompt}. Use following database information for this purpose (info key is a database column name and info value is explanation). {info}

        --------

        Put your query in the  JSON structure with key name is 'query'

        """
        pr_ = PromptTemplate(input_variables=["prompt", "info"], template=template)
        final_prompt = pr_.format(
            prompt=prompt,
            info=info,
        )
        gpt_query: Dict["str", "str"] = json.loads(self.llm(final_prompt))

        return gpt_query

    def query_to_result(self, gpt_query: Dict[str, str]) -> str:

        raw_res: str = SqlConnector(query=gpt_query["query"]).main()

        return raw_res

    def raw_result_to_processed(self, raw_result: str) -> str:

        res_processing_template = """
        Your mission is convert database result to meaningful sentences. Here is the database result: {database_result}
        """
        db_pr = PromptTemplate(
            input_variables=["database_result"], template=res_processing_template
        )
        final_prompt = db_pr.format(database_result=raw_result)
        procesed_result: str = self.llm(final_prompt)

        return procesed_result


if __name__ == "__main__":

    ap = argparse.ArgumentParser()  
    ap.add_argument("-p", "--prompt", required=False, help = "Write your sql prompt")
    args = vars(ap.parse_args())
    csql = ChatSql()
    query = csql.prompt_to_query(args["prompt"])
    print(query)
    # print(type(result))
    print("CHATGPT QUERY------------------:")
    print(query["query"])
    raw_result = csql.query_to_result(query)
    print("RAW RESULT------------------: ")
    print(raw_result)
    print("PROCESSED RESULT------------------ :")
    processed_res = csql.raw_result_to_processed(raw_result)
    print(processed_res)
