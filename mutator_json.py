import json
import sys
import numpy as np
from mutator_base import BaseMutator
from format_finder import try_json

class JsonIntMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        print(text)
        int_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        int_set = int.from_bytes(input[1].tobytes()[2:4], "little")
        multiplier = (input[1] * 2 - 1) * int_set

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            json_update_dict(j, int, int_index, multiplier, 0)
        elif isinstance(j, list):
            json_update_list(j, int, int_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which int to modify
        Second element of vector = what to set it to.
        """
        return 2



class JsonFloatMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        float_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        multiplier = input[1] * 2 - 1
        if multiplier <= -0.99: multiplier = float("-inf")
        elif -0.01 <= multiplier <= 0.01: multiplier = 0.0
        elif multiplier >= 0.99: multiplier = float("inf")

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            json_update_dict(j, float, float_index, multiplier, 0)
        elif isinstance(j, list):
            json_update_list(j, float, float_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which float to modify
        Second element of vector = what to set it to.
        """
        return 2

def json_update_dict(json: dict, target_type, target_index: int, multiplier: float, cur_index = 0):
    for k, v in json.items():
        if isinstance(v, target_type):
            if cur_index == target_index:
                json[k] = target_type(json[k] * multiplier)
                return
            cur_index += 1
        elif isinstance(v, dict):
            json_update_dict(v, target_type, target_index, multiplier, cur_index)
        elif isinstance(v, list):
            json_update_list(v, target_type, target_index, multiplier, cur_index)

def json_update_list(json: list, target_type, target_index: int, multiplier: float, cur_index = 0):
    for i, v in enumerate(json):
        if isinstance(v, target_type):
            if cur_index == target_index:
                json[i] = target_type(json[i] * multiplier)
                return
            cur_index += 1
        elif isinstance(v, dict):
            json_update_dict(v, target_type, target_index, multiplier, cur_index)
        elif isinstance(v, list):
            json_update_list(v, target_type, target_index, multiplier, cur_index)

