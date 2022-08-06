import sys
import json
import numpy as np
from mutator_base import BaseMutator
from format_finder import try_json
from typing import Any

class JsonIntMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
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

class JsonExtremeIntMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        int_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        int_set = int.from_bytes(input[1].tobytes()[2:4], "little")
        multiplier = (input[1] * 2 - 1) * int_set

        if multiplier <= -0.99: multiplier = -sys.maxsize - 1
        elif -0.01 <= multiplier <= 0.01: multiplier = 0
        elif multiplier >= 0.99: multiplier = sys.maxsize

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

class JsonListMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        list_index = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        multiplier = int.from_bytes(input[1].tobytes()[2:4], "little")

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            json_update_dict(j, list, list_index, multiplier, 0)
        elif isinstance(j, list):
            json_update_list(j, list, list_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which list to modify
        Second element of vector = number to repeat
        """
        return 2

class JsonEntryMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        key_index = int.from_bytes(input[0].tobytes()[2:4], "little") % len(text)
        multiplier = int.from_bytes(input[1].tobytes()[2:4], "little")

        if not try_json(text):
            return text
        j = json.loads(text)
        if isinstance(j, dict):
            json_update_dict(j, (str, Any), key_index, multiplier, 0)
        elif isinstance(j, list):
            json_update_list(j, (str, Any), key_index, multiplier, 0)

        return json.dumps(j).encode()

    def get_dimension(self) -> "int":
        """
        First element of vector = which key to modify
        Second element of vector = number to repeat
        """
        return 2

def json_update_dict(json: dict, target_type, target_index: int, multiplier: float, cur_index = 0):
    for k, v in json.items():
        if target_type == (str, Any):
            if cur_index == target_index:
                if multiplier == 0:
                    json.pop(k)
                elif multiplier > 1:
                    for i in range(0, multiplier):
                        json.add(k, v)
                return
            cur_index += 1
        elif isinstance(v, target_type):
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
        if target_type == (str, Any):
            if cur_index == target_index:
                if multiplier == 0:
                    json.pop(i)
                elif multiplier > 1:
                    for k in range(0, multiplier):
                        json.add(i, v)
                return
            cur_index += 1
        elif isinstance(v, target_type):
            if cur_index == target_index:
                json[i] = target_type(json[i] * multiplier)
                return
            cur_index += 1
        elif isinstance(v, dict):
            json_update_dict(v, target_type, target_index, multiplier, cur_index)
        elif isinstance(v, list):
            json_update_list(v, target_type, target_index, multiplier, cur_index)

if __name__ == "__main__":
    from combiner import apply
    with open(sys.argv[1], 'rb') as f:
        text = f.read()

    print(apply(text, [JsonListMutator()], np.array([0, 0.4])))

