import copy
import sys
from mutator_base import BaseMutator
import numpy as np

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

# Returns a new xml with the tag lengths being multiplied
# by the number from 'input'.
class XMLOverFlowMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        number = int.from_bytes(input[0].tobytes()[2:7], "little")
        xmlTemplate="""
        {tag1}
            {input1}
            {input2}
        {tag2}
        """
        return xmlTemplate.format(tag1=("<tag>"*number), input1=("<input>" * number), input2=("</input>" * number), tag2=("</tag>" * number))

    """
    First element of vector, number of repititions of the Entities in the xml.
    """
    def get_dimension(self) -> "int":
                return 1

# Returns a xmlbomb, with entities set as 10 copies of the previous entity.
class XMLBombMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        return  """
        <?xml version="1.0"?>
        <!DOCTYPE lolz [
        <!ENTITY lol "lol">
        <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
        <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
        <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
        <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
        <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
        <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
        <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
        <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
        <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
        <!ENTITY lolz "&lol9;">
        ]>
        <root>&lolz;</root>
        """
    """ Doesn't require any paramaters"""
    def get_dimension(self) -> "int":
            return 0

# Changes all of the attributes for all tags to the set character
# mulitplied by the number from 'input'
class XMLAttributeMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        tree = ET.fromstring(text)

        for element in tree.iter():
            element.attrib = {"%p": "%p" * int.from_bytes(input[0].tobytes()[2:7], "little")}

        return ET.tostring(tree)
    
    """
    First element of vector, number of repititions of the attribute added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1


# Changes all of the 'href' attributes to the set character, by the
# number of 'input'
class XMLhrefAttributeMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        tree = ET.fromstring(text)

        for element in tree.iter():
            if 'href' in element.attrib:
                print(element.attrib)
                element.attrib['href'] = "%s" * int.from_bytes(input[0].tobytes()[2:7], "little")

        return ET.tostring(tree)
    
    """
    First element of vector, number of repititions of the attribute added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1


# Modifies all of the tags, except the root tag to the set character,
# mulitplied by the number of 'input'
class XMLTagMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        tree = ET.fromstring(text)
        tags_list = XMLTagMutator.get_XMLTags(text)
        for tag in tags_list:
            for elem in tree.findall(tag.tag):
                elem.tag = "%p" * int.from_bytes(input[0].tobytes()[2:7], "little")
        return ET.tostring(tree)

    # Returns a list of all tags in the xml file.
    def get_XMLTags(sample_text):
        xmlTree = ET.fromstring(sample_text)
        tags_list = []
        for tag in xmlTree.iter():
            tags_list.append(tag)

        return tags_list
    
    """
    First element of vector, number of repititions of the tag added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1


# Modifies the Root tag by the number of times from the 'input'
class XMLRootTagMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        root = XMLRootTagMutator.get_RootTag(text)
        tree = ET.fromstring(text)
        for elem in tree.iter():
            if elem.tag == root.tag:
                elem.tag = "%p" * int.from_bytes(input[0].tobytes()[2:7], "little")

        return ET.tostring(tree)

    #returns the root tag.
    def get_RootTag(sample_text):
        tree = ET.ElementTree(ET.fromstring(sample_text))
        root = tree.getroot()
        return root

    """
    First element of vector, number of repititions of the Root tag added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1
    
# Add's children (New elements) to the xml by appending the tree to itself
# by the number of times from the 'input'.
class XMLChildrenMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        tree = ET.fromstring(text)
        new_tree = copy.deepcopy(tree)
        for i in range(0, int.from_bytes(input[0].tobytes()[2:7], "little")):
            tree.append(new_tree)

        return ET.tostring(tree)

    """
    First element of vector, number of repititions for the number the tree replicate added to the xml.
    """
    def get_dimension(self) -> "int":
        return 1


def main():
    file = sys.argv[1]
    with open(file, "r+") as f:
        sample_text = f.read()

        array = np.random.rand(10)
        print(XMLChildrenMutator.get_mutation(XMLTagMutator, sample_text, array))


if __name__ == "__main__":
    main()