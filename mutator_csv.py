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

def to_csv(list: mutated_list) -> bytes:
        #TODO implement this function
        f = io.StringIO()
        w = csv.writer(f)
        w.writerows(mutated)
        return None
        

