import csv
import io
from mutator_base import BaseMutator
from format_finder import try_json

class CSVRepeatRowMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little")
        repeat = int.from_bytes(input[1].tobytes()[2:4], "little")
        repeat = min(repeat, 10000)

        if not try_csv(text):
            return text
            
        c = list(csv.reader(text))
        if not index < len(c):
            return text
        mutated = c[:index] + ([c[index]] * repeat) + c[index + 1:]
        return to_csv(mutated)
        
    def get_dimension(self) -> "int":
        """
        First element of vector = which row to repeat
        Second element of vector = how many times to repeat.
        """
        return 2

class CSVEmptyRowMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_csv(text):
            return text
            
        c = list(csv.reader(text))
        if not index < len(c):
            return text
        c[index] = [""] * len(c[index])
        return to_csv(c)

    def get_dimension(self) -> "int":
        """
        First element of vector = which row to make empty
        """
        return 1

class CSVRepeatColMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little")
        repeat = int.from_bytes(input[1].tobytes()[2:4], "little")
        repeat = min(repeat, 10000)

        if not try_csv(text):
            return text
        # Transpose array so we can operate on columns as rows    
        t = np.transpose(list(csv.reader(text)))
        
        if not index < len(t):
            return text
        
        mutated = t[:index] + ([t[index]] * repeat) + t[index + 1:]
        return to_csv(np.transpose(mutated))
        
    def get_dimension(self) -> "int":
        """
        First element of vector = which column to repeat
        Second element of vector = how many times to repeat.
        """
        return 2

class CSVEmptyColMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_csv(text):
            return text
            
        t = np.transpose(list(csv.reader(text)))
        if not index < len(t):
            return text
        
        t[index] = [""] * len(t[index])
        return to_csv(np.transpose(t))

    def get_dimension(self) -> "int":
        """
        First element of vector = which column to make empty
        """
        return 1


class CSVEmptyColHeaderMutator(BaseMutator):
    """
    Same as CSVEmptyColMutator but leaves the top entry empty to account for
    CSV files with headers
    """
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        index = int.from_bytes(input[0].tobytes()[2:4], "little")

        if not try_csv(text):
            return text
            
        t = np.transpose(list(csv.reader(text)))
        # Check for no header and no entries
        if not index < len(t) || len(t[index]) < 1:
            return text
        
        t[index] = t[index][0] + ([""] * len(t[index] - 1))
        return to_csv(np.transpose(t))

    def get_dimension(self) -> "int":
        """
        First element of vector = which column to make empty
        """
        return 1

class CSVCellMultiplierMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        r_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        c_index = int.from_bytes(input[1].tobytes()[2:4], "little")
        multiplier = int.from_bytes(input[2].tobytes()[2:4], "little")

        if not try_csv(text):
            return text
            
        c = list(csv.reader(text))
        if not r_index < len(c) || not c_index < len(c[r_index]):
            return text
        if isdecimal(c[r_index][c_index]):
            multiplier = (input[2] * 2 - 1) * multiplier
            c[r_index][c_index] = str(int(c[r_index][c_index]) * multiplier)
        elif is_float(c[r_index][c_index]):
            multiplier = input[2] * 2 - 1
            if multiplier <= -0.99: multiplier = float("-inf")
            elif -0.01 <= multiplier <= 0.01: multiplier = 0.0
            elif multiplier >= 0.99: multiplier = float("inf")
            c[r_index][c_index] = str(float(c[r_index][c_index]) * multiplier)
        else:
            multiplier = (input[2] * 2 - 1) * multiplier
            c[r_index][c_index] = extend_str(c[r_index][c_index], multiplier)
        return to_csv(c)
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the row of the cell to make empty
        Second element of vector = the col of the cell to make empty
        Third element of vector = the value of the multiplier
        """
        return 3

class CSVEmptyCellMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        r_index = int.from_bytes(input[0].tobytes()[2:4], "little")
        c_index = int.from_bytes(input[1].tobytes()[2:4], "little")

        if not try_csv(text):
            return text
            
        c = list(csv.reader(text))
        if not r_index < len(c) || not c_index < len(c[r_index]):
            return text
        c[r_index][c_index] = ""
        return to_csv(c)
        
    def get_dimension(self) -> "int":
        """
        First element of vector = the row of the cell to make empty
        Second element of vector = the col of the cell to make empty
        """
        return 2

def to_csv(list: mutated) -> bytes:
        f = io.StringIO()
        w = csv.writer(f)
        w.writerows(mutated)
        return f.getvalue().encode()

def extend_str(str: string, int length) -> str:
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
            

def is_float(str: value) -> boolean:
    try:
        float(value)
        return True
    except:
        return False       
