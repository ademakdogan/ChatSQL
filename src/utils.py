import os
import json
from typing import List, Any, Dict, Union

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

def get_final_path(sub_count: int, join_list: List[str]) -> str:

    path = os.path.dirname(os.path.realpath(__file__))
    for _ in range(sub_count):
        path = os.path.dirname(os.path.normpath(path))
    for join_elem in join_list:
        path = os.path.join(path, join_elem)

    return path

def read_json(config_path: str) -> Dict[str, object]:

    with open(config_path, 'r', encoding = 'utf-8') as f_conf:
        config: Dict[str, object] = json.load(f_conf)

    return config
