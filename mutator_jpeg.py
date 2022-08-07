from PIL import Image, ExifTags
import io
import numpy as np
from mutator_base import BaseMutator
from format_finder import try_jpg

class JPEGFilenameMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        length = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(text)
        length = (input[0] * 2 - 1) * length
        try:
            image.filename = extend_str(image.filename, length)
        except:
            return text

        mutated = io.BytesIO()
        image.save(mutated)

        return mutated
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the length of the new filename
        """
        return 1

    def get_name(self) -> "str":
        return "Change filename mutator"

class JPEGSizeMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        width = int.from_bytes(input[0].tobytes()[2:4], "little")
        height = int.from_bytes(input[1].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(text)

        width = (input[0] * 2 - 1) * width
        height = (input[1] * 2 - 1) * height
        try:
            image.size = tuple(image.size[0] * width, image.size[1] * height)
        except:
            return text

        mutated = io.BytesIO()
        image.save(mutated)

        return mutated
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the width of the new filename
        Second element of vector = the height of the new filename
        """
        return 2

    def get_name(self) -> "str":
        return "Multiplier for size mutator"

class JPEGWidthMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        width = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(text)

        width = (input[0] * 2 - 1) * width
        try:
            image.width *= width
        except:
            return text

        mutated = io.BytesIO()
        image.save(mutated)

        return mutated
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the width of the new filename
        """
        return 1

    def get_name(self) -> "str":
        return "Multiplier for width mutator"

class JPEGHeightMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        height = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(text)

        height = (input[0] * 2 - 1) * height
        try:
            image.height *= height
        except:
            return text

        mutated = io.BytesIO()
        image.save(mutated)

        return mutated
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the height of the new filename
        """
        return 1

    def get_name(self) -> "str":
        return "Multiplier for height mutator"

class JPEGMultiplierMutator(BaseMutator):
    #TODO Finish this
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little")
        multiplier = int.from_bytes(input[1].tobytes()[2:4], "little")

        if not try_jpg(text):
            return text

        image = Image.open(text)

        exif = image.getexif()

        if not index < len(exif):
            return text
        exif = sorted(exif)
        key = list(exif.keys())[index]
        
        if is_int(exif[key]):
            multiplier = (input[1] * 2 - 1) * multiplier
            exif[key] = str(int(exif[key]) * multiplier)
        elif is_float(exif[key]):
            multiplier = input[2] * 2 - 1
            if multiplier <= -0.99: multiplier = float("-inf")
            elif -0.01 <= multiplier <= 0.01: multiplier = 0.0
            elif multiplier >= 0.99: multiplier = float("inf")
            exif[key] = str(float(c[r_index][c_index]) * multiplier)
        else:
            multiplier = (input[2] * 2 - 1) * multiplier
            exif[key] = extend_str(exif[key], multiplier)
        mutated = io.BytesIO()
        image.save(mutated)

        return mutated
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the index of the metadata item to change
        Second element of vector = what to change the item by
        """
        return 2

    def get_name(self) -> "str":
        return "Repeated row in csv"





def extend_str(string: str, length: int) -> str:
    if string == "":
        return ""
    new_str = []
    i = 0
    while (True):
        for char in string:
            if i >= length:
                return ''.join(new_str)
            new_str.append(char)
            i += 1   

def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except:
        return False

def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except:
        return False